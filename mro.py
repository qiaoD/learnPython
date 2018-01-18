class A(list):
    def show(self):
        print("A:show")

class B(list):
    def show(self):
        print("B:show")

class C(A):
    pass

class D(B,C):
    pass

d = D()
d.show()
