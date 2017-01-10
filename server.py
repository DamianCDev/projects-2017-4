from tornado.ncss import Server

def loginRequired(fn):
	def inner(response, *args, **kwargs):
		user = response.get_secure_cookie('userCookie')
		if user is None:
			response.redirect('/login')
		else:
			return fn(response, *args, **kwargs)
	return inner

def home(response):
	with open('templates/main.html') as mainHTML:
		response.write(mainHTML.read())

def login(response): 
	with open ('templates/login.html') as loginHTML: 
		response.write(loginHTML.read())

	
def profile(response,name):
        response.write('Hi, ' + str(name))
		
	
def login_handler(response):
	email = response.get_field("email")
	password = response.get_field("password")
	if (email + password) == "loginpassword":	
		response.set_secure_cookie('userCookie', email)
		
		response.redirect('/home')
	else: 
		response.write("invalid user")
def signup(response):
		response.write('signup here')

def post(response,post_id):
		response.write('Look at this neato post - ' + post_id)


		
def demo(response):
		with open('templates/demo.html') as demoHTML:
			response.write(demoHTML.read())

@loginRequired
def submit(response):
		response.write('submit a post here jks you cant do that yet')
@loginRequired	
def logout(response):
		response.clear_cookie("userCookie")
		response.write("Logged out")

server = Server()


server.register(r'/?(?:home)?', home)
server.register(r'/profile(?:/([\w\.\-]+))?', profile)
server.register(r'/login', login, post=login_handler)
server.register(r'/signup',signup)
server.register(r'/post/([\w\.\-]+)',post)
server.register(r'/submit',submit)
server.register(r'/demo',demo)
server.register(r'/logout',logout)


server.run()
