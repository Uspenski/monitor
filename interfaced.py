#!/usr/bin/env python

from requested import RequestConstructor, ControlRequest

def sortByCPU(inputstr):
	return inputstr.rstrip().split(';')[2]

def sortByMEM(inputstr):
	return inputstr.rstrip().split(';')[3]

class Interface:
	"""
	Using: Needed to process obj_set
	version: 0.1
	date: 15.09.2015
	Status: finished
	using manual:
		for obj in self.obj_set:
			obj.__dict__['process'].append()
		map(lambda x: Interface(x).Users_process(), self.obj_set) ==[:||||:]==> Interface.__init(obj)__ + self.Users_process('root', 0)
	"""
	def __init__(self, obj):
		self.obj = obj
	def Users_process(self, position=0, col=1):
		answ_gen = list(ControlRequest(str(RequestConstructor("ps aux", *["awk '$%s==\"%s\"'" % (col, self.obj.name)]+["awk ' { print $2\";\"$3\";\"$4\";\"$11\";\"$9} '"]))))
		self.obj.process+=sorted(answ_gen, key=sortByCPU, reverse=True)[:5]
		map(lambda x: self.obj.process.append(x), filter(lambda x: x not in self.obj.process, sorted(answ_gen, key=sortByMEM, reverse=True)[:5]))

if __name__ == '__main__':
	pass