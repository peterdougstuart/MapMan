# coding: utf-8

loadings = {}
levels = {}
delays = {}
x_hides = {}
level_messages = {}

MAX_ROWS = 12
MAX_COLUMNS = 17

START_LEVEL = 1

def next():
	current = this()
	if current is None:
		return 1
	else:
		return this()+1

def this():
	if len(levels) == 0:
		return None
	else:
		return max(levels.keys())
		
def verify_levels(levels, loadings):
	
	for number in levels:
		
		level = levels[number]
		
		rows = level.split('\n')
		
		if len(rows) > MAX_ROWS:
			print level
			raise Exception('Too many rows ({0}) in level {1}'.format(len(rows), number))
			
		for row in rows:
			
			if len(row) > MAX_COLUMNS:
				print level
				raise Exception('Too many columns ({0}) in level {1}'.format(len(row), number))
		
		print 'level {0} ok'.format(number)
		
	print 'all ok'

check_points = [15, 30, 40, 50, 60, 70, 80, 90]

DEFAULT_X_HIDES = 25
DEFAULT_DELAY = 0.05

levels[next()] = '''
 wccccccc
        c
 cccccccc
 c
 cccccccb
'''

level_messages[this()] = 'tilt to move'

loadings[this()] = '''
 zyxwvuts
        r
 jklmnopq
 i
 hgfedcba
'''

levels[next()] = '''
-------------b
-------------c
-p--p--p--p--c
-c--c--c--c--c
-c--c--c--c--c
-c--c--c--c--c
wccccccccccccc
'''

loadings[this()] = '''
-------------a
-------------b
-w--t--q--n--c
-v--s--p--m--d
-u--r--o--l--e
-t--q--n--k--f
tsrqponmlkjihg
'''

levels[next()] = '''
-bc----------
--cc---------
---cc--------
----ccccccccp
-----cc------
------cc-----
pcccccccc----
--------cc---
---------cs--
'''

loadings[this()] = '''
-ab----------
--cd---------
---ef--------
----ghijklmno
-----ij------
------kl-----
tsrqponmn----
--------op---
---------qr--
'''

levels[next()] = '''
p--ccccccccccc--
p--c---------c--
p--c-ccccccc-c--
p--c-c-----c-c--
uccc-c--bccc-c--
p--c-c-------c--
p--c-ccccccccc--
p--c------------
p--cccccccccccce
'''

loadings[this()] = '''
*--kkjjiihhggf--
*--l---------f--
*--l-6655443-e--
*--m-7-----3-e--
wvvm-7--1122-d--
*--n-8-------d--
*--n-899aabbcc--
*--o------------
*--oppqqrrssttuu
'''

levels[next()] = '''
 ccz Wc
 c c  z
 z zczc
 c
 rzcrccb
'''

loadings[this()] = '''
 klm ut
 j n  s
 i opqr
 h
 gfedcba
'''

levels[next()] = '''
---------cccc--
---------c--c--
-----ccccc--ccE
-pcccc---------
-----cr-----b--
------cr----c--
-------ccc3cc--
'''

loadings[this()] = '''
---------opqr--
---------n--s--
-----ijklm--tuv
-12345---------
-----67-----h--
------89----g--
-------abcdef--
'''

levels[next()] = '''
-----------
bccccccchii
----------i
iihcccccuii
i----------
iiuccccchii
----------i
wcccccccuii
-----------
'''

loadings[this()] = '''
-----------
aabbccddeef
----------f
lkkjjiihhgg
l----------
mmnnooppqqr
----------r
xwwvvuuttss
-----------
'''

levels[next()] = '''
--iiucncccc
--i-------c
--i-------c
--i-------c
--iiihc9ccc
------c----
bcccccc----
'''

loadings[this()] = '''
--qrstutsrq
--p-------p
--o-------o
--n-------n
--mlkjijklm
------h----
abcdefg----
'''

levels[next()] = '''
  pp   rr
 ppppcrrrE
 pppp rrrr
  pp   rr
  c
  c
  c
  ccccyyyb
'''

loadings[this()] = '''
  oo   qr
 nnnnopqrs
 mmmm pqrs
  ll   qr
  k
  j
  i
  hgfedcba
'''

levels[next()] = '''
pccccccccccccccp
-------cc-------
-----cccccc-----
-----c----c-----
----cc----cc----
----c------c----
---cc------xc---
--wc--------cb--
'''

x_hides[this()] = 17

loadings[this()] = '''
utsrqponnopqrstu
-------mm-------
-----nmlkji-----
-----o----h-----
----qp----gf----
----r------e----
---ts------dc---
--vu--------ba--
'''

levels[next()] = '''
bcccccccc---
--c-----c---
--c-----ccc-
cyccccv---r-
c-----c--cc-
c-----c--c--
ccccccccccce
'''

loadings[this()] = '''
abcdefghi---
--d-----j---
--e-----kll-
ggfghij---m-
h-----j--nn-
h-----l--o--
iijklmmnopqr
''' 

