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
		avatar = data['avatar']
		password = data['password'].encode('utf-8')
		hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
		username_insert_query = "INSERT INTO user (username, password, avatar) VALUES ('%s', '%s', '%s')" % (username, hashed_password, avatar)

		cursor.execute(username_insert_query)
		conn.commit()
		return "reg successful"
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

	get_avatar_query = "SELECT avatar FROM user WHERE username = '%s'" % username
	cursor.execute(get_avatar_query)
	get_avatar_result = cursor.fetchone()

	if bcrypt.hashpw(password.encode('utf-8'), check_password_result[0].encode('utf-8')) == check_password_result[0].encode('utf-8'):
		return jsonify(get_avatar_result[0])

@app.route('/get_posts', methods=['POST'])
def get_posts():
	data = request.get_json()
	username = data['username']

	get_user_id_query = "SELECT id FROM user WHERE username = '%s'" % username
	cursor.execute(get_user_id_query)
	user_id = cursor.fetchone()
	# get_posts_query = "SELECT user.avatar, username, content, votes, time, location FROM posts JOIN user ON uid = user.id"
	get_posts_query = "SELECT user.avatar, username, content, votes, time, location, uid, posts.id FROM posts LEFT JOIN user ON uid = user.id LEFT JOIN follow on following_id = posts.uid WHERE follow.following_id IN (SELECT following_id from follow where follower_id = {0}) OR uid = {0} GROUP BY user.avatar, username, content, votes, time, location, uid, posts.id ORDER BY time ASC".format(user_id[0])

	cursor.execute(get_posts_query)
	get_posts_result = cursor.fetchall()
	conn.commit()
	return jsonify(get_posts_result)

@app.route('/new_post', methods=['POST'])
def new_post():
	data = request.get_json()
	new_post_content = data['newPostContent']
	username = data['username']

	get_user_id_query = "SELECT id FROM user WHERE username = '%s'" % username
	cursor.execute(get_user_id_query)
	get_user_id_result = cursor.fetchone()

	insert_post_query = "INSERT INTO posts (content, uid) VALUES (%s, %s)" 
	print insert_post_query
	cursor.execute(insert_post_query, (new_post_content, get_user_id_result[0]))
	conn.commit()
	return "success"

@app.route('/get_trending_users', methods=['POST'])
def get_trending_users():
	data = request.get_json()
	username = data['username']

	get_user_id_query = "SELECT id FROM user WHERE username = '%s'" % username
	cursor.execute(get_user_id_query)
	user_id = cursor.fetchone()
	print user_id

	# get_trending_users_query = "SELECT id, avatar, username FROM user WHERE username != '%s'" % username

	# get_trending_users_query = "SELECT user.id, avatar, username FROM user LEFT JOIN follow on following_id = user.id WHERE follow.following_id NOT IN (SELECT following_id from follow where follower_id = {0}) AND user.id != {0} GROUP BY user.id, avatar, username".format(user_id[0])

	get_trending_users_query = "SELECT user.id, avatar, username FROM user WHERE user.id NOT IN (SELECT following_id FROM follow WHERE follower_id = {0} GROUP BY following_id) AND user.id != {0} GROUP BY user.id, avatar, username ORDER BY rand()".format(user_id[0])
	cursor.execute(get_trending_users_query)
	trending_users_result = cursor.fetchall()
	print trending_users_result
	return jsonify(trending_users_result)

@app.route('/follow', methods=['POST'])
def follow():
	data = request.get_json()
	username = data['username']
	following_id = data['following_id']

	get_user_id_query = "SELECT id FROM user WHERE username = '%s'" % username
	cursor.execute(get_user_id_query)
	user_id = cursor.fetchone()

	follow_query = "INSERT INTO follow (follower_id, following_id) VALUES ('%s', '%s')" % (user_id[0], following_id)
	print follow_query
	cursor.execute(follow_query)
	conn.commit()

	return "yay!"


