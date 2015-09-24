#!/usr/bin/env python

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

if __name__ == '__main__':
	pass