levels[next()] = '''
      cccc
     8c--cc
bccccc----ccccE
     c-----c
     rc--rcc
      cccc
'''

loadings[this()] = '''
      ijkl
     gh--mn
abcdef----opqrs
     g-----p
     hi--nop
      jklm
'''

levels[next()] = '''
ccc ccc ccc ccc
c c c c c c c c
r c c c c c c c
c c c c c c c c
c c c c c c c c
b ccc ccc ccc S
'''

loadings[this()] = '''
fgh fgh fgh fgh
e e e e e e e e
d d d d d d d d
c c c c c c c c
b b b b b b b b
a fgh fgh fgh a
'''

delays[this()] = 0.1

levels[next()] = '''
-bc----------
--hi---------
---ii--------
----iiccccccp
-----ii------
------ii-----
pccccccii----
--------iu---
---------cs--
'''

loadings[this()] = '''
-ab----------
--cd---------
---ef--------
----ghijklmno
-----ij------
------kl-----
tsrqponmn----
--------op---
---------qr--
'''

levels[next()] = '''
ccc ccc ccc
c c c c c c
x c c c c c
c c c c c c
c c c c c c
b ccc ccc S
'''

delays[this()] = 0.1

loadings[this()] = '''
fgh fgh fgh
e e e e e e
d d d d d d
c c c c c c
b b b b b b
a fgh fgh a
'''

levels[next()] = '''
-br----------
--cc---------
---cc--------
----ccccccccp
-----cc------
------cc-----
lcccccccc----
--------cc---
---------cs--
'''

loadings[this()] = '''
-ab----------
--cd---------
---ef--------
----ghijklmno
-----ij------
------kl-----
tsrqponmn----
--------op---
---------qr--
'''

levels[next()] = '''
---ccccccccccc--
---c---------c--
---c-ccccccc-c--
---c-c-----c-c--
cccc-c--bccr-c--
c--c-c-------c--
c--c-ccccccccc--
c--c------------
l--cccccccccccce
'''

loadings[this()] = '''
---kkjjiihhggf--
---l---------f--
---l-6655443-e--
---m-7-----3-e--
***m-7--1122-d--
*--n-8-------d--
*--n-899aabbcc--
*--o------------
*--oppqqrrssttuu
'''

levels[next()] = '''
ccccccchccb
--i--------
ccccccccccc
------i----
ccccccccccc
i----------
cccccccucce
'''

loadings[this()] = '''
feeddccbbaa
--f--------
ggfgghhiijj
------i----
llkkjjijjkk
m----------
mnnooppqqrr
'''

levels[next()] = '''
---ccccccccccc--
--cc---------c--
--c---cccccccc--
--c---c---------
--rce-rcccccccb-
--c---c---------
--c---cccccccc--
--cc---------c--
---ccccccccccc--
'''

loadings[this()] = '''
---eeddcccbbaa--
--ff---------9--
--g---56677889--
--g---5---------
--hhi-44332211b-
--g---5---------
--g---56677889--
--ff---------9--
---eeddcccbbaa--
'''

levels[next()] = '''
----------------
----n------b----
----c------c----
----r------y----
----y------r----
----c------c----
----r------y----
----yccryccr----
----------------
'''

loadings[this()] = '''
----------------
----k------1----
----j------2----
----i------3----
----h------4----
----g------5----
----f------6----
----edcba987----
----------------
'''

levels[next()] = '''
----------------
--bcccccccccc---
------------c---
-----dye----c---
------c-----c---
------c-----c---
------ccccccc---
----------------
----------------
'''

loadings[this()] = '''
----------------
--123456789ab---
------------c---
-----qpq----d---
------o-----e---
------n-----f---
------mlkjihg---
----------------
----------------
'''

levels[next()] = '''
----------------
--bcccccccccc---
------------c---
-----dre----c---
------c-----c---
------c-----c---
------ccccccc---
----------------
----------------
'''

loadings[this()] = '''
----------------
--123456789ab---
------------c---
-----qpq----d---
------o-----e---
------n-----f---
------mlkjihg---
----------------
----------------
'''

levels[next()] = '''
-ddddddddddd-
bccccccccccce
-ddddddddddd-
'''

loadings[this()] = '''
-efghijklmno-
abcdefghijklm
-efghijklmno-
'''


levels[next()] = '''
-ddddddddddd-
bcycycycycyce
-ddddddddddd-
'''

loadings[this()] = '''
-efghijklmno-
abcdefghijklm
-efghijklmno-
'''

levels[next()] = '''
-ddddddddddd-
brycycycycyce
-ddddddddddd-
'''

loadings[this()] = '''
-efghijklmno-
abcdefghijklm
-efghijklmno-
'''

levels[next()] = '''
bchiiiiiiiid
----------i-
--n-------i-
--i----diiii
--i-----i--d
-diiiiiii---
--------d---
'''

loadings[this()] = '''
aabbccddeeff
----------f-
--o-------g-
--o----iihhg
--n-----j--h
-nmmllkkj---
--------k---
'''

