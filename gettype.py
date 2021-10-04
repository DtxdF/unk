import datetime
import time

def getint(data):
	data = int(data)

	return data

def getfloat(data):
	data = float(data)

	return data

def getboolean(data):
	if (isinstance(data, bool)):
		return data

	if (isinstance(data, int)):
		return bool(data)

	data = data.lower()

	if (data == '0' or data == 'false'):
		return False
	elif (data == '1' or data == 'true'):
		return True
	else:
		raise ValueError("This is not valid boolean value")

def getdate(data):
	f = "%Y-%m-%d"
	t = time.strptime(data, f)
	return datetime.date(
		t.tm_year,
		t.tm_mon,
		t.tm_mday
	)

def gettime(data):
	f = "%H:%M:%S"
	t = time.strptime(data, f)
	return datetime.time(
		t.tm_hour,
		t.tm_min,
		t.tm_sec
	)

def getdatetime(data):
	f = "%Y-%m-%d %H:%M:%S"
	t = time.strptime(data, f)

	return datetime.datetime(
		t.tm_year,
		t.tm_mon,
		t.tm_mday,
		t.tm_hour,
		t.tm_min,
		t.tm_sec
	)

def date2datetime(date_data):
	return datetime.datetime(
		year=date_data.year,
		month=date_data.month,
		day=date_data.day
	)
