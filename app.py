from flask import (
    Flask,
    flash,
    redirect,
    url_for,
    render_template,
    session
)
from api.forms import (
    login_form,
    register_form,
    CommentForm
)
from api.posts import POSTS
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


post_handler = POSTS()
auth = AUTH()

#post routes
@app.route("/new-post", methods=['POST', 'GET'])
def add_new_post():
    return render_template("new-post.html", is_edit=False)


@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def show_post(post_id):
    request_post = post_handler.get_posts_by_id(post_id)
    comments = post_handler.get_all_comments(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        newcomment = post_handler.add_newComments(text=comment, comment_author='userName', parent_post=request_post)
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


@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    post = post_handler.get_posts_by_id(post_id)
    return render_template("make-post.html")

#user routes
@app.route('/', methods=['GET', 'POST'])
def home():
    print(session.get('session_id'))
    if session.get('session_id'):
        posts = post_handler.get_all_posts()
        return render_template('home.html', all_posts=posts)
    else:
        return redirect(url_for('login'))
        

@app.route('/user/register', methods=['POST', 'GET'])
def register():
    form = register_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        try:
            auth.register(email=email, password=password, full_name=full_name)
            flash(f"Account succesfully created", "success")
            return redirect(url_for('login'))
        except Exception as e:
            auth.session_manager().rollback()
            flash(f"{e}", "warning")
        
    return render_template('register.html', form=form)


@app.route('/user/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            session_id = auth.login(email=email, password=password)
            session['session_id'] = session_id
            return redirect(url_for('home'))
        except Exception as e:
            auth.session_manager().rollback()
            flash(f"{e}", "warning")
         
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    print('before logout', session.get('session_id'))
    if 'session_id' in session:
        session['session_id'] = None
    print('after logout', session.get('session_id'))
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
