## copy!
 # the copy module has only two functions, copy() and deepcopy()

 # When copy() is used on a list, a new list is created, and the old list items are appended

import copy

class MyClass:
    def __init__(self, name):
        self.name = name
    def __cmp__(self, other):
        return cmp(self.name, other.name)

a = MyClass('a')
my_list = [a]
dup = copy.copy(my_list)

print 'copy():'
print '             my_list:', my_list
print '                 dup:', dup
print '      dup is my_list:', (dup is my_list)
print '      dup == my_list:', (dup == my_list)
print 'dup[0] is my_list[0]:', (dup[0] is my_list[0])
print 'dup[0] == my_list[0]:', (dup[0] == my_list[0])

 # When deepcopy() is used on a list, a new list is created, the items from the new list are
 # copied, and then the copies are appended to the new list

dup = copy.deepcopy(my_list)

print '\ndeepcopy():'
print '             my_list:', my_list
print '                 dup:', dup
print '      dup is my_list:', (dup is my_list)
print '      dup == my_list:', (dup == my_list)
print 'dup[0] is my_list[0]:', (dup[0] is my_list[0])
print 'dup[0] == my_list[0]:', (dup[0] == my_list[0])

class SecondClass(MyClass):
    def __copy__(self):
        print '\n__copy__()'
        return SecondClass(self.name)
    def __deepcopy__(self, memo):
        print '__deepcopy__(%s)' % str(memo)
        return SecondClass(copy.deepcopy(self.name, memo))

b = SecondClass('b')
sc = copy.copy(b)
dc = copy.deepcopy(b)
