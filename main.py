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
		pass

class GoView:
	def __init__(self):
		pass

if __name__ == '__main__':
	Controller = GoControl()
	Controller.go()