levels[next()] = '''
    cccd
  ccc cp
  c   cd
bcc   cp
      cd
      cp
  wccccd
   dpdp
'''

loadings[this()] = '''
    hiju
  efg kl
  d   lv
abc   mn
      nw
      op
  tsrqpx
   zryp
'''

levels[next()] = '''
-wccuci-------
--!!--i-------
-iiiiiii!-----
--i--!--------
-iiiiiicchcccb
'''

loadings[this()] = '''
-dcba98-------
--cb--8-------
-dcba9876-----
--c--9--------
-dcba987654321
'''

levels[next()] = '''
 Wrrrrr
      r
 rccccr
 r
 rrrrrb
'''

loadings[this()] = '''
 jihgfe
      d
 cbaabc
 d
 efghuj
'''

levels[next()] = '''
 Wccctccc
    dmd ccttl
 cccccccc
 c
 cccccccb
'''

loadings[this()] = '''
 qponmlkj
    vwv irstu
 abcdefgh
 9
 87654321
'''

levels[next()] = '''
----------------
----------------
---yyyyyyyy-----
--dy      c-----
-wly      ccccb-
--dy      c-----
---yyyyyyyy-----
----------------
----------------
'''

loadings[this()] = '''
----------------
----------------
---tsrqppon-----
--ef      m-----
-adc      54321-
--ef      m-----
---tsrqppon-----
----------------
----------------
'''

levels[next()] = '''
ccrccrccrccE
c
crcrcrccrcrc
-----------c
bcrcrcrcrccc
'''

loadings[this()] = '''
312312312345
2
132132132132
-----------1
123123123123
'''

levels[next()] = '''
 Wyyyyyyy
        y
 yyyyyyyy
 y
 yyyyyyyb
'''

loadings[this()] = '''
 qdpcobna
        m
 i6j7k8l9
 5
 h4g3f2e1
'''

levels[next()] = '''
 N
 t      
 t    m
 t    c
 t    c
 ccccccb
'''

loadings[this()] = '''
 k
 j      
 i    n
 h    m
 g    l
 fedcba0
'''

levels[next()] = '''
 Wtcccc        l
      c    d   y
      c----m   y
      cccccccccm
        tt
        tt
        c
     byyy
'''

loadings[this()] = '''
 fedcba        f
      9    a   e
      8----9   d
      7656789abc
        41
        32
        4
     8765
'''

levels[next()] = '''
bcpccpccpccp----
--c--c--c--c----
-cvccvccvccvc---
--c--c--c--c----
--pccpccpccpcp--
-----c--c--c----
---ccvccvccvccv-
-----c--c--c--c-
----cdccdccdccpe
'''

loadings[this()] = '''
123456789abc----
--p--p--o--p----
-onmlkjihgfed---
--q--q--q--q----
--123456789abc--
-----r--r--r----
---onmlkjihgfed-
-----s--s--s--s-
----123456789abc
'''

levels[next()] = '''
bcpccpccpccp----
--c--c--c--c----
-cyccyccyccyc---
--c--c--c--c----
--pccpccpccpcp--
-----c--c--c----
---ccrccrccrccr-
-----c--c--c--c-
----cdccdccdccre
'''

loadings[this()] = '''
123456789abc----
--p--p--o--p----
-onmlkjihgfed---
--q--q--q--q----
--123456789abc--
-----r--r--r----
---onmlkjihgfed-
-----s--s--s--s-
----123456789abc
'''

levels[next()] = '''
----------------
--bccccccccccx--
--c----------p--
--c----------p--
--c----------p--
--c----------p--
--c----------p--
--s----------d--
----------------
'''

loadings[this()] = '''
----------------
--189abcdefghi--
--2----------j--
--3----------k--
--4----------l--
--5----------m--
--6----------n--
--7----------o--
----------------
'''

levels[next()] = '''
-----clc--------
----cc-c--------
---cc--c--------
--tc---t--------
-bc----mccccce--
--tp---t--------
---pp--p--------
----pp-p--------
-----ppp--------
'''

loadings[this()] = '''
-----9ab--------
----78-c--------
---56--d--------
--34---e--------
-12----fghijkl--
--34---e--------
---56--d--------
----78-c--------
-----9ab--------
'''

levels[next()] = '''
----------------
---ccccccccc----
---h-------c----
---b-------c----
-----------c----
-------ccccc----
-------ciiii----
-------!!!i!----
-------siiii----
'''

loadings[this()] = '''
----------------
---3456789ab----
---2-------c----
---1-------d----
-----------e----
-------jihgf----
-------kjihg----
-------lkjih----
-------mlkji----
'''


levels[next()] = '''
n---------------
c-bccccccccccc--
ccc----------c--
---cccccccc--c--
-ppc------c--ccc
pp------ccc----c
p--cccccc------c
p--c--------cccc
---cccccccccc---
'''

loadings[this()] = '''
6---------------
5-1789abcdefgh--
432----------h--
---wwvvvuuu--i--
-xxw------t--ijj
yx------stt----k
y--qrrrss------k
y--q--------mmll
---qpppooonnn---
'''

