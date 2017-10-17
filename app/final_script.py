import MySQLdb
import requests
from dateutil import parser
import re, smtplib

def check_status(flight_id, flight_date):

    dt = parser.parse(flight_date)
    year = dt.year
    day = dt.day
    month = dt.month

    #sepearting text and number
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(flight_id)
    airline = m.group(1)
    id = m.group(2)

    appid = "f69749da"
    fxmlUrl = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/%s/%s/arr/%s/%s/%s/" % \
              (airline, id, year, month, day)
    appKey = "a3c8532df635acc481ef1929f99a0a6d"

    payload = {'appID':appid, 'appKey':appKey, 'utc':'true'}
    response = requests.get(fxmlUrl, headers=payload)
    flight_json = response.json()
    flight_delay = flight_json["flightStatuses"][0]["delays"]["arrivalGateDelayMinutes"]

    return flight_delay

db = MySQLdb.connect(user='dt_admin', passwd='dt2016',
                              host='127.0.0.1',
                              db='appdb')

cursor = db.cursor()

cursor.execute("SELECT * from users")

# Fetch a single row using fetchone() method.
data = cursor.fetchall()

for row in data:
    email = row[1]
    first_name = row[2]
    flight_id = row[7]
    flight_date = row[11]
    rates_15 = row[13]
    rates_60 = row[14]
    rates_120 = row[15]

    delay = check_status(flight_id, flight_date)
    payout = 0

    if delay > 120:
        payout = rates_120
    elif delay > 60:
        payout = rates_60
    elif delay > 15:
        payout = rates_15

    msg = "Your flight %s  on %s has landed and it was delayed for %s minutes. " \
          "You will receive %s Euros in your hypothetical account as the payout " \
          % (flight_id, flight_date, delay, payout)

    subject = "Hello %s" % first_name

    message = 'Subject: {}\n\n{}'.format(subject, msg)

    # Credentials (if needed)
    username = 'vineetchawla19@gmail.com'
    password = 'new_era2007'

    # The actual mail sending
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(email, username, message)
    server.quit()

    exit(0)

db.close()


