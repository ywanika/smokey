from flask import Flask, render_template, request, flash, redirect, session
import pymongo
import datetime
import os
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "gguu"
if os.environ.get("MONGO_URI") == None :
    file = open("connection_string.txt","r")
    connection_string = file.read().strip()
    app.config['MONGO_URI']=connection_string
else:
    app.config['MONGO_URI']= os.environ.get("MONGO_URI")
mongo = PyMongo(app)

print("app has been configured")
@app.route("/") # / is the landing page
def index():
    email = request.args.get("email")
    print (email)
    if "user" in session:
        user_data = mongo.db.smokey_user_data.find_one({"email":session["user"]})
        if "status" in user_data:
            return render_template("index.html", name = user_data["name"], email = email, status = user_data["status"])
        else:
            return render_template("index.html", name = user_data["name"], email = email, status = None)
    else:
        flash("Please log in")
        return redirect("/login")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        user_data = mongo.db.smokey_user_data.find_one({"email":email})
        if confirm_password != password:
            flash("PASSWORDS DO NOT MATCHHHHHHHHHH")
            return redirect("/register")
        else:
            if user_data is None:
                mongo.db.smokey_user_data.insert_one({"name":name, "email":email, "password":password, "registration_time":str(datetime.datetime.now())})
                flash("Registered!")
                return redirect("/login")
            else:
                flash("email already registered")
                return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print (email, password)
        user_data = mongo.db.smokey_user_data.find_one({"email":email})
        print (user_data)
        if user_data != None:
            if user_data["password"] == password:
                session["user"] = email
                flash("Sucessful login")
                mongo.db.smokey_user_data.update_one({"email":email}, {"$set":{"logged_in":True}})
                print ("jijiiji")
                return redirect("/?email="+email)
            else:
                flash("Incorrect password")
                return redirect("/login")
        else:
            flash("Email not registered")
            return redirect("/register")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    email = request.args.get("email")
    session.pop("user")
    mongo.db.smokey_user_data.update_one({"email":email}, {"$set":{"logged_in":False}})
    flash("You have logged out")
    return redirect("/login")

@app.route("/setstatus", methods=["GET", "POST"])
def setstatus():
    email = request.args.get("email")
    if request.method == "POST":
        status = request.form["status"]
        mongo.db.smokey_user_data.update_one({"email":email}, {"$set":{"status":status}})
        return redirect("/?email="+email)
    else:
        return render_template("setStatus.html")

if __name__=='__main__':
    app.run()

#posts - http://127.0.0.1:5000/?email=fire@water.com