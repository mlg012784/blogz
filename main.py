from flask import Flask, request, redirect, render_template, flash

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mlg012784@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
app.secret_key = 'naya073115'





class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120))

    body = db.Column(db.String(500))



    def __init__(self, title, body):

        self.title = title

        self.body = body





@app.route('/blog', methods=['POST', 'GET'])
def index():
    
    if "id" in request.args:

        blogid = request.args.get("id")
        blogview = Blog.query.filter_by(id = blogid).first()
        

        return render_template('blogpost.html',blogview = blogview)
    
    else:
        blogs = Blog.query.all()

    
    
    
    #
   
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
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            newblogid = str(new_blog.id)
        return redirect('/blog?id=' + newblogid)
            

    return render_template('/newpost.html')

        
       
    
    
            

if __name__ == '__main__':

    app.run()