import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Local imports
from models import db, User, Job, Candidate, MatchScore
from utils.nlp_engine import extract_text, extract_skills, suggest_missing_skills, generate_interview_questions
from utils.matcher import calculate_match_score

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

# Vercel Compatibility: Use /tmp for writable files
IS_VERCEL = os.environ.get('VERCEL') == '1'
if IS_VERCEL:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Custom Jinja Filter
app.jinja_env.filters['from_json'] = json.loads

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def seed_jobs():
    """Seed the database with initial job listings if they don't exist."""
    default_jobs = [
        {"title": "Full Stack Developer", "description": "We are looking for a Full Stack Developer proficient in Python, Flask, React, and SQL. Experience with REST APIs and cloud deployment is a plus."},
        {"title": "Data Scientist", "description": "Seeking a Data Scientist with strong skills in Python, Pandas, Scikit-learn, and Machine Learning. Experience with data visualization and SQL is required."},
        {"title": "Frontend Developer", "description": "Looking for a Frontend Developer with expertise in React, Javascript, HTML, and CSS. Experience with modern UI frameworks like Tailwind or Bootstrap is preferred."},
        {"title": "Backend Developer", "description": "We need a Backend Developer specialized in Python and Django/Flask. Strong knowledge of database design, Redis, and microservices is expected."},
        {"title": "UI/UX Designer", "description": "Creative UI/UX Designer wanted to lead user research, wireframing, and high-fidelity prototyping using Figma or Adobe XD."},
        {"title": "DevOps Engineer", "description": "DevOps Engineer needed to manage CI/CD pipelines, Docker, Kubernetes, and AWS infrastructure. Knowledge of Terraform and Ansible is a plus."},
        {"title": "Product Manager", "description": "Seeking a Product Manager with experience in Agile, Scrum, and product roadmap planning. Excellent communication and leadership skills are essential."},
        {"title": "Machine Learning Engineer", "description": "Machine Learning Engineer with focus on TensorFlow, PyTorch, and deploying AI models at scale. Experience with NLP or Computer Vision is a plus."},
        {"title": "Content Writer", "description": "Content Writer to create high-quality blogs, articles, and marketing copy. Knowledge of SEO, content strategy, and social media management is preferred."},
        {"title": "QA Automation Engineer", "description": "QA Engineer to build automated test suites using Selenium or PyTest. Focus on ensuring software quality through rigorous testing."},
        {"title": "Marketing Specialist", "description": "Digital Marketing Specialist to handle SEO, SEM, and social media campaigns. Data-driven approach to marketing and lead generation is required."},
        {"title": "HR Manager", "description": "Experienced HR Manager to handle recruitment, employee relations, and company culture. Strong interpersonal and organizational skills are a must."}
    ]
    
    for job_data in default_jobs:
        if not Job.query.filter_by(title=job_data["title"]).first():
            job = Job(title=job_data["title"], description=job_data["description"])
            db.session.add(job)
    
    db.session.commit()
    print("Default jobs checked/seeded successfully!")

# --- Database Initialization ---
with app.app_context():
    db.create_all()
    seed_jobs()
    # Create default admin if not exists
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('admin123', method='pbkdf2:sha256')
        admin = User(username='admin', password=hashed_password, role='admin')
        db.session.add(admin)
        db.session.commit()

# --- Routes ---

@app.route('/')
@login_required
def dashboard():
    total_jobs = Job.query.count()
    total_candidates = Candidate.query.count()
    recent_matches = MatchScore.query.order_by(MatchScore.score.desc()).limit(5).all()
    
    # Data for Chart.js (simplified)
    # Jobs by date or similar
    return render_template('index.html', 
                           total_jobs=total_jobs, 
                           total_candidates=total_candidates,
                           recent_matches=recent_matches)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Job Routes ---

@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_job = Job(title=title, description=description)
        db.session.add(new_job)
        db.session.commit()
        flash('Job added successfully')
        return redirect(url_for('jobs'))
        
    all_jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/job/delete/<int:id>')
@login_required
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted')
    return redirect(url_for('jobs'))

# --- Resume Routes ---

@app.route('/resumes', methods=['GET', 'POST'])
@login_required
def resumes():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['resume']
        job_id = request.form.get('job_id')
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and job_id:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # NLP Processing
            text = extract_text(file_path)
            skills = extract_skills(text)
            
            # Save Candidate
            candidate = Candidate(
                name=filename.split('.')[0].replace('_', ' ').title(),
                resume_filename=filename,
                extracted_skills=",".join(skills),
                raw_text=text
            )
            db.session.add(candidate)
            db.session.commit()
            
            # Calculate Match
            job = Job.query.get(job_id)
            score = calculate_match_score(text, job.description)
            
            # AI Suggestions
            job_skills = extract_skills(job.description)
            missing = suggest_missing_skills(skills, job_skills)
            questions = generate_interview_questions(skills)
            
            match_score = MatchScore(
                job_id=job.id,
                candidate_id=candidate.id,
                score=score,
                suggestions=",".join(missing),
                interview_questions=json.dumps(questions)
            )
            db.session.add(match_score)
            db.session.commit()
            
            flash(f'Resume processed! Match Score: {score}%')
            return redirect(url_for('resumes'))
            
    all_candidates = Candidate.query.order_by(Candidate.created_at.desc()).all()
    all_jobs = Job.query.all()
    return render_template('resumes.html', candidates=all_candidates, jobs=all_jobs)

@app.route('/candidate/<int:id>')
@login_required
def candidate_detail(id):
    try:
        candidate = Candidate.query.get_or_404(id)
        # Order matches by ID descending to get the most recent one first if needed, 
        # though template uses [-1] on all()
        matches = MatchScore.query.filter_by(candidate_id=id).order_by(MatchScore.id.asc()).all()
        return render_template('candidate_detail.html', candidate=candidate, matches=matches)
    except Exception as e:
        flash(f"Error loading candidate report: {str(e)}")
        return redirect(url_for('resumes'))

if __name__ == '__main__':
    app.run(debug=True)
