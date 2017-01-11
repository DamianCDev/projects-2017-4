from hashlib import sha512
import sqlite3

conn = sqlite3.connect('street.db')
cur = conn.cursor()

def database_connect():
    if conn is None:
        conn = sqlite3.connect('street.db')
        cur = conn.cursor()

    return conn

def hash_password( email, password ):
    '''
    This function is used to salt and hash passwords
    Uses strong recent hashing algorithms + salts to ensure
    that our users are secure at all times.

    Email address is used as a salt.
    '''
    string = email + password
    h = sha512()
    h.update( string.encode() )
    return h.hexdigest()

class User:
    '''
    User Object
    '''
    def __init__(self, user_id, email, username, level, is_verified, profile_picture ):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.level = level
        self.is_verifed = is_verified
        self.profile_picture = profile_picture

    @staticmethod
    def login( email, password ):
        '''
        Given an email address and an unhashed password
        Will return a User object if valid login
        Will throw error if invalid login
        '''
        c = conn.cursor()
        password = hash_password( email, password )
        # Ensure that the user is in the database
        c.execute('SELECT * FROM user WHERE email = ?;', (email,) )
        data = c.fetchone()
        if data is None:
            raise ValueError("User is not in database")
        else:
            storedhash = data[1]
            # Hash the given password and compare it to the storedhash
            if password == storedhash:
                return User( data[0], data[2], data[3], data[4], data[5], data[6] )
            else:
                raise ValueError("Password Mismatch")

    @staticmethod
    def register( email, password, username ):
        '''
        Given the required data, registers an account in the database
        Will return False if the account does not meet registration requirements
        '''
        c = conn.cursor()
        # Check that the email is not currently in the database
        c.execute('SELECT email FROM user WHERE email = ?;', (email,) )
        if len( c.fetchall() ) > 0:
            return False
        else:
            password = hash_password( email, password )
            # Get the maximum user_id in the database to increment for next user
            c.execute('SELECT MAX(user_id) FROM user;')
            user_id = 0
            fetch = c.fetchone()
            if fetch[0] is not None:
                user_id = fetch[0] + 1
            # Insert the user into the database
            c.execute('INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?);', (user_id, password, email, username, 0, 0, 'default.png') )
            conn.commit()
            return User( user_id, email, username, 0, 0, 'default.png' )

    @staticmethod
    def get( email ):
        '''
        Gets a user object given an email.
        '''
        c = conn.cursor()
        c.execute('SELECT * FROM user WHERE email = ?;', (email,) )
        data = c.fetchone()
        if data is None:
            raise ValueError("User is not in database")
        else:
            return User( data[0], data[2], data[3], data[4], data[5], data[6] )

    def get_all():
        '''
        Returns a list of all the users
        NOTE: This can be large - be careful
        '''
        print( 'All users.' )

    def edit_displayname( self, newname ):
        '''
        Changes the displayname of a user class.
        '''
        self.displayname = newname
        print( 'Display name updated.' )

    def get_posts( self ):
        '''
        Returns a list of all the post objects that the user has made
        '''
        print( 'Post objects.' )

    def rate( self, post, rating ):
        '''
        Gets the user to vote on a given post object
        Rating should be -1, 0, or 1
        '''
        print( 'Vote cast!' )

    # TODO: Functions for verified status and title management

class Post:
    def __init__(self, post_id, author_id, location, title, description, image):
        self.id = post_id
        self.author_id = author_id
        self.location = location
        self.title = title
        self.description = description
        self.image = image
        self.rating = Rating.post_rating(post_id)

    def create( user, title, description, image, location ):
        '''
        Creates a new post given the user object, title, description, image, and location.
        '''
        cur = conn.cursor()
        cur.execute('SELECT id FROM post ORDER BY id DESC LIMIT 1;')
        post_id = cur.fetchone()
        print(post_id)
        # cur.execute("""
        # INSERT INTO post
        # VALUES (
        # id,
        # author_id,
        # location,
        # title,
        # description,
        # image,
        # rating
        # )""", (
        #
        # ))
        print( 'New post created!' )
        return Post()

    def get( postid ):
        '''
        Returns a post object given a postid
        '''
        print( 'Obtained post!' )
        return Post()

    def get_all():
        '''
        Returns a list containing every post object
        NOTE: This can be large - be careful
        '''
        print( 'All the posts!' )

    def get_by_recent( amount ):
        '''
        Returns some of the most recent posts created
        '''
        cur = conn.execute('''
        SELECT *
        FROM post
        ORDER BY post_id DESC LIMIT ?

        ''', (amount,))

    def get_by_location(location, amount):
        '''
        Returns some of the nearest posts
        '''
        return(location, amount)



        print( 'Nearby posts' )

    def rating(post_id):
        '''
        Returns the rating of a post.
        '''
        return Ratings.post_ratings(post_id)
        print( 'Return ratings.' )

    def comments(post_id):
        '''
        Returns a list of all the comments on the post
        '''
        cur = conn.execute('''

        SELECT *
        FROM comments c
        WHERE c.post_id = ?


        ''', (post_id))

        comments_section = []
        for row in cur:
            comments_section.append(row)

        return comments_section

class Comment:
    def __init__(self, comment_id, author, post, content):
        self.comment_id = comment_id
        self.author = author
        self.post = post
        self.content = content

    def create(user_id, postid, contents ):
        '''
        Given a user object, a post object, and a string
        creates a new comment on the specified post
        '''


        cur = conn.execute('''

        INSERT INTO comments (post_id, author, comment) VALUES (?, ?, ?);

        ''', (postid, user_id, contents))
        conn.commit()
        return Comment(cur.lastrowid, user_id, postid, contents)

class Ratings:
    def __init__(self, rating_id, user, post, rating):
        self.rating_id = rating_id
        self.user = user
        self.post = post
        self.rating = rating
    def user_rate(user, post, rating):
        '''Makes a user cast a vote on a post '''

        cur = conn.execute('''

        INSERT INTO post_ratings (user, post, rating) VALUES (?, ?, ?);
        ''', (user, post, rating))
        conn.commit()
        return Ratings(cur.lastrowid, user, post, rating)

    def post_ratings(postid):
        '''Returns rating of a post summation of user votes '''

        cur = conn.execute('''

        SELECT SUM(rating)
        FROM post_ratings

        WHERE post = ?


        ''' ,(postid,))

        row = cur.fetchone()
        return row[0]


print(Post.get_by_recent(10))

cur = conn.execute('SELECT * FROM Post')

for row in cur:
    print(row)
