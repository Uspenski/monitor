#!/usr/bin/env python

import time, MySQLdb
from datetime import datetime
from objected import UserDict
from interfaced import Interface
from requested import RequestConstructor, ControlRequest

class PSView:
	def __init__(self):
		pass
	
class PSModel:
	""""""
	def __init__(self):
		self._mObservers = []
	def add_Obj(self, UserCpuMem):
		self._mObservers.append(UserDict(UserCpuMem))
	def filling_storage(self):
		map(self.add_Obj, ControlRequest(str(RequestConstructor("ps aux", "grep -v USER", "awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \";\"suma[i]\";\"sumb[i]}'"))))
		for elem in self._mObservers:
			elem.Users_process()
	def update(self):
		self._mObservers = []
		self.filling_storage()

class PSControl(PSModel):
	def __init__(self):
		self.model=PSModel()
		self.filling_storage()



if __name__ == '__main__':
	a=PSModel()
	a.filling_storage()