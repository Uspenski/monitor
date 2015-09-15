#!/usr/bin/env python

import time, MySQLdb, subprocess
from datetime import datetime

def sortByCPU(inputstr):
	return inputstr.rstrip().split(';')[2]

def sortByMEM(inputstr):
	return inputstr.rstrip().split(';')[3]

class ObjectSet:
	"""
	Base object methods
	"""
	def __str__(self):
		"""
		version: 0.2
		date: 15.09.2015
		Status: finished
		"""
		return reduce(lambda res, x: res+x, map(lambda x: "PID: %s, CPU: %s, MEM: %s, COMMAND: %s, TIME: %s \n" % tuple(x.split(";")), self.process), "name: '%s', CPU: %s, MEM: %s \n" % (self.name, self.CPU, self.MEM))

class UserDict(ObjectSet):
	"""
	Users, CPU, MEM, process object constructor
	"""
	def __init__(self, UserCpuMem):
		"""
		User-object constructor
		existing: string separated by ';' like 'root;0;0.2'
		Returns:
			object:
				properties:
					type(self.name) == str
					type(self.CPU) == str
					type(self.MEM) == str
					type(self.process) == list
				methods:
					__str__: return ("name: '%s', CPU: %s, MEM: %s PROC: %s" % (self.name, self.CPU, self.MEM, self.process[0]))
		"""
		UserCpuMem = UserCpuMem.split(';')
		self.name=UserCpuMem[0]
		self.CPU=UserCpuMem[1]
		self.MEM=UserCpuMem[2]
		self.process=[]

"""
using:
for obj in self.obj_set:
	obj.__dict__['process'].append()
map(lambda x: Interface(x).Users_process(), self.obj_set) ==[:||||:]==> Interface.__init(obj)__ + self.Users_process('root', 0)
"""

class Interface:
	"""
	Using: Needed to process obj_set
	version: 0.1
	date: 15.09.2015
	Status: finished
	"""
	def __init__(self, obj):
		self.obj = obj
	def Users_process(self, position=0, col=1):
		answ_gen = list(ControlRequest(str(RequestConstructor("ps aux", *["awk '$%s==\"%s\"'" % (col, self.obj.name)]+["awk ' { print $2\";\"$3\";\"$4\";\"$11\";\"$9} '"]))))
		self.obj.process+=sorted(answ_gen, key=sortByCPU, reverse=True)[:5]
		map(lambda x: self.obj.process.append(x), filter(lambda x: x not in self.obj.process, sorted(answ_gen, key=sortByMEM, reverse=True)[:5]))
		
class RequestConstructor:
	"""
	Using:
		Needed to create requests for Popen_request method
		RequestConstructor("ps aux", "grep -v USER", "awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \";\"suma[i]\";\"sumb[i]}'")
		# ... ps aux | grep -v USER | awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i ";"suma[i]";"sumb[i]}'
	Exists:
		1: func  		- Name of recuest function, like 'ps', 'ls', ... Type: str
		2: *param 		- Collection of single params. Type: str
	Returns:
		string
			Looks like: ps aux | grep -v USER | awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \":\"suma[i]\":\"sumb[i]}'
	Used in: 
		ClassControlRequest to perform params to str
	Status: finished
	version: 0.1
	date: --:--:----
	"""
	request = ""
	def __init__(self, func, *param):
		self.parametrs=list(param)
		self.request = func
		for req_param in self.parametrs:
			self.request += ' | '+req_param
	def __str__(self):
		return self.request

class ControlRequest:
	"""
	Using:
		Needed to convert request in second argument to answers by using function in first argument
		+ exec request and return list of answer strings
	Exists:
		1: function 	- functions must return generator. Type: Function, which returns generator object
		2: req 			- must be str or iteration object (must has attribute '__iter__') Type: str or iteration object
	Returns:
		generator:
			- one string of request
			+ list of strings
	Used in: ProcessSnapshot.__init__
	Status: finished
	version : 1.0.1
	date: 10.09.2015
	"""
	def Popen_request(self, req):
		"""
		used in: Class ProcessSnapshot.__init__() second argument of 'map'
		Appeal to module subprocess /bin/shell with request and return LIST OF STRINGS
		Returns: LIST of string like: ['101:0:0.3', '104:0:0.2', '112:0:16.1', 'andy:0:4.1', ...]
		Returns: 
			- generator of strings from list
			+ List of strings
		"""
		values = subprocess.Popen(req, shell=True, stdout=subprocess.PIPE) 
		return values.stdout.read().rstrip().split('\n')
		#return (str(i) for i in values.stdout.read().rstrip().split('\n'))
	def __init__(self, req, function=''):
		self.requests = []
		if function: 
			self.function = function
		else:
			self.function=self.Popen_request
		if type(req) == str: 
			self.requests.append(req)
		else: 
			if hasattr(req, '__iter__'): self.requests=req
		self.main_iterable_obj = iter(self.requests)
		self.answer_gen = (i for i in self.function(next(self.main_iterable_obj)))
	def __iter__(self):
		return self
	def next(self):
		try:
			answ = next(self.answer_gen)
		except StopIteration:
			try:
				now_request = next(self.main_iterable_obj)
			except StopIteration:
				raise StopIteration
			else:
				self.answer_gen = (i for i in self.function(now_request))
				answ = next(self.answer_gen)
		return answ

class ProcessSnapshot:
	"""
	Class to control PS requests in Control_class
	Used in: 	Control_class.__init__
	Status: 	under constraction
	version: 	0.1.2
	last fix:	adding self.Popen_request method to class RequestConstructor
	date: 		10.09.2015
	"""
	def __init__(self):
		map(lambda x: self.obj_set.append(UserDict(x)), ControlRequest(str(RequestConstructor("ps aux", "grep -v USER", "awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \";\"suma[i]\";\"sumb[i]}'"))))
		map(lambda x: Interface(x).Users_process(), self.obj_set)
	def PrintPlease(self):
		for objects in self.obj_set:
			print objects
	
class Control_class(ProcessSnapshot):
	obj_set = []
	def __init__(self):
		ProcessSnapshot.__init__(self)
		ProcessSnapshot.PrintPlease(self)

def main_func():
	Control_class()

if __name__ == '__main__':
	main_func()
