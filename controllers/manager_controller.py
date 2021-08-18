import pymongo
from pymongo import MongoClient
client=MongoClient()
db=client['extensiondb']
managers=db.managers
# return all managers
def getall():
    return managers.find({})
#return manager by password
def getbypassword(password):
    return  managers.find({"password":password}).next()
#insert new manager
def insert_manager(new_manager):
    managers.insert_one(new_manager)
#delete manager
def delete_manager(password):
    managers.delete_one({"password":password})
#update manager
def update_manager(new_manager):
    managers.delete_one({"password":new_manager["password"]})
    managers.insert_one(new_manager)