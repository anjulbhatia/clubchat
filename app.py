import re

from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO

users = [
    {'name': "Anjul Bhatia", 'username': "anjulbhatia", 'password': "1234"},
    {'name': "Siddhi Queen 👑", 'username': "sidx69", 'password': "12345"}
]

Current_User = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = '[123_xxx_456]'
socketio = SocketIO(app)


@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/signup')
def signup():
    return render_template('index.html', code=100)

@app.route('/login')
def login():
    return render_template('index.html', code=200)


@app.route('/signup/q', methods=['GET', 'POST'])
def getuser():
    global Current_User
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
 
        # Validate username
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', username):
            return render_template('index.html', users=Current_User, code=600, errmsg="Invalid username. It must start with a letter or an underscore.")


        # Save user data (you should store this in a database)
        Current_User = {'name': name, 'username': username, 'password': password}
        users.append(Current_User)
        
        return render_template('dashboard.html', user=Current_User, code=600)


@app.route('/login/q', methods=['GET', 'POST'])
def loginq():
    global Current_User
    if request.method == 'POST':
        phone_email_username = request.form['phone_email_username']
        password = request.form['password']

        # Validate username
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_.@]*$', phone_email_username):
            return render_template('index.html', users=Current_User, code=500, errmsg="Invalid username. It must start with a letter or an underscore.")


        # Check if the user exists (you should query your database)
        for user in users:
            if (user['phone_email'] == phone_email_username or
                user['username'] == phone_email_username) and user['password'] == password:
                Current_User = user
                return render_template('dashboard.html', user=Current_User, code=400)

        return render_template('index.html', user=Current_User, code=500, errmsg="Invalid login credentials. Please try again.")


@socketio.on('message')
def handle_message(data):
    message = data['message']
    username = data['username']
    socketio.emit('message', {'message': message, 'username': username})


@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html", users=users)




@app.route('/calculator')
def calculator(): 
    return render_template('calculator.html')

if __name__ == "__main__":
    #app.run(host="192.168.29.59", port="5000",debug=True)
    socketio.run(app, host="192.168.29.59", port="5000", debug=True)