levels[next()] = '''
----------------
--wcyccc--------
-------c--------
-------ccccccc--
-------------c--
-------------c--
--bctttccccccc--
----------------
----------------
'''

loadings[this()] = '''
----------------
--srqpon--------
-------m--------
-------lkjihgf--
-------------e--
-------------d--
--123456789abc--
----------------
----------------
'''

levels[next()] = '''
--n-dccccccccc--
t-c---c------c--
tcccccc--d---c--
t--------c---c--
t--------ccccccd
c--------c------
c------dcccccccc
c--------------c
bccccccccccccccc
'''

loadings[this()] = '''
--8-uttssrrqqp--
5-7---u------p--
456wvvu--m---o--
4--------m---o--s
3--------lmmnnoo
3--------l------
2------mllkkjjii
2--------------h
1aabbccddeeffggh
'''


levels[next()] = '''
ppp-----ppp-----
pbpcccccpppccc--
ppp-----ppp--c--
-------------c--
--ppp----ppp-c--
--pnp----pppcc--
--ppp----ppp----
---c------c-----
---cccccccc-----
'''

loadings[this()] = '''
344-----99a-----
315667788babbc--
225-----99a--c--
-------------d--
--nnn----ggf-d--
--mom----hhfee--
--mlm----ggf----
---l------g-----
---kkjjiihh-----
'''

levels[next()] = '''
ppp-----ppp-----
pbpcccccpdpccc--
ppp-----ppp--c--
-------------c--
--ppp----ppp-c--
--pnp----pdpcc--
--ppp----ppp----
---c------c-----
---cccccccc-----
'''

loadings[this()] = '''
344-----99a-----
315667788babbc--
225-----99a--c--
-------------d--
--nnn----ggf-d--
--mom----hhfee--
--mlm----ggf----
---l------g-----
---kkjjiihh-----
'''


levels[next()] = '''
-------n--------
------ccc-------
------cdc-------
----ccyyycc-----
---wcdybydce----
----ccyyycc-----
------cdc-------
------ccc-------
-------s--------
'''

loadings[this()] = '''
-------7--------
------565-------
------484-------
----5432345-----
---768414867----
----5432345-----
------484-------
------565-------
-------7--------
'''

levels[next()] = '''
-------n--------
--iiii!ui!iii---
--i!iiiiiiiii---
--iii!iiiiii!---
--iiiii!iiiii---
--iiiiiiiiiii---
-------h--------
-------ccccccb--
----------------
'''

loadings[this()] = '''
-------e--------
--ihgefdefghi---
--hgefdcdefgh---
--gfedcbcdefg---
--fedcbabcdef---
--edcba9abcde---
-------8--------
-------7654321--
----------------
'''

levels[next()] = '''
----------------
----------------
--ppppnpppp-----
--ppppppppp-----
--wppppppppxccb-
--ppppppppp-----
--ppppspppp-----
----------------
----------------
'''

x_hides[this()] = 50

loadings[this()] = '''
----------------
----------------
--utsrqppon-----
--efghijklm-----
--dcba987654321-
--efghijklm-----
--utsrqppon-----
----------------
----------------
'''

levels[next()] = '''
----------------
----------------
--dpppnpppd-----
--ppppppppp-----
--wppdpdpppxccb-
--ppppppppp-----
--doppspppd-----
----------------
----------------
'''

x_hides[this()] = 50

loadings[this()] = '''
----------------
----------------
--utsrqppon-----
--efghijklm-----
--dcba987654321-
--efghijklm-----
--utsrqppon-----
----------------
----------------
'''

levels[next()] = '''
----------------
----------------
-----tiihccpc---
-----i------c---
--wcui------t---
-----!-yccrcc---
-------c--------
-------b--------
----------------
'''

loadings[this()] = '''
----------------
----------------
-----ihgfedcb---
-----j------a---
--nmlk------9---
-----o-345678---
-------2--------
-------1--------
----------------
'''

levels[next()] = '''
----------------
----------------
----------------
-cccccdcccccdcce
bccdcccccdccccc-
----------------
----------------
----------------
----------------
'''

loadings[this()] = '''
----------------
----------------
----------------
-3456789abcdefgh
123456789abcdef-
----------------
----------------
----------------
----------------
'''


levels[next()] = '''
-----------p----
-----pd----yd---
-----y-----y----
-cccccdcccccdcce
bccdcccccdccccc-
--y-----y-------
--yd----pd------
--p-------------
----------------
'''

loadings[this()] = '''
-----------o----
-----lq----ns---
-----k-----m----
-3456789abcdefgh
123456789abcdef-
--i-----l-------
--jp----mr------
--k-------------
----------------
'''

levels[next()] = '''
wu--------------
-cccccccccccccc-
-cccccccccccccc-
-cccccccccccccc-
-!!!c!!!!!!!!!!-
-cccccccccccccc-
-cccccccccccccc-
-cccccccccccccc-
--------------hb
'''

