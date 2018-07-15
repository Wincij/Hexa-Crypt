from PyQt4 import QtCore, QtGui
from math import *
import random, struct, os, datetime
yeahs = 0
nopes = 0
x = 0
__cphtbl__ = []
for i in range(100):
    x = 0
    __cphtbl__ = []
    y = 127
    z = 0
    while z in range(8):
        __cphtbl__.append([random.randint(69, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y)])
        z+=1

    __key__ = 0
    for i in range(8):
        for j in range(8):
            __key__ += __cphtbl__[i][j]
            __key__ = __key__ << 8
    __key__ = __key__ >> 8
    mystring=  str(bin(__key__))

    if mystring.count('1') + mystring.count('0') == 512:
        yeahs +=1
    else:
        nopes +=1

print("Yeahs: %d" %yeahs)
print("Nopes: %d" %nopes)
