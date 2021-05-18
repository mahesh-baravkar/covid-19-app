from config import db 
from datetime import datetime

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)
    country_name = db.Column(db.String(500), nullable=False)
    total_cases = db.Column(db.Integer)
    active_cases = db.Column(db.Integer)
    recovered_cases = db.Column(db.Integer)
    deceased_cases = db.Column(db.Integer)
    vaccinated_cases = db.Column(db.Integer)
    state = db.relationship('State', backref='states', lazy=True)

    def __repr__(self):
        return f"Country('{self.id}', '{self.country_name}')"

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)
    state_name = db.Column(db.String(500), nullable=False)
    total_cases = db.Column(db.Integer)
    active_cases = db.Column(db.Integer)
    recovered_cases = db.Column(db.Integer)
    deceased_cases = db.Column(db.Integer)
    vaccinated_cases = db.Column(db.Integer)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    district = db.relationship('District', backref='districts', lazy=True)


    def __repr__(self):
        return f"Country('{self.id}', '{self.state_name}')"


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)
    district_name = db.Column(db.String(500), nullable=False)
    active_cases = db.Column(db.Integer)
    confirmd_cases = db.Column(db.Integer)
    recovered_cases = db.Column(db.Integer)
    deceased_cases = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)


    def __repr__(self):
        return f"District('{self.id}', '{self.district_name}')"
