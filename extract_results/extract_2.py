from pathlib import *

path = "C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\new res store"
p = Path(path)
files = list(p.glob("**/*.txt"))

for file in files:
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    if len(lines) > 2:
        print(lines)