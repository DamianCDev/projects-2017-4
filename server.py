from tornado.ncss import Server 
from re_template_renderer import render_template

def home(response):
		html = render_template('main.html', {})
		response.write(html)

def profile(response,name):
        response.write('Hi, ' + str(name))
		
def login(response): 
	with open ('templates/login.html') as loginHTML: 
		response.write(loginHTML.read())
		
def signup(response):
		response.write('signup here')

def post(response,post_id):
		response.write('Look at this neato post - ' + post_id)

def submit(response):
		response.write('submit a post here jks you cant do that yet')
		
def demo(response):
		with open('templates/demo.html') as demoHTML:
			response.write(demoHTML.read())
		
server = Server()


server.register(r'/?(?:home)?', home)
server.register(r'/profile/([\w\.\-]+)', profile)
server.register(r'/login', login)#, post#fix this)
server.register(r'/signup',signup)
server.register(r'/post/([\w\.\-]+)',post)
server.register(r'/submit',submit)
server.register(r'/demo',demo)



server.run()
