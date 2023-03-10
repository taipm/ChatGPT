from ssl import CertificateError
from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Welcome to my blog!"

# if __name__ == "__main__":
#     app.run()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from pymongo import MongoClient

app = Flask(__name__)
#dBjKFnQLiLHM1Jyd
app.secret_key = "dBjKFnQLiLHM1Jyd"

login_manager = LoginManager()
login_manager.init_app(app)

#client = MongoClient("mongodb://localhost:27017/")
#db = client["BlogGPT"]
#users_collection = db["users"]


client = MongoClient("mongodb+srv://taipm:dBjKFnQLiLHM1Jyd@cluster0.op5mel7.mongodb.net/?retryWrites=true&w=majority")
db = client['BlogGPT']
users_collection = db["users"]

class User(UserMixin):
    def __init__(self, username, password, id):
        self.username = username
        self.password = password
        self.id = id

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": user_id})
    if user:
        return User(user["username"], user["password"], user["_id"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if username and password and email:
            existing_user = User.objects(username=username).first()
            if existing_user is None:
                hash_password = generate_password_hash(password)
                user = User(username=username, password=hash_password, email=email).save()
                flash('Đăng ký thành công! Hãy đăng nhập.')
                return redirect(url_for('login'))
            else:
                flash('Tên người dùng đã tồn tại! Vui lòng chọn tên khác.')
        else:
            flash('Vui lòng điền đầy đủ thông tin!')
    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            user_obj = User(user["username"], user["password"], user["_id"])
            login_user(user_obj)
            flash("Login successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
