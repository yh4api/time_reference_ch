#-*- coding:utf-8 -*-
"""
Created on Mon Jul 25 14:13:04 2016
Last Modified on Thu Nov 10 10:45:28 2016
This file is used to normalize chinese date expression to YYYY-MM-DD format

Usage and examples:
>>> python timeRefCHM.py
>>> 明年6月我要去英国看温布顿
00-04 2017-6-XX
>>> 今年10月到明年1月间应该不会有台风了！
START 2016-10-01 END 2017-01-31
>>> 陈书安每天早上10点到晚上6点都在打扰大家。
005-010: 早上10点
011-015: 晚上6点
START 2016-01-01 END 2016-12-31
>>> 美国联邦调查局长科米告诉国会，他没有改变他在今年7月20号得出的结论。
22-29 2016-7-20
>>> 我要去韩国玩5天

>>> 总统大选将在2个月后举行。
START 2017-01-09
>>> exit

@author: yenhsi.lin
"""
import re
from datetime import date
from datetime import timedelta

monthDayTable = [0, 31,28,31,30,31,30,31,31,30,31,30,31]
difference = {u"大前":-3, u"前":-2, u"明":1, u"后":2, u"大后":3, u"上上":-2,u"上":-1,u"下":1, u"下下":2, u"上个":-1, u"下个":1, u"上上个":-2, u"下下个":-2, u"去":-1}
temporalType = "None" #0: none 1:specific 2:range
dateStart = {}
dateEnd = {}
regTime1 = u"(\d{1,2}(点|时)\d{1,2}分(\d{1,2}秒)?)"
compTime1 = re.compile(regTime1)
regTime2 = u"(\d{1,2}(点|时)(整|半))"
compTime2 = re.compile(regTime2)

regMiddleRange = u"(清晨|早上|上午|中午|下午|傍晚|晚上|晚间|凌晨)\d{1,2}(点|时)"
compMiddle = re.compile(regMiddleRange)

today = date.today()
# Y:P M:P D:P W:C WD:C
class temporalItem:
	def __init__(self, tid):
		self.y = None
		self.m = None
		self.d = None
		self.w = None
		self.wd = None
		self.pos = None
		self.definiteRange = 0
		self.Id = tid

		
#====== 年自成一格 
regDate1 = u"(\d{1,2})(月)(\d{1,2})(日|號)" #M = g(1) D = g(3) sure
regDate5 = u"(本|这个|上个|下个|上上个|下下个)(月)(\d{1,2})(日|号)" #M = P+difference[g(1)], D = g(3) sure
regDate7 = u"(本|这个)月" #M = 1
regDate8 = u"(上|下){1,2}个月"#M = P+difference[g(1)]
regDate2 = u"(\d{1,2})(月)"#M = g(1)
#======

regDate4 = u"(大前|前|今|明|后|大后)(年|天)" #if g(2) == "年": Y = P+difference[g(1)] else:D=P+difference[g(1)] #date is sure
regDate6 = u"昨天" #D = P-1 sure
regDate3 = u"(\d{1,}|去)(年)"#if g(2) == "去": Y = P-1 else: Y = P 

regDate15 = u"(\d{1,}|去|大前|前|今|明|后|大后)年[^0-9]?(\d{1,2})月((\d{1,2})(日|号))?" #specific

regDate9 = u"(\d+)(个月|週|星期|个礼拜|个星期|天|世紀)" ##一個月 一天 一週 只能為range必須要有搭配詞

regDate11 = u"(上|下|上上|下下|这|本|这个)?(週|周|星期|礼拜)([1-6])" #WD = g(3) W = C+difference[g(1)] date is sure
regDate12 = u"(上|下|上上|下下|这|本|这个)?(週|周|星期|礼拜)(天|日)" #WD = g(3) W = C+difference[g(1)] date is sure
regDate10 = u"(上|下|上上|下下|这|本|这个)(週|周|星期|礼拜)" #WD = 1 W = C+difference[g(1)]

regDigitDate1 = "(\d{4})-(\d{1,2})-(\d{1,2})"
regDigitDate2 = "(\d{4})\.(\d{1,2})\.(\d{1,2})"
regDigitDate3 = "(\d{4})/(\d{1,2})/(\d{1,2})"
regDigitDate4 = "(\d{4})(\d{2})(\d{2})"


