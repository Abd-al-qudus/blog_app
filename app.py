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

userDb = DATABASE()
auth = AUTH()

@app.route('/user/register', methods=['POST'])
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

@app.route('/user/login', methods=['POST'])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
