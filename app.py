from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'donttellanybodythiskeyatall'  # Secret key for session management and flash messages

# MySQL connection placeholder (replace with real credentials later)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/chickendb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking to save resources

db = SQLAlchemy(app)  # Initialize SQLAlchemy ORM

# --- Models ---

# User model to store account info
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password

# Egg log model to track egg counts
class EggLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=False)

# Feed log model to track feed amounts
class FeedLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Water log model to track water amounts
class WaterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

# --- Routes ---

@app.route('/')
def home():
    # Render the main home page
    return render_template('index.html')

@app.route('/feed')
def feed():
    # Render the feed tracking page
    return render_template('feed.html')

@app.route('/water')
def water():
    # Render the water tracking page
    return render_template('water.html')

@app.route('/eggs')
def eggs():
    # Render the egg tracking page
    return render_template('eggs.html')

@app.route('/settings')
def settings():
    # Render the user settings page if logged in
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('settings.html', user=user)
    # Redirect to login if user is not authenticated
    return redirect(url_for('login'))

@app.route('/test-flash')
def test_flash():
    # Route to test flash messages
    flash('This is a test success message!', 'success')
    flash('This is a test error message!', 'error')
    return render_template('flash_test.html')
    
# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle registration form submission
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password for security
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pw)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    # Render registration form if GET request
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query database for user
        user = User.query.filter_by(username=username).first()
        # Check password hash
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('settings'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    # Render login form if GET request
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear user session and logout
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

# --- Egg Log API ---

@app.route('/api/eggs', methods=['POST'])
def add_egg_log():
    # API route to add a new egg log
    data = request.get_json()
    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        count = int(data['count'])
        new_log = EggLog(date=date, count=count)
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Egg log added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/eggs', methods=['GET'])
def get_egg_logs():
    # API route to retrieve all egg logs
    logs = EggLog.query.all()
    return jsonify([{'id': log.id, 'date': log.date.strftime('%Y-%m-%d'), 'count': log.count} for log in logs])

# --- Feed Log API ---

@app.route('/api/feed', methods=['POST'])
def add_feed_log():
    # API route to add a new feed log
    data = request.get_json()
    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        amount = float(data['amount'])
        new_log = FeedLog(date=date, amount=amount)
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Feed log added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/feed', methods=['GET'])
def get_feed_logs():
    # API route to retrieve all feed logs
    logs = FeedLog.query.all()
    return jsonify([{'id': log.id, 'date': log.date.strftime('%Y-%m-%d'), 'amount': log.amount} for log in logs])

# --- Water Log API ---

@app.route('/api/water', methods=['POST'])
def add_water_log():
    # API route to add a new water log
    data = request.get_json()
    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        amount = float(data['amount'])
        new_log = WaterLog(date=date, amount=amount)
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Water log added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/water', methods=['GET'])
def get_water_logs():
    # API route to retrieve all water logs
    logs = WaterLog.query.all()
    return jsonify([{'id': log.id, 'date': log.date.strftime('%Y-%m-%d'), 'amount': log.amount} for log in logs])

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