compName = ["compDate"+str(j) for j in [1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,18,19]]
regName = [regDate1, regDate2, regDate3, regDate4, regDate5, regDate6, regDate7, regDate8, regDate9, regDate10, regDate11, regDate12, regDate15, regDigitDate1, regDigitDate2, regDigitDate3, regDigitDate4]

for compNamei, regNamei in zip(compName, regName):
	globals()[compNamei] = re.compile(regNamei)



"""
compDate1 = re.compile(regDate1)
compDate2 = re.compile(regDate2)
compDate3 = re.compile(regDate3)
compDate4 = re.compile(regDate4)
compDate5 = re.compile(regDate5)
compDate6 = re.compile(regDate6)
compDate7 = re.compile(regDate7)
compDate8 = re.compile(regDate8)
compDate9 = re.compile(regDate9)
compDate10 = re.compile(regDate10)
compDate11 = re.compile(regDate11)
compDate12 = re.compile(regDate12)
compDate15 = re.compile(regDate15)

compDate16 = re.compile(regDigitDate1)
compDate17 = re.compile(regDigitDate2)
compDate18 = re.compile(regDigitDate3)
compDate19 = re.compile(regDigitDate4)
"""
regRange1 = u"\d(之前|以前|前|之后|以后|后|起|开始|之内|以内|内|来|以来|以上|以下)"
regRange2 = u"(从|自|到|至)\d"
compRange1 = re.compile(regRange1)
compRange2 = re.compile(regRange2)

today = date.today()

