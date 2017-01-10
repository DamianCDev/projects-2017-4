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
    def __init__(self, email, displayname, displaypicture, verified):
        self.email = email
        self.displayname = displayname
        self.displaypicture = displaypicture
        self.verifed = verified

    def login( email, password ):
        '''
        Given a email address and a password, will return the user class or False depending
        on whether or not the login was successful.

        Currently will only return James Curran
        '''
        print( 'Logging in as Supreme Overlord James Curran' )
        return User( 'james.r.curran@sydney.edu.au', 'James Curran', 'jamescurran.png', True )

    def register( email, password, username ):
        c = conn.cursor()
        # Check that the email is not currently in the database
        print( email )
        c.execute('SELECT email FROM user WHERE email = ?;', (email,) )
        print( c.fetchall() )
        if len( c.fetchall() ) > 0:
            return False
        else:
            password = hash_password( email, password )
            c.execute('SELECT user_id FROM user ORDER BY user_id DESC LIMIT 1;')
            user_id = 0
            fetch = c.fetchone()
            if fetch:
                print( fetch )
            c.execute('INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?);', (user_id, password, email, username, 0, False, 'default.png') )
            return User( 'james.r.curran@sydney.edu.au', 'James Curran', 'jamescurran.png', True )

    def get( email ):
        '''
        Gets a user object given an email.
        '''
        print( 'Obtained user.' )
        return User( 'james.r.curran@sydney.edu.au', 'James Curran', 'jamescurran.png', True )

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
        print( 'Most recent posts' )

    def get_by_location( location, amount ):
        '''
        Returns some of the nearest posts
        '''
        print( 'Nearby posts' )

    def rating( self ):
        '''
        Returns the rating of a post.
        '''
        print( 'Return ratings.' )

    def comments( self ):
        '''
        Returns a list of all the comments on the post
        '''
        print( 'Return comments.' )

class Comment:
    def __init__(self, comment_id, author, post, content):
        self.comment_id = comment_id
        self.author = author
        self.post = post
        self.content = content
        print( 'Incredible new comment!' )

    def create(user_id, postid, contents ):
        '''
        Given a user object, a post object, and a string
        creates a new comment on the specified post
        '''

        cur = conn.execute('''
        SELECT MAX(comment_id)
        FROM comments;
        ''')
        if cur.fetchone() is None:
            print('This is the first item')
        cur = conn.execute('''

        INSERT INTO comments VALUES (comment_id, postid, user_id, contents);

        ''')
        print( 'New comment has been created!' )
        return Comment()

class Ratings:
    def __init__(self):
        print('post ratings')
    def create(rating_id, user, post, rating):

        pass

'''
class Ratings:
	def __init__(self):
        print(' post ratings')

	def create(rating_id, user, post, rating):

        pass
'''
print(Comment.create(0, 10, 'testing 1 2 3'))
