#
# FILE              : helper.py
# PROJECT			: SENG2040 - Assignment 03
# PROGRAMMER		: Filipe Brito
# FIRST VERSION     : 26/02/2020
# DESCRIPTION		:
# 	This file is the classes holder.
# 	There are two classes in this file, one of them is ErrorLevel a
# 	simple enum for the error level of the LogEntry. LogEntry is the
#   other one, this class holds an entry to be written to the log.
#
from enum import Enum
import time

#
# Class: ErrorLevel
# Description: Enum for all the levels supported by the logger.
#
ErrorLevel = Enum('Level', 'OFF TRACE DEBUG INFO WARN ERROR FATAL')

#
# Class: EntryLog
# Description: Class that represents an entry in the log file.
#
class EntryLog:
    """A class for log entries."""

    # Function:		__init__
    # Description:	Default constructor for the EntryLog class
    # Params:		line = string with all the info of the log
    # Returns:		void
    def __init__(self, line, ip=""):
        self.raw_message = line
        self.date = self.parse_date(line)
        self.time = self.parse_time(line)
        self.level = self.parse_error_level(line)
        self.message = self.parse_message(line)
        if ip != "":
            self.ip = ip

    # Function:		get_full_string
    # Description:	Returns a concatenated string with all info within the object.
    # Params:		self - reference to the instance of the class
    # Returns:		str - contents of self concatenated
    def get_full_string(self):
        full_message = ""
        if self.is_date_set():
            full_message += "[" + self.date + "] "
        if self.is_time_set():
            full_message += "[" + self.time + "] "
        if self.is_ip_set():
            full_message += "[" + self.ip + "] "
        if self.is_level_set():
            full_message += "[" + self.level.name + "] "
        if self.is_message_set():
            full_message += self.message

        if full_message == "":
            return False
        else:
            return full_message

    # Function:		get_message_string
    # Description:	Returns a concatenated string with some info within the object.
    # Params:		self - reference to the instance of the class
    # Returns:		str - some contents of self concatenated
    def get_message_string(self):
        message = ""
        if self.is_ip_set():
            message += "[" + self.ip + "] "
        if self.is_level_set():
            message += "[" + self.level.name + "] "
        if self.is_message_set():
            message += self.message

        if message == "":
            return False
        else:
            return message

    # Function:		all_fields_present
    # Description:	Returns a boolean stating if all the fields of the object are properly filled.
    # Params:		self - reference to the instance of the class
    # Returns:		True - if all the fields are present
    #               False otherwise
    def all_fields_present(self):
        return \
            self.is_date_set() & \
            self.is_time_set() & \
            self.is_level_set() & \
            self.is_ip_set() & \
            self.is_message_set()

    # Function:		is_date_set
    # Description:	Returns a boolean stating if the date field is properly filled.
    # Params:		self - reference to the instance of the class
    # Returns:		True - if the field is correctly filled
    #               False otherwise
    def is_date_set(self):
        return (self.date != "") & (self.date is not False)

    # Function:		is_time_set
    # Description:	Returns a boolean stating if the time field is properly filled.
    # Params:		self - reference to the instance of the class
    # Returns:		True - if the field is correctly filled
    #               False otherwise
    def is_time_set(self):
        return (self.time != "") & (self.time is not False)

    # Function:		is_level_set
    # Description:	Returns a boolean stating if the level field is properly filled.
    # Params:		self - reference to the instance of the class
    # Returns:		True - if the field is correctly filled
    #               False otherwise
    def is_level_set(self):
        return self.level is not False

    # Function:		is_ip_set
    # Description:	Returns a boolean stating if the ip field is properly filled.
    # Params:		self - reference to the instance of the class
    # Returns:		True - if the field is correctly filled
    #               False otherwise
    def is_ip_set(self):
        return (self.ip != "") & (self.ip is not False)

    # Function:		is_message_set
    # Description:	Returns a boolean stating if the message field is properly filled.
    # Params:		self - reference to the instance of the class
    # Returns:		True - if the field is correctly filled
    #               False otherwise
    def is_message_set(self):
        return (self.message != "") & (self.message is not False)

    # Function:		parse_date
    # Description:	Will go through the message string checking if there is a date in the correct format.
    # Params:		line - string with the whole log entry
    # Returns:		date - a string date from the line that matches the format
    #               False otherwise
    @staticmethod
    def parse_date(line):
        words = line.split()

        for date in words:
            try:
                temp = time.strptime(date, "%Y/%m/%d")
            except ValueError:
                pass
                continue
            if isinstance(temp, time.struct_time):
                return date
        return False

    # Function:		parse_time
    # Description:	Will go through the message string checking if there is a time in the correct format.
    # Params:		line - string with the whole log entry
    # Returns:		hour - a string time from the line that matches the format
    #               False otherwise
    @staticmethod
    def parse_time(line):
        words = line.split()

        for hour in words:
            try:
                temp = time.strptime(hour, "%H:%M:%S")
            except ValueError:
                pass
                continue
            if isinstance(temp, time.struct_time):
                return hour
        return False

    # Function:		parse_error_level
    # Description:	Will go through the message string checking if there is an ErrorLevel in the correct format.
    # Params:		line - string with the whole log entry
    # Returns:		ErrorLevel - a parsed string to ErrorLevel enum
    #               False otherwise
    @staticmethod
    def parse_error_level(line):
        levels = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
        words = line.split()
        for lvl in words:
            try:
                temp = levels.index(lvl.upper())
            except ValueError:
                pass
                continue
            if isinstance(temp, int):
                return ErrorLevel[lvl]
        return False

    # Function:		parse_message
    # Description:	Will go through the message string checking if there is a message.
    # Params:		line - string with the whole log entry
    # Returns:		str - a string with the message found
    #               False otherwise
    @staticmethod
    def parse_message(line):
        if line == "":
            return False
        message = ""
        words = line.split()
        count = 0

        if EntryLog.parse_date(line) is not False:
            count += 1
        if EntryLog.parse_time(line) is not False:
            count += 1
        if EntryLog.parse_error_level(line) is not False:
            count += 1

        for word in words:
            if count > 0:
                count -= 1
                continue
            else:
                message += word + " "

        return message.rstrip()
