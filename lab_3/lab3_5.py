A=[]
B=[]

print("Введите 10 элементов массива A через пробел:")
A=[int(x) for x in input().split()]


print("Введите 10 элементов массива B через пробел:")
B=[int(x) for x in input().split()]

A,B=B,A

print("Преобразованный массив A:",A)
print("Преобразованный массив B:",B)