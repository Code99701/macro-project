from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batting_team = db.Column(db.String(100), nullable=False)
    bowling_team = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    target = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    overs = db.Column(db.Float, nullable=False)
    wickets = db.Column(db.Integer, nullable=False)
    win_probability = db.Column(db.Float, nullable=False)
    loss_probability = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'batting_team': self.batting_team,
            'bowling_team': self.bowling_team,
            'city': self.city,
            'target': self.target,
            'score': self.score,
            'overs': self.overs,
            'wickets': self.wickets,
            'win_probability': self.win_probability,
            'loss_probability': self.loss_probability,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
