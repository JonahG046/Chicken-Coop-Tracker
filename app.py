from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# MySQL connection placeholder (replace with credentials later)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/chickendb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class EggLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=False)

class FeedLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

class WaterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

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