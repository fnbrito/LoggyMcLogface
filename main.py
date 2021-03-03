#
# FILE              : main.py
# PROJECT			: SENG2040 - Assignment 03
# PROGRAMMER		: Filipe Brito
# FIRST VERSION     : 21/02/2020
# DESCRIPTION		:
# 	This file is the main logic for the server.
# 	It instanciates a LogEntry class and writes it to file if
#  possible. It also decides what's best to do according to options.
#
import socket
import configparser
import helper
from helper import ErrorLevel
import threading
from threading import Lock
import time
from distutils.util import strtobool

MAX_MESSAGE = 2048


# Function:		handle
# Description:	Handling logs from clients.
# Params:		client - connection object
#               the_ip - ip of the client
# Returns:		void
def handle(client, the_ip):
    global writes
    global forced_format
    global force_complete
    global force_date
    global force_time
    global force_level

    while True:
        all_ok = True

        try:
            message = client.recv(MAX_MESSAGE)
            message = message.decode()
        except:
            # Removing And Closing Clients
            # index = clients.index(client)
            clients.remove(client)
            client.close()
            break

        if message != "":
            new_log_line = helper.EntryLog(message, the_ip)

            if forced_format:

                if force_complete:
                    if new_log_line.all_fields_present() is False:
                        all_ok = False
                if force_date and all_ok:
                    if new_log_line.is_date_set() is False:
                        all_ok = False
                if force_time and all_ok:
                    if new_log_line.is_time_set() is False:
                        all_ok = False
                if force_level and all_ok:
                    if new_log_line.is_level_set() is False:
                        all_ok = False
                if all_ok:
                    all_ok = level.value <= new_log_line.level.value

            if override_timestamp:
                to_be_sent = new_log_line.get_message_string()
                to_be_sent = timestamp(to_be_sent) + "\n"
            else:
                to_be_sent = new_log_line.get_full_string() + "\n"

            if all_ok:
                if writes < 30:
                    mutex.acquire()
                    try:
                        f = open(file, "a+")
                        f.write(to_be_sent)
                        f.close()
                    except IOError:
                        pass
                    mutex.release()
                    if abuse_protection:
                        writes += 1
                else:
                    print("Spam protection activated!")


# Function:		prevent_abuse
# Description:	This function will help prevent spam/abuse from clients.
# Params:		void
# Returns:		void
def prevent_abuse():
    global writes
    while True:
        if writes >= 10:
            writes -= 10
            time.sleep(0.5)
        else:
            time.sleep(0.5)
            continue


# Function:		prevent_abuse
# Description:	This function will add a timestamp to the original message.
# Params:		message - string to be added to a timestamp
# Returns:		time_string - string of timestamp + message
def timestamp(message):
    time_now = time.localtime()
    time_string = time.strftime("[%Y/%m/%d] [%H:%M:%S] ", time_now)
    time_string = time_string + message
    return time_string


# Function:		prevent_abuse
# Description:	Receiving / Listening Function
# Params:		void
# Returns:		void
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        clients.append(client)

        # Start Handling Thread for client
        thread = threading.Thread(target=handle, args=(client, str(address[0])))
        thread.start()


# Function:		set_config
# Description:	This function applies the configuration to the .ini file inside the same dir as this script.
# Params:		void
# Returns:		True
def set_config():
    config = configparser.RawConfigParser(allow_no_value=True)
    print("config.ini is being reinitialized")
    config['INSTRUCTIONS'] = {}
    config.set('INSTRUCTIONS', "# file: default file for storing logs\n")
    config.set('INSTRUCTIONS', "# host: IP address\n")
    config.set('INSTRUCTIONS', "# port: port\n")
    config.set('INSTRUCTIONS',
               "# level: level of logging: 0 - OFF, 1 - TRACE, 2 - DEBUG, 3 - INFO, 4 - WARN, 5 - ERROR, 6 - FATAL\n")
    config.set('INSTRUCTIONS', "# abuse_protection: this will toggle protection against spam\n")
    config.set('INSTRUCTIONS',
               "# override_timestamp: this will append a local timestamp to the log message, overwriting its original timestamp\n")
    config.set('INSTRUCTIONS', "# forced_format: this will check if the format is being followed, see above\n")
    config.set('INSTRUCTIONS',
               "# force_complete: checks if all fields are properly filled - [DATE] [TIME] [LEVEL] [MSG]\n")
    config.set('INSTRUCTIONS', "# force_date: checks if the date is set (\"YYYY/MM/DD\" format)\n")
    config.set('INSTRUCTIONS', "# force_time: checks if the time is set (\"HH:MM:SS\" format)\n")
    config.set('INSTRUCTIONS',
               "# force_level: checks if the level in the log message is set and if it matches the level set, see levels above\n")

    config['DEFAULT'] = {
        'file': 'log.txt',
        'host': '127.0.0.1',
        'port': 55555,
        'level': '6',
        'abuse_protection': 'False',
        'override_timestamp': 'True',
        'forced_format': 'False',
        'force_complete': 'True',
        'force_date': 'True',
        'force_time': 'True',
        'force_level': 'True'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return True


# Function:		get_config
# Description:	This function tries to read the config.ini file.
# Params:		void
# Returns:		True - file was read and it's ready
#               False - file could not be located / read
def get_config():
    config = configparser.RawConfigParser()
    config.read('config.ini')
    config_details = dict(config.items('DEFAULT'))
    if len(config_details) == 11:
        return config_details
    else:
        return False


details_dict = get_config()
if details_dict is False:
    set_config()
    details_dict = get_config()

# Default variables
file = details_dict['file']
host = details_dict['host']
port = int(details_dict['port'])
level = ErrorLevel(int(details_dict['level']))
abuse_protection = bool(strtobool(details_dict['abuse_protection']))
override_timestamp = bool(strtobool(details_dict['override_timestamp']))
forced_format = bool(strtobool(details_dict['forced_format']))
force_complete = bool(strtobool(details_dict['force_complete']))
force_date = bool(strtobool(details_dict['force_date']))
force_time = bool(strtobool(details_dict['force_time']))
force_level = bool(strtobool(details_dict['force_level']))

# Connection Data
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []  # List for clients
mutex = Lock()
writes = 0

# Starts abuse prevention system
if abuse_protection:
    protect = threading.Thread(target=prevent_abuse)
    protect.start()

# Starting Server
server.bind((host, port))
server.listen()

receive()
