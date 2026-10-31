a= [int(x) for x in input("Введите элементы списка через пробел:").split()]
odd =[]
for x in a:
    if x%2 != 0:
        odd.append(x)

if len(odd)>0:
    print("Наименьший нечетный элемент:",min(odd))
else:
    print("В списке нет нечетных элементов")
    
        
