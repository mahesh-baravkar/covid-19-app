from requests.api import request
from config import app  
from models import Country, State, District 
from flask import render_template, request


@app.route("/home", methods= ['GET', 'POST'])
def home():
    districtsValueOption = {'AN': 'Andaman and Nicobar Islands', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CH': 'Chandigarh', 'CT': 'Chhattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli and Daman and Diu', 'GA': 'Goa', 'GJ': 'Gujarat', 'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala', 'LA': 'Ladakh', 'LD': 'Lakshadweep', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Odisha', 'PB': 'Punjab', 'PY': 'Puducherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal'}
    if request.method == "POST":
        if request.form.get('dropdown') != "All":
            stateFD = State.query.filter_by(state_name=request.form.get('dropdown')).order_by(State.id.desc()).first()
            district = District.query.filter_by(state_id=stateFD.id).order_by(District.id.desc())
            return render_template("index.html", cardd=stateFD, district=district, selected=request.form.get('dropdown'), dropdownval=districtsValueOption.values()) 
    
    country = Country.query.order_by(Country.id.desc()).first()
    state = State.query.order_by(State.id.desc()).limit(36)
    return render_template("index.html", cardd= country, statedata=state, dropdownval=districtsValueOption.values()) 