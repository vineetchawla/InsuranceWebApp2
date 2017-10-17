from datetime import date, time, datetime
from dateutil import parser
import requests, subprocess

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

def call_service(location, time):
    baseURL = "https://api.darksky.net/forecast/50703cec8c0b8f26a09008c3b65b130b/%(location)s,%(time)s" \
              % {'location': location, 'time': time}
    #baseURL = unicode(baseURL, errors='replace')
    payload = {'exclude' : 'hourly,daily,flags', 'units' : 'si'}

    r = requests.get(baseURL, params = payload)
    data = r.json()
    return data['currently']


def random_forest(flight_id, date, airline, aircraft, airport_code,
                          arrival_time, flight_duration):

    date_time = date + " " + arrival_time
    dt = parser.parse(date_time)
    epoch = datetime(1970, 1, 1)

    # needed for Darksky weather API, seconds from 1970
    delta_time = (dt - epoch).total_seconds()

    # time is divided in 12 blocks of hours, we assign hour as the nearest lower even number
    time_block = dt.hour
    if (time_block % 2) != 0:
        time_block = time_block - 1

    weekend = 0
    if dt.weekday() > 4:
        weekend = 1

    #get weather
    weather = call_service(airport_location[airport_code], int(delta_time))

    # params = {
    #     'arrival_airport' : airport_dict[airport_code],
    #     'airline' : airline,
    #     'aircraft' : aircraft,
    #     'flight_time' : flight_duration,
    #     'weekend' : weekend,
    #     'time_block': time_block,
    #     'apparentTemperature': weather["apparentTemperature"],
    #     'dewPoint' : weather["dewPoint"],
    #     'humidity': weather["humidity"],
    #     'windSpeed': weather["windSpeed"],
    #     'windBearing': weather["windBearing"],
    #     'visibility': weather["visibility"],
    #     'cloudCover': weather["cloudCover"],
    #     'pressure': weather["pressure"]
    # }

    #cant pass list to shell as an argument. so made all strings and then concatenated to one string
    #String passed to r . it can be separated later in R
    params = [
             '%s' % str(airport_dict[airport_code]),
        '%s' % str(airline),
        '%s' % str(aircraft),
        '%s' % str(flight_duration),
        '%s' % str(weekend),
        '%s' % str(time_block),
        '%s' % str(weather["apparentTemperature"]),
        '%s' % str(weather["dewPoint"]),
        '%s' % str(weather["humidity"]),
        '%s' % str(weather["windSpeed"]),
        '%s' % str(weather["windBearing"]),
        '%s' % str(weather["visibility"]),
        '%s' % str(weather["cloudCover"]),
        '%s' % str(weather["pressure"]),
        '%s' % str(weather["summary"])
    ]
    new_param = ":".join(params)

    command = 'Rscript'
    arg = '--vanilla'
    path = "/Users/vineetchawla/PycharmProjects/InsuranceWebApp2/app/predictor_script.R"

    #cmd = [command + " " +path] + abc
    x = subprocess.check_output([command, arg, path, new_param], universal_newlines=True)

    print x

    flight_rates = {'no_delay' : 0, 'upto_15_mins' : 30, 'upto_1_hour':60 ,
                    'more_than_1_hour' : 90}

    return flight_rates

def set_blockchain(user_data):
    anchor = {}
    return anchor
