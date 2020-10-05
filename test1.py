from flask import Flask, render_template, request, flash, redirect
app = Flask ("game") #flask is a class
app.config["SECRET_KEY"] = "gguu"
login_info={}

@app.route("/") # / is the landing page
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])  #get is to show the page, post is submitting 
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email in login_info:
            if password == login_info[email]:
                flash("Logged in")
                return redirect("/")
            else:
                flash("wrong password")
                return redirect("/login")
        else:
            flash("email not registered")
            return redirect("/login")
    else:
        return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if confirm_password != password:
            flash("PASSWORDS DO NOT MATCHHHHHHHHHH")
        else:
            if email not in login_info:
                login_info[email] = password
                print (login_info)
                flash("Registeredddd!!!!!")
            else:
                flash("already registered this email")
        return redirect("/register")
    else:
        return render_template("register.html")

app.run(debug=True, host="0.0.0.0")