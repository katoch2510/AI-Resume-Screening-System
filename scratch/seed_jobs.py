import sys
import os

# Add the root directory to sys.path to find 'app' and 'models'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Job

def seed_jobs():
    with app.app_context():
        sample_jobs = [
            {
                "title": "Python Backend Developer",
                "description": "We are looking for a Python Developer with experience in Flask, Django, and SQL. Knowledge of REST APIs and Microservices is a plus. Requirements: Python, Flask, Git, Docker, PostgreSQL."
            },
            {
                "title": "Frontend React Engineer",
                "description": "Develop modern web interfaces using React.js and Redux. Must be proficient in JavaScript (ES6+), HTML5, CSS3, and Bootstrap or Tailwind. Experience with REST API integration is required."
            },
            {
                "title": "Data Scientist",
                "description": "Join our AI team to build predictive models. Proficiency in Python, Pandas, NumPy, Scikit-learn, and SQL is essential. Experience with NLP (spaCy, NLTK) or Deep Learning (TensorFlow) is a major advantage."
            },
            {
                "title": "Full Stack Developer",
                "description": "Build end-to-end web applications. Must be proficient in Python/Flask and React.js. Knowledge of Docker, Kubernetes, and AWS is required for deployment and scaling."
            },
            {
                "title": "DevOps Engineer",
                "description": "Maintain CI/CD pipelines and cloud infrastructure. Skills required: Docker, Kubernetes, Jenkins, Ansible, Terraform, and cloud platforms like AWS or Azure."
            },
            {
                "title": "Java Enterprise Developer",
                "description": "Develop scalable enterprise applications using Java and Spring Boot. Experience with Microservices, MySQL, and Kafka is highly desirable."
            },
            {
                "title": "AI/ML Researcher",
                "description": "Conduct research in Natural Language Processing and Computer Vision. Experience with PyTorch, Transformers, and academic research papers is required."
            }
        ]
        
        for job_data in sample_jobs:
            # Check if job title already exists
            existing_job = Job.query.filter_by(title=job_data["title"]).first()
            if not existing_job:
                job = Job(title=job_data["title"], description=job_data["description"])
                db.session.add(job)
                print(f"Added: {job_data['title']}")
            else:
                print(f"Exists: {job_data['title']}")
        
        db.session.commit()
        print("Finished seeding jobs!")

if __name__ == "__main__":
    seed_jobs()
