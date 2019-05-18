from datetime import date, datetime, time, timedelta, timezone

import math
import subprocess


def shell_cmd(cmd):
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def get_first_of_following_month(utcnow):
    year = utcnow.year
    month = utcnow.month + 1
    if (month == 13):
        year += 1
        month = 1
    result = datetime(year, month, 1, 0, 0, 0, 0, timezone.utc)
    return result
    

def get_first_of_next_month():
    utcnow = get_utcnow()
    return get_first_of_following_month(utcnow)


def get_formatted_datetime(date_time):
    result = date_time.strftime('%Y-%m-%d %H:%M:%S %Z (%z)')
    return result


def get_formatted_timedelta(delta, include_relative_indicator=True):
    total_seconds = delta.total_seconds()
    is_past = total_seconds < 0
    if is_past:
        total_seconds = abs(total_seconds)
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    seconds = round(seconds)
    minutes = math.floor(minutes)
    hours = math.floor(hours)
    days = math.floor(days)
    weeks = math.floor(weeks)
    result = ''
    if (weeks > 0):
        result += '{:d}w '.format(weeks)
    result += '{:d}d {:d}h {:d}m {:d}s'.format(days, hours, minutes, seconds)
    if include_relative_indicator:
        if is_past:
            result += ' ago'
        else:
            result = 'in {}'.format(result)
    return result


def get_utcnow():
    return datetime.now(timezone.utc)


#---------- DB utilities ----------
DB_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def db_get_column_definition(column_name, column_type, is_primary=False, not_null=False):
    column_name_txt = column_name.upper()
    column_type_txt = column_type.upper()
    is_primary_txt = ''
    not_null_txt = ''
    if is_primary:
        is_primary_txt = ' PRIMARY KEY'
    if not_null:
        not_null_txt = ' NOT NULL'
    result = '{} {}{}{}'.format(column_name_txt, column_type_txt, is_primary_txt, not_null_txt)
    return result


def db_get_where_string(column_name, column_value, is_text_type=False):
    print('+ called db_get_where_string({}, {}, {})'.format(column_name, column_value, is_text_type))
    column_name = column_name.lower()
    if is_text_type:
        column_value = db_convert_text(column_value)
    return '{} = {}'.format(column_name, column_value)


def db_convert_boolean(value):
    if value:
        return 'TRUE'
    else:
        return 'FALSE'
    
def db_convert_text(value):
    if value:
        result = str(value)
        result = result.replace('\'', '\'\'')
        result = '\'{}\''.format(result)
        return result
    else:
        return ''
    
def db_convert_timestamp(datetime):
    if datetime:
        result = datetime.strftime(DB_TIMESTAMP_FORMAT)
        return result
    else:
        return None

def db_convert_to_boolean(db_boolean):
    db_upper = db_boolean.upper()
    if db_upper == 'TRUE' or db_upper == '1' or db_upper == 'T' or db_upper == 'Y' or db_upper == 'YES':
        return True
    else:
        return False
    
def db_convert_to_datetime(db_timestamp):
    result = db_timestamp.strptime(DB_TIMESTAMP_FORMAT)
    
