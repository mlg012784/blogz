from flask import Flask, request, redirect, render_template, flash, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:mlg012784@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
app.secret_key = 'naya073115'





class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120))

    body = db.Column(db.String(500))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    



    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(120))

    password = db.Column(db.String(120))

    blog = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        
        self.username = username

        self.password = password
        
@app.before_request
def require_login():
    allowed_routes = ['login', 'index', 'signup','blog' ]
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
        
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        existing_user = User.query.filter_by(username=username).first()
        has_error = False
        if user and user.password != password:
            has_error =True
            flash('Password is incorrect', 'error')
        if not existing_user:
            has_error = True
            flash('Username does not exist', 'error')
        if has_error:
            return render_template('login.html', username=username)
        if not has_error and user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        request.form['verify']
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        has_error = False
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            name_error = 'Username already exists'
            return render_template('signup.html', name_error=name_error)
        if len(username) < 3:
            flash('Enter valid username', 'error')
            has_error = True
        if len(password) < 3:
            flash('Enter valid password', 'error')
            has_error= True
        if verify != password:
            flash('Passwords do not match', 'error')
            has_error= True
        if existing_user:
            flash('Username already exists', 'error')
            has_error = True
        if has_error:
            return render_template('signup.html', username= username)
        if not existing_user and not has_error:
            new_user = User(username, password)
            db.session.add(new_user)             
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
    return render_template('signup.html')




@app.route('/blog', methods=['POST', 'GET'])
def list_blogs():
    owner = User.query.filter_by(username=session['username']).first()
    
    
    if "id" in request.args:
        blogid = request.args.get("id")
        blogview = Blog.query.filter_by(id = blogid).first()
        return render_template('blogpost.html',blogview = blogview)
    if "user" in request.args:
        bloguser = request.args.get("user")
        userblogs= Blog.query.filter_by(owner_id = bloguser).all()
        return render_template('singleUser.html',userblogs = userblogs)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs = blogs)








@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        title_error = ""
        body_error = ""
        if title == "":
            title_error ="Title error"
        if body == "":
            body_error = "Body error"
        if title_error or body_error:
            return render_template('/newpost.html', title_error= title_error, body_error= body_error)
        else:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            newblogid = str(new_blog.id)
        return redirect('/blog?id=' + newblogid)
            

    return render_template('/newpost.html')

        
       
    
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
            

if __name__ == '__main__':

    app.run()