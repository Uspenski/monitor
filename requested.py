#!/usr/bin/env python

import subprocess

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

if __name__ == '__main__':
	pass