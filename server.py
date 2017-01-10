from tornado.ncss import Server 
from re_template_renderer import render_template
from db.plutonium import User,Post,Comment


###DECORATORS###
def loginRequired(fn):
    def inner(response, *args, **kwargs):
        user = response.get_secure_cookie('userCookie')
        if user is None:
            response.redirect('/login')
        else:
            return fn(response, *args, **kwargs)
    return inner

    
def home(response):
    user = get_current_user(response)        
    html = render_template('main.html', {'user': user})
    response.write(html)



def login_handler(response):
    email = response.get_field("email")
    password = response.get_field("password")
    if (email + password) == "loginpassword":    
        response.set_secure_cookie('userCookie', email)
        
        response.redirect('/home')
    else: 
        response.write("invalid user")
    
def profile(response,name):
    user = get_current_user(response)        
    html = render_template('profile.html', {'user': user})
    response.write(html)
    
def get_current_user(response):
    email = response.get_secure_cookie("userCookie")
    
    user = User()
     
    
    if email is not None:
        email = email.decode()
        return user
    return None
    
        


def post(response,post_id):
    user = get_current_user(response)        
    html = render_template('new_post.html', {'user': user})
    response.write(html)
        
def demo(response):
    user = get_current_user(response)        
    html = render_template('demo.html', {'user': user})
    response.write(html)

def notfound(response):
    response.write("Lol not found")
    
###NOT LOGGED IN EXCLUSIVE PAGES###    
def login(response): 
    user = get_current_user(response)        
    html = render_template('login.html', {'user': user})
    response.write(html)
    
def signup(response):
    user = get_current_user(response)        
    html = render_template('registration.html', {'user': user})
    response.write(html)    
    
    
###LOGIN EXCLUSIVE PAGES###    
@loginRequired
def submit(response):
    html = render_template('new_post.html', {})
    response.write(html)
        
@loginRequired    
def logout(response):
    response.clear_cookie("userCookie")
    response.redirect('/home')
        
        
server = Server()
server.register(r'/?(?:home)?', home)
server.register(r'/profile(?:/([\w\.\-]+))?', profile)
server.register(r'/login', login, post=login_handler)
server.register(r'/signup',signup)
server.register(r'/post/([\w\.\-]+)',post)
server.register(r'/submit',submit)
server.register(r'/demo',demo)
server.register(r'/logout',logout)
server.register(r'.+',notfound)


server.run()
