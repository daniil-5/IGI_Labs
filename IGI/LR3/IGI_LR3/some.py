from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper():
        print("До вызова функции")
        func()
    return wrapper

@decorator
def hello():
    print("Hello!")

# Вызов с декоратором
f = hello
hello()
print("После вызова функции")
# Вызов без декоратора (через __wrapped__)
hello.__wrapped__()

print(True and 5)

# print(isinstance(False, int))
print(issubclass(bool, int))
array = [1,2,3,4,5,6,7,8,9,10]
arr = [77,66,77,55]
array.sort(key=lambda x: x % 2)
print(array)
del array[1:5]
print(array)
rr = zip(arr,array)
print(*rr)
from copy import deepcopy
list1 = ['a','b',['x', 'y']]
#list2 = list1.copy()
#list2 = deepcopy(list1)
list2 = list1[:]
list2[2][1] = "xtQ"
print(id(list1[2]))
print(id(list2[2]))
print(list2)
print(list1)
print(print("hhhhhhhh"))
print(dir(6))
print(arr.pop(2))