@app.route('/process_vote', methods=['POST'])
def process_vote():
	data = request.get_json()
	pid = data['vid']
	vote_type = data['voteType']
	username = data['username']

	get_user_id_query = "SELECT id FROM user WHERE username = '%s'" % username
	cursor.execute(get_user_id_query)
	get_user_id_result = cursor.fetchone()

	# check_user_votes_query = "SELECT * FROM vote INNER JOIN user ON user.id = vote.uid WHERE user.username = '%s' AND vote.pid = '%s' AND vote_type = '%s' AND user.id != %s" % (username, pid, vote_type, get_user_id_result[0])

	# check_user_votes_query = "SELECT * FROM vote INNER JOIN user ON user.id = vote.uid INNER JOIN posts on vote.pid = posts.id WHERE user.username = '%s' AND vote.pid = '%s' AND vote_type = '%s' OR posts.uid = %s" % (username, pid, vote_type, get_user_id_result[0])

	# check_user_votes_query = "SELECT * FROM vote INNER JOIN user ON user.id = vote.uid INNER JOIN posts on vote.pid = posts.id WHERE user.username = '%s' AND vote.pid = '%s' AND vote_type = '%s' OR posts.uid = %s" % (username, pid, vote_type, get_user_id_result[0])

	check_user_votes_query = "SELECT vote.id, vote.uid, vote.pid FROM vote INNER JOIN user ON user.id = vote.uid WHERE user.id = '%s' AND vote.pid = '%s' AND vote_type = '%s' OR vote.pid = %s IN (SELECT id FROM posts where uid = %s)" % (get_user_id_result[0], pid, vote_type, pid, get_user_id_result[0])

	cursor.execute(check_user_votes_query)
	check_user_votes_result = cursor.fetchone()
	print check_user_votes_query
	print check_user_votes_result

	# it's possible we get none back because the user hasn't voted on this post
	if check_user_votes_result is None:
		# print "I am here"
		insert_user_vote_query = "INSERT INTO vote (pid, uid, vote_type) VALUES ('%s', '%s', '%s')" %(pid,get_user_id_result[0], vote_type)
		cursor.execute(insert_user_vote_query)
		conn.commit()

		update_post_votes = "SELECT SUM(vote_type) AS user_votes FROM vote WHERE pid = '%s'" %(pid)
		cursor.execute(update_post_votes)
		post_vote = cursor.fetchone()
		conn.commit()

		update_vote_query = "UPDATE posts SET posts.votes = %s WHERE posts.id = %s" % (post_vote[0], pid)
		cursor.execute(update_vote_query)
		conn.commit()

		get_posts_query = "SELECT user.avatar, user.username, content, votes, time, location, uid, posts.id FROM posts LEFT JOIN user ON posts.uid = user.id LEFT JOIN follow on following_id = posts.uid WHERE follow.following_id IN (SELECT following_id from follow where follower_id = '%s') GROUP BY user.avatar, user.username, content, votes, time, location, uid, posts.id" % get_user_id_result
		cursor.execute(get_posts_query)
		get_post_result = cursor.fetchall()	
		conn.commit()
		if get_post_result:
			print 'voteCounted'
			return jsonify(get_post_result)
	else:
		print 'alreadyVoted'
		return jsonify('alreadyVoted')

# @app.route('/profile/<id>')
# def user_profile(id):

# 	get_posts_query = "SELECT user.avatar, user.username, content, votes, time, location, uid, posts.id FROM posts LEFT JOIN user ON posts.uid = user.id LEFT JOIN follow on following_id = posts.uid WHERE follow.following_id IN (SELECT following_id from follow where follower_id = '%s') GROUP BY user.avatar, user.username, content, votes, time, location, uid, posts.id" % id
# 	cursor.execute(get_posts_query)
# 	get_posts_result = cursor.fetchall()

# 	return render_template('profile.html', data = jsonify(get_posts_result) )




if __name__ == "__main__":
	app.run(debug=True)