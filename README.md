# time_reference_ch
It recognizes and normalize time expression in traditional/simplfied Chinese<br>
issue 1: it handles time expression in only digits, no characters(一二三etc)<br>
issue 2: duration needs more study<br>
issue 3: it assumes year is in Gregorian calendar system.<br>
usage:<br>
```
python timeRefCHM.py<enter>
我3天后回来，下周1的会议准备如何了？(in simplified chinese)<enter>
```
output:
```
07-10 2016-11-7
START 2016-11-04
```
Edit line 512: 
```
temporalDetect(0) => turn off detailed info
temporalDetect(1) => turn on detailed info
```
input "exit" to exit or "debug" to see the result of last sentence<br>

Older version
```
python timeRef.py <enter>
我2天後要出發去韓國(traditional chinese)
```
output
```
START 2016-11-03
```
python timeRefCN.py for simplfied chinese
