import pandas as pd
import matplotlib.pyplot as plt
import os
from data_utils import save_data, clean_text
import random

def generate_synthetic_data():
    # Helper to generate long text (Medium Difficulty)
    def long_text(base):
        return f"{base} This concept is fundamental to understanding the broader implications of the field. It requires a deep analysis of key factors, including historical context, theoretical frameworks, and practical applications. Experts have debated this for decades, leading to various interpretations and complex models that attempt to explain the phenomenon in detail."

    # Helper to generate short text (Easy Difficulty)
    def short_text(base):
        return base

    subjects_data = [
        # --- Science ---
        {"sub": "Science", "topic": "Biology", "easy": "Cells are the basic building blocks of life.", "medium": "Cellular respiration is a set of metabolic reactions and processes that take place in the cells of organisms to convert biochemical energy from nutrients into adenosine triphosphate (ATP), and then release waste products."},
        {"sub": "Science", "topic": "Physics", "easy": "Gravity pulls objects towards the earth.", "medium": "General relativity generalizes special relativity and refines Newton's law of universal gravitation, providing a unified description of gravity as a geometric property of space and time or spacetime."},
        
        # --- Math ---
        {"sub": "Math", "topic": "Algebra", "easy": "Algebra uses letters to represent numbers in equations.", "medium": "Abstract algebra is the study of algebraic structures. Algebraic structures include groups, rings, fields, modules, vector spaces, lattices, and algebras. The term abstract algebra was coined in the early 20th century to distinguish this area of study from older parts of algebra."},
        {"sub": "Math", "topic": "Geometry", "easy": "A triangle has three sides and three angles.", "medium": "Non-Euclidean geometry consists of two geometries based on axioms closely related to those specifying Euclidean geometry. As Euclidean geometry lies at the intersection of metric geometry and affine geometry, non-Euclidean geometry arises when either the metric requirement is relaxed, or the parallel postulate is replaced with an alternative one."},
        
        # --- History ---
        {"sub": "History", "topic": "World War II", "easy": "World War II was a global war that lasted from 1939 to 1945.", "medium": "The causes of World War II were debated in the context of the rise of fascism in Europe, the aggressive expansionism of Nazi Germany and the Empire of Japan, and the failure of the League of Nations to prevent conflict. It involved the vast majority of the world's countries—including all of the great powers—forming two opposing military alliances: the Allies and the Axis."},
        {"sub": "History", "topic": "Ancient Rome", "easy": "Rome was a powerful empire in ancient times.", "medium": "The Roman Empire was the post-Republican period of ancient Rome. As a polity it included large territorial holdings around the Mediterranean Sea in Europe, North Africa, and Western Asia ruled by emperors. From the accession of Caesar Augustus to the military anarchy of the 3rd century, it was a principate with Italy as the metropole of the provinces and the city of Rome as the sole capital."},

        # --- Economics ---
        {"sub": "Economics", "topic": "Supply & Demand", "easy": "Prices go up when demand is high and supply is low.", "medium": "In microeconomics, supply and demand is an economic model of price determination in a market. It postulates that, holding all else equal, in a competitive market, the unit price for a particular good, or other traded item such as labor or liquid financial assets, will vary until it settles at a point where the quantity demanded (at the current price) will equal the quantity supplied (at the current price), resulting in an economic equilibrium for price and quantity transacted."},
        {"sub": "Economics", "topic": "Inflation", "easy": "Inflation means things get more expensive over time.", "medium": "Inflation is a quantitative measure of the rate at which the average price level of a basket of selected goods and services in an economy increases over some period of time. It is the rise in the general level of prices where a unit of currency generally buys fewer goods and services. Consequently, inflation reflects a reduction in the purchasing power per unit of money – a loss of real value in the medium of exchange and unit of account within the economy."},
        
        # --- Psychology ---
        {"sub": "Psychology", "topic": "Cognitive Dissonance", "easy": "Cognitive dissonance is feeling bad about conflicting beliefs.", "medium": "In the field of psychology, cognitive dissonance occurs when a person holds contradictory beliefs, ideas, or values, and is typically experienced as psychological stress when they participate in an action that goes against one or more of them. According to this theory, when two actions or ideas are not psychologically consistent with each other, people do all in their power to change them until they become consistent."},
        {"sub": "Psychology", "topic": "Behaviorism", "easy": "Behaviorism studies observable actions.", "medium": "Behaviorism (or behaviourism) is a systematic approach to understanding the behavior of humans and other animals. It assumes that behavior is either a reflex evoked by the pairing of certain antecedent stimuli in the environment, or a consequence of that individual's history, including especially reinforcement and punishment contingencies, together with the individual's current motivational state and controlling stimuli."},
        
        # --- Art ---
        {"sub": "Art", "topic": "Renaissance", "easy": "The Renaissance was a time of great art in Europe.", "medium": "The Renaissance is a period in European history marking the transition from the Middle Ages to modernity and covering the 15th and 16th centuries. It occurred after the Crisis of the Late Middle Ages and was associated with great social change. In addition to the standard periodization, proponents of a long Renaissance put its beginning in the 14th century and its end in the 17th century."},
        {"sub": "Art", "topic": "Impressionism", "easy": "Impressionism used small brush strokes to show light.", "medium": "Impressionism was a 19th-century art movement characterized by relatively small, thin, yet visible brush strokes, open composition, emphasis on accurate depiction of light in its changing qualities (often accentuating the effects of the passage of time), ordinary subject matter, inclusion of movement as a crucial element of human perception and experience, and unusual visual angles."}
    ]
    
    data = []
    
    # Generate data with EXPLICIT length differences
    for item in subjects_data:
        # Easy Entry
        data.append({
            "text": short_text(item['easy']),
            "summary": f"Summary of {item['topic']} (Easy).",
            "subject": item['sub'],
            "topic": item['topic']
        })
        # Medium Entry
        data.append({
            "text": long_text(item['medium']),
            "summary": f"Summary of {item['topic']} (Medium).",
            "subject": item['sub'],
            "topic": item['topic']
        })
        
    # Duplicate for volume (20x) -> ~240 rows
    final_data = []
    for _ in range(20):
        for d in data:
            final_data.append(d.copy())
            
    df = pd.DataFrame(final_data)
    
    # Clean text
    df['cleaned_text'] = df['text'].apply(clean_text)
    df['cleaned_summary'] = df['summary'].apply(clean_text)
    
    return df

def perform_eda(df):
    print("Dataset Shape:", df.shape)
    print("Subject Counts:\n", df['subject'].value_counts())
    
    # Visualization
    plt.figure(figsize=(10, 6))
    df['subject'].value_counts().plot(kind='bar', color='#7000ff') # Updated color
    plt.title('Distribution of Subjects')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/subject_distribution.png')
    print("Visualization saved to static/subject_distribution.png")

if __name__ == "__main__":
    df = generate_synthetic_data()
    perform_eda(df)
    save_data(df, "data/dataset.csv")
