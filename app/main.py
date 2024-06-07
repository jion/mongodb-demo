from pymongo import MongoClient
import mongoengine as me

# Connect to MongoDB using pymongo
client = MongoClient('mongodb://mongodb:27017/')
db = client.demo

# Define a sample model using mongoengine
class Customer(me.Document):
    customer_id = me.StringField(required=True)
    name = me.StringField(required=True)
    subscriptions = me.ListField(me.DictField())
    error_logs = me.ListField(me.DictField())

# Connect to MongoDB using mongoengine
me.connect('demo', host='mongodb')

print("Connected to MongoDB")
