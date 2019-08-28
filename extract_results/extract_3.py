from pathlib import *
import shutil

path = "C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\results tesi"
p = Path(path)
files = list(p.glob("**/*.txt"))

results = []

total = 0

ok_no_match = 0

ind_follow_ok = 0
ind_follow_false = 0
ind_follow_no_match = 0

blacklist_follow_ok = 0
blacklist_follow_false = 0
blacklist_follow_no_match = 0

whitelist_follow_ok = 0
whitelist_follow_false = 0
whitelist_follow_no_match = 0

phantom_follow_ok = 0
phantom_follow_false = 0
phantom_follow_no_match = 0

ind_retweet_ok = 0
ind_retweet_false = 0
ind_retweet_no_match = 0

whitelist_retweet_ok = 0
whitelist_retweet_false = 0
whitelist_retweet_no_match = 0

blacklist_retweet_ok = 0
blacklist_retweet_false = 0
blacklist_retweet_no_match = 0

mass_retweet_ok = 0
mass_retweet_false = 0
mass_retweet_no_match = 0

ind_like_ok = 0
ind_like_false = 0
ind_like_no_match = 0

whitelist_like_ok = 0
whitelist_like_false = 0
whitelist_like_no_match = 0

blacklist_like_ok = 0
blacklist_like_false = 0
blacklist_like_no_match = 0

mass_like_ok = 0
mass_like_false = 0
mass_like_no_match = 0

mimic_ok = 0
mimic_false = 0
mimic_no_match = 0

constraints_ok = 0
constraints_false = 0
constraints_no_match = 0

generic_pause_ok = 0
generic_pause_false = 0
generic_pause_no_match = 0

store_ok = 0
store_no_match = 0
store_false = 0

