from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime

tweet={}


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
           now = datetime.now()
           tweet={"title":request.form['title'],"text":request.form['text'], "uid": login_session['user']['localId'],"time":now.strftime("%d/%m/%Y %H:%M:%S"),"likes":0}
           db.child("Tweets").push(tweet)
       except:
           print("Couldn't add article")
    return render_template("add_tweet.html",    tweets2=db.child("Tweets").get().val()
)

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweet():
    if request.method == 'POST':
        print("YOOOOOOOOOOOOOOOOOO")
        try:
            print("yoyoyo")
            return render_template("tweets.html")
        except:
            print("Couldn't add article")
            redirect(url_for('add_tweet'))
    return render_template("tweets.html",tweets2=db.child("Tweets").get().val())

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    login_session['user'] = None
    auth.current_user = None

@app.route('/like/<string:k>', methods=['GET', 'POST'])
def like(k):
    if request.method == 'POST':
        
        try:
            likes = {'likes' : db.child('Tweets').child(k).get().val()['likes'] + 1}
            db.child("Tweets").child(k).update(likes)
            return redirect(url_for('all_tweet'))
        except:
            return redirect(url_for('all_tweet'))
    return redirect(url_for('all_tweet'))
if __name__ == '__main__':
    app.run(debug=True)