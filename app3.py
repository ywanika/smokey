from flask import Flask, render_template, request, flash, redirect
import pymongo
import datetime
app = Flask("smokey")
app.config["SECRET_KEY"] = "gguu"

client = pymongo.MongoClient ("mongodb+srv://anika_user:mongoDB123@anikasharma.eorxq.mongodb.net/smokey_user_data?retryWrites=true&w=majority")
database = client["smokey"]
login_info= database["smokey_user_data"]


@app.route("/") # / is the landing page
def index():
    email = request.args.get("email")
    print (email)
    if email is not None:
        user_data = login_info.find_one({"email":email})
        if "logged_in" in user_data:
            if user_data["logged_in"] == True:
                return render_template("index.html", name = user_data["name"], email = email)
            else: 
                return redirct("/login")
        else: 
            flash("shoo away hacker")
            return redirect ("/login") 
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
        user_data = login_info.find_one({"email":email})
        if confirm_password != password:
            flash("PASSWORDS DO NOT MATCHHHHHHHHHH")
            return redirect("/register")
        else:
            if user_data is None:
                login_info.insert_one({"name":name, "email":email, "password":password, "registration_time":str(datetime.datetime.now())})
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
        user_data = login_info.find_one({"email":email})
        if user_data != None:
            if user_data["password"] == password:
                flash("Sucessful login")
                login_info.update_one({"email":email}, {"$set":{"logged_in":True}})
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
    login_info.update_one({"email":email}, {"$set":{"logged_in":False}})
    flash("You have logged out")
    return redirect("/login")

@app.route("/setstatus")
def setstatus():
    return render_template("setStatus.html")

app.run()

#posts