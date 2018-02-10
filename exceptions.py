'''

author : QD
time   : 2018/02/09
  
info   : Exceptions

'''

'''

# 1
def f():
    g()
def g():
    h()
def h():
    i = 1/0
f()

'''

import sys

try:
    filePath = 'test.txt'
    f = open(filePath)
except FileNotFoundError:
    exc_type, exc_val, exc_tb = sys.exc_info()
    print('exc_type is :', exc_type)
    print('exc_val is  :', exc_val)
    print('exc_tb is   :', exc_tb)
else:
    print(f.read())

finally:
    f.close()

