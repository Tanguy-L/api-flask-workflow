from mongoengine import connect

from models import Projects, Sprints, Tasks, Users

connect("graphene-mongo-example", host="mongodb://localhost:27017/workflow-api", alias="default")


def init_db():
    # Create the fixtures
    print("test")
    task1 = Tasks(name="Test1", description="OUia sad asd", priority=1, difficulty=2)
    task2 = Tasks(name="Test2", description="Ceci n'est pas une fixture", priority=3, difficulty=0)

    newSprint = Sprints(name="new sprint", deadline=datetime.now, tasks=[task1, task2])

    newProject = Projects(name="Test", description="Oui", sprints=[newSprint])
    newProject.save()

    User1 = Users(name="User1", password="$2y$10$Cm2i2KVhfnuJrK5YrP/Dnuk6dCPYTcEpUbchqTqES/kJVZYJQNlpi", email="test@test.fr")
    User1.save()