for f in files:
    total += 1
    flag = False
    copied_no_match = False
    copied_false = False
    with open(f, 'r') as r:
        lines = r.readlines()
        for line in lines:
            if "----" in line:
                flag = True
            if flag:
                if "----" not in line and line.strip() != '':
                    if 'ind_retweet_ok' in line.lower():
                        ind_retweet_ok += 1
                    if 'ind_retweet_no_match' in line.lower():
                        ind_retweet_no_match += 1
                    if 'ind_retweet_false' in line.lower()\
                            or ('ind_retweet_ok' in line.lower() and 'semant' in line.lower()):
                        ind_retweet_false += 1
                    if 'blacklist_retweet_ok' in line.lower():
                        blacklist_retweet_ok += 1
                    if 'blacklist_retweet_no_match' in line.lower():
                        blacklist_retweet_no_match += 1
                    if 'blacklist_retweet_false' in line.lower()\
                            or ('blacklist_retweet_ok' in line.lower() and 'semant' in line.lower()):
                        blacklist_retweet_false += 1
                    if 'whitelist_retweet_ok' in line.lower():
                        whitelist_retweet_ok += 1
                    if 'whitelist_retweet_no_match' in line.lower():
                        whitelist_retweet_no_match += 1
                    if 'whitelist_retweet_false' in line.lower()\
                            or ('whitelist_retweet_ok' in line.lower() and 'semant' in line.lower()):
                        whitelist_retweet_false += 1
                    if 'mass_retweet_ok' in line.lower():
                        mass_retweet_ok += 1
                    if 'mass_retweet_no_match' in line.lower():
                        mass_retweet_no_match += 1
                    if 'mass_retweet_false' in line.lower()\
                            or ('mass_retweet_ok' in line.lower() and 'semant' in line.lower()):
                        mass_retweet_false += 1
                    if 'ind_like_ok' in line.lower():
                        ind_like_ok += 1
                    if 'ind_like_no_match' in line.lower():
                        ind_like_no_match += 1
                    if 'ind_like_false' in line.lower()\
                            or ('ind_like_ok' in line.lower() and 'semant' in line.lower()):
                        ind_like_false += 1
                    if 'blacklist_like_ok' in line.lower():
                        blacklist_like_ok += 1
                    if 'blacklist_like_no_match' in line.lower():
                        blacklist_like_no_match += 1
                    if 'blacklist_like_false' in line.lower()\
                            or ('blacklist_like_ok' in line.lower() and 'semant' in line.lower()):
                        blacklist_like_false += 1
                    if 'whitelist_like_ok' in line.lower():
                        whitelist_like_ok += 1
                    if 'whitelist_like_no_match' in line.lower():
                        whitelist_like_no_match += 1
                    if 'whitelist_like_false' in line.lower()\
                            or ('whitelist_like_ok' in line.lower() and 'semant' in line.lower()):
                        whitelist_retweet_false += 1
                    if 'mass_like_ok' in line.lower():
                        mass_like_ok += 1
                    if 'mass_like_no_match' in line.lower():
                        mass_like_no_match += 1
                    if 'mass_like_false' in line.lower()\
                            or ('mass_like_ok' in line.lower() and 'semant' in line.lower()):
                        mass_like_false += 1
                    if 'ind_follow_ok' in line.lower():
                        ind_follow_ok += 1
                    if 'ind_follow_no_match' in line.lower():
                        ind_follow_no_match += 1
                    if 'ind_follow_false' in line.lower()\
                            or ('ind_follow_ok' in line.lower() and 'semant' in line.lower()):
                        ind_follow_false += 1
                    if 'blacklist_follow_ok' in line.lower():
                        blacklist_follow_ok += 1
                    if 'blacklist_follow_no_match' in line.lower():
                        blacklist_follow_no_match += 1
                    if 'blacklist_follow_false' in line.lower()\
                            or ('blacklist_follow_ok' in line.lower() and 'semant' in line.lower()):
                        blacklist_follow_false += 1
                    if 'whitelist_follow_ok' in line.lower():
                        whitelist_follow_ok += 1
                    if 'whitelist_follow_no_match' in line.lower():
                        whitelist_follow_no_match += 1
                    if 'whitelist_follow_false' in line.lower()\
                            or ('whitelist_follow_ok' in line.lower() and 'semant' in line.lower()):
                        whitelist_follow_false += 1
                    if 'phantom_follow_ok' in line.lower():
                        phantom_follow_ok += 1
                    if 'phantom_follow_no_match' in line.lower():
                        phantom_follow_no_match += 1
                    if 'phantom_follow_false' in line.lower()\
                            or ('phantom_follow_ok' in line.lower() and 'semant' in line.lower()):
                        phantom_follow_false += 1
                    if 'constraints_ok' in line.lower():
                        constraints_ok += 1
                    if 'constraints_no_match' in line.lower():
                        constraints_no_match += 1
                    if 'constraints_false' in line.lower()\
                            or ('constraints_ok' in line.lower() and 'semant' in line.lower()):
                        constraints_false += 1
                    if 'constraint_ok' in line.lower():
                        constraints_ok += 1
                    if 'constraint_no_match' in line.lower():
                        constraints_no_match += 1
                    if 'constraint_false' in line.lower()\
                            or ('constraint_ok' in line.lower() and 'semant' in line.lower()):
                        constraints_false += 1
                    if 'mimic_ok' in line.lower():
                        mimic_ok += 1
                    if 'mimic_no_match' in line.lower():
                        mimic_no_match += 1
                    if 'mimic_false' in line.lower()\
                            or ('mimic_ok' in line.lower() and 'semant' in line.lower()):
                        mimic_false += 1
                    if 'store_ok' in line.lower():
                        store_ok += 1
                    if 'store_no_match' in line.lower():
                        store_no_match += 1
                    if 'store_false' in line.lower()\
                            or ('store_ok' in line.lower() and 'semant' in line.lower()):
                        store_false += 1
                    if 'ok_no_match' in line.lower():
                        ok_no_match += 1
                    if 'generic_pause_ok' in line.lower():
                        generic_pause_ok += 1
                    if 'generic_pause_no_match' in line.lower():
                        generic_pause_no_match += 1
                    if 'generic_pause_false' in line.lower()\
                            or ('generic_pause_ok' in line.lower() and 'semant' in line.lower()):
                        generic_pause_false += 1
    copied_false = False
    copied_no_match = False

