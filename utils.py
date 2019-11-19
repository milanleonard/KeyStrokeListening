import datetime
import numpy as np
import os

data_dir = "./raw_data/"
tmp_dir = "./tmp/"
dictionary_mapping = {"Key.shift_r" : "rshift","Key.control_r" : "rctrl",
    "Key.control_l" : "lctrl","Key.space" : "space","Key.backspace" : "backspace","Key.shift_l" : "lshift"}

def convert_times(arr):
	'''
	Returns: array of length input arr of unix times
	converts logging times to unix time
	'''
	timezone = datetime.datetime.now().astimezone().tzinfo
	output = np.zeros(len(arr))
	date_arr = np.zeros((len(arr),7))
	for i in range(len(arr)):
		dmy = arr[i][0].split('-') # date-month-year
		date_arr[i,0],date_arr[i,1],date_arr[i,2] = dmy[0],dmy[1],dmy[2]
		hms = arr[i,1].split(':') # hour minutes (packaged seconds microseconds) 
		sms = hms[-1].split(',')
		date_arr[i,3],date_arr[i,4],date_arr[i,5],date_arr[i,6] = hms[0], hms[1], sms[0],sms[1]
	date_arr = date_arr.astype(int)
	date_arr[:,-1] *= 1000 # convert milliseconds to microseconds
	for i in range(len(date_arr)):
		output[i] = datetime.datetime(date_arr[i,0], date_arr[i,1], date_arr[i,2], date_arr[i,3], date_arr[i,4], date_arr[i,5], date_arr[i,6],timezone).timestamp()
	return output



def make_dirs():
	""" 
	Make's the required directories
	"""
	if not os.path.exists("./raw_data"):
		os.makedirs("./raw_data")
	if not os.path.exists("./tmp"):
		os.makedirs("./tmp")
	if not os.path.exists("./proc_data"):
		os.makedirs("./proc_data")

def get_nonexistant_path(fname_path):
    """
    Get the path to a filename which does not exist by incrementing path.

    Examples
    --------
    >>> get_nonexistant_path('/etc/issue')
    '/etc/issue-1'
    >>> get_nonexistant_path('whatever/1337bla.py')
    'whatever/1337bla.py'
    """
    if not os.path.exists(fname_path):
        return fname_path
    filename, file_extension = os.path.splitext(fname_path)
    i = 1
    new_fname = "{}-{}{}".format(filename, i, file_extension)
    while os.path.exists(new_fname):
        i += 1
        new_fname = "{}-{}{}".format(filename, i, file_extension)
    return new_fname