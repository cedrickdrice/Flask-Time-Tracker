"""
Import and Configure Flask App and DB
"""
from app import app, db
from app.models.project import Project

# Configure the Flask App
def create_app():
    with app.app_context():
        db.create_all()

        if Project.query.count() == 0:
            projects = [
                Project(name="Project 1", description="Project 1 Description"),
                Project(name="Project 2", description="Project 1 Description"),
                Project(name="Project 3", description="Project 3 Description")
            ]

            for project in projects:
                db.session.add(project)
                
            db.session.commit()
    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=5000)