print('IND FOLLOW TP: ' + str(ind_follow_ok))
print('IND FOLLOW FN: ' + str(ind_follow_no_match))
print('IND FOLLOW FP: ' + str(ind_follow_false))
print('BLACKLIST FOLLOW TP: ' + str(blacklist_follow_ok))
print('BLACKLIST FOLLOW FN: ' + str(blacklist_follow_no_match))
print('BLACKLIST FOLLOW FP: ' + str(blacklist_follow_false))
print('WHITELIST FOLLOW TP: ' + str(whitelist_follow_ok))
print('WHITELIST FOLLOW FN: ' + str(whitelist_follow_no_match))
print('WHITELIST FOLLOW FP: ' + str(whitelist_follow_false))
print('PHANTOM FOLLOW TP: ' + str(phantom_follow_ok))
print('PHANTOM FOLLOW FN: ' + str(phantom_follow_no_match))
print('PHANTOM FOLLOW FP: ' + str(phantom_follow_false))

print('IND RETWEET TP: ' + str(ind_retweet_ok))
print('IND RETWEET FN: ' + str(ind_retweet_no_match))
print('IND RETWEET FP: ' + str(ind_retweet_false))
print('BLACKLIST RETWEET TP: ' + str(blacklist_retweet_ok))
print('BLACKLIST RETWEET FN: ' + str(blacklist_retweet_no_match))
print('BLACKLIST RETWEET FP: ' + str(blacklist_retweet_false))
print('WHITELIST RETWEET TP: ' + str(whitelist_retweet_ok))
print('WHITELIST RETWEET FN: ' + str(whitelist_retweet_no_match))
print('WHITELIST RETWEET FP: ' + str(whitelist_retweet_false))
print('MASS RETWEET TP: ' + str(mass_retweet_ok))
print('MASS RETWEET FN: ' + str(mass_retweet_no_match))
print('MASS RETWEET FP: ' + str(mass_retweet_false))

print('IND LIKE TP: ' + str(ind_like_ok))
print('IND LIKE FN: ' + str(ind_like_no_match))
print('IND LIKE FP: ' + str(ind_like_false))
print('BLACKLIST LIKE TP: ' + str(blacklist_like_ok))
print('BLACKLIST LIKE FN: ' + str(blacklist_like_no_match))
print('BLACKLIST LIKE FP: ' + str(blacklist_like_false))
print('WHITELIST LIKE TP: ' + str(whitelist_like_ok))
print('WHITELIST LIKE FN: ' + str(whitelist_like_no_match))
print('WHITELIST LIKE FP: ' + str(whitelist_like_false))
print('MASS LIKE TP: ' + str(mass_like_ok))
print('MASS LIKE FN: ' + str(mass_like_no_match))
print('MASS LIKE FP: ' + str(mass_like_false))

print('CONSTRAINTS TP: ' + str(constraints_ok))
print('CONSTRAINTS FN: ' + str(constraints_no_match))
print('CONSTRAINTS FP: ' + str(constraints_false))

print('MIMIC TP: ' + str(mimic_ok))
print('MIMIC FN: ' + str(mimic_no_match))
print('MIMIC FP: ' + str(mimic_false))

print('GENERIC PAUSE TP: ' + str(generic_pause_ok))
print('GENERIC PAUSE FN: ' + str(generic_pause_no_match))
print('GENERIC PAUSE FP: ' + str(generic_pause_false))

print("STORE TP: " + str(store_ok))
print("STORE FN: " + str(store_no_match))
print("STORE FP: " + str(store_false))

print("TOTAL: " + str(total))
########constraint o constraints stessa roba
#############generic pausa and no match
