#!/usr/bin/env python

import time, MySQLdb
from datetime import datetime
from objected import UserDict
from interfaced import Interface
from requested import RequestConstructor, ControlRequest

class PS:
	def __init__(self):
		pass

class PSControl(PSModel):
	def __init__(self):
		pass
		
class PSModel:
	def __init__(self):
		pass
	def fill(self):
		map(lambda x: self.obj_set.append(UserDict(x)), ControlRequest(str(RequestConstructor("ps aux", "grep -v USER", "awk '{suma[$1] += $3; sumb[$1] += $4}END {for(i in suma)print i \";\"suma[i]\";\"sumb[i]}'"))))
		
if __name__ == '__main__':
	pass