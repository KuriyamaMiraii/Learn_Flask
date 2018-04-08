from flask import Flask,render_template,session,redirect,url_for,flash
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class NameForm(Form):
	name = StringField('What is your name?',validators=[Required()])
	submit = SubmitField('Submit')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=\
	'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db=SQLAlchemy(app)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '123456'


class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User',backref='role')
	def __repr__(self):
		return '<Role %r>'%self.name

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True,index=True)
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>'% self.username




@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name=session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Look,you have changed your name!')
		session['name']=form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'))


@app.route('/usr/<name>')
def usr(name):
	return render_template('user.html',name=name)

 
if __name__ == '__main__':
	app.run(host='0.0.0.0',port = 5000,debug=True)

