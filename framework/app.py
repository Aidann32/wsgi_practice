from api import API

app = API()

@app.route('/home')
def home(request, response):
    response.text = "Home page"

@app.route('/about')
def about(request, response):
    response.text = "About page"

@app.route('/greeting/{person_name}')
def greeting(request, response, person_name):
    response.text = f"Greetings, {person_name}"