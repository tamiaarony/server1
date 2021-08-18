import pymongo
from pymongo import MongoClient
import manager_controller as mc
client=MongoClient()
db=client['extensiondb']
users=db.users
# return all users
def getall():
    return users.find({})
#return user by password
def getbypassword(password):
    return  users.find({"password":password}).next()
#insert new user
def insert_user(new_user): 
    users.insert_one(new_user)
#delete user
def delete_user(password):
    users.delete_one({"password":password})
#update user
def update_user(new_user):
    users.delete_one({"password":new_user["password"]})
    users.insert_one(new_user)
print(mc.getall().next())

    
 