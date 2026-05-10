import os
import re
import PyPDF2
import docx
import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # If not found, you'll need to run: python -m spacy download en_core_web_sm
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Predefined skill dictionary
SKILL_DB = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust", "typescript",
    # Web Frameworks
    "flask", "django", "react", "angular", "vue", "nodejs", "express", "laravel", "spring", "asp.net",
    # Databases
    "sqlite", "mysql", "postgresql", "mongodb", "redis", "oracle", "sql server", "cassandra",
    # Tools & DevOps
    "git", "docker", "kubernetes", "aws", "azure", "google cloud", "jenkins", "ansible", "terraform",
    # Data Science & AI
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "nltk", "spacy", "opencv", "tableau", "power bi",
    # Others
    "html", "css", "bootstrap", "tailwind", "rest api", "graphql", "microservices", "agile", "scrum"
]

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    return text

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    return ""

def extract_skills(text):
    text = text.lower()
    doc = nlp(text)
    
    extracted = []
    # Using PhraseMatcher for better accuracy
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILL_DB]
    matcher.add("SKILLS", patterns)
    
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if span.text.lower() not in extracted:
            extracted.append(span.text.lower())
            
    return extracted

def suggest_missing_skills(resume_skills, job_description_skills):
    return [skill for skill in job_description_skills if skill not in resume_skills]

def generate_interview_questions(skills):
    questions = []
    for skill in skills[:5]:  # Top 5 skills
        questions.append(f"Can you describe a project where you heavily used {skill.capitalize()}?")
        questions.append(f"What are some common challenges you've faced while working with {skill.capitalize()}?")
    return questions