loadings[this()] = '''
dd--------------
-ccbbaa99887766-
-cbbaa998877665-
-bbaa9988776655-
-baa99887766554-
-aa998877665544-
-a9988776655443-
-99887766554433-
-------------21-
'''


levels[next()] = '''
wu--------------
-cccccccccccccc-
-cccccccccccccc-
-!!!!!!!!!c!!!!-
-cccccccccccccc-
-!c!!!!!!!!!!!!-
-cccccccccccccc-
-cccccccccccccc-
--------------hb
'''

loadings[this()] = '''
dd--------------
-ccbbaa99887766-
-cbbaa998877665-
-bbaa9988776655-
-baa99887766554-
-aa998877665544-
-a9988776655443-
-99887766554433-
--------------21
'''

levels[next()] = '''
--ddddddddddddddd
--dccccccccccccxd
wcccdddddcdddddcd
--ddd---dld---dcd
bcccd---ddd---dcd
--dcd---------dcd
--dcdddddddddddcd
--dxccccccccccccd
--ddddddddddddddd
'''

x_hides[this()] = 12

loadings[this()] = '''
--xwvuttssrrqqppo
--ykjjihhggffeedo
mllkvuttthrqqpoin
--yxw---shr---ncn
1122b---ssr---mcm
--c3c---------lbm
--c3cdfgghhiijkbl
--c44566778899aal
--ddeffgghhiijjkk
'''

levels[next()] = '''
--ddddddddddddddd
--dcccccccccccccd
wcccdddddldddddcd
--ddd---drd---dcd
bcrcd---ddd---dcd
--dcd---------dcd
--dcdddddddddddcd
--dcccccccccccccd
--ddddddddddddddd
'''

loadings[this()] = '''
--xwvuttssrrqqppo
--ykjjihhggffeedo
mllkvuttthrqqpoin
--yxw---shr---ncn
1122b---ssr---mcm
--c3c---------lbm
--c3cdfgghhiijkbl
--c44566778899aal
--ddeffgghhiijjkk
'''

levels[next()] = '''
wu--------------
-cccccccccccccc-
-c!!!!!!!!!!!!!-
-cccccccccccccc-
-!!!!!!!!!!c!!!-
-cccccccccccccc-
-!!!!!!!!!c!!!!-
-cccccccccccccc-
--------------hb
'''

loadings[this()] = '''
dd--------------
-ccbbaa99887766-
-cbbaa998877665-
-bbaa9988776655-
-baa99887766554-
-aa998877665544-
-a9988776655443-
-99887766554433-
--------------21
'''

levels[next()] = '''
-----cup------
-----c-p------
-----ccp------
--ppp-y-ddd---
--w-cybyc-e---
--ddd-y-ppp---
-----pcc------
-----p-c------
-----puc------
'''

loadings[this()] = '''
-----ccc------
-----c-c------
-----ccc------
--***-c-***---
--*-*ccc*-*---
--***-c-***---
-----ccc------
-----c-c------
-----ccc------
'''

levels[next()] = '''
 Wcccccd
 dddddcd
 ccccccd
 cdddddd
 cccdcccccb
 ddcdcdd
 ddcccdd
 ddddddd
'''

loadings[this()] = '''
 srqponx
 xxxxxmx
 ghijklx
 fxxxxxx
 edcx654321
 xxbx7xx
 xxa98xx
 xxxxxxx
'''

levels[next()] = '''
 Wccccrcd   ppppm
 d     c    p
 ccccccvccccp
 c
 tcyyyyyytyyyyccb
  c           c
  cccccttcccccc
'''

loadings[this()] = '''
 mkjihgfn   jklmn
 o     e    i
 aabccdeefggh
 9
 8766555444333221
  7           2 
  7666555544433
'''
 
levels[next()] = '''
 Wcccccd
 dddddcd
 ccccccd
 cdddddd
 cccdcccccb
 ddcdrdd
 ddcccdd
 ddddddd
'''

loadings[this()] = '''
 srqponx
 xxxxxmx
 ghijklx
 fxxxxxx
 edcx654321
 xxbxzxx
 xxa98xx
 xxxxxxx
'''

levels[next()] = '''
     d
 hii iiid
 c i i i
 c i i iiid
 c iii   iiii
 c d i      S
 c   iiiiu
 c
 cccccccb
'''

loadings[this()] = '''
     m
 gnn nnnj
 f o o o
 e p p pppj
 d qqq   qqqq
 c h r      l
 b   uuuuk
 a
 87654321
'''

levels[next()] = '''
       N
       t
       t
       t
       t
 mccvccbccrccm
       c
       y
       m
'''

loadings[this()] = '''
       m
       l
       k
       j
       i
hmgedcb1234557
       8
       9
       a
'''

levels[next()] = '''
 Wcccccd
 dddddcd
 ccccccd
 cdddddd
 cccdcccccb
 ddcdvdd
 ddcccdd
 ddddddd
'''

