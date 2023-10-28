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
    register_form,
    CommentForm
)
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError
)
from api.database import DATABASE
from api.models import User
from api.authentication import AUTH
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar


app = Flask(__name__)

app.secret_key = "%70386728037#567289376bdf7wgsn"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
CKEditor(app)

# gravatar = Gravatar(app,
#                     size=100,
#                     rating='g',
#                     default='retro',
#                     force_default=False,
#                     force_lower=False,
#                     use_ssl=False,
#                     base_url=None)


userDb = DATABASE()
auth = AUTH()


@app.route("/new-post", methods=['POST', 'GET'])
def add_new_post():
    return render_template("new-post.html", is_edit=False)

@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def show_post(post_id):
    request_post = userDb.get_posts_by_id(post_id)
    comments = userDb.get_all_comments(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        newcomment = userDb.add_newComments(text=comment, comment_author='userName', parent_post=request_post)
        if(newcomment):
            flash('Success')
        else:
            flash('Error')
    else:
        flash('Error')
    return render_template("post.html", post=request_post, all_comment=comments, form=form)

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    return redirect(url_for('get_all_posts'))

@app.route('/', methods=['POST','GET'])
def get_all_posts():
    posts = userDb.get_all_posts()
    return render_template('home.html', all_posts=posts)


@app.route('/home', methods=['GET'])
def home():
    posts = userDb.get_all_posts()
    return render_template('home.html', all_posts=posts)


@app.route('/user/register', methods=['POST', 'GET'])
def register_user():
    form = register_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        print(f"{email} -- {password} -- {full_name}")
        try:
            with userDb._session.begin():
                new_user = auth.register(email=email, password=password, full_name=full_name)
                print(new_user.email)
            flash(f"Account succesfully created", "success")
            return redirect(url_for('login'))
        except Exception as e:
            userDb._session.rollback()
            flash(f"{e}", "warning")
        
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

@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    post = userDb.get_posts_by_id(post_id)
    return render_template("make-post.html")


@app.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
