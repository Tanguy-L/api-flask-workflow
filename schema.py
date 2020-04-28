import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Tasks as TasksModel
from models import Sprints as SprintsModel
from models import Projects as ProjectsModel
from models import Users as UsersModel


class Tasks(MongoengineObjectType):
    class Meta:
        model = TasksModel
        interfaces = (Node,)

class Sprints(MongoengineObjectType):
    class Meta:
        model = SprintsModel
        interfaces = (Node,)

class Projects(MongoengineObjectType):
    class Meta:
        model = ProjectsModel
        interfaces = (Node,)

class Users(MongoengineObjectType):
    class Meta:
        model = UsersModel
        interfaces = (Node,)

class Query(graphene.ObjectType):
    node = Node.Field()
    all_projects = MongoengineConnectionField(Projects)
    all_users = MongoengineConnectionField(Users)

schema = graphene.Schema(query=Query, types=[Users, Projects])