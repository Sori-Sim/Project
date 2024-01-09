from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, make_response
import requests, subprocess
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

url = "https://felixtien.github.io/Data/webproject.json"

response = requests.get(url)
jsondata = response.json()

class MyForm(FlaskForm):
    codeArea = TextAreaField("CodeArea")
    runButton = SubmitField("Run")

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'jaychinandfelixtien'

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

# Add the new routes for login, signup, and secret-page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for('index'))
        
        else:
            flash('Invalid user information. Try again :)', 'error')
            # Redirect back to login page with error message
            return render_template('login.html')

    # Check if "Remember Me" cookies exist and pre-fill the login form
    remembered_email = request.cookies.get('remembered_email')
    remembered_password_hash = request.cookies.get('remembered_password')
    return render_template('login.html', remembered_email=remembered_email, remembered_password_hash=remembered_password_hash)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login'))

        # Create a new user and add it to the database
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/member')
def member():
    return render_template('member.html')

@app.route('/question')
def question():
    return render_template('question.html', jsondata = jsondata)

@app.route('/likecode', methods=['GET', 'POST'])
def likecode():
    form = MyForm()
    if request.method == 'POST' and not form.validate_on_submit():
        data = request.get_json()  # Extract the JSON payload from the request
        id = data['id']  # Get the 'id' from the JSON payload

        return jsonify({"message": "Data received successfully"})  # Send a JSON response

    id = int(request.args.get('id')) # Get the 'id' query parameter from the URL

    if form.validate_on_submit():
        inputCode = form.codeArea.data
        lang = request.form.get("language")
        if lang == "python":
            with open('temp.py', 'w') as file:
                file.write(inputCode)
            result = ""
            try:
                # Execute the code and capture the output
                result = subprocess.check_output(['python', 'temp.py'], stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                result = e.output
            
            if jsondata[id-1]['output'] == 'false':
                answer = result[:-1] == 'False' or result == 'False'
                expected = 'False'
            elif jsondata[id-1]['output'] == 'true':
                answer = result[:-1] == 'True' or result == 'True'
                expected = 'True'
            else:
                answer = result[:-1] == jsondata[id-1]['output']
                expected = jsondata[id-1]['output']
            user = result
            if len(result) != 0:
                user = result[:-1] if result[-1] == '\n' else result
            return render_template('answer.html', user=user, expected=expected, answer=answer)
        elif lang == "java":
            with open('Main.java', 'w') as file:
                file.write(inputCode)
            result = ""
            try:
                subprocess.run(['javac', 'Main.java'], check=True, stderr=subprocess.PIPE)
                result = subprocess.run(['java', 'Main'], capture_output=True, text=True)

                if result.returncode != 0:
                    result = result.stderr
                else:
                    result = result.stdout
            except subprocess.CalledProcessError as e:
                result = e.stderr

            answer = result[:-1] == jsondata[id-1]['output']
            expected = jsondata[id-1]['output']
            user = result
            if len(result) != 0:
                user = result[:-1] if result[-1] == '\n' else result
            return render_template('answer.html', user=user, expected=expected, answer=answer)
        elif lang == "c":
            with open('code.c', 'w') as file:
                file.write(inputCode)
            result = ""
            try:
                # Compile the C code
                subprocess.run(['gcc', 'code.c', '-o', 'executable'], check=True, stderr=subprocess.PIPE)
                
                # Execute the compiled executable and capture the output
                result = subprocess.run(['./executable'], capture_output=True, text=True)
                
                # Check if there was any error during execution
                if result.returncode != 0:
                    result = result.stderr
                else:
                    result = result.stdout
            except subprocess.CalledProcessError as e:
                result = e.stderr
            
            if jsondata[id-1]['output'] == 'false':
                answer = result[:-1] == '0' or result == '0'
                expected = '0'
            elif jsondata[id-1]['output'] == 'true':
                answer = result[:-1] == '1' or result == '1'
                expected = '1'
            else:
                answer = result[:-1] == jsondata[id-1]['output'] or result == jsondata[id-1]['output']
                expected = jsondata[id-1]['output']
            user = result
            if len(result) != 0:
                user = result[:-1] if result[-1] == '\n' else result
            return render_template('answer.html', user=user, expected=expected, answer=answer)
        elif lang == "c++":
            result = ""
            with open('code.cpp', 'w') as file:
                file.write(inputCode)
    
            try:
                # Compile the C++ code
                subprocess.run(['g++', 'code.cpp', '-o', 'executable'], check=True, stderr=subprocess.PIPE)
                
                # Execute the compiled executable and capture the output
                result = subprocess.run(['./executable'], capture_output=True, text=True)
                
                # Check if there was any error during execution
                if result.returncode != 0:
                    result = result.stderr
                else:
                    result = result.stdout
            except subprocess.CalledProcessError as e:
                output = e.stderr

            if jsondata[id-1]['output'] == 'false':
                answer = result[:-1] == '0' or result == '0'
                expected = '0'
            elif jsondata[id-1]['output'] == 'true':
                answer = result[:-1] == '1' or result == '1'
                expected = '1'
            else:
                answer = result[:-1] == jsondata[id-1]['output'] or result == jsondata[id-1]['output']
                expected = jsondata[id-1]['output']
            user = result
            if len(result) != 0:
                user = result[:-1] if result[-1] == '\n' else result
            return render_template('answer.html', user=user, expected=expected, answer=answer)

    return render_template('likecode.html', id = id-1,form=form, jsondata = jsondata)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()     # Create the database tables before running the app
    app.run(debug=True)
