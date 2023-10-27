from flask import (
    Flask,
    request,
    jsonify,
    abort,
    flash,
    redirect,
    url_for,
    render_template
)
from api.forms import (
    login_form,
    register_form
)
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError
)
from api.user.database import DATABASE
from api.user.models import User
from api.user.authentication import AUTH



app = Flask(__name__)
app.secret_key = "%70386728037#567289376bdf7wgsn"


userDb = DATABASE()
auth = AUTH()

@app.route('/', methods=['POST','GET'])
def get_all_posts():
    posts = userDb.get_all_posts()
    return render_template('home.html', all_posts=posts)

@app.route("/new-post", methods=['POST', 'GET'])
def add_new_post():
    return render_template("New Post")

@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def show_post(post_id):
    # requested_post = BlogPost.query.get(post_id)
    # form = CommentForm()
    # all_comment = Comment.query.filter_by(post_id=post_id).all()
    # if form.validate_on_submit():
    #     if not current_user.is_authenticated:
    #         flash("You need to login or register to comment.")
    #         return redirect(url_for("login"))
        
    #     comment = form.comment.data
    #     new_comment = Comment(
    #         text=comment,
    #         comment_author=current_user,
    #         parent_post=requested_post
    #     )
    #     db.session.add(new_comment)
    #     db.session.commit()
    # else:
    #     flash('Error')
    return render_template("post.html")

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    return redirect(url_for('get_all_posts'))

@app.route('/user/register', methods=['POST', 'GET'])
def register_user():
    form = register_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
    try:
        new_user = auth.register(email=email, password=password, full_name=full_name)
        flash(f"Account succesfully created", "success")
        return redirect(url_for('login'))
    except InvalidRequestError:
        userDb._session.rollback()
        flash(f"Something went wrong!", "danger")
    except IntegrityError:
        userDb._session.rollback()
        flash(f"User already exists!.", "warning")
    except DataError:
        userDb._session.rollback()
        flash(f"Invalid Entry", "warning")
    except InterfaceError:
        userDb._session.rollback()
        flash(f"Error connecting to the database", "danger")
    except DatabaseError:
        userDb._session.rollback()
        flash(f"Error connecting to the database", "danger")
    
    return render_template('register.html', form=form)

@app.route('/user/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:    
            auth.login(email=email, password=password)
            return redirect(url_for('home'))
        except Exception as e:
            userDb._session.rollback()
            flash(f"{e}", "warning")
         
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
