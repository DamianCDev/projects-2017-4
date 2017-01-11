import unittest
import os
from robert import database_connect
from robert import terminate_connection
from robert import User
from create_db import init_db

class TestPlutonium(unittest.TestCase):

    def setUp(self):
        init_db( 'test.db' )
        self.conn = database_connect('test.db' )
        self.cur = self.conn.cursor()
        
    def test_connection(self):
        self.cur.execute('SELECT 7')
        self.assertEqual( self.cur.fetchone()[0], 7 )
        
    def test_register(self):
        u = User.register( 'james.r.curran@sydney.edu.au', 'tomtom', 'James Curran' )
        self.assertEqual( u.username, 'James Curran' )
    
    def test_register_fail(self):
        User.register( 'james.r.curran@sydney.edu.au', 'cranberry', 'James Currant' )
        print( self.cur.fetchall() )
        with self.assertRaises( ValueError ):
            User.register( 'james.r.curran@sydney.edu.au', 'cranberry', 'James Currant' )
    
    def test_login(self):
        User.register( 'james.r.curran@sydney.edu.au', 'tomtom', 'James Curran' )
        u = User.login( 'james.r.curran@sydney.edu.au', 'tomtom' )
        self.assertEqual( u.username, 'James Curran' )
        
    def test_getuser(self):
        User.register( 'james.r.curran@sydney.edu.au', 'tomtom', 'James Curran' )
        u = User.get( 'james.r.curran@sydney.edu.au' )
        self.assertEqual( u.username, 'James Curran' )
    
    def tearDown(self):
        terminate_connection()
        os.remove( 'test.db' )

if __name__ == '__main__':
    unittest.main()