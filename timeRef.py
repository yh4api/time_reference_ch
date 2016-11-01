#-*- coding:utf-8 -*- 
#this file resolve time reference with input in only traditional chinese 
import re
from datetime import date
from datetime import timedelta
#digit
"""
assume all are roman digits
{0,1,2,3,4,5,6,7,8,9}

一二三四五六七八九十
百千萬

"""

#Date Specific
"""
秒
分
時
小時 點 點鐘

年 月 日/號

上/下{1,2}  + 週/星期/禮拜 + 1~6 日/天
上/下{1,2} + 個月 

清晨 早上 上午 中午 下午 傍晚 晚上 晚間 凌晨

大前/前/今/明/後/大後 + 年/天
去年/昨天
本月
"""
#Date Range
"""
秒 分 小時 天 週/星期 個月 年 世紀

之前 之後 以前 以後 
前 後 起
之內 以內 內
從__到__(間)

"""
monthDayTable = [0, 31,28,31,30,31,30,31,31,30,31,30,31]
difference = {u"大前":-3, u"前":-2, u"明":1, u"後":2, u"大後":3, u"上上":-2,u"上":-1,u"下":1, u"下下":2, u"上個":-1, u"下個":1, u"上上個":-2, u"下下個":-2, u"去":-1}
temporalType = "None" #0: none 1:specific 2:range
dateStart = {}
dateEnd = {}
regTime1 = u"(\d{1,2}(點|時)\d{1,2}分(\d{1,2}秒)?)"
compTime1 = re.compile(regTime1)
regTime2 = u"(\d{1,2}(點|時)(整|半))"
compTime2 = re.compile(regTime2)

regMiddleRange = u"(清晨|早上|上午|中午|下午|傍晚|晚上|晚間|凌晨)\d{1,2}(點|時)"
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
		self.typ = "DATE" #date or range
		self.Id = tid
class sentenceTemporal:
	def __init__(self):
		pass


#====== 年自成一格 
regDate1 = u"(\d{1,2})(月)(\d{1,2})(日|號)" #M = g(1) D = g(3) sure
regDate5 = u"(本|這個|上個|下個|上上個|下下個)(月)(\d{1,2})(日|號)" #M = P+difference[g(1)], D = g(3) sure
regDate7 = u"(本|這個)月" #M = 1
regDate8 = u"(上|下){1,2}個月"#M = P+difference[g(1)]
regDate2 = u"(\d{1,2})(月)"#M = g(1)
#======

regDate4 = u"(大前|前|今|明|後|大後)(年|天)" #if g(2) == "年": Y = P+difference[g(1)] else:D=P+difference[g(1)] #date is sure
regDate6 = u"昨天" #D = P-1 sure
regDate3 = u"(\d{1,}|去)(年)"#if g(2) == "去": Y = P-1 else: Y = P 

regDate15 = u"(\d{1,}|去|大前|前|今|明|後|大後)年.?(\d{1,2})月((\d{1,2})(日|號))?" #specific

regDate9 = u"(\d+)(個月|週|星期|個禮拜|個星期|天|世紀)" ##一個月 一天 一週 只能為range必須要有搭配詞

regDate11 = u"(上|下|上上|下下|這|本|這個)?(週|周|星期|禮拜)([1-6])" #WD = g(3) W = C+difference[g(1)] date is sure
regDate12 = u"(上|下|上上|下下|這|本|這個)?(週|周|星期|禮拜)(天|日)" #WD = g(3) W = C+difference[g(1)] date is sure
regDate10 = u"(上|下|上上|下下|這|本|這個)(週|周|星期|禮拜)" #WD = 1 W = C+difference[g(1)]

regDigitDate1 = "(\d{4})-(\d{1,2})-(\d{1,2})"
regDigitDate2 = "(\d{4})\.(\d{1,2})\.(\d{1,2})"
regDigitDate3 = "(\d{4})/(\d{1,2})/(\d{1,2})"
regDigitDate4 = "(\d{4})(\d{2})(\d{2})"



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

regRange1 = u"\d(之前|以前|前|之後|以後|後|起|開始|之內|以內|內|來|以來|以上|以下)"
# 開始 截止 為止 is stronger than 前 之後 以後
regRange2 = u"(從|自|到|至)\d"
compRange1 = re.compile(regRange1)
compRange2 = re.compile(regRange2)

temporalId = 1
twBuffer = []
timeItemDict = {}
occupied = set()
today = date.today()
def printGroup(group, y, debug = 0):
	if debug:
		print "Group%d  %02d-%02d: %s"%(group, y.start(), y.end(), y.group(0))
	

