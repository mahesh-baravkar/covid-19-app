from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

scheduler1 = BackgroundScheduler(daemon=True)
scheduler2 = BackgroundScheduler(daemon=True)


import routes
from apidata import  CountrynStateData, DistrictsData

scheduler1.add_job(func= CountrynStateData, trigger="interval", minutes=10)
scheduler2.add_job(func= DistrictsData, trigger="interval", minutes=13)
scheduler1.start()
scheduler2.start()
atexit.register(lambda: scheduler1.shutdown())
atexit.register(lambda: scheduler2.shutdown())
