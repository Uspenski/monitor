#!/usr/bin/env python

import time, MySQLdb
from datetime import datetime
from objected import UserDict
from interfaced import Interface

import subprocess

class RequestConstructor:
	request = ""
	def __init__(self, func, *param):
		self.parametrs=list(param)
		self.request = func
		for req_param in self.parametrs:
			self.request += ' | '+req_param

class ControlRequest(RequestConstructor):
	def Popen_request(self, req):
		values = subprocess.Popen(req, shell=True, stdout=subprocess.PIPE) 
		return values.stdout.read().rstrip().split('\n')
	def __init__(self):
		RequestConstructor.__init__(self, "ps aux", "grep -v USER", "awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \";\"suma[i]\";\"sumb[i]}'")
		self.requests = []
		if type(self.request) == str: 
			self.requests.append(self.request)
		else: 
			if hasattr(self.request, '__iter__'): self.requests=self.request
		self.main_iterable_obj = iter(self.requests)
		self.answer_gen = (i for i in self.Popen_request(next(self.main_iterable_obj)))
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

class PSView:
	def __init__(self, inController, inModel):
		self.model = inModel
		self.controller = inController
	
class PSModel:
	""""""
	def __init__(self):
		self._mObservers = []
	def appendObservers(self, inObserver):
		self._mObservers.append(UserDict(inObserver))
	def notifyObservers(self):
		self._mObservers = []
		map(self.appendObservers, ControlRequest())
		for x in self._mObservers:
			x.modelIsChanged()

class PSControl:
	def __init__(self):
		self.model=PSModel()
		self.view=PSView(self, self.model)



if __name__ == '__main__':
	a=PSControl