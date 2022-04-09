from django.test import TestCase

# Create your tests here.
def tes():
    list = []
    for i in range(1,10):
        list.append(i)
    print(list)
    print(list[:4])
    print(list[4:])


tes()