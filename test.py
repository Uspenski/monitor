#!/usr/bin/env python

import time, MySQLdb
from datetime import datetime
from objected import UserDict
from interfaced import Interface
from requested import RequestConstructor, ControlRequest
		
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
	def __init__(self):
		self.obj_set = []
		ProcessSnapshot.__init__(self)
		ProcessSnapshot.PrintPlease(self)

def main_func():
	Control_class()

if __name__ == '__main__':
	main_func()
