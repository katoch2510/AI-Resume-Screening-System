from app import app, db, Job
with app.app_context():
    count = Job.query.count()
    print(f"Total Jobs: {count}")
