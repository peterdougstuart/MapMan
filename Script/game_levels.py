# coding: utf-8

loadings = {}
levels = {}
delays = {}
x_hides = {}
level_messages = {}

MAX_ROWS = 12
MAX_COLUMNS = 17

#teleport
#a tile that disappears (or turns to death) once you have walked over 

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

check_points = [10, 20, 30, 40]

START_LEVEL = 1

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
pccccccccccccccp
------cc-------
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
9 c c c c c c c
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

levels[next()] = '''
 Wyyyyyyyy
         y
 yyyyryyyy
 y
 yyyyyyyyb
'''

levels[next()] = '''
 Wryryryr
        y
 yryryryr
 r
 yryryryb
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

levels[next()] = '''
  yyyyyyydyyyyyyn
  yyyyyyydyyyyyyy
  yyyyyyyddddxddd
  yyyyyyyryyyyyyy
  yyyyyyydyyyyyyy
  yyyyyyydyyyyyyy
bcyyyyyyydyyyyyyy
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
bcccdddddddddddd
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

#START_LEVEL = this() - 2


if __name__ == '__main__':
	verify_levels(levels, loadings)
