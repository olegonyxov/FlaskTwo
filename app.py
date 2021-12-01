from flask import Flask, render_template, request, make_response
a=0
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def get_count_of_user_visits_by_cookie():  # т.к. не сбрасываются по дефолту
    visited = 0
    usern = request.cookies.get('username')
    if request.cookies.get('visited'):
        try:
            visited = int(request.cookies['visited'])
        except ValueError:
            return make_response(render_template('index.html', visited='Incorrect'))

    response = make_response(render_template('index.html', visited=visited, usern=usern))
    response.set_cookie('visited', str(visited + 1))
    return response


@app.route("/login", methods=['POST', 'GET'])
def login_form():
    usern = request.cookies.get('username')
    if usern:
        response = make_response(render_template('helloUser.html', username=usern))
        return response
    else:
        if request.method == 'GET':
            return """
                     <form action='http://localhost:5000/login', method='POST'>
                         <input name="username">
                         <input type="submit">
                     </form>
                    """
        elif request.method == 'POST':
            username = request.form['username']
            response = make_response(render_template('helloUser.html', username=username))
            response.set_cookie("username", username)
            return response


@app.route("/logout", methods=['GET'])
def delete_cookie():
    response = make_response("Logging out")
    response.delete_cookie("username")
    return response
