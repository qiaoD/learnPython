'''

author : QD
time   : 2018/02/09
  
info   : Context-Management-Protocol
         contextmanager.__enter__()
         contextmanager.__exit__(exc_type, exc_val, exc_tb)

'''

class MyCMP:
    def __init__(self, tag):
        self.tag = tag
        print("[__init__]:%s" % tag)
		
    def __enter__(self):
        print("[__enter__]:%s" % self.tag)
    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_tb is None:
            print("[__exit__]: %s" % self.tag)
        else:
            print("exc_type :%s" % exc_type )
            print("exc_val  :%s" % exc_val)
            print("exc_tb   :%s" % exc_tb)
            return 1
            

with MyCMP('normal'):
    print('with-body')

print('================================')

with MyCMP('with-exception'):
    print('with-body')
    raise Exception




