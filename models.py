from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
    IntField
)

class Users(Document):
    meta = {"collection": "users"}
    name = StringField()
    password = StringField()
    email = StringField()

class Tasks(EmbeddedDocument):
    name = StringField()
    description = StringField()
    priority = IntField()
    difficulty = IntField()
    assign_to = ReferenceField(Users)

class Sprints(EmbeddedDocument):
    name = StringField()
    deadline = DateTimeField()
    tasks = ListField(EmbeddedDocumentField(Tasks))

class Projects(Document):
    meta = {"collection": "projects"}
    name = StringField()
    description = StringField()
    sprints = ListField(EmbeddedDocumentField(Sprints))

class Workbench(Document):
    meta = {"collection": "workbench"}
    name = StringField()
    users = ReferenceField(Users)
    admins = ReferenceField(Users)
    projects = ReferenceField(Projects)