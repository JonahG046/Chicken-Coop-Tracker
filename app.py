from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'donttellanybodythiskeyatall' # Super Secret Key Tell NOBODY

# MySQL connection placeholder (replace with credentials later)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/chickendb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---

# --- User Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# --- Egg Log Model ---
class EggLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=False)

# --- Feed Log Model ---
class FeedLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

# --- Water Log Model ---
class WaterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feed')
def feed_page():
    return render_template('feed.html')

@app.route('/settings')
def settings():
    if 'user_id' in session:
            user = User.query.get(session['user_id'])
            return render_template('settings.html', user=user)
    return redirect(url_for('login'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_pw = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('settings'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


# --- Egg Log API ---
@app.route('/api/eggs', methods=['POST'])
def add_egg_log():
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
    logs = EggLog.query.all()
    return jsonify([{'id': log.id, 'date': log.date.strftime('%Y-%m-%d'), 'count': log.count} for log in logs])

# --- Feed Log API ---
@app.route('/api/feed', methods=['POST'])
def add_feed_log():
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
    logs = FeedLog.query.all()
    return jsonify([{'id': log.id, 'date': log.date.strftime('%Y-%m-%d'), 'amount': log.amount} for log in logs])

# --- Water Log API ---
@app.route('/api/water', methods=['POST'])
def add_water_log():
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
    logs = WaterLog.query.all()
    return jsonify([{'id': log.id, 'date': log.date.strftime('%Y-%m-%d'), 'amount': log.amount} for log in logs])

if __name__ == '__main__':
    app.run(debug=True)