loadings[this()] = '''
 srqponx
 xxxxxmx
 ghijklx
 fxxxxxx
 edcx654321
 xxbxzxx
 xxa98xx
 xxxxxxx
'''

levels[next()] = '''
 Wrrrrr
      r
 rrrrrr
 r
 rrrrrb
'''

loadings[this()] = '''
 jihgfe
      d
 cbaabc
 d
 efghuj
'''

levels[next()] = '''
ccc ccc ccc ccc
c c c c c c c c
r c c c c c c c
x c c c c c c c
c c c c c c c c
b ccc ccc ccc S
'''

x_hides[this()] = 100

loadings[this()] = '''
fgh fgh fgh fgh
e e e e e e e e
d d d d d d d d
c c c c c c c c
b b b b b b b b
a fgh fgh fgh a
'''

delays[this()] = 0.1

levels[next()] = '''
 Wcccccd
 dddddcd
 ccccccd
 cdddddd
 cccdrccccb
 ddcdvdd
 ddcccdd
 ddddddd
'''

loadings[this()] = '''
 srqponx
 xxxxxmx
 ghijklx
 fxxxxxx
 edcxy54321
 xxbxzxx
 xxa98xx
 xxxxxxx
'''

levels[next()] = '''
   rcccccccr
   c       c
   c rcccr c
   c c   c c
   c c b c c
   c c c c c
   c c tcr c
   c c     c
   S rcccccr
'''

loadings[this()] = '''
   xllkkjjiw
   m       i
   m t987s h
   n a   6 h
   n a 1 5 g
   o b 2 4 g
   o b q3r f
   p c     f
   y ucddeev
'''

levels[next()] = '''
 Wyyyyyd
 dddddyd
 yyyyyyd
 ydddddd
 yyydyyyyyb
 ddydydd
 ddyyydd
 ddddddd
'''

loadings[this()] = '''
 srqponx
 xxxxxmx
 ghijklx
 fxxxxxx
 edcx654321
 xxbx7xx
 xxa98xx
 xxxxxxx
'''

levels[next()] = '''
crcrcrcrcrcrcE
r
crcrcrccrcrcrc
-------------r
bcrcrcrcrcrcrc
'''

loadings[this()] = '''
nmlkjihgfedcba
o
tuvwxyzzyxwvut
-------------o
abcdefghijklmn
'''

levels[next()] = '''
 lllcccbc
        c
 ppdccccc
 p  c
 ppdccccd
 p   c
 pcccucce
'''

loadings[this()] = '''
 zyxwvuts
        *
 ********
 *  z
 ********
 *   *
 z***z***
'''

levels[next()] = '''
iiippppplppppiii
i              i
i  yyydyyydyyy i
iicc c c c c c i
   c c c c c i i
bccc yyydyyy ccs
'''

loadings[this()] = '''
****************
*              *
*  ccc ccc ccc *
**cc c c c c c *
   c c c c c c *
bccc ccc ccc ccs
'''

levels[next()] = '''
n mcc     mcc
t c c     c c
t ctccctccctcccm
t c   c c   c
ttt   mcc bcc
'''

loadings[this()] = '''
z pon     987
y q m     a 6
x rzlkjzdcbz5zzz
w s   i e   4
vut   hgf 123
'''

levels[next()] = '''
-------------n--
------------dcd-
------------dyd-
------------dcd-
------------dyd-
------------dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycyd-
--ddddddddddddd-
'''

loadings[this()] = '''
-------------a--
------------dbd-
------------ccc-
------------bdb-
------------aea-
------------9f9-
------------8g8-
--11223345678h8-
-utsrqponmlkji7-
--1122334455667-
'''

levels[next()] = '''
-------------n--
------------dcd-
------------dyd-
------------dcd-
------------dyd-
------------dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycrd-
--ddddddddddddd-
'''

loadings[this()] = '''
-------------a--
------------dbd-
------------ccc-
------------bdb-
------------aea-
------------9f9-
------------8g8-
--11223345678h8-
-utsrqponmlkji7-
--1122334455667-
'''

levels[next()] = '''
----------ddddd-
---------dcycyd-
--------dcyddcd-
-------dcyd-dyd-
-------dsd--dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycyd-
--ddddddddddddd-
'''

loadings[this()] = '''
----------98887-
---------9a9997-
--------9aaaa87-
-------abbb-a86-
-------bbb--986-
------------976-
--5556667778875-
-33344455566675-
--1112223334445-
'''

levels[next()] = '''
 Wyyyyyyyy
         y
 yyyyryyyy
 y
 yyyyyyyyb
'''

loadings[this()] = '''
 123456789
         a
 bcdefedcb
 a
 987654321
'''

levels[next()] = '''
 Wryryryr
        y
 yryryryr
 r
 yryryryb
'''

loadings[this()] = '''
 fedcba76
        5
 43211234
 5
 67abcdef
'''

levels[next()] = '''
----------ddddd-
---------dcycyd-
--dddddddcyddcd-
-wcycycycyd-dyd-
--dddddddd--dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycyd-
--ddddddddddddd
'''