class temporalDetect:
	def __init__(self, debug):
		self.debug = debug
		self.temporalId = 1
		self.twBuffer = []
		self.timeItemDict = {}
		self.occupied = set()
		#for range record
		self.rangeStart = [None]
		self.rangeEnd = [None]
	def printGroup(self, group, y):
		if self.debug:
			print "Group%d  %02d-%02d: %s"%(group, y.start(), y.end(), y.group(0))

	def fillBuffer(self, y, filler=None, caseNumber = None):
		#global temporalId
		if filler == None:
			thisOccupied = set(j for j in range(y.start(), y.end()))
			if thisOccupied&self.occupied != set():
				if self.debug:
					print "overlapped expression"
			else:
				for j in range(y.start(), y.end()):
				
					self.twBuffer[j] = self.temporalId
					self.occupied.add(j)	
	
			tItem = temporalItem(self.temporalId)
			tItem.pos = "%02d-%02d"%(y.start(), y.end())
			if caseNumber == 15:
				
				if re.match("\d+", y.group(1)):
					tItem.y = int(y.group(1))
				else:
					tItem.y = today.year+difference.get(y.group(1), 0)
				tItem.m = int(y.group(2))
				tItem.d = int(y.group(4)) if y.group(4)!=None else None
								 
			elif caseNumber == 1:
				tItem.m = int(y.group(1))
				tItem.d = int(y.group(3))
			elif caseNumber == 5:
				tItem.d = int(y.group(3))
				tItem.m = today.month + difference.get(y.group(1), 0)
				tItem.y = today.year
			elif caseNumber == 7:
				tItem.m = today.month
				tItem.y = today.year
			elif caseNumber == 8:#timedelta
				tItem.m = today.month + difference.get(y.group(1), 0)
				tItem.y = today.year
			elif caseNumber == 2:
				tItem.m = int(y.group(1))
			elif caseNumber == 4:
				if y.group(2) == u"年":
					tItem.y = today.year + difference.get(y.group(1), 0)
				else:
					tItem.d = today.day + difference.get(y.group(1), 0)
					tItem.m = today.month
					tItem.y = today.year
	
			elif caseNumber == 6:
				#??? timedelta today-1
				d2 = today+timedelta(days = -1)
				tItem.y = d2.year
				tItem.m = d2.month
				tItem.d = d2.day
					
			elif caseNumber == 3:
				if y.group(1) == u"去":
					tItem.y = today.year-1
				else:
					tItem.y = int(y.group(1))
	
			elif caseNumber == 9:
				tItem.definiteRange = 1
				if y.group(2) == u"个月":
					#tItem.m = y.group(1)
					tItem.wd = 30*int(y.group(1))
				elif y.group(2) in [u"週", u"周", u"星期", u"个礼拜", u"个星期"]:
					#tItem.wk = y.group(1)
					tItem.wd = 7*int(y.group(1))
				elif y.group(2) == u"天":
					tItem.wd = int(y.group(1))
	
	
			elif caseNumber == 11:
				if y.group(1) == None:
					w = 0
				else:
				  	w = difference.get(y.group(1), 0)*7
				daydelta = int(y.group(3)) - today.isoweekday() + w
				d2 = today+timedelta(days = daydelta)
				tItem.y = d2.year
				tItem.m = d2.month
				tItem.d = d2.day
	
			elif caseNumber == 12:
				if y.group(1) == None:
					w = 0
				else:
					w = difference.get(y.group(1), 0)*7
				daydelta = 7 - today.isoweekday() + w
				d2 = today+timedelta(days = daydelta)
				tItem.y = d2.year
				tItem.m = d2.month
				tItem.d = d2.day
	
			elif caseNumber == 10:
				#week 開始
				#week 結束
				pass
	
			elif 16 <= caseNumber <= 19:
				tmpY = int(y.group(1))
				tmpM = int(y.group(2))
				tmpD = int(y.group(3))
				if 0 < tmpM < 13:
					if 0 < tmpD <= monthDayTable[tmpM]:
						tItem.y = tmpY
						tItem.m = tmpM
						tItem.d = tmpD
	
			self.timeItemDict[self.temporalId] = tItem
			self.temporalId += 1
		else:
			for j in range(y.start(1), y.end(1)):
				self.twBuffer[j] = filler

	def parseTime(self, query):#temporal item detection
		for regi in [compTime1, compTime2, compMiddle]:
			for x in regi.finditer(query):
				print "%03d-%03d: %s"%(x.start(), x.end(), x.group(0))
				self.fillBuffer(x) 
	def parseDate(self, query):
		#group1: if or elif
		if compDate15.search(query) != None:
			for x in compDate15.finditer(query):
				self.printGroup(1, x)
				self.fillBuffer(x, caseNumber = 15)
		if compDate1.search(query) != None:
			for x in compDate1.finditer(query):
				self.printGroup(1, x)
				self.fillBuffer(x, caseNumber = 1)
		if compDate5.search(query) != None:
			for x in compDate5.finditer(query):
				self.printGroup(1, x)
				self.fillBuffer(x, caseNumber = 5)
		if compDate7.search(query) != None:
			for x in compDate7.finditer(query):
				self.printGroup(1, x)
				self.fillBuffer(x, caseNumber = 7)
		if compDate8.search(query) != None:
			for x in compDate8.finditer(query):
				self.printGroup(1, x)
				self.fillBuffer(x, caseNumber = 8)
		if compDate2.search(query) != None:
			for x in compDate2.finditer(query):
				self.printGroup(1, x)
				self.fillBuffer(x, caseNumber = 2)
		#group2
		for i in [3, 4, 6]:
			regi = eval("compDate"+str(i))
			for x in regi.finditer(query):
				self.printGroup(2, x)
				self.fillBuffer(x, caseNumber = i)
		
		#group3
		rangeNeeded = []
		for x in compDate9.finditer(query):
			self.printGroup(3, x)
			self.fillBuffer(x, caseNumber = 9)
		
		#group4 switch to week# and weekday
		if compDate12.search(query) != None:
			for x in compDate12.finditer(query):
				self.printGroup(4, x)
				self.fillBuffer(x, caseNumber = 12)
		if compDate11.search(query) != None:
			for x in compDate11.finditer(query):
				self.printGroup(4, x)
				self.fillBuffer(x, caseNumber = 11)
		if compDate10.search(query) != None:
			for x in compDate10.finditer(query):
				self.printGroup(4, x)
				self.fillBuffer(x, caseNumber = 10)
	
		#group5 georgian date detection
		if compDate16.search(query) != None:
			for x in compDate16.finditer(query):
				self.printGroup(5, x)
				self.fillBuffer(x, caseNumber = 16)
		if compDate17.search(query) != None:
			for x in compDate17.finditer(query):
				self.printGroup(5, x)
				self.fillBuffer(x, caseNumber = 17)
	
		if compDate18.search(query) != None:
			for x in compDate18.finditer(query):
				self.printGroup(5, x)
				self.fillBuffer(x, caseNumber = 18)
		if compDate19.search(query) != None:
			for x in compDate19.finditer(query):
				self.printGroup(5, x)
				self.fillBuffer(x, caseNumber = 19)

	def findRange(self, wSeq, twBuffer):
		
		for x in compRange1.finditer(wSeq):
			if x.group(1) in [u"之后", u"以后", u"起", u"开始", u"后"]:
				self.fillBuffer(x, filler="SL")
			else:
				if x.group(1) in [u"之前", u"前", u"以前"]:
					self.fillBuffer(x, filler="EL1")
				else:
					self.fillBuffer(x, filler="EL")
				# 之前|以前|前|之內|以內|內  2年內的報紙 -2y but 2年內做好 +2y
				# range + 之前 --> -range???
		
		for x in compRange2.finditer(wSeq):
			if x.group(1) in [u"从", u"自"]:
				self.fillBuffer(x, filler="SR")
			else:
				self.fillBuffer(x, filler="ER")#到|至
				# 今天到10月10號, starting point可以省略起始詞
		
		if self.debug:
			print twBuffer
		globalRef = None 
		for tid, t in enumerate(twBuffer):
			#print tid, t
			if t == "SL":
				if not isinstance(twBuffer[tid-1], int):
					continue
				if self.timeItemDict[twBuffer[tid-1]].definiteRange == 1:
					self.timeItemDict[twBuffer[tid-1]].definiteRange = "SL"
				r = self.timeItemDict[twBuffer[tid-1]]
				if r.definiteRange == 0:
					if r.y == None:
						r.y = today.year
					if r.d == None and r.m == None:
						#print "START", date(r.y, 1, 1) 
						self.addRangeItem("start", date(r.y, 1, 1))
					elif r.d == None:
						#print "START", date(r.y, r.m, 1)
						self.addRangeItem("start", date(r.y, r.m, 1))
					else:
						#print "START", date(r.y, r.m, r.d)
						self.addRangeItem("start", date(r.y, r.m, r.d))
					globalRef = r.y
				#else:
				elif r.definiteRange!="toDel": #situation like 從 2011年 開始, 2 cue terms share same temporal slot
					#print "START", today+timedelta(days = r.wd)
					self.addRangeItem("start", today+timedelta(days = r.wd))
					globalRef = (today+timedelta(days = r.wd)).year
				
				self.timeItemDict[twBuffer[tid-1]].definiteRange = "toDel"
	
			elif t=="EL" or t=="EL1":
				if not isinstance(twBuffer[tid-1], int):
					continue
	
				if self.timeItemDict[twBuffer[tid-1]].definiteRange == 1:
					self.timeItemDict[twBuffer[tid-1]].definiteRange = "EL"
				r = self.timeItemDict[twBuffer[tid-1]]
				if r.definiteRange == 0:
					if r.y == None:
						r.y = globalRef or today.year
					if r.d == None and r.m == None:
						#print "END", date(r.y, 12, 31) 
						self.addRangeItem("end", date(r.y, 12, 31))
					elif r.d == None:
						#print "END", date(r.y, r.m, monthDayTable[r.m])
						self.addRangeItem("end", date(r.y, r.m, monthDayTable[r.m]))
					else:
						#print "END", date(r.y, r.m, r.d)
						self.addRangeItem("end", date(r.y, r.m, r.d))
				elif r.definiteRange != "toDel":
					if t == "EL1":
						#print "END", today-timedelta(days = r.wd)
						self.addRangeItem("end", today-timedelta(days = r.wd))
					else:
						#
						#print "START", today-timedelta(days = r.wd)
						self.addRangeItem("start", today-timedelta(days = r.wd))
						#
						#print "END", today+timedelta(days = r.wd)
						self.addRangeItem("end", today+timedelta(days = r.wd))
	
	
				self.timeItemDict[twBuffer[tid-1]].definiteRange = "toDel"
			elif t == "SR":
				if not isinstance(twBuffer[tid+1], int):
					continue
	
				if self.timeItemDict[twBuffer[tid+1]].definiteRange == 1:
					self.timeItemDict[twBuffer[tid+1]].definiteRange = "SR"
				r = self.timeItemDict[twBuffer[tid+1]]
	
				if r.definiteRange == 0:
					if r.y == None:
						r.y = today.year
					if r.d == None and r.m == None:
						#print "START", date(r.y, 1, 1)
						self.addRangeItem("start", date(r.y, 1, 1))
					elif r.d == None:
						#print "START", date(r.y, r.m, 1)
						self.addRangeItem("start", date(r.y, r.m, 1))
					else:
						#print "START", date(r.y, r.m, r.d)
						self.addRangeItem("start", date(r.y, r.m, r.d))
					globalRef = r.y
				elif r.definiteRange != "toDel":
					#print today+timedelta(days = r.wd)
					self.addRangeItem("start", today+timedelta(days = r.wd))
					globalRef = (today+timedelta(days = r.wd)).year
				self.timeItemDict[twBuffer[tid+1]].definiteRange = "toDel"
			elif t == "ER":
				if not isinstance(twBuffer[tid+1], int):
					continue
				###今天到10月31號 no starting cue for 今天 so check twBuffer[tid-1]
				if isinstance(twBuffer[tid-1], int) and self.timeItemDict[twBuffer[tid-1]].definiteRange == 0:
					r = self.timeItemDict[twBuffer[tid-1]]
	
					if r.y == None:
						r.y = today.year
					if r.d == None and r.m == None:
						#print "START", date(r.y, 1, 1)
						self.addRangeItem("start", date(r.y, 1, 1))
					elif r.d == None:
						#print "START", date(r.y, r.m, 1)
						self.addRangeItem("start", date(r.y, r.m, 1))
					else:
						#print "START", date(r.y, r.m, r.d)
						self.addRangeItem("start", date(r.y, r.m, r.d))
					globalRef = r.y
					self.timeItemDict[twBuffer[tid-1]].definiteRange = "toDel"
		
				###
				if self.timeItemDict[twBuffer[tid+1]].definiteRange == 1:
					self.timeItemDict[twBuffer[tid+1]].definiteRange = "ER"
				r = self.timeItemDict[twBuffer[tid+1]]
				if r.definiteRange == 0:
					if r.y == None:
						r.y = globalRef or today.year
					if r.d == None and r.m == None:
						#print "END", date(r.y, 12, 31)
						self.addRangeItem("end", date(r.y, 12, 31))
					elif r.d == None:
						#print "END", date(r.y, r.m, monthDayTable[r.m])
						self.addRangeItem("end", date(r.y, r.m, monthDayTable[r.m]))
					else:
						#print "END", date(r.y, r.m, r.d)
						self.addRangeItem("end", date(r.y, r.m, r.d))
				elif r.definiteRange != "toDel":
					#print "END", today+timedelta(days = r.wd)
					self.addRangeItem("end", today+timedelta(days = r.wd))
				self.timeItemDict[twBuffer[tid+1]].definiteRange = "toDel"
	
	def addRangeItem(self, item, value):
		if item == "start" and self.rangeStart[-1] == None:
			self.rangeStart[-1] = value
		elif item == "start" and self.rangeStart[-1]!=None:
			self.rangeStart.append(None) #create new one
			self.rangeEnd.append(None)
			self.rangeStart[-1] = value
		elif item == "end" and self.rangeEnd[-1] == None :
			self.rangeEnd[-1] = value
		elif item == "end" and self.rangeEnd[-1] != None:
			self.rangeStart.append(None) #create new one
			self.rangeEnd.append(None)
			self.rangeEnd[-1] = value
	
	def clear(self):
		
		self.temporalId = 1
		self.twBuffer = ["x" for q in query]
		self.timeItemDict = {}
		self.occupied = set()
		self.rangeStart = [None]
		self.rangeEnd = [None]
	
	def parse(self, query):
		self.clear()
		self.parseTime(query)
		self.parseDate(query)
		with open("timeRefBuf.txt", "w") as fo:
			fo.write(query.encode("utf-8"))
		tmpWSeq = [query[m] if self.twBuffer[m] =="x" else str(self.twBuffer[m]) for m in range(len(self.twBuffer))]
		wSeq = "".join(tmpWSeq)
		self.findRange(wSeq, self.twBuffer)
	
	def printDate(self):
		for k in self.timeItemDict.keys():
			if self.timeItemDict[k].definiteRange != 0:# 1 or symbol
				del self.timeItemDict[k]
		for c in set(self.twBuffer):
			if isinstance(c, int) and (c in self.timeItemDict):
				print "%s %s-%s-%s"%(self.timeItemDict[c].pos, (self.timeItemDict[c].y or "XXXX"), (self.timeItemDict[c].m or "XX"), (self.timeItemDict[c].d or "XX"))
				
	def printRange(self):
		
		for s, e in zip(self.rangeStart, self.rangeEnd):
			if s != None and e != None:
				print "START %s END %s"%(s,e)
			elif s!= None and e == None:
				print "START %s"%s
			elif s == None and e!= None:
				print "END %s"%e
			
if __name__=="__main__":
	query = raw_input()
	TD1 = temporalDetect(0)
	
	while query!="exit":
		if query == "debug":
			query = open("timeRefBuf.txt", "r").read()
			print query
		query = query.decode("utf-8")
		TD1.parse(query)
		TD1.printDate()
		TD1.printRange()
		
		query = raw_input()
