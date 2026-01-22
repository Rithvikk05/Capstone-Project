import pandas as pd
import os

# 1. Read the original valid part (approx first 530 lines)
# We use 'error_bad_lines=False' or 'on_bad_lines=skip' to salvage what we can if strict parsing fails
try:
    # Try reading as utf-8 first, then latin1
    try:
        df = pd.read_csv('data/dataset.csv', encoding='utf-8', on_bad_lines='skip')
    except UnicodeDecodeError:
        df = pd.read_csv('data/dataset.csv', encoding='latin1', on_bad_lines='skip')
        
    print(f"Loaded {len(df)} rows.")
    
    # 2. Define the new data strictly as a list of dictionaries
    new_data = [
        {"text": "DNA replication is the process by which a double-stranded DNA molecule is copied to produce two identical DNA molecules.", "summary": "Summary of Genetics.", "subject": "Science", "topic": "Genetics"},
        {"text": "Mitosis is a part of the cell cycle when replicated chromosomes are separated into two new nuclei.", "summary": "Summary of Mitosis.", "subject": "Science", "topic": "Biology"},
        {"text": "The Big Bang theory is the prevailing cosmological model for the observable universe from the earliest known periods through its subsequent large-scale evolution.", "summary": "Summary of Cosmology.", "subject": "Science", "topic": "Physics"},
        {"text": "Chemical bonds are attractions between atoms that allow the formation of chemical substances that contain two or more atoms.", "summary": "Summary of Chemistry.", "subject": "Science", "topic": "Chemistry"},
        {"text": "Ecology is the branch of biology which studies the interactions among organisms and their environment.", "summary": "Summary of Ecology.", "subject": "Science", "topic": "Biology"},
        {"text": "Plate tectonics is a scientific theory describing the large-scale motion of seven large plates and the movements of a larger number of smaller plates of Earth's lithosphere.", "summary": "Summary of Geology.", "subject": "Science", "topic": "Geology"},
        {"text": "Thermodynamics is a branch of physics that deals with heat work and temperature and their relation to energy entropy and the physical properties of matter.", "summary": "Summary of Thermodynamics.", "subject": "Science", "topic": "Physics"},
        {"text": "Organic chemistry is a subdiscipline within chemistry involving the scientific study of the structure properties and reactions of organic compounds and organic materials.", "summary": "Summary of Organic Chemistry.", "subject": "Science", "topic": "Chemistry"},
        {"text": "Evolution is change in the heritable characteristics of biological populations over successive generations.", "summary": "Summary of Evolution.", "subject": "Science", "topic": "Biology"},
        {"text": "Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles.", "summary": "Summary of Quantum Mechanics.", "subject": "Science", "topic": "Physics"},
        {"text": "Linear algebra is the branch of mathematics concerning linear equations such as linear maps and their representations in vector spaces and through matrices.", "summary": "Summary of Linear Algebra.", "subject": "Math", "topic": "Linear Algebra"},
        {"text": "Calculus II usually covers integration techniques sequences and series.", "summary": "Summary of Calculus II.", "subject": "Math", "topic": "Calculus"},
        {"text": "Probability theory is the branch of mathematics concerned with probability.", "summary": "Summary of Probability.", "subject": "Math", "topic": "Probability"},
        {"text": "Number theory is a branch of pure mathematics devoted primarily to the study of the integers and integer-valued functions.", "summary": "Summary of Number Theory.", "subject": "Math", "topic": "Number Theory"},
        {"text": "Topology is concerned with the properties of a geometric object that are preserved under continuous deformations such as stretching twisting crumpling and bending.", "summary": "Summary of Topology.", "subject": "Math", "topic": "Topology"},
        {"text": "Differential equations involve equations that relate one or more functions and their derivatives.", "summary": "Summary of Differential Equations.", "subject": "Math", "topic": "Differential Equations"},
        {"text": "Combinatorics is an area of mathematics primarily concerned with counting both as a means and an end in obtaining results.", "summary": "Summary of Combinatorics.", "subject": "Math", "topic": "Combinatorics"},
        {"text": "Graph theory is the study of graphs which are mathematical structures used to model pairwise relations between objects.", "summary": "Summary of Graph Theory.", "subject": "Math", "topic": "Graph Theory"},
        {"text": "Logic is the systematic study of the form of valid inference and the most general laws of truth.", "summary": "Summary of Logic.", "subject": "Math", "topic": "Logic"},
        {"text": "Set theory is the branch of mathematical logic that studies sets which can be informally described as collections of objects.", "summary": "Summary of Set Theory.", "subject": "Math", "topic": "Set Theory"},
        {"text": "The American Civil War was a civil war in the United States from 1861 to 1865.", "summary": "Summary of American Civil War.", "subject": "History", "topic": "American Civil War"},
        {"text": "The Great Depression was a severe worldwide economic depression that took place feverishly during the 1930s.", "summary": "Summary of Great Depression.", "subject": "History", "topic": "Great Depression"},
        {"text": "Feudalism was the dominant social system in medieval Europe.", "summary": "Summary of Feudalism.", "subject": "History", "topic": "Feudalism"},
        {"text": "The Enlightenment was an intellectual and philosophical movement that dominated the world of ideas in Europe during the 17th and 18th centuries.", "summary": "Summary of Enlightenment.", "subject": "History", "topic": "Enlightenment"},
        {"text": "The fall of the Western Roman Empire was the process of decline in the Western Roman Empire in which the Empire failed to enforce its rule.", "summary": "Summary of Fall of Rome.", "subject": "History", "topic": "Fall of Rome"},
        {"text": "The Mongol Empire existed during the 13th and 14th centuries and was the largest contiguous land empire in history.", "summary": "Summary of Mongol Empire.", "subject": "History", "topic": "Mongol Empire"},
        {"text": "The Victorian era was the period of Queen Victoria's reign from 20 June 1837 until her death on 22 January 1901.", "summary": "Summary of Victorian Era.", "subject": "History", "topic": "Victorian Era"},
        {"text": "The Space Race was a 20th-century competition between two Cold War rivals the Soviet Union and the United States to achieve firsts in spaceflight capability.", "summary": "Summary of Space Race.", "subject": "History", "topic": "Space Race"},
        {"text": "Apartheid was a system of institutionalised racial segregation that existed in South Africa and South West Africa from 1948 until the early 1990s.", "summary": "Summary of Apartheid.", "subject": "History", "topic": "Apartheid"},
        {"text": "The Scientific Revolution was a series of events that marked the emergence of modern science during the early modern period.", "summary": "Summary of Scientific Revolution.", "subject": "History", "topic": "Scientific Revolution"},
        {"text": "Keynesian economics consists of various macroeconomic theories about how in the short run and especially during recessions economic output is strongly influenced by aggregate demand.", "summary": "Summary of Keynesian Economics.", "subject": "Economics", "topic": "Keynesian Economics"},
        {"text": "Monopolistic competition is a type of imperfect competition such that there are many producers competing against each other but selling products that are differentiated from one another.", "summary": "Summary of Monopolistic Competition.", "subject": "Economics", "topic": "Monopolistic Competition"},
        {"text": "Oligopoly is a market form wherein a market or industry is dominated by a small group of large sellers.", "summary": "Summary of Oligopoly.", "subject": "Economics", "topic": "Oligopoly"},
        {"text": "Gross Domestic Product (GDP) is a monetary measure of the market value of all the final goods and services produced in a specific time period.", "summary": "Summary of GDP.", "subject": "Economics", "topic": "GDP"},
        {"text": "Fiscal policy is the use of government revenue collection and expenditure to influence a country's economy.", "summary": "Summary of Fiscal Policy.", "subject": "Economics", "topic": "Fiscal Policy"},
        {"text": "Monetary policy is the policy adopted by the monetary authority of a country that controls the interest rate payable on very short-term borrowing or the money supply.", "summary": "Summary of Monetary Policy.", "subject": "Economics", "topic": "Monetary Policy"},
        {"text": "International trade is the exchange of capital goods and services across international borders or territories.", "summary": "Summary of International Trade.", "subject": "Economics", "topic": "International Trade"},
        {"text": "Behavioral economics studies the effects of psychological cognitive emotional cultural and social factors on the decisions of individuals and institutions.", "summary": "Summary of Behavioral Economics.", "subject": "Economics", "topic": "Behavioral Economics"},
        {"text": "Development economics is a branch of economics which deals with economic aspects of the development process in low-income countries.", "summary": "Summary of Development Economics.", "subject": "Economics", "topic": "Development Economics"},
        {"text": "Labor economics seeks to understand the functioning and dynamics of the markets for wage labor.", "summary": "Summary of Labor Economics.", "subject": "Economics", "topic": "Labor Economics"},
        {"text": "Social psychology is the scientific study of how the thoughts feelings and behaviors of individuals are influenced by the actual imagined or implied presence of others.", "summary": "Summary of Social Psychology.", "subject": "Psychology", "topic": "Social Psychology"},
        {"text": "Developmental psychology is the scientific study of how and why human beings change over the course of their life.", "summary": "Summary of Developmental Psychology.", "subject": "Psychology", "topic": "Developmental Psychology"},
        {"text": "Abnormal psychology is the branch of psychology that studies unusual patterns of behavior emotion and thought which may or may not be understood as precipitating a mental disorder.", "summary": "Summary of Abnormal Psychology.", "subject": "Psychology", "topic": "Abnormal Psychology"},
        {"text": "Personality psychology is a branch of psychology that studies personality and its variation among individuals.", "summary": "Summary of Personality Psychology.", "subject": "Psychology", "topic": "Personality Psychology"},
        {"text": "Neuropsychology is a branch of psychology that is concerned with how the brain and the rest of the nervous system influence a person's cognition and behaviors.", "summary": "Summary of Neuropsychology.", "subject": "Psychology", "topic": "Neuropsychology"},
        {"text": "Clinical psychology is an integration of science, theory, and clinical knowledge for the purpose of understanding, preventing, and establishing psychologically-based distress.", "summary": "Summary of Clinical Psychology.", "subject": "Psychology", "topic": "Clinical Psychology"},
        {"text": "Forensic psychology involves the application of psychological knowledge and methods to civil and criminal legal questions.", "summary": "Summary of Forensic Psychology.", "subject": "Psychology", "topic": "Forensic Psychology"},
        {"text": "Educational psychology is the branch of psychology concerned with the scientific study of human learning.", "summary": "Summary of Educational Psychology.", "subject": "Psychology", "topic": "Educational Psychology"},
        {"text": "Industrial and organizational psychology is the scientific study of human behavior in organisms and the workplace.", "summary": "Summary of I/O Psychology.", "subject": "Psychology", "topic": "IO Psychology"},
        {"text": "Health psychology is the study of psychological and behavioral processes in health illness and healthcare.", "summary": "Summary of Health Psychology.", "subject": "Psychology", "topic": "Health Psychology"},
        {"text": "Baroque art is a style of architecture music dance painting sculpture and other arts that flourished in Europe from the early 17th century until the 1740s.", "summary": "Summary of Baroque Art.", "subject": "Art", "topic": "Baroque Art"},
        {"text": "Romanticism was an artistic literary musical and intellectual movement that originated in Europe towards the end of the 18th century.", "summary": "Summary of Romanticism.", "subject": "Art", "topic": "Romanticism"},
        {"text": "Realism in the arts is the attempt to represent subject matter truthfully without artificiality and avoiding artistic conventions.", "summary": "Summary of Realism.", "subject": "Art", "topic": "Realism"},
        {"text": "Expressionism was a modernist movement initially in poetry and painting originating in Germany at the beginning of the 20th century.", "summary": "Summary of Expressionism.", "subject": "Art", "topic": "Expressionism"},
        {"text": "Abstract expressionism is a post-World War II art movement in American painting developed in New York in the 1940s.", "summary": "Summary of Abstract Expressionism.", "subject": "Art", "topic": "Abstract Expressionism"},
        {"text": "Minimalism describes movements in various forms of art and design especially visual art and music where the work is set out to expose the essence essentials or identity of a subject through eliminating all non-essential forms features or concepts.", "summary": "Summary of Minimalism.", "subject": "Art", "topic": "Minimalism"},
        {"text": "Contemporary art is the art of today produced in the second half of the 20th century or in the 21st century.", "summary": "Summary of Contemporary Art.", "subject": "Art", "topic": "Contemporary Art"},
        {"text": "Art Deco is a style of visual arts and decoration making its debut in France just before World War I.", "summary": "Summary of Art Deco.", "subject": "Art", "topic": "Art Deco"},
        {"text": "Dada was an art movement of the European avant-garde in the early 20th century with early centers in Zürich Switzerland and New York City.", "summary": "Summary of Dada.", "subject": "Art", "topic": "Dada"},
        {"text": "Fauvism is the style of les Fauves a group of early 20th-century modern artists whose works emphasized painterly qualities and strong color over the representational or realistic values retained by Impressionism.", "summary": "Summary of Fauvism.", "subject": "Art", "topic": "Fauvism"},
        {"text": "Machine learning is a field of inquiry devoted to understanding and building methods that 'learn' that is methods that leverage data to improve performance on some set of tasks.", "summary": "Summary of Machine Learning.", "subject": "Computer Science", "topic": "Machine Learning"},
        {"text": "Operating systems are system software that manages computer hardware software resources and provides common services for computer programs.", "summary": "Summary of Operating Systems.", "subject": "Computer Science", "topic": "Operating Systems"},
        {"text": "Databases are an organized collection of data generally stored and accessed electronically from a computer system.", "summary": "Summary of Databases.", "subject": "Computer Science", "topic": "Databases"},
        {"text": "Computer networks are a set of computers sharing resources located on or provided by network nodes.", "summary": "Summary of Computer Networks.", "subject": "Computer Science", "topic": "Computer Networks"},
        {"text": "Cybersecurity is the practice of protecting systems networks and programs from digital attacks.", "summary": "Summary of Cybersecurity.", "subject": "Computer Science", "topic": "Cybersecurity"},
        {"text": "Software engineering is the systematic application of engineering approaches to the development of software.", "summary": "Summary of Software Engineering.", "subject": "Computer Science", "topic": "Software Engineering"},
        {"text": "Cloud computing is the on-demand availability of computer system resources especially data storage and computing power without direct active management by the user.", "summary": "Summary of Cloud Computing.", "subject": "Computer Science", "topic": "Cloud Computing"},
        {"text": "Theory of computation is a branch that deals with how efficiently problems can be solved on a model of computation using an algorithm.", "summary": "Summary of Theory of Computation.", "subject": "Computer Science", "topic": "Theory of Computation"},
        {"text": "Human-computer interaction is a multidisciplinary field of study focusing on the design of computer technology and the interaction between humans and computers.", "summary": "Summary of HCI.", "subject": "Computer Science", "topic": "HCI"},
        {"text": "Computer graphics is a branch of computer science that deals with generating images with the aid of computers.", "summary": "Summary of Computer Graphics.", "subject": "Computer Science", "topic": "Computer Graphics"},
        {"text": "Poetry is a form of literature that uses aesthetic and rhythmic qualities of language to evoke meanings in addition to or in place of the prosaic ostensible meaning.", "summary": "Summary of Poetry.", "subject": "Literature", "topic": "Poetry"},
        {"text": "Drama is the specific mode of fiction represented in performance: a play opera mime ballet etc performed in a theatre or on radio or television.", "summary": "Summary of Drama.", "subject": "Literature", "topic": "Drama"},
        {"text": "Non-fiction is any document or media entity that attempts in good faith to convey information only about the real world rather than being grounded in imagination.", "summary": "Summary of Non-fiction.", "subject": "Literature", "topic": "Non-fiction"},
        {"text": "Science fiction is a genre of speculative fiction that typically deals with imaginative and futuristic concepts such as advanced science and technology.", "summary": "Summary of Science Fiction.", "subject": "Literature", "topic": "Science Fiction"},
        {"text": "Fantasy is a genre of speculative fiction involving magical elements typically set in a fictional universe and sometimes inspired by mythology and folklore.", "summary": "Summary of Fantasy.", "subject": "Literature", "topic": "Fantasy"},
        {"text": "Mystery is a fiction genre where the nature of an event usually a murder or other crime remains mysterious until the end of the story.", "summary": "Summary of Mystery.", "subject": "Literature", "topic": "Mystery"},
        {"text": "Thriller is a genre of fiction having numerous overlapping subgenres.", "summary": "Summary of Thriller.", "subject": "Literature", "topic": "Thriller"},
        {"text": "Horror is a genre of speculative fiction which is intended to frighten scare or disgust.", "summary": "Summary of Horror.", "subject": "Literature", "topic": "Horror"},
        {"text": "Satire is a genre of literature and performing arts usually in the form of fiction and less frequently non-fiction in which vices follies abuses and shortcomings are held up to ridicule.", "summary": "Summary of Satire.", "subject": "Literature", "topic": "Satire"},
        {"text": "Biography is a detailed description of a person's life.", "summary": "Summary of Biography.", "subject": "Literature", "topic": "Biography"}
    ]
    
    # 3. Append and fill helper columns
    new_df = pd.DataFrame(new_data)
    # Helper columns as app expects them
    import re
    def clean_text(text):
        return re.sub(r'[^a-zA-Z0-9\s]', '', str(text).lower())
        
    new_df['cleaned_text'] = new_df['text'].apply(clean_text)
    new_df['cleaned_summary'] = new_df['summary'].apply(clean_text)
    
    combined_df = pd.concat([df, new_df], ignore_index=True)
    
    # 4. Save clean file
    combined_df.to_csv('data/dataset.csv', index=False, encoding='utf-8')
    print(f"Repaired and updated dataset. Total rows: {len(combined_df)}")

except Exception as e:
    print(f"Error: {e}")
