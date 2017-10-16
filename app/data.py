from datetime import date, time, datetime
from dateutil import parser

airport_dict = {
    'MUN': 'Munich (MUC)',
    'SXF': 'Berlin (SXF)',
    'TXL': 'Berlin (TXL)',
    'BRE': 'Bremen (BRE)',
    'CGN': 'Cologne (CGN)',
    'DTM': 'Dortmund (DTM)',
    'DRS': 'Dresden (DRS)',
    'DUS': 'Dusseldorf (DUS)',
    'ERF': 'Erfurt (ERF)',
    'FRA': 'Frankfurt (FRA)',
    'FDH': 'Friedrichshafen (FDH)',
    'HHN': 'Hahn (HHN)',
    'HAM': 'Hamburg (HAM)',
    'HAJ': 'Hannover (HAJ)',
    'FKB': 'Karlsruhe/Baden-Baden (FKB)',
    'KSF': 'Kassel (KSF)',
    'LEJ': 'Leipzig (LEJ)',
    'FMM': 'Memmingen (FMM)',
    'FMO': 'Munster (FMO)',
    'NUE': 'Nurnberg (NUE)',
    'PAD': 'Paderborn (PAD)',
    'SCN': 'Saarbrucken (SCN)',
    'STR': 'Stuttgart (STR)',
    'NRN': 'Weeze (NRN)'
}

airport_location = {
    'MUN': '48.354,11.786',
    'SXF': '52.380,13.523',
    'TXL': '52.38,13.523',
    'BRE': '53.047,8.787',
    'CGN': '50.866,7.143',
    'DTM': '51.518,7.612',
    'DRS': '51.133,13.767',
    'DUS': '51.289,6.767',
    'ERF': '50.980,10.958',
    'FRA': '50.026,8.543',
    'FDH': '47.671,9.511',
    'HHN': '49.950,7.264',
    'HAM': '53.63,9.988',
    'HAJ': '52.461,9.685',
    'FKB': '48.801,8.087',
    'KSF': '51.408,9.378',
    'LEJ': '51.424,12.236',
    'FMM': '47.989,10.239',
    'FMO': '52.134,7.685',
    'NUE': '49.499,11.078',
    'PAD': '51.614,8.616',
    'SCN': '49.214,7.109',
    'STR': '48.69,9.222',
    'NRN': '51.599,6.148'
}

def call_service(latitude, longitude, time):
    baseURL = "https://api.darksky.net/forecast/50703cec8c0b8f26a09008c3b65b130b/%(latitude)s,%(longitude)s,%(time)s" \
              % {'latitude': latitude, 'longitude': longitude, 'time': time}
    baseURL = unicode(baseURL, errors='replace')
    payload = {'exclude' : 'hourly,daily,flags', 'units' : 'si'}
    try:
        r = requests.get(baseURL, params = payload)
        data = r.json()
        print data['currently']
        return data['currently']
    except:# This is the correct syntax
        print 'some error'
        return 'blank'

def random_forest(flight_id, date, airline, aircraft, airport_code,
                          arrival_time, flight_duration):

    time2 = arrival_time
    datetime = date + " " + time2
    dt = parser.parse(datetime)
    epoch = datetime(1970, 1, 1)
    delta_time = (dt - epoch).total_seconds()



    flight_rates = {'no_delay' : 0, 'upto_15_mins' : 30, 'upto_1_hour':60 ,
                    'more_than_1_hour' : 90}
    #will add algorithm later
    return flight_rates

def set_blockchain(user_data):
    anchor = {}
    return anchor