loadings[this()] = '''
----------dccbb-
---------dbbaaa-
--ihggffedcba9a-
-ihggffddcd-999-
--ihggffee--989-
------------888-
--1122334456778-
-11223344556677-
--1122334455667-
'''

delays[this()] = 0.1

levels[next()] = '''
----------ddddd-
---------dcycrd-
--dddddddcyddcd-
-wcycycycyd-dyd-
--dddddddd--dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycyd-
--ddddddddddddd-
'''

loadings[this()] = '''
----------dccbb-
---------dbbaza-
--ihggffedcba9a-
-ihggffddcd-999-
--ihggffee--989-
------------888-
--1122334456778-
-11223344556677-
--1122334455667-
'''

delays[this()] = 0.1

levels[next()] = '''
-ddddddddddd-
bryryryryryre
-ddddddddddd-
'''

loadings[this()] = '''
-efghijklmno-
abcdefghijklm
-efghijklmno-
'''

levels[next()] = '''
d d d d d d d d
ccc ccc ccc ccc
c c c c c c c c
c c c c c c c c
c c c c c c c c
c c c c c c c c
b ccc ccc ccc S
  d d d d d d
'''

loadings[this()] = '''
i j k l m n o p
fgh fgh fgh fgh
e e e e e e e e
d d d d d d d d
c c c c c c c c
b b b b b b b b
a fgh fgh fgh a
  q r s t u v
'''

delays[this()] = 0.1

levels[next()] = '''
        ccc
        c-c
        c-c
        c-c
bcccxcccc-h
          i
          i
  wcciiiiii
          d
'''

loadings[this()] = '''
        abc
        j-j
        i-i
        h-h
123456789-g
          f
          e
  123456789
          d
'''

x_hides[this()] = 100

levels[next()] = '''
 b     ccccc
 xcc  dcd dcd
   ccccc   c
    d     dcd
  n        c
 dcd d   d c
  cccccccccc
     d   d
'''

loadings[this()] = '''
 1     bcdef
 234  xax ygy
   56789   h
    x     yiy
  w        j
 zvz z   z k
  utsrqponml
     z   z
'''

levels[next()] = '''
         cccu
         c  c
   ccccccc  c
   ccccc    c
   ccbcc    c
   ccccc    c
   ccccc    ccce
'''

loadings[this()] = '''
         ****
         *  *
   ccccc**  *
   ccccc    *
   ccbcc    *
   ccccc    *
   ccccc    ****
'''

levels[next()] = '''
   cccc   piip
   c  c   i  i
   c  c   i  i
  cc  cc ip  pi
  c    c i    i
  c    c i    i
 cc    ccu    pi
 c      s      i
cc             pi
b               l
'''

loadings[this()] = '''
   cccc   ****
   c  c   *  *
   c  c   *  *
  cc  cc **  **
  c    c *    *
  c    c *    *
 cc    ccc    **
 c      c      *
cc             **
b               *
'''

levels[next()] = '''
mdpdpdpdmdpdpdpdn
ccccccccccccccccc
cdcdcdcdcdcdcdcdc
ccccccccccccccccc
cdcdcdcdcdcdcdcdc
ccccccccccccccccc
bdpdpdpdmdpdpdpdl
'''

loadings[this()] = '''
imimimimimimimimi
123456789abcdefgh
jnjnjnjnjnjnjnjnj
123456789abcdefgh
kokokokokokokokok
123456789abcdefgh
lplplplplplplplpl
'''

delays[this()] = 0.1

levels[next()] = '''
mrrrrrrrrrrrrrrrn
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
brrrrrrrrrrrrrrrm
'''

loadings[this()] = '''
2rrrrrrrrrrrrrrr4
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrrr
1rrrrrrrrrrrrrrr3
'''

delays[this()] = 0.2


levels[next()] = '''
yyy   ppp
ydycccpdpcce
yyy   ppp
 c
 c
 c
rrr   ppp
rdrcccpdpccb
rrr   ppp
'''

loadings[this()] = '''
789   ghi
612mnofabjkl
543   edc
 q
 p
 q
ghi   789
fabjkl612mno
edc   543
'''

levels[next()] = '''
  yyyyyyydyyyyyyn
  yyyyyyydyyyyyyy
  yyyyyyyddddxddd
  yyyyyyyryyyyyyy
  yyyyyyydyyyyyyy
  yyyyyyydyyyyyyy
bcyyyyyyydyyyyyyy
'''

loadings[this()] = '''
  fffffffe1111111
  gggggggd2222222
  hhhhhhhc3333333
  iiiiiiib4444444
  jjjjjjja5555555
  kkkkkkk96666666
lllllllll87777777
'''

x_hides[this()] = 50

levels[next()] = '''
--ddddddddddddd
--dcccccccccccd-
--dcdddddddddcd-
--dcdcccccccdcd-
--dcdcdddddcdcd-
--dcdcdwccccdcd-
--dcdcdddddddcd-
--dcdcccccccccd-
bcccddddddddddd-
'''

