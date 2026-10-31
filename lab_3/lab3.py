n=int(input("Введите количество учеников в каждом классе:"))

sum1=0
sum2=0

print ("Введите оценки первого класса через пробел:")
grades1=[int(x) for x in input().split()]
for i in range(n):
    sum1+=grades1[i]

print ("Введите оценки второго класса через пробел:")
grades2=[int(x) for x in input().split()]
for i in range(n):
    sum2+=grades2[i]

average1=sum1/n
average2=sum2/n

print("Средняя оценка первого класса:",average1)
print("Средняя оценка второго класса:",average2)

