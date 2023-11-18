from app import app, db
from app.models.project import Project

# Configure the Flask App
with app.app_context():
    db.create_all()
    
    if Project.query.count() == 0:
        """
        Insert project records
        """
        projects = [
            Project(name="Project 1", description="Project 1 Description"),
            Project(name="Project 2", description="Project 2 Description"),
            Project(name="Project 3", description="Project 3 Description"),
            Project(name="Project 4", description="Project 4 Description"),
            Project(name="Project 5", description="Project 5 Description"),
        ]

        for project in projects:
            db.session.add(project)
            
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
