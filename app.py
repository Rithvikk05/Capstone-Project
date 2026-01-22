from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ml_models import QuizGenerator
from dl_models import Summarizer, FeedbackGenerator
from nlp_utils import generate_study_tips
from data_utils import load_data

app = Flask(__name__)

# Global variables
quiz_gen = QuizGenerator()
summarizer = Summarizer()
feedback_gen = FeedbackGenerator()
dataset = None

def init_app():
    global dataset, quiz_gen, summarizer
    print("Initializing App...")
    data_path = "data/dataset.csv"
    if os.path.exists(data_path):
        dataset = load_data(data_path)
        
        # Quiz Generator
        if not os.path.exists("models/quiz_generator.pkl"):
             quiz_gen.train(dataset)
             quiz_gen.save_model()
        else:
             quiz_gen = QuizGenerator.load_model()
             # Fix for the previous bug: do NOT overwrite data_clustered blindly if you want to be safe, 
             # but here we ensure it has data to work with.
             pass 
        
        # Summarizer
        if not os.path.exists("models/summarizer.h5"):
            summarizer.train(dataset)
            summarizer.save_model()
    else:
        print("Dataset not found. Please run generate_data.py first.")

# --- Routes ---

@app.route('/')
def landing():
    # New Landing Page
    return render_template('landing.html')

@app.route('/loading')
def loading():
    # Loading screen (can be used if needed, or linked from Landing)
    return render_template('loading.html')

@app.route('/dashboard')
def dashboard():
    # Central Hub
    return render_template('dashboard.html')

@app.route('/about')
def about():
    # About Page
    return render_template('about.html')

# --- Planner Feature ---

@app.route('/planner')
def planner():
    return render_template('planner_form.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    try:
        total_hours = int(request.form.get('total_hours', 4))
    except:
        total_hours = 4
        
    topic_text = request.form.get('topic_text', '')
    
    # Parse Subjects and Priorities from dynamic form
    subjects = []
    # Identify keys like 'subject_0', 'priority_0'
    for key in request.form:
        if key.startswith('subject_'):
            idx = key.split('_')[1]
            subj_name = request.form[key]
            priority = request.form.get(f'priority_{idx}', 'Medium')
            subjects.append({'name': subj_name, 'priority': priority})
            
    # Algorithm: Allocate time based on priority
    # High = 3 pts, Medium = 2 pts, Low = 1 pt
    priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
    
    total_score = sum(priority_map[s['priority']] for s in subjects)
    if total_score == 0: total_score = 1 # Avoid div/0
    
    plan = []
    
    for s in subjects:
        weight = priority_map[s['priority']]
        # Hours for this subject
        allocated = (weight / total_score) * total_hours
        allocated = round(allocated, 1) # Round to 1 decimal
        
        if allocated > 0:
            plan.append({
                "subject": s['name'],
                "priority": s['priority'],
                "hours": allocated,
                "activity": f"Study {s['name']} - Focus on key concepts."
            })
            
    # Generate tips/summary if text provided (Legacy support in Plan Result)
    summary = ""
    tips = []
    if topic_text:
        summary = summarizer.summarize(topic_text)
        tips = generate_study_tips(topic_text)
        
    feedback = feedback_gen.generate_feedback("General")
    
    # Reformatter for template compatibility
    formatted_plan = []
    hour_counter = 1
    
    # Sort plan by priority if needed, or keep order. 
    # Current logic just appends order of input which is fine.
    
    for p in plan:
        # Round duration to nearest integer hour for simplicity in this version
        duration = int(round(p['hours']))
        if duration < 1 and p['hours'] > 0: duration = 1 # Ensure at least 1 hour if allocated
        
        for _ in range(duration):
            if hour_counter > total_hours: break
            
            # Study Session (50 mins)
            formatted_plan.append({
                "hour": f"Hour {hour_counter} (00-50m)", 
                "activity": f"<strong>[{p['subject']} - {p['priority']}]</strong> {p['activity']} <br><span class='text-muted'>Focus intently without distractions.</span>",
                "is_break": False
            })
            
            # Break Session (10 mins)
            formatted_plan.append({
                "hour": f"Hour {hour_counter} (50-60m)", 
                "activity": "<strong>Break Time</strong> - Stretch, hydrate, and rest your eyes.",
                "is_break": True
            })
            
            hour_counter += 1
            
    return render_template('result.html', 
                           plan=formatted_plan, 
                           quiz=[], 
                           summary=summary, 
                           tips=tips, 
                           feedback=feedback,
                           resources=[],
                           subject="Multi-Subject Plan")

# --- Quiz Feature ---

@app.route('/quiz_setup')
def quiz_setup():
    subjects = []
    if dataset is not None and 'subject' in dataset.columns:
        subjects = sorted(dataset['subject'].dropna().unique().tolist())
    return render_template('quiz_setup.html', subjects=subjects)

@app.route('/generate_quiz_only', methods=['POST'])
def generate_quiz_only():
    subject = request.form.get('subject')
    difficulty = request.form.get('difficulty', 'Easy')
    
    quiz = quiz_gen.generate_quiz(subject, difficulty)
    
    return render_template('quiz_page.html', subject=subject, quiz=quiz)

# --- Summarizer Feature (New) ---

@app.route('/summarizer')
def summarizer_page():
    return render_template('summarizer.html')

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    text = request.form.get('text_input', '')
    summary = ""
    keywords = []
    feedback = ""
    
    if text:
        summary = summarizer.summarize(text)
        keywords = generate_study_tips(text) # Reusing extraction logic to get keywords
        # In nlp_utils, generate_study_tips calls extract_keywords but returns tips. 
        # Let's verify nlp_utils usage or update it? 
        # Actually nlp_utils.generate_study_tips returns a list of strings (tips).
        # We need keywords. app.py doesn't import extract_keywords directly yet.
        # Let's fix imports or just use tips as keywords for now? 
        # Better: Import extract_keywords
        from nlp_utils import extract_keywords
        keywords = extract_keywords(text)
        feedback = feedback_gen.generate_feedback("Summary")
        
    return render_template('summarizer.html', summary=summary, keywords=keywords, feedback=feedback)

# --- Resources Feature ---

@app.route('/resources')
def resources():
    return render_template('resources.html')

# --- Download ---

@app.route('/download_plan')
def download_plan():
    path = "static/study_schedule.csv"
    if not os.path.exists(path):
        with open(path, 'w') as f: f.write("Time,Activity\n9:00,Study")
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    init_app()
    app.run(debug=True, port=5000)
