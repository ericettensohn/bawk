from flask import Flask, render_template, redirect, request, jsonify
from flaskext.mysql import MySQL
import bcrypt as bcrypt


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'bawk'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

app.secret_key = 'ahdsljahdasddjhlsdgjh'

conn = mysql.connect()
cursor = conn.cursor()


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register_submit', methods=['POST'])
def register_submit():
	data = request.get_json()
	username = data['username']
	check_username_query = "SELECT username FROM user WHERE username = '%s'" % (username)

	cursor.execute(check_username_query)
	check_username_result = cursor.fetchone()


	if check_username_result is None:
		email = data['email']
		password = data['password'].encode('utf-8')
		hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
		username_insert_query = "INSERT INTO user (username, password, email) VALUES ('%s', '%s', '%s')" % (username, hashed_password, email)

		cursor.execute(username_insert_query)
		conn.commit()
		return "you are logged in"
	else:
		print "username taken"
		return redirect('/register?username=taken')

	# return "done"

# @app.route('/register')
# def register():
# 	if request.args.get('username'):
# 		return render_template('register.html',
# 			message = "that username is already taken")
# 	else:
# 		return render_template('index.html')

@app.route('/login_submit', methods=['POST'])
def login_submit():
	data = request.get_json()
	username = data['username']
	password = data['password']

	check_password_query = "SELECT password FROM user WHERE username = '%s'" % username
	cursor.execute(check_password_query)

	check_password_result = cursor.fetchone()

	# to check a hash against english
	# if bcrypt.hashpw(password, check_password_result[0]) == check_password_result:
	# 	print "match!"

	if bcrypt.hashpw(password.encode('utf-8'), check_password_result[0].encode('utf-8')) == check_password_result[0].encode('utf-8'):
		return "true"

@app.route('/get_posts')
def get_posts():
	get_posts_query = "SELECT posts.avatar, username, content, votes, time, location FROM posts JOIN user ON uid = user.id"
	cursor.execute(get_posts_query)
	get_posts_result = cursor.fetchall()
	return jsonify(get_posts_result)



if __name__ == "__main__":
	app.run(debug=True)