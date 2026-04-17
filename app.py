from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import re
from functools import wraps

from database import init_db, create_user, get_user_by_username, create_note, get_notes_by_user

app = Flask(__name__)

# SECURITY FEATURE 4 — Session Management:
# HTTPONLY stops JavaScript from reading the cookie.
# SAMESITE prevents cross-site request forgery.
app.secret_key = 'supersecretkey123!@#changethis'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

bcrypt = Bcrypt(app)
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # SECURITY FEATURE 5 — Input Validation:
        # All fields are checked server-side before any 
        # database operation happens.
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not (3 <= len(username) <= 20):
            return render_template('register.html', error="Username must be 3 to 20 characters.")
            
        if not re.match('^[a-zA-Z0-9]+$', username):
            return render_template('register.html', error="Username can only contain letters and numbers.")
            
        if len(password) < 8:
            return render_template('register.html', error="Password must be at least 8 characters.")
            
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")
            
        existing_user = get_user_by_username(username)
        if existing_user:
            return render_template('register.html', error="That username is already taken.")
            
        # SECURITY FEATURE 1 — Password Hashing:
        # We never store the real password, only the hash.
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        
        create_user(username, hashed)
        flash("Account created! Please login.", "success")
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = get_user_by_username(username)
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/notes')
            
        # SECURITY: Generic error message prevents 
        # attackers from knowing if a username exists.
        return render_template('login.html', error="Invalid username or password.")
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    # SECURITY FEATURE 4 — Session Management:
    # session.clear() destroys the session completely 
    # so the user cannot go back using the browser 
    # back button and see protected content.
    return redirect('/login')

import bleach

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    user_id = session['user_id']
    username = session['username']
    
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        
        if not content:
            notes_list = get_notes_by_user(user_id)
            return render_template('notes.html', notes=notes_list, username=username, error="Note cannot be empty.")
            
        if len(content) > 500:
            notes_list = get_notes_by_user(user_id)
            return render_template('notes.html', notes=notes_list, username=username, error="Note must be under 500 characters.")
            
        # SECURITY FEATURE 3 — XSS Prevention:
        # XSS means Cross-Site Scripting. It is when an 
        # attacker types <script>alert('hacked')</script> 
        # into a form, hoping it runs in other users browsers.
        # bleach.clean() with tags=[] strips ALL HTML tags 
        # from the input before saving to database.
        # Jinja2 also auto-escapes {{ }} in templates,
        # which is a second layer of XSS protection.
        content = bleach.clean(content, tags=[], strip=True)
        
        create_note(user_id, content)
        return redirect('/notes')
        
    notes_list = get_notes_by_user(user_id)
    return render_template('notes.html', notes=notes_list, username=username)