def fillBuffer(y, filler=None, caseNumber = None):
	global temporalId
	if filler == None:
		thisOccupied = set(j for j in range(y.start(), y.end()))
		if thisOccupied&occupied != set():
			print "overlapped expression"
		else:
			for j in range(y.start(), y.end()):
			
				twBuffer[j] = temporalId
				occupied.add(j)	

		tItem = temporalItem(temporalId)
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
			if y.group(2) == u"個月":
				#tItem.m = y.group(1)
				tItem.wd = 30*int(y.group(1))
			elif y.group(2) in [u"週", u"周", u"星期", u"個禮拜", u"個星期"]:
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

		timeItemDict[temporalId] = tItem
		temporalId += 1
	else:
		for j in range(y.start(1), y.end(1)):
			twBuffer[j] = filler

def Combined(l, r):
	pass

query = raw_input()
while query!="exit":
	if query == "debug":
		query = open("timeRefBuf.txt", "r").read()
		print query
	temporalId = 1
	query = query.decode("utf-8")
	twBuffer = ["x" for q in query]
	occupied = set()
	timeItemDict = {}
	for regi in [compTime1, compTime2, compMiddle]:
		for x in regi.finditer(query):
			print "%03d-%03d: %s"%(x.start(), x.end(), x.group(0))
			fillBuffer(x) 
	
	#group1: if or elif
	if compDate15.search(query) != None:
		for x in compDate15.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 15)
	if compDate1.search(query) != None:
		for x in compDate1.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 1)
	if compDate5.search(query) != None:
		for x in compDate5.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 5)
	if compDate7.search(query) != None:
		for x in compDate7.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 7)
	if compDate8.search(query) != None:
		for x in compDate8.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 8)
	if compDate2.search(query) != None:
		for x in compDate2.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 2)
	"""
	elif compDate3.search(query) != None:
		for x in compDate2.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 3)
	elif compDate4.search(query) != None:
		for x in compDate2.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 4)
	elif compDate6.search(query) != None:
		for x in compDate2.finditer(query):
			printGroup(1, x)
			fillBuffer(x, caseNumber = 6)
	"""

	
	#group2
	for i in [3, 4, 6]:
		regi = eval("compDate"+str(i))
		for x in regi.finditer(query):
			printGroup(2, x)
			fillBuffer(x, caseNumber = i)
	
	#group3
	rangeNeeded = []
	for x in compDate9.finditer(query):
		printGroup(3, x)
		fillBuffer(x, caseNumber = 9)
	
	#group4 switch to week# and weekday
	if compDate12.search(query) != None:
		for x in compDate12.finditer(query):
			printGroup(4, x)
			fillBuffer(x, caseNumber = 12)
	if compDate11.search(query) != None:
		for x in compDate11.finditer(query):
			printGroup(4, x)
			fillBuffer(x, caseNumber = 11)
	if compDate10.search(query) != None:
		for x in compDate10.finditer(query):
			printGroup(4, x)
			fillBuffer(x, caseNumber = 10)

	#group5 georgian date detection
	if compDate16.search(query) != None:
		for x in compDate16.finditer(query):
			printGroup(5, x)
			fillBuffer(x, caseNumber = 16)
	if compDate17.search(query) != None:
		for x in compDate17.finditer(query):
			printGroup(5, x)
			fillBuffer(x, caseNumber = 17)

	if compDate18.search(query) != None:
		for x in compDate18.finditer(query):
			printGroup(5, x)
			fillBuffer(x, caseNumber = 18)
	if compDate19.search(query) != None:
		for x in compDate19.finditer(query):
			printGroup(5, x)
			fillBuffer(x, caseNumber = 19)

	### Range define block
	with open("timeRefBuf.txt", "w") as fo:
		fo.write(query.encode("utf-8"))
	#print twBuffer

	tmpWSeq = [query[m] if twBuffer[m] =="x" else str(twBuffer[m]) for m in range(len(twBuffer))]
	wSeq = "".join(tmpWSeq)
	
	for x in compRange1.finditer(wSeq):
		if x.group(1) in [u"之後", u"以後", u"起", u"開始", u"後"]:
			fillBuffer(x, filler="SL")
		else:
			if x.group(1) in [u"之前", u"前", u"以前"]:
				fillBuffer(x, filler="EL1")
			else:
				fillBuffer(x, filler="EL")
			# 之前|以前|前|之內|以內|內  2年內的報紙 -2y but 2年內做好 +2y
			# range + 之前 --> -range???
	for x in compRange2.finditer(wSeq):
		if x.group(1) in [u"從", u"自"]:
			fillBuffer(x, filler="SR")
		else:
			fillBuffer(x, filler="ER")#到|至
			# 今天到10月10號, starting point可以省略起始詞
	
	#print twBuffer
	globalRef = None 
	for tid, t in enumerate(twBuffer):
		print tid, t
		if t == "SL":
			if not isinstance(twBuffer[tid-1], int):
				continue
			if timeItemDict[twBuffer[tid-1]].definiteRange == 1:
				timeItemDict[twBuffer[tid-1]].definiteRange = "SL"
			r = timeItemDict[twBuffer[tid-1]]
			if r.definiteRange == 0:
				if r.y == None:
					r.y = today.year
				if r.d == None and r.m == None:
					print "START", date(r.y, 1, 1) 
				elif r.d == None:
					print "START", date(r.y, r.m, 1)
				else:
					print "START", date(r.y, r.m, r.d)
				globalRef = r.y
			#else:
			elif r.definiteRange!="toDel": #situation like 從 2011年 開始, 2 cue terms share same temporal slot
				print "START", today+timedelta(days = r.wd)
				globalRef = (today+timedelta(days = r.wd)).year
			
			timeItemDict[twBuffer[tid-1]].definiteRange = "toDel"

		elif t=="EL" or t=="EL1":
			if not isinstance(twBuffer[tid-1], int):
				continue

			if timeItemDict[twBuffer[tid-1]].definiteRange == 1:
				timeItemDict[twBuffer[tid-1]].definiteRange = "EL"
			r = timeItemDict[twBuffer[tid-1]]
			if r.definiteRange == 0:
				"""
				# 100年前 => 西元100年 or timeRange 100年 前
				if r.y != None and r.m == None:
					if r.y < 50 :
						print "END", date(today.year-r.y, 12, 31)
				"""
				if r.y == None:
					r.y = globalRef or today.year
				if r.d == None and r.m == None:
					print "END", date(r.y, 12, 31) 
				elif r.d == None:
					print "END", date(r.y, r.m, monthDayTable[r.m])
				else:
					print "END", date(r.y, r.m, r.d)
			elif r.definiteRange != "toDel":
				if t == "EL1":
					print "END", today-timedelta(days = r.wd)
				else:
					#
					print "START", today-timedelta(days = r.wd)
					#
					print "END", today+timedelta(days = r.wd)


			timeItemDict[twBuffer[tid-1]].definiteRange = "toDel"
		elif t == "SR":
			if not isinstance(twBuffer[tid+1], int):
				continue

			if timeItemDict[twBuffer[tid+1]].definiteRange == 1:
				timeItemDict[twBuffer[tid+1]].definiteRange = "SR"
			r = timeItemDict[twBuffer[tid+1]]

			if r.definiteRange == 0:
				if r.y == None:
					r.y = today.year
				if r.d == None and r.m == None:
					print "START", date(r.y, 1, 1)
				elif r.d == None:
					print "START", date(r.y, r.m, 1)
				else:
					print "START", date(r.y, r.m, r.d)
				globalRef = r.y
			elif r.definiteRange != "toDel":
				print today+timedelta(days = r.wd)
				globalRef = (today+timedelta(days = r.wd)).year
			timeItemDict[twBuffer[tid+1]].definiteRange = "toDel"
		elif t == "ER":

			if not isinstance(twBuffer[tid+1], int):
				continue
			###今天到10月31號 no starting cue for 今天 so check twBuffer[tid-1]
			if isinstance(twBuffer[tid-1], int) and timeItemDict[twBuffer[tid-1]].definiteRange == 0:
				r = timeItemDict[twBuffer[tid-1]]

				if r.y == None:
					r.y = today.year
				if r.d == None and r.m == None:
					print "START", date(r.y, 1, 1)
				elif r.d == None:
					print "START", date(r.y, r.m, 1)
				else:
					print "START", date(r.y, r.m, r.d)
				globalRef = r.y
				timeItemDict[twBuffer[tid-1]].definiteRange = "toDel"
	
			###
			if timeItemDict[twBuffer[tid+1]].definiteRange == 1:
				timeItemDict[twBuffer[tid+1]].definiteRange = "ER"
			r = timeItemDict[twBuffer[tid+1]]
			if r.definiteRange == 0:
				if r.y == None:
					r.y = globalRef or today.year
				if r.d == None and r.m == None:
					print "END", date(r.y, 12, 31)
				elif r.d == None:
					print "END", date(r.y, r.m, monthDayTable[r.m])
				else:
					print "END", date(r.y, r.m, r.d)
			elif r.definiteRange != "toDel":
				print "END", today+timedelta(days = r.wd)
			timeItemDict[twBuffer[tid+1]].definiteRange = "toDel"
	###
	#print twBuffer
	#for k, v in timeItemDict.iteritems():
	#	print k, v.y, v.m, v.d, v.w, v.wd
	for k in timeItemDict.keys():
		if timeItemDict[k].definiteRange != 0:# 1 or symbol
			del timeItemDict[k]
	for c in set(twBuffer):
		if isinstance(c, int) and (c in timeItemDict):
			print timeItemDict[c].pos, (timeItemDict[c].y or "XXXX"),"-", (timeItemDict[c].m or "XX") ,"-", (timeItemDict[c].d or "XX")
			
			
	#if specialterms have no following prefix, they are no special.
	query = raw_input()
#print date.today()
