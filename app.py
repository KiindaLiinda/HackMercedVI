from datetime import datetime
from flask import Flask
from flask import request, Response, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from forms import SignUpForm, LoginForm

app = Flask(__name__)
#helps with debugging errors while flask app is running
app.config["DEBUG"] = True

#SECRET_KEY generated using python interpreter:
# $ python
# >>> import secrets
# >>> secrets.token_hex(16)
# >>> a65643b9b52d637a11b3182e923e5703
app.config["SECRET_KEY"]= 'a65643b9b52d637a11b3182e923e5703'
login_manager = LoginManager()
login_manager.init_app(app)

#Using SQLite for development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackmerced.db'
db = SQLAlchemy(app)

###***** Users Table ******###
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(89))
    fullname = db.Column(db.String(89))
    email = db.Column(db.String(89))
    ucmId = db.Column(db.String(89))
    pwd = db.Column(db.String(128))
    bio = db.Column(db.String(500))
    major = db.Column(db.String(89))
    gradDate = db.Column(db.String(89))

    def check_password(self, userinputPwd):
        return check_password_hash(self.pwd, userinputPwd)

    def get_id(self):
        return self.email
###***** Users Table ******###

###***** Tracks Table ******###
class Threads(db.Model):
    __tablename__ = "Threads"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(89))
    addedTimeStamp = db.Column(db.DateTime, default=datetime.now)
    #we might need a different database type to hold comments (can be very long)
    description = db.Column(db.String(3000))
    '''{"owner": INT , "comment": String},{},{},{}'''
    replies = db.Column(db.String(3000), default=" ")
    upvotes = db.Column(db.Integer, default=0)
    downupvotes = db.Column(db.Integer, default=0)
    usersUpvoted = db.Column(db.String(3000), default=" ")
    userDownvoted = db.Column(db.String(3000), default=" ")
    owner_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    owner = db.relationship('Users', foreign_keys=owner_id)
###***** Tracks Table ******###

@login_manager.user_loader
def load_user(userInputEmail):
    return Users.query.filter_by(email=userInputEmail).first()

@app.route("/signout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def dashboard_home():
    return render_template('dashboard.html')

@app.route('/signup', methods= ['GET', 'POST'])
def register():
    form = SignUpForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash('Please enter valid credentials!', 'danger')
            return redirect(url_for('register'))


        #Check if username already exists
        #Make password atleast 8 charlong
        #Take to "finish making profile" one time page
        if not Users.query.filter_by(username=request.form['username']).first() and not Users.query.filter_by(email=request.form['email']).first():
            print('Query responded with None.')
            #create a row in DataBases

            newUser = Users(username=request.form['username'],
                           fullname=request.form['username'],
                           email=request.form['email'],
                           pwd= generate_password_hash(str(request.form['password'])))

            db.session.add(newUser)
            db.session.commit()
            flash('Thanks for signing up, you will now be able to login!', 'success')
            return redirect(url_for('login'))


        if Users.query.filter_by(username=request.form['username']).first():
            flash(f'That username is taken! Select another.', 'danger')
            return redirect(url_for('register'))

        if Users.query.filter_by(email=request.form['email']).first():
            flash('That email cannot be used.', 'danger')
            return redirect(url_for('register'))

        return redirect(url_for('register'))

    if request.method == "GET":
        return render_template('signup.html', form=form)




@app.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if not Users.query.filter_by(email=request.form['email']).first():
            flash('No user with that email!', 'danger')
            return redirect(url_for('login'))

        user = load_user(str(request.form['email']))
        if not user.check_password(request.form['password']):
            flash('Wrong password!', 'danger')
            return redirect(url_for('login'))


        print(type(user))
        login_user(user)
        return redirect(url_for('dashboard_home'))



    return render_template('login.html', form=form)

@app.route("/thread", methods=['GET','POST'])
@login_required
def make_thread():
    if request.method == "POST":
        if(request.form['title'] and request.form['description']):
            newThread = Threads(title=request.form['title'],
                                description=request.form['description'],
                                owner=current_user)
    else:
        return render_template("createpost.html")






    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8081")
