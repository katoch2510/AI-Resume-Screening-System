import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Job

with app.app_context():
    jobs = Job.query.all()
    print(f"Number of jobs in database: {len(jobs)}")
    for job in jobs:
        print(f"- {job.title}")
