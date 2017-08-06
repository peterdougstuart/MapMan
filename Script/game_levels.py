# coding: utf-8

loadings = {}
levels = {}
delays = {}
x_hides = {}
level_messages = {}

check_points = [10, 20, 30]

START_LEVEL = 1
DEFAULT_X_HIDES = 25
DEFAULT_DELAY = 0.05

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
   ----------------
   --bcccccccc-----
   ----c-----c-----
   ----c-----ccc---
   --cyccccv---r---
   --c-----c--cc---
   --c-----c--c----
   --ccccccccccce--
   ----------------
'''

level_messages[this()] = 'which way?'

loadings[this()] = '''
   ----------------
   --abcdefghi-----
   ----d-----j-----
   ----e-----kll---
   --ggfghij---m---
   --h-----j--nn---
   --h-----l--o----
   --iijklmmnopqr--
   ----------------
'''


levels[next()] = '''
p--ccccccccccc---
p--c---------c---
p--c-ccccccc-c---
p--c-c-----c-c---
uccc-c--bccc-c---
p--c-c-------c---
p--c-ccccccccc---
p--c-------------
p--cccccccccccce-
'''

level_messages[this()] = 'round & round'

loadings[this()] = '''
*--kkjjiihhggf---
*--l---------f---
*--l-6655443-e---
*--m-7-----3-e---
wvvm-7--1122-d---
*--n-8-------d---
*--n-899aabbcc---
*--o-------------
*--oppqqrrssttuu-
'''

levels[next()] = '''
   ----------------
   --------------b-
   --------------c-
   --p--p--p--p--c-
   --c--c--c--c--c-
   --c--c--c--c--c-
   --c--c--c--c--c-
   -wccccccccccccc-
   ----------------
'''

level_messages[this()] = 'get points'

loadings[this()] = '''
   ----------------
   --------------a-
   --------------b-
   --w--t--q--n--c-
   --v--s--p--m--d-
   --u--r--o--l--e-
   --t--q--n--k--f-
   -tsrqponmlkjihg-
   ----------------
'''


levels[next()] = '''
   ---bc-----------
   ----cc----------
   -----cc---------
   ------cc--------
   -------cc-------
   --------cc------
   ---------cc-----
   ----------cc----
   -----------cs---
'''

loadings[this()] = '''
   ---ab-----------
   ----cd----------
   -----ef---------
   ------gh--------
   -------ij-------
   --------kl------
   ---------mn-----
   ----------op----
   -----------qr---
'''

levels[next()] = '''
   ---bc-----------
   ----hi----------
   -----ii---------
   ------ii--------
   -------ii-------
   --------ii------
   ---------ii-----
   ----------iu----
   -----------cs---
'''

loadings[this()] = '''
   ---ab-----------
   ----cd----------
   -----ef---------
   ------gh--------
   -------ij-------
   --------kl------
   ---------mn-----
   ----------op----
   -----------qr---
'''


levels[next()] = '''
   ----------------
   ----iiucncccc---
   ----i-------c---
   ----i-------c---
   ----i-------c---
   ----iiihc9ccc---
   --------c-------
   --bcccccc-------
   ----------------
'''

loadings[this()] = '''
   ----------------
   ----qrstutsrq---
   ----p-------p---
   ----o-------o---
   ----n-------n---
   ----mlkjijklm---
   --------h-------
   --abcdefg-------
   ----------------
'''

levels[next()] = '''
   ----------------
   --bccccccchii---
   ------------i---
   --iihcccccuii---
   --i-------------
   --iiuccccchii---
   ------------i---
   --wcccccccuii---
   ----------------
'''

loadings[this()] = '''
   ----------------
   --aabbccddeef---
   ------------f---
   --lkkjjiihhgg---
   --l-------------
   --mmnnooppqqr---
   ------------r---
   --xwwvvuuttss---
   ----------------
'''

levels[next()] = '''
   ----------------
   --ccccccchccb---
   ----i-----------
   --ccccccccccc---
   --------i-------
   --ccccccccccc---
   --i-------------
   --cccccccucce---
   ----------------
'''

loadings[this()] = '''
   ----------------
   --feeddccbbaa---
   ----f-----------
   --ggfgghhiijj---
   --------i-------
   --llkkjjijjkk---
   --m-------------
   --mnnooppqqrr---
   ----------------
'''


levels[next()] = '''
   ----------------
   ----------------
   -----cccccc-----
   -----c----c-----
   ----cc----cc----
   ----c------c----
   ---cc------xc---
   --wc--------cb--
   ----------------
'''

x_hides[this()] = 17

loadings[this()] = '''
   ----------------
   ----------------
   -----nmlkji-----
   -----o----h-----
   ----qp----gf----
   ----r------e----
   ---ts------dc---
   --vu--------ba--
   ----------------
'''

levels[next()] = '''
   ----------------
   ----------------
   ----------------
   ----------------
   --ddddddddddd---
   -bccccccccccce--
   --ddddddddddd---
   ----------------
   ----------------
'''

loadings[this()] = '''
   ----------------
   ----------------
   ----------------
   ----------------
   --efghijklmno---
   -abcdefghijklm--
   --efghijklmno---
   ----------------
   ----------------
'''


levels[next()] = '''
   ----------------
   ----------------
   ----------------
   ----------------
   --ddddddddddd---
   -bcycycycycyce--
   --ddddddddddd---
   ----------------
   ----------------
'''

loadings[this()] = '''
   ----------------
   ----------------
   ----------------
   ----------------
   --efghijklmno---
   -abcdefghijklm--
   --efghijklmno---
   ----------------
   ----------------
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
---------cccc---
---------c--c---
-----ccccc--ccE-
-pcccc----------
-----cr-----b---
------cr----c---
-------ccc3cc---
'''

loadings[this()] = '''
---------opqr---
---------n--s---
-----ijklm--tuv-
-12345----------
-----67-----h---
------89----g---
-------abcdef---
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
