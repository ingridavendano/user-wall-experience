import sqlite3
from datetime import date

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551
DB = None
CONN = None

################## HELPER FUNCTIONS ##################
def connect_to_db():
	global CONN 
	CONN = sqlite3.connect('thewall.db')
	global DB 
	DB = CONN.cursor()


def get_username_by_id(user_id):
	query = """SELECT username 
				FROM users
				WHERE id=?"""
	DB.execute(query, (user_id,))

	return DB.fetchone()[0]


def get_id_by_username(username):
	query = """SELECT id
				FROM users
				WHERE username=?"""
	DB.execute(query, (username,))
	
	return DB.fetchone()[0]
######################################################


def authenticate(username, password):
	query = """SELECT id, username, password FROM users WHERE username = ?"""
	DB.execute(query, (username,))
	row = DB.fetchone()

	if username == row[1] and str(hash(password)) == row[2]:
		return row[0]
	else:
		return None


# returns the content, date, username of authors that write wall posts 
def get_user_by_name(username):
	query = """SELECT wp.content, wp.created_at, owner.username, author.username
			FROM users AS author, users AS owner
			INNER JOIN wall_posts AS wp ON (owner.id = wp.owner_id)
			WHERE (wp.author_id = author.id) AND owner.username =?"""

	DB.execute(query, (username,))
	rows = DB.fetchall()
	return rows 


def make_wall_post(author_id, owner_username, content):
	# grab the id of a owner by their username
	owner_id = get_id_by_username(owner_username)

	# make a post providing all the information we need 
	insert_query = """INSERT INTO wall_posts
					VALUES (NULL, ?, ?, ?, ?)"""
	DB.execute(insert_query, (owner_id, author_id, date.today(), content))
	CONN.commit()


def create_new_user(username, password):
	# use a hash password in case DB gets broken into
	print "username", username
	print "password", password
	hash_password = str(hash(password))

	new_user_query = """INSERT INTO users
						VALUES (NULL, ?, ?)"""
	DB.execute(new_user_query, (username, hash_password))
	CONN.commit()
	return

	