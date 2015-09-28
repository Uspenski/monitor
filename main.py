#!/usr/bin/env python

import time, MySQLdb
from datetime import datetime
from objected import UserDict
from interfaced import Interface
from requested import RequestConstructor, ControlRequest
from daemon import Daemon

import PSModule

class GoControl:
	def __init__(self):
		self.model = GoModel()
		self.view = GoView()
	def go(self):
		pass
		
class GoModel:
	def __init__(self):
		self.obj_set=[]
	def __str__(self):
		return reduce(lambda res, x: res+x, map(lambda x: "PID: %s, CPU: %s, MEM: %s, COMMAND: %s, TIME: %s \n" % tuple(x.split(";")), self.process), "name: '%s', CPU: %s, MEM: %s \n" % (self.name, self.CPU, self.MEM))
	def AddObj(self, UserCpuMem):
		UserCpuMem = UserCpuMem.split(';')
		self.name=UserCpuMem[0]
		self.CPU=UserCpuMem[1]
		self.MEM=UserCpuMem[2]
		self.process=[]

class GoView:
	def __init__(self):
		pass

if __name__ == '__main__':
	Controller = GoControl()
	Controller.go()