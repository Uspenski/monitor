#!/usr/bin/env python
import subprocess
from datetime import datetime

def sortByCPU(inputstr):
	return inputstr.rstrip().split(';')[2]

def sortByMEM(inputstr):
	return inputstr.rstrip().split(';')[3]

class ObjectSet:
	def __str__(self):
		return reduce(lambda res, x: res+x, map(lambda x: "PID: %s, CPU: %s, MEM: %s, COMMAND: %s, TIME: %s \n" % tuple(x.split(";")), self.process), "name: '%s', CPU: %s, MEM: %s \n" % (self.name, self.CPU, self.MEM))

class UserDict(ObjectSet):
	def __init__(self, UserCpuMem):
		UserCpuMem = UserCpuMem.split(';')
		self.name=UserCpuMem[0]
		self.CPU=UserCpuMem[1]
		self.MEM=UserCpuMem[2]
		self.process=[]

class Interface:
	def __init__(self, obj):
		self.obj = obj
	def Users_process(self, position=0, col=1):
		answ_gen = list(ControlRequest(str(RequestConstructor("ps aux", *["awk '$%s==\"%s\"'" % (col, self.obj.name)]+["awk ' { print $2\";\"$3\";\"$4\";\"$11\";\"$9} '"]))))
		self.obj.process+=sorted(answ_gen, key=sortByCPU, reverse=True)[:5]
		map(lambda x: self.obj.process.append(x), filter(lambda x: x not in self.obj.process, sorted(answ_gen, key=sortByMEM, reverse=True)[:5]))
		
class RequestConstructor:
	def __init__(self, func, *param):
		self.parametrs=list(param)
		self.request = func
		for req_param in self.parametrs:
			self.request += ' | '+req_param
	def __str__(self):
		return self.request

class ControlRequest:
	def Popen_request(self, req):
		values = subprocess.Popen(req, shell=True, stdout=subprocess.PIPE) 
		return values.stdout.read().rstrip().split('\n')
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