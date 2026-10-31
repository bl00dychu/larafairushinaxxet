text = input("Введите строку:")
words= text.split()
for word in words:
    if word.endswith("я"):
        print(word)