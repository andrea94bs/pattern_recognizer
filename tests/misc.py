from pathlib import *
import logging
import subprocess
import os
import sys
import multiprocessing
import time
import shutil
import datetime
import traceback

path_dir_1 = "C:\\Users\\Andrea\\Desktop\\results tesi"
p_dir_1 = Path(path_dir_1)
files_1 = list(p_dir_1.glob("**/*.txt"))

path_dir_2 = "C:\\Users\\Andrea\\Desktop\\results tesi\\_new"
p_dir_2 = Path(path_dir_2)
files_2 = list(p_dir_2.glob("**/*.txt"))

print(files_1[0].name == files_2[0].name)

print(files_1)
print(files_2)

path_dir = "C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset"
p_dir = Path(path_dir)
dirs = [x for x in p_dir.iterdir()]
for fold in dirs:
    for z in files_1 + files_2:
        if (str(fold.name).strip() == str(z.name)[0:len(str(z.name)) - 4].strip()):
            break
    else:
        print(str(fold.name))
        try:
            shutil.move(str(fold),
                   "C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset_2")
        except:
            print("can't move " + str(fold.name))