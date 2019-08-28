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
        path_dir = "../recheck/dataset"
        p_dir = Path(path_dir)
        self.dirs = [x for x in p_dir.iterdir()]

        # STORE
        path_store_pattern = "./store_patterns"
        p_store_patterns = Path(path_store_pattern)
        self.store_patterns_files = list(p_store_patterns.glob("*"))


    def get_store_fsas_basic(self):
        store_strings_patterns = []
        get_tweets_strings = self.get_get_all_tweets_patterns_basic()
        store_strings = self.get_store_patterns_basic()
        get_users_strings = self.get_get_users_patterns_basic()
        for tweet in get_tweets_strings:
            for s in store_strings:
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n" + s)
        for user in get_users_strings:
            for s in store_strings:
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n" + s)
        fsas = []
        for store_strings_pattern in store_strings_patterns:
            try:
                fsas.append(
                    (Fsa(parser.parse(store_strings_pattern, first_iter=True, with_ids=True)), store_strings_pattern))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(store_strings_pattern))
        return fsas

    def get_store_fsas_derived(self):
        store_strings_patterns = []
        get_tweets_strings_derived = self.get_all_tweets_patterns_derived
        get_tweets_strings_basic = self.get_get_all_tweets_patterns_basic()
        store_strings_derived = self.store_patterns_derived
        store_strings_basic = self.get_store_patterns_basic()
        get_users_strings_derived = self.get_user_patterns_derived
        get_users_strings_basic = self.get_get_users_patterns_basic()
        for tweet in get_tweets_strings_basic:
            for s in store_strings_derived:
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n" + s)
        for tweet in get_tweets_strings_derived:
            for s in store_strings_basic:
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n" + s)
        for tweet in get_tweets_strings_derived:
            for s in store_strings_derived:
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    tweet + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n" + s)
        for user in get_users_strings_basic:
            for s in store_strings_derived:
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n" + s)
        for user in get_users_strings_derived:
            for s in store_strings_basic:
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n" + s)
        for user in get_users_strings_derived:
            for s in store_strings_derived:
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + s)
                store_strings_patterns.append(
                    user + "\n_STAT_MULTI_\n" + "for _VAR_TWEET_ in _VAR_USERS_:\n\t_STAT_MULTI_\n" + s)
        fsas = []
        for store_strings_pattern in store_strings_patterns:
            try:
                fsas.append(
                    (Fsa(parser.parse(store_strings_pattern, first_iter=True, with_ids=True)), store_strings_pattern))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(store_strings_pattern))
        return fsas


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

        store_fsas_basic = main.get_store_fsas_basic()

        store_fsas = store_fsas_basic + main.get_store_fsas_derived()

        store_results = []

        for f in files:
            with open(f, 'r', encoding='utf-8') as fi:
                feed = fi.read()
            try:
                feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
                for fsa in store_fsas:
                    result = fsa[0].run(feed_tree)
                    for res in result:
                        store_results.append((Module(body=res), fsa[1]))
                with open("../recheck/results/" + fold.name + ".txt", 'a', encoding='utf-8') as result_file:
                    result_file.truncate(0)
                    result_file.write("STORE PATTERNS:\n")
                    for res in store_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("MIMIC PATTERNS:\n")
            except SyntaxError:
                logging.error("ERROR PARSING PROGRAM: " + str(f.name))
    except BaseException as e:
        logging.debug("ERROR ON PROJECT " + str(fold))
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
        try:
            shutil.move(str(fold), "../recheck/error")
        except:
            shutil.rmtree(str(fold))
        ret[index_0] = -1
        return
    ret[index_0] = 1
    try:
        shutil.move(str(fold), "../recheck/done")
    except:
        shutil.rmtree(str(fold))


# except BaseException as e_out:
#   try:
#         logging.error("ERROR ON PROJECT :" + str(dir.name))
#         logging.error(traceback.format_exc())
#         print("ERROR ON PROJECT :" + str(dir.name))
#         print(traceback.format_exc())
#     except UnicodeEncodeError as u:
#         log_file = open(log_file_path, 'a', encoding='utf-8')
#         log_file.write("ERROR ON PROJECT :" + str(dir.name))
#         log_file.write("ERROR IN LOG: \n")
#         log_file.write(u)
#         log_file.write("\n")
#         log_file.close()

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
                try:
                    shutil.move(str(return_dict[1]), "../recheck/error")
                except BaseException as e:
                    shutil.rmtree(str(return_dict[1]))
            elif return_dict[0] != 1:
                try:
                    shutil.move(str(return_dict[1]), "../recheck/error")
                except BaseException as e:
                    shutil.rmtree(str(return_dict[1]))
        except BaseException as e:
            print(traceback.format_exc())
        os.execl('./runme.sh', './runme.sh', *sys.argv)
