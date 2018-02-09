'''

author : QD
time   : 2018/02/09
  
info   : Context-Management-Protocol
         contextmanager.__enter__()
         contextmanager.__exit__(exc_type, exc_val, exc_tb)

'''

class MyCMP:
    def __init__(self, tag=""):
        self.tag = tag
        print('Resource is [%s]' % self.tag)
        
    def __enter__(self):
        print('[__enter__():%s]:Allocate the Resource' % self.tag)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('[__exit__():%s]:free the Resource' % self.tag)
        if exc_tb is None:
            print('[__exit__():%s]:without exception' % self.tag)
        else:
            print('[__exit__():%s]:with exception' % self.tag)
            return False

with MyCMP('qiao'):
    print('load MyCMP')


with MyCMP('with-exception'):
    raise Exception


