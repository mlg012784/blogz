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


    def __init__(self, name, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(120))

    password = db.Column(db.String(120))

    blog = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        
        self.username =username

        self.password = password

        
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect,or user does not exist', 'error')
    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    name_error =''
    pass_error= ''
    ver_error= ''
    
    
    if request.method == 'POST':

        
        if len(username) < int(3) or len(username) > int(20):
            username = ''
            name_error = 'Enter valid username'
        else:
            if ' ' in username:
                name_error = 'Enter valid username'
                username = ''

        if len(password) < int(3) or len(password) > int(20):
            pass_error = "That's not a valid password"
            password = '' 
        else:
            if ' ' in password:
                pass_error = "That's not a valid password"
                password = ''
        if password != verify:
            ver_error = 'passwords do not match' 
            verify= ''
        existing_user = User.query.filter_by(username=username).first()    
        

        
        if not existing_user and not name_error and not pass_error and not ver_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            if existing_user:
                flash('Username already exists')
                return render_template('signup.html')

        
    else:
        return render_template('signup.html', name_error=name_error, username=username, pass_error=pass_error, password=password,ver_error=ver_error, verify=verify)

@app.route('/blog', methods=['POST', 'GET'])
def index():
    
    if "id" in request.args:

        blogid = request.args.get("id")
        blogview = Blog.query.filter_by(id = blogid).first()
        

        return render_template('blogpost.html',blogview = blogview)
    
    else:
        blogs = Blog.query.all()

    
    
    

   
        return render_template('blog.html', blogs = blogs)



@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        title_error = ""
        body_error = ""
        if title == "":
            title_error ="titleerror"
        if body == "":
            body_error = "bodyerror"
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
    return redirect('/')
            

if __name__ == '__main__':

    app.run()