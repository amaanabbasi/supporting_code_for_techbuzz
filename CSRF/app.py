from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, IntegerField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'thisshouldbesecret'
app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30), unique=True)
    savings = db.Column(db.Integer)

class EmailForm(FlaskForm):
    email_address = StringField('Email')
    transfer = IntegerField("Transfer") 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    user = User.query.get(1)
    login_user(user)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = EmailForm()

    if form.validate_on_submit():
        transfer_to_email = form.email_address.data
        transfer_amount = int(form.transfer.data)
        
        current_user.savings -= transfer_amount
      
        u = User.query.filter_by(email_address = transfer_to_email).first()
        u.savings += transfer_amount
        

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('transfer.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
