import requests 
import pandas as pd
# import threading


from requests.sessions import session


from config import db
from models import Country, State, District 
import time

districtsValueOption = {'AN': 'Andaman and Nicobar Islands', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CH': 'Chandigarh', 'CT': 'Chhattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli and Daman and Diu', 'GA': 'Goa', 'GJ': 'Gujarat', 'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala', 'LA': 'Ladakh', 'LD': 'Lakshadweep', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Odisha', 'PB': 'Punjab', 'PY': 'Puducherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal'}


def CountrynStateData():
    print('Loaded CountryState')
    start_time = time.time()
    datavaccin = pd.DataFrame(requests.get("https://api.covid19india.org/v4/min/data.min.json").json()).loc[['total'],::].transpose()['total']
    url = "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
    vaccinated = {districtsValueOption[i]:j['vaccinated'] for i,j in datavaccin.items() if i in districtsValueOption.keys()}
    state_data = pd.DataFrame(requests.get(url).json()['regionData']).loc[::,['region','activeCases','deceased','totalInfected','recovered']] 

    state_data['vaccinated'] = vaccinated.values()
    country_data = state_data.sum()
    
    if not country_data.empty:
        c_table = Country(country_name="India", total_cases=int(country_data['totalInfected']), active_cases=int(country_data['activeCases']), recovered_cases= int(country_data['recovered']), deceased_cases=int(country_data['deceased']), vaccinated_cases=int(country_data['vaccinated']))
        db.session.add(c_table)
        db.session.commit()
        
    
    try:
        if not state_data.empty:
            country_md = Country.query.order_by(Country.id.desc()).first()
            # print(country_md)
            for state_d in range(len(state_data.transpose().columns)):
                s_table = State(state_name=state_data['region'][state_d], total_cases=int(state_data['totalInfected'][state_d]), active_cases=int(state_data['activeCases'][state_d]), recovered_cases=int(state_data['recovered'][state_d]), deceased_cases=int(state_data['deceased'][state_d]), vaccinated_cases=int(state_data['vaccinated'][state_d]))
                s_table.states = country_md
                db.session.add(s_table)
                db.session.commit()
                # print(state_data['region'][state_d],state_data['totalInfected'][state_d],state_data['activeCases'][state_d],state_data['recovered'][state_d],state_data['deceased'][state_d],state_data['vaccinated'][state_d])
            
    except:
        raise Exception("Data Not Found")
    print(time.time()-start_time)


def DistrictsData():
    print("Loaded District")
    start_time = time.time()
    datadistrict = pd.DataFrame(requests.get("https://api.covid19india.org/state_district_wise.json").json())

    try:
        if not datadistrict.empty:
            for state in districtsValueOption.values():
                state_md = State.query.filter_by(state_name = state).order_by(State.id.desc()).first()
                for dis in datadistrict[state]['districtData'].keys():
                    district_table = District(district_name=dis,active_cases=int(datadistrict[state]['districtData'][dis]['active']),confirmd_cases=int(datadistrict[state]['districtData'][dis]['confirmed']),deceased_cases=int(datadistrict[state]['districtData'][dis]['deceased']), recovered_cases=int(datadistrict[state]['districtData'][dis]['recovered']))
                    district_table.districts = state_md
                    db.session.add(district_table)
                    db.session.commit()
    except:
        raise Exception("Data not Found.")
    print(time.time()-start_time)
        
        

# threadCS = threading.Thread(target=CountrynStateData)
# threasD = threading.Thread(target=DistrictsData)
# threadCS.start()
# threasD.start()
# threadCS.join()
# threasD.join()

# StoreData()