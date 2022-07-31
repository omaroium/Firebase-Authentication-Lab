from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

Config = {
  "apiKey": "AIzaSyANLPhKM9jGfaDSogaOumeFzbf8KtcS1_I",
  "authDomain": "fir-1-96645.firebaseapp.com",
  "projectId": "fir-1-96645",
  "storageBucket": "fir-1-96645.appspot.com",
  "messagingSenderId": "522523454877",
  "appId": "1:522523454877:web:04ad1af07ce78ff2969374",
  "measurementId": "G-KL0299R963",
  "databaseURL":"https://fir-1-96645-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase=pyrebase.initialize_app(Config)
auth = firebase.auth()
db=firebase.database()
#Initialize Firebase


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['username']
        firstname = request.form['firstname']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": name, "email": email,"password":password,"firstname":firstname}
            db.child("Users").child(login_session['user']
            ['localId']).set(user)
            return redirect(url_for('signin'))
        except:
           error = "Authentication failed"
   return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def signin():

    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
       try:
           article = {"name": request.form['title'],"content": request.form['text']}
           db.child("Articles").push(article)
       except:
           print("Couldn't add article")
    return render_template("add_tweet.html")

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    login_session['user'] = None
    auth.current_user = None

    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)