loadings[this()] = '''
--kkkkkkkkkkkkk
--l44556677889m-
--l4ooooooooo9m-
--l3pffggghhqam-
--l3pfttttthqam-
--l3pesjjiiiqam-
--l2perrrrrrrbm-
--l2oedddcccbbm-
1112nnnnnnnnnnn-
'''

levels[next()] = '''
--ddddddddddddd
--dcccccccccccd-
--dcdddddddddcd-
--dcdcccccccdcd-
--dcdcdddddcdcd-
--dcdcdwccccdcd-
--dcdcdddddddcd-
--dcdcccccccccd-
bcrcddddddddddd-
'''

loadings[this()] = '''
--kkkkkkkkkkkkk
--l44556677889m-
--l4ooooooooo9m-
--l3pffggghhqam-
--l3pfttttthqam-
--l3pesjjiiiqam-
--l2perrrrrrrbm-
--l2oedddcccbbm-
1112nnnnnnnnnnn-
'''

levels[next()] = '''
--ddddddddddddd
--dcccccccccccd-
--dcdddddddddcd-
--dcdcccccccdcd-
--dcdcdddddcdcd-
--dcdcdwccccdcd-
--dcdcdddddddcd-
--dcdcccccccccd-
bcxcddddddddddd-
'''

loadings[this()] = '''
--kkkkkkkkkkkkk
--l44556677889m-
--l4ooooooooo9m-
--l3pffggghhqam-
--l3pfttttthqam-
--l3pesjjiiiqam-
--l2perrrrrrrbm-
--l2oedddcccbbm-
1112nnnnnnnnnnn-
'''

x_hides[this()] = 100

levels[next()] = '''
--!!!!!!!!!!!!!-
--!iiiiciiiiii!-
--!i!!!!!!!!!i!-
--!i!iiiiiii!i!-
--!i!i!!!!!c!i!-
--!i!i!wcccu!i!-
--!i!i!!!!!!!i!-
--!i!iiiiiicii!-
bcch!!!!!!!!!!!-
'''

loadings[this()] = '''
--kkkkkkkkkkkkk-
--l44556677889m-
--l4ooooooooo9m-
--l3pffggghhqam-
--l3pfttttthqam-
--l3pesjjiiiqam-
--l2perrrrrrrbm-
--l2oedddcccbbm-
1112nnnnnnnnnnn-
'''

levels[next()] = '''
wu--------------
-cccccccccccccc-
-cccccccccccccc-
-cccccccccccccc-
-!!!i!!!!!!!!!!-
-cccccccccccccc-
-cccccccccccccc-
-cccccccccccccc-
--------------hb
'''

loadings[this()] = '''
dd--------------
-ccbbaa99887766-
-cbbaa998877665-
-bbaa9988776655-
-baa99887766554-
-aa998877665544-
-a9988776655443-
-99887766554433-
-------------21-
'''


levels[next()] = '''
wu--------------
-cccccccccccccc-
-cccccccccccccc-
-!!!!!!!!!i!!!!-
-cccccccccccccc-
-!i!!!!!!!!!!!!-
-cccccccccccccc-
-cccccccccccccc-
--------------hb
'''

loadings[this()] = '''
dd--------------
-ccbbaa99887766-
-cbbaa998877665-
-bbaa9988776655-
-baa99887766554-
-aa998877665544-
-a9988776655443-
-99887766554433-
--------------21
'''

levels[next()] = '''
wu--------------
-cccccccccccccc-
-i!!!!!!!!!!!!!-
-cccccccccccccc-
-!!!!!!!!!!i!!!-
-cccccccccccccc-
-!!!!!!!!!i!!!!-
-cccccccccccccc-
--------------hb
'''

loadings[this()] = '''
dd--------------
-ccbbaa99887766-
-cbbaa998877665-
-bbaa9988776655-
-baa99887766554-
-aa998877665544-
-a9988776655443-
-99887766554433-
--------------21
'''

levels[next()] = '''
dnd-------ddddd-
dyd------dcycyd-
dcdddddddcyddcd-
dycycycycyd-dyd-
dddddddddd--dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycyd-
--ddddddddddddd
'''

loadings[this()] = '''
vut-------didid-
qrs------jehehe-
pkpkpkpkpkfgfgf-
olololololf-789-
mnmnmnmnmnm-cba-
------------789-
--3434343434343-
-22525252525252-
--1616161616161
'''

levels[next()] = '''
dnd-------ddddd-
dyd------dcycrd-
dcdddddddcyddcd-
dycycycycyd-dyd-
dddddddddd--dcd-
------------dyd-
--dddddddddddcd-
-bcycycycycycyd-
--ddddddddddddd
'''

loadings[this()] = '''
vut-------didid-
qrs------jehehe-
pkpkpkpkpkfgfgf-
olololololf-789-
mnmnmnmnmnm-cba-
------------789-
--3434343434343-
-22525252525252-
--1616161616161
'''

if __name__ == '__main__':
	verify_levels(levels, loadings)
