""""
Project File: db_connection_details
"""

from mysql_connection_db import mysql_connection_db as db_con

## Database Configuration
db_config =  {
            'host':"127.0.0.1",                 # database host
            'port': 3306,                       # port
            'user':"test",                      # username
            'passwd':"newpassword",             # password
            'db':"is238_account_storage",       # database
            'charset':'utf8'                    # charset encoding
            }


#  ------------------ Defining DB Connection Details ------------------------------
# Establish Connection
dbcon = db_con(db_config)

# Define Curosr
dbcursor = dbcon.cursor

#  ------------------ DB Connection Functions ------------------------------
#Phone Login
def do_db_log_in(phone_num):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_status_log_in(%s)"
            data_tuple = (str(phone_num),)
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ' successfully logged in')
        except:
            print('Error in Updating Log In for ' + phone_num)
    else:
        print("Unable to log in to database!")

#Phone Log out
def do_db_log_out(phone_num):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_status_log_out(%s)"
            data_tuple = (str(phone_num),)
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ' successfully logged out')
        except:
            print('Error in Updating Log Out for ' + phone_num)
    else:
        print("Unable to log in to database!")

#Phone Update OTP
def do_update_otp(phone_num, otp):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_otp(%s,%s)"
            data_tuple = (str(phone_num), int(otp))
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print('OTP ' + otp + ' for ' + phone_num + ' successfully updated')
        except:
            print('Error in Updating OTP for ' + phone_num)
    else:
        print("Unable to log in to database!")

#Check Connection Status
def do_check_status(phone_num):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.check_status(%s)"
        data_tuple = (str(phone_num),)
        dbcursor.execute(sql_procedure_query, data_tuple)
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")

# Convert Phone from
def convert_to_ph_mobile(phone_num):
    ph_mob = '0' + phone_num[3:]
    return ph_mob

def check_otp_phone_num_in_db(phone_num,otp):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.check_if_record_exists(%s,%s) as query_check"
        data_tuple = (str(phone_num),int(otp))
        dbcursor.execute(sql_procedure_query, data_tuple)
        #record = dbcursor.fetchall()
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")

def get_last_activity(phone_num):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.get_last_activity(%s) as activity_check"
        data_tuple = (str(phone_num),)
        dbcursor.execute(sql_procedure_query, data_tuple)
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")

def update_last_activity(phone_num):
    if (dbcon):
        try:
            sql_procedure_query = "CALL s238_account_storage.update_activity((%s)"
            data_tuple = (str(phone_num),)
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ' activity updated')
        except:
            print('Error in Updating Last Acitivty for ' + phone_num)
    else:
        print("Unable to log in to database!")