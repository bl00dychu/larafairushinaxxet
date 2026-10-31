n=int(input("Введите количество учеников в каждом классе:"))

sum1=0
sum2=0

print ("Введите оценки первого класса:")
for i in range(n):
    grade=int(input())
    sum1 += grade

print ("Введите оценки второго класса:")
for i in range(n):
    grade=int(input())
    sum2 += grade

average1=sum1/n
average2=sum2/n

print("Средняя оценка первого класса:",average1)
print("Средняя оценка второго класса:",average2)

