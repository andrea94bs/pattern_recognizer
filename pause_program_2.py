from builtins import BaseException
from pathlib import *
from fsa.Fsa2 import *
from parse_regex import parser
import traceback
import shutil
import time
import gc
import os
import logging
import sys
import multiprocessing
import datetime

LOG = "./log.txt"
print("opened log")
logging.basicConfig(filename=LOG, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)


class Main:

    def __init__(self):
        path_dir = "../dataset"
        p_dir = Path(path_dir)
        self.dirs = [x for x in p_dir.iterdir()]


        path_pause_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\generic"
        p_pause_patterns = Path(path_pause_patterns)
        self.pause_files = list(p_pause_patterns.glob("*"))

        path_pause_large = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\large"
        p_pause_large = Path(path_pause_large)
        self.pauses_large_files = list(p_pause_large.glob("*"))

        path_pause_little = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\little"
        p_pause_little = Path(path_pause_little)
        self.pauses_little_files = list(p_pause_little.glob("*"))

        path_time_little = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\time_assignment_little"
        p_time_little = Path(path_time_little)
        self.time_little_files = list(p_time_little.glob("*"))

        path_time_large = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\time_assignment_large"
        p_time_large = Path(path_time_large)
        self.time_large_files = list(p_time_large.glob("*"))


    def initialize_patterns(self, files):
        self.pauses_little_derived = self.get_pauses_little_derived(files)
        self.pauses_large_derived = self.get_large_pauses_patterns_derived(files)

    def get_generic_pause_patterns(self):
        pauses = []
        for pause in self.pause_files:
            file = open(pause, 'r', encoding='utf-8')
            pauses.append(file.read())
        return pauses

    def get_large_pauses_patterns_derived(self, python_files):
        pauses_large_strings = []
        for pauses_large in self.time_large_files:
            file = open(pauses_large, 'r', encoding='utf-8')
            pauses_large_string = file.read()
            try:
                fsa = Fsa(parser.parse(pauses_large_string, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                if isinstance(res.targets[0], Name):
                                    name = res.targets[0].id
                                elif isinstance(res.targets[0], Attribute):
                                    name = res.targets[0].attr
                                else:
                                    continue
                                new_pattern = "_VAR_MULTI_.sleep(" + name + ")"
                                if new_pattern not in pauses_large_strings:
                                    pauses_large_strings.append(new_pattern)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + pauses_large_string)
        return pauses_large_strings

    def get_large_pauses_patterns_basic(self):
        pauses_large_strings = []
        for p in self.pauses_large_files:
            file = open(p, 'r', encoding='utf-8')
            pauses_large_strings.append(file.read())
        return pauses_large_strings

    def get_pauses_little_derived(self, python_files):
        pauses_little_strings = []
        for pauses_little in self.time_little_files:
            file = open(pauses_little, 'r', encoding='utf-8')
            pauses_little_string = file.read()
            try:
                fsa = Fsa(parser.parse(pauses_little_string, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                if isinstance(res.targets[0], Name):
                                    name = res.targets[0].id
                                elif isinstance(res.targets[0], Attribute):
                                    name = res.targets[0].attr
                                else:
                                    continue
                                new_pattern = "_VAR_MULTI_.sleep(" + name + ")"
                                if new_pattern not in pauses_little_strings:
                                    pauses_little_strings.append(new_pattern)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + pauses_little_string)
        return pauses_little_strings

    def get_pauses_little_basic(self):
        pauses_little_strings = []
        for p in self.pauses_little_files:
            file = open(p, 'r', encoding='utf-8')
            pauses_little_strings.append(file.read())
        return pauses_little_strings


    def get_mimic_fsas_basic(self):
        mimic_fsas = []
        pause_strings =  self.get_large_pauses_patterns_basic()
        for pause_string in pause_strings:
            try:
                mimic_fsas.append(
                    (Fsa(parser.parse(pause_string, first_iter=True, with_ids=True)), pause_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(pause_string))
        return mimic_fsas

    def get_mimic_fsas_derived(self):
        mimic_fsas = []
        pause_strings = self.pauses_large_derived
        for pause_string in pause_strings:
            try:
                mimic_fsas.append(
                    (Fsa(parser.parse(pause_string, first_iter=True, with_ids=True)), pause_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(pause_string))
        return mimic_fsas

    def get_constraint_fsas_basic(self):
        constraint_strings = []
        for pause in self.get_generic_pause_patterns():
            constraint_strings.append("if _VAR_1 < _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
            constraint_strings.append("if _VAR_1 <= _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
            constraint_strings.append("if _VAR_1 >= _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
            constraint_strings.append("if _VAR_1 > _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
        little_strings = self.get_pauses_little_basic()
        for little in little_strings:
            constraint_strings.append(little)
        constraint_fsas = []
        for constraint_string in constraint_strings:
            try:
                constraint_fsas.append(
                    (Fsa(parser.parse(constraint_string, first_iter=True, with_ids=True)), constraint_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(constraint_string))
        return constraint_fsas

    def get_constraint_fsas_derived(self):
        constraint_strings = []
        for pause in self.get_generic_pause_patterns():
            constraint_strings.append("if _VAR_1 < _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
            constraint_strings.append("if _VAR_1 <= _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
            constraint_strings.append("if _VAR_1 >= _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
            constraint_strings.append("if _VAR_1 > _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
        little_strings = self.pauses_little_derived
        for little in little_strings:
            constraint_strings.append(little)
        constraint_fsas = []
        for constraint_string in constraint_strings:
            try:
                constraint_fsas.append(
                    (Fsa(parser.parse(constraint_string, first_iter=True, with_ids=True)), constraint_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(constraint_string))
        return constraint_fsas

    def get_generic_fsas(self):
        generic_fsas = []
        generic_pauses = self.get_generic_pause_patterns()
        for generic_pause in generic_pauses:
            try:
                generic_fsas.append(
                    (Fsa(parser.parse(generic_pause, first_iter=True, with_ids=True)), generic_pause))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(generic_pause))
        return generic_fsas




def run(index_0, index_1, fold, ret):
    ret[index_1] = fold
    ret[index_0] = -1
    try:
        logging.debug("SCANNING PROJECT " + str(fold.name))
        print("SCANNING PROJECT " + str(fold.name))
        files = list(fold.glob("**/*.py"))

        all_files = files
        types = ["**/^(results_patterns).txt", "**/*.json", "**/*.cfg"]
        for t in types:
            all_files += list(fold.glob(t))

        main.initialize_patterns(files)

        mimic_fsas_basic = main.get_mimic_fsas_basic()
        constraint_fsas_basic = main.get_constraint_fsas_basic()
        generic_pauses_fsas_basic = main.get_generic_fsas()

        mimic_fsas = mimic_fsas_basic + main.get_mimic_fsas_derived()
        constraint_fsas = constraint_fsas_basic + main.get_constraint_fsas_derived()
        generic_pauses_fsas = generic_pauses_fsas_basic

        mimic_results = []
        constraint_results = []
        generic_pauses_results = []

        for f in files:
            with open(f, 'r', encoding='utf-8') as fi:
                feed = fi.read()
            try:
                feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
                with open("../results/res.txt", 'a', encoding='utf-8') as result_file:
                    for fsa in mimic_fsas:
                        result = fsa[0].run(feed_tree)
                        if result:
                            result_file.write("m ")
                    for fsa in constraint_fsas:
                        result = fsa[0].run(feed_tree)
                        if result:
                            result_file.write("c ")
                    if not mimic_results and not constraint_results:
                        for fsa in generic_pauses_fsas:
                            result = fsa[0].run(feed_tree)
                            if result:
                                result_file.write("g ")
            except SyntaxError:
                logging.error("ERROR PARSING PROGRAM: " + str(f.name))
    except BaseException as e:
        logging.debug("ERROR ON PROJECT " + str(fold))
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
        try:
            shutil.move(str(fold), "../error")
        except:
            shutil.rmtree(str(fold))
        ret[index_0] = -1
        return
    ret[index_0] = 1
    shutil.rmtree(str(fold))


if __name__ == '__main__':
    main = Main()
    log_file_path = "./log.txt"

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    # flag = run()
    if len(main.dirs) > 0:
        try:
            p = multiprocessing.Process(target=run, name="Run", args=(0, 1, main.dirs[0], return_dict))
            p.daemon = True
            p.start()
            p.join(600)
            if p.is_alive():
                print("JOIN EXPIRED")
                p.terminate()
                p.join()
                shutil.rmtree(str(return_dict[1]))
            elif return_dict[0] != 1:
                shutil.rmtree(str(return_dict[1]))
        except BaseException as e:
            print(traceback.format_exc())
        os.execl('./runme.sh', './runme.sh', *sys.argv)
