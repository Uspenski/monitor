#!/usr/bin/env python
from requested import RequestConstructor, ControlRequest

def sortByCPU(inputstr):
	return inputstr.rstrip().split(';')[2]

def sortByMEM(inputstr):
	return inputstr.rstrip().split(';')[3]

class ObjectSet:
	"""
	---Observer---
	Base object methods
	"""
	def __str__(self):
		"""
		version: 0.2
		date: 15.09.2015
		Status: finished
		"""
		return reduce(lambda res, x: res+x, map(lambda x: "PID: %s, CPU: %s, MEM: %s, COMMAND: %s, TIME: %s \n" % tuple(x.split(";")), self.process), "name: '%s', CPU: %s, MEM: %s \n" % (self.name, self.CPU, self.MEM))
	def Users_process(self, position, col):
		answ_gen = list(ControlRequest(str(RequestConstructor("ps aux", *["awk '$%s==\"%s\"'" % (col, self.name)]+["awk ' { print $2\";\"$3\";\"$4\";\"$11\";\"$9} '"]))))
		self.process+=sorted(answ_gen, key=sortByCPU, reverse=True)[:5]
		map(lambda x: self.process.append(x), filter(lambda x: x not in self.process, sorted(answ_gen, key=sortByMEM, reverse=True)[:5]))

class UserDict(ObjectSet):
	"""
	---ConcreateObserver---
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
	def Users_process(self):
		ObjectSet.Users_process(self, position=0, col=1)

if __name__ == '__main__':
	pass