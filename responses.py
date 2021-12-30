#  ------------------ Libraries ------------------------------
from datetime import datetime as dt
import datetime
import db_connection_details as dbd

#  ------------------ Variables ------------------------------
f = "%d/%m/%Y %H:%M:%S"                     # date format
time_out = datetime.timedelta(minutes=1)    # time duration, set to 1 minute

#  ------------------ Functions ------------------------------
# Check if current time - last activity time exceeds time out
# last activity is the last message / command (excluding log in and log out)
# For example, you said hellow (unrecognized message) it will still treat that as an activity

def check_for_time_out(phone_number):
    global time_out
    global current_time
    _last_act = dbd.get_last_activity(phone_number)
    last_act = dt.strptime(_last_act.strftime(f),f)
    _current_time = datetime.datetime.now()
    current_time = dt.strptime(_current_time.strftime(f), f)
    if current_time - last_act < time_out:
        print(current_time)
        print(last_act)
        print(str(current_time - last_act))
        return True
    else:
        return False

# List of sample responses such as hi. hello and sup -- only for testing purposes
def sample_responses(input_text):
    user_message = str(input_text).lower()
    if user_message in ("hello","hi","sup"):
        return "Hey! How it's going?"

    if user_message in ("who are you?", "who are you"):
        return "I am Alpha Bot"

    if user_message in ("time", "time?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        return str(date_time)

    return "I don't understand you!"