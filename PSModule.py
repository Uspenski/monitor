#!/usr/bin/env python

import time, MySQLdb
import subprocess
from datetime import datetime
from abc import ABCMeta, abstractmethod

def sortByCPU(inputstr):
	return inputstr.rstrip().split(';')[2]

def sortByMEM(inputstr):
	return inputstr.rstrip().split(';')[3]

class ObjectSet:
	__metaclass__ = ABCMeta
	@abstractmethod
	def modelIsChanged(self):
		pass
	def __str__(self):
		return reduce(lambda res, x: res+x, map(lambda x: "PID: %s, CPU: %s, MEM: %s, COMMAND: %s, TIME: %s \n" % tuple(x.split(";")), self.process), "name: '%s', CPU: %s, MEM: %s \n" % (self.name, self.CPU, self.MEM))
	def Users_process(self, position, col):
		answ_gen = list(ControlRequest(str(RequestConstructor("ps aux", *["awk '$%s==\"%s\"'" % (col, self.name)]+["awk ' { print $2\";\"$3\";\"$4\";\"$11\";\"$9} '"]))))
		self.process+=sorted(answ_gen, key=sortByCPU, reverse=True)[:5]
		map(lambda x: self.process.append(x), filter(lambda x: x not in self.process, sorted(answ_gen, key=sortByMEM, reverse=True)[:5]))

class UserDict(ObjectSet):
	def __init__(self, UserCpuMem):
		UserCpuMem = UserCpuMem.split(';')
		self.name=UserCpuMem[0]
		self.CPU=UserCpuMem[1]
		self.MEM=UserCpuMem[2]
		self.process=[]
	def modelIsChanged(self):
		ObjectSet.Users_process(self, position=0, col=1)

class ControlRequest_iterator:
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

class ControlRequest(ControlRequest_iterator):
	request = None
	def __init__(self):
		self.RequestConstruct(request)
		self.requests = []
		self.AppendRequest()
		self.main_iterable_obj = iter(self.requests)
		self.answer_gen = (i for i in self.Popen_request(next(self.main_iterable_obj)))
	def AppendRequest(self):
		if type(self.request) == str: 
			self.requests.append(self.request)
		else: 
			if hasattr(self.request, '__iter__'): self.requests=self.request
	def RequestConstruct(self, *param):
		self.parametrs=list(param)
		for req_param in self.parametrs:
			self.request += ' | '+req_param
	def Popen_request(self, req):
		values = subprocess.Popen(req, shell=True, stdout=subprocess.PIPE) 
		return values.stdout.read().rstrip().split('\n')

class PSView:
	def __init__(self, inController, inModel):
		self.model = inModel
		self.controller = inController
		self.model.appendObservers( self )
	def modelIsChanged(self):
		pass

class Users_process(ControlRequest):
	"""Users_process"""
	request = list("ps aux", *["awk '$%s==\"%s\"'" % (col, self.name)]+["awk ' { print $2\";\"$3\";\"$4\";\"$11\";\"$9} '"])
	def __init__(self):
		pass

class Users_in_system(Users_process):
	"""Users_in_system"""
	request = list("ps aux", "grep -v USER", "awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \";\"suma[i]\";\"sumb[i]}'")
	def __init__(self):
		pass		
	
class PSModel(Users_in_system):
	""""""
	def __init__(self):
		self.obj_set=[]
		self._mObservers = []
	def appendObservers(self, inObserver):
		self._mObservers.append(inObserver)
	def notifyObservers(self):
		for x in self._mObservers:
			x.modelIsChanged()
		#map(self.appendObservers, ControlRequest())
		#for x in self._mObservers:
		#	x.modelIsChanged()

class PSControl:
	def __init__(self):
		self.model=PSModel()
		self.view=PSView(self, self.model)

if __name__ == '__main__':
	a=PSControl()