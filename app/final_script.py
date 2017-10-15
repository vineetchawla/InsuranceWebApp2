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

    appid = "206301f3"
    fxmlUrl = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/%s/%s/arr/%s/%s/%s/" % \
              (airline, id, year, month, day)
    appKey = "ac59166440b0780b5e6cbefd1f531c74"



    payload = {'appID':appid, 'appKey':appKey, 'utc':'true'}
    response = requests.get(fxmlUrl, headers=payload)
    flight_json = response.json()
    print flight_json
    #flight_delay = flight_json["flightTrack"]["delayMinutes"]
    flight_delay = 10

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

    msg = "Your flight %s  on % has landed and it was delayed for %s minutes. " \
          "You will receive %s Euros in your hypothetical account as the payout " \
          % (flight_id, flight_date, delay, payout)

    subject = "Hello %s" % first_name

    message = 'Subject: {}\n\n{}'.format(subject, msg)

    # Credentials (if needed)
    username = 'vineetchawla19@gmail.com'
    password = 'new_era2007'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    # server.sendmail(user_email, username, message)
    server.quit()

    exit(0)

db.close()
#mysql://dt_admin:dt2016@localhost/appdb



