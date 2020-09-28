import pymongo
import datetime
client = pymongo.MongoClient ("mongodb+srv://anika_user:mongoDB123@anikasharma.eorxq.mongodb.net/schools?retryWrites=true&w=majority")
database = client["schools"]
my_collection= database["abc_schools"]

#student1 = {"Name":"Ben", "age":4, "grade": 11}
#my_collection.insert_one(student1)

#student2 = {"Name":"may", "age":17, "grade": 11}
#student3 = {"Name":"joel", "age":12, "grade": 4}
#students = [student2, student3]
#my_collection.insert_many(students)

#who=my_collection.find_one({"age":17})
#print(who)

#student4 = {"Name":"joel", "age":12, "grade": 4, "time": str(datetime.datetime.now().time())}
#my_collection.insert_one(student4)

# vvv = my_collection.find ()
# print (vvv)
# for x in vvv:
#     print (x)

# vvv = my_collection.find_one()
# print (vvv)
# print (vvv["age"])

# vvv = my_collection.find({"grade":11})
# for x in vvv:
#     print (x)

"""collection.update_one({what to update}, {what to change to})"""
#my_collection.update_one({"Name":"joel"}, {"$set":{"grade":5}})

#my_collection.update_many({"Name":"joel"}, {"$set":{"grade":6}})

#my_collection.delete_many({"Name":"joel"})
#my_collection.delete_one({"Name":"Ben"})


vvv = my_collection.find_one({"Name": "may"})
print (vvv["grade"])