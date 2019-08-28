from pathlib import *
import random

path = 'C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Def useful data\\dataset\\classes_python'
p = Path(path)
files = []
files += list(p.glob("**/*.txt"))

urls = []
dataset = open("C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset13.txt", 'a',
               encoding='utf-8')
for file in files:
    f = open(file, 'r', encoding='utf-8')
    write = True
    for line in f.readlines():
        if write:
            urls.append(line)
            write = False
        if line.strip() == "":
            write = True
print(len(urls))
rand = []
for i in range(0, 30):
    rand.append(random.randint(0, len(urls) - 1))

dataset.truncate(0)
for j in rand:
    try:
        url = urls[j]
        to_append = ""
        index = url.find("https")
        to_append = url[index:]
        dataset.write(to_append)
    except IndexError as e:
        print(j)
        print(e)

