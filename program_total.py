from builtins import BaseException
from pathlib import *
from fsa.Fsa2 import *
from parse_regex import parser
import traceback

import logging

LOG = "C:\\Users\\Andrea\\Desktop\\log.txt"
logging.basicConfig(filename=LOG, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)


class Main:

    def __init__(self):
        path_dir = "C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset"
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

        # GET TWEETS
        path_query_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\query"
        p_query_patterns = Path(path_query_patterns)
        self.tweets_patterns_files = list(p_query_patterns.glob("*"))

        # BLACKLIST TWEETS
        path_tweetsblacklisted_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_tweets"
        p_tweetsblacklisted_patterns = Path(path_tweetsblacklisted_patterns)
        self.tweets_blacklisted_files = list(p_tweetsblacklisted_patterns.glob("*"))

        # WHITELIST TWEETS
        path_tweetswhitelisted_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\whitelist_tweets"
        p_tweetswhitelisted_patterns = Path(path_tweetswhitelisted_patterns)
        self.tweets_whitelisted_files = list(p_tweetswhitelisted_patterns.glob("*"))

        # GET FOLLOWERS
        path_followers_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\followers"
        p_followers_patterns = Path(path_followers_patterns)
        self.followers_patterns_files = list(p_followers_patterns.glob("*"))

        # GET FRIENDS
        path_friends_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\friends"
        p_friends_patterns = Path(path_friends_patterns)
        self.friends_patterns_files = list(p_friends_patterns.glob("*"))

        # GET USERS BY NAME
        path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\by_name"
        p_user_patterns = Path(path_user_patterns)
        self.users_by_name_files = list(p_user_patterns.glob("*"))

        # GET USERS BY QUERY
        path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\by_query"
        p_user_patterns = Path(path_user_patterns)
        self.users_by_query_files = list(p_user_patterns.glob("*"))

        # BLACKLIST USERS
        path_blacklist_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_users"
        p_blacklist_user_patterns = Path(path_blacklist_user_patterns)
        self.blacklist_user_files = list(p_blacklist_user_patterns.glob("*"))

        # WHITELIST USERS
        path_whitelist_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\whitelist_users"
        p_whitelist_user_patterns = Path(path_whitelist_user_patterns)
        self.whitelist_user_files = list(p_whitelist_user_patterns.glob("*"))

        # BLACKLIST-BASED FOLLOW PATTERNS
        path_blacklist_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\blacklist-based follow"
        p_blacklist_patterns = Path(path_blacklist_patterns)
        self.blacklist_patterns_files = list(p_blacklist_patterns.glob("*"))

        # UNFOLLOW PATTERNS
        path_unfollow_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\unfollow"
        p_unfollow_patterns = Path(path_unfollow_patterns)
        self.unfollow_patterns_files = list(p_unfollow_patterns.glob("*"))

        # INDISCRIMINATE FOLLOW PATTERNS
        path_basic_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\indiscrimate follow\\basic"
        p_basic_patterns = Path(path_basic_patterns)
        self.follow_files = list(p_basic_patterns.glob("*"))

        # GET USER TWEETs
        path_usertweets_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\user_tweets"
        p_usertweets_patterns = Path(path_usertweets_patterns)
        self.usertweets_files = list(p_usertweets_patterns.glob("*"))

        # LIKE
        path_like_patterns_simple = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\like\\simple"
        p_like_patterns_simple = Path(path_like_patterns_simple)
        self.like_files_simple = list(p_like_patterns_simple.glob("*"))

        path_like_patterns_composite = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\like\\composite"
        p_like_patterns_composite = Path(path_like_patterns_composite)
        self.like_files_composite = list(p_like_patterns_composite.glob("*"))

        # GET MENTIONS
        path_mentions_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\mentions"
        p_mentions_patterns = Path(path_mentions_patterns)
        self.mentions_files = list(p_mentions_patterns.glob("*"))

        # RETWEET
        path_retweet_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\retweet"
        p_retweet_patterns = Path(path_retweet_patterns)
        self.retweet_files = list(p_retweet_patterns.glob("*"))

        # STORE
        path_store_pattern = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\store_patterns"
        p_store_patterns = Path(path_store_pattern)
        self.store_patterns_files = list(p_store_patterns.glob("*"))

    def initialize_patterns(self, files):
        self.get_all_tweets_patterns_derived = self.get_get_all_tweets_patterns_derived(files)
        self.get_user_patterns_derived = self.get_get_users_patterns_derived(files)
        self.store_patterns_derived = self.get_store_patterns_derived(files)
        self.retweet_patterns_derived = self.get_retweet_pattern_derived(files)
        self.user_tweets_patterns_derived = self.get_get_user_tweets_patterns_derived(files)
        self.get_generic_tweets_patterns = self.get_get_generic_tweets_patterns_derived(files)
        self.like_patterns_derived = self.get_like_patterns_derived(files)
        self.get_friends_patterns_derived = self.get_get_friends_pattern_derived(files)
        self.unfollow_patterns_derived = self.get_unfollow_patterns_derived(files)
        self.follow_patterns_derived = self.get_follow_patterns_derived(files)
        #self.get_tweets_mentions_patterns_derived = self.get_get_tweets_mentions_patterns_derived(files)
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

    def get_get_all_tweets_patterns_derived(self, python_files):
        get_tweets_strings = []
        for tweets_files in (self.tweets_patterns_files + self.usertweets_files):
            file = open(tweets_files, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_tweets_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_assign = "_VAR_TWEETS_ = _VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in get_tweets_strings:
                                    get_tweets_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return get_tweets_strings

    def get_get_all_tweets_patterns_basic(self):
        get_tweets_strings = []
        for tweets_files in (self.tweets_patterns_files + self.usertweets_files):
            file = open(tweets_files, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            get_tweets_strings.append(get_tweets_string)
        return get_tweets_strings

    def get_get_users_patterns_derived(self, python_files):
        get_users_strings = []
        for get_followers in (
                self.followers_patterns_files + self.friends_patterns_files + self.users_by_name_files + self.users_by_query_files):
            file = open(get_followers, 'r', encoding='utf-8')
            get_followers_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_followers_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_assign = "_VAR_USERS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in get_users_strings:
                                    get_users_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return get_users_strings

    def get_get_users_patterns_basic(self):
        get_users_strings = []
        for get_followers in (
                self.followers_patterns_files + self.friends_patterns_files + self.users_by_name_files + self.users_by_query_files):
            file = open(get_followers, 'r', encoding='utf-8')
            get_followers_string = file.read()
            get_users_strings.append(get_followers_string)
        return get_users_strings

    def get_store_patterns_derived(self, python_files):
        store_strings = []
        for store_file in (self.store_patterns_files):
            file = open(store_file, 'r', encoding='utf-8')
            store_string = ""
            for s in file.readlines():
                store_string = store_string + s
            try:
                fsa = Fsa(parser.parse("def _FUN_():\n\t" + store_string, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_assign = "_VAR_USERS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in store_strings:
                                    store_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + "def _FUN_():\n\t" + store_string)
        return store_strings

    def get_store_patterns_basic(self):
        store_strings = []
        for store_file in (self.store_patterns_files):
            file = open(store_file, 'r', encoding='utf-8')
            store_string = ""
            for s in file.readlines():
                store_string = store_string + s
            store_strings.append(store_string)
        return store_strings

    def get_get_friends_pattern_derived(self, python_files):
        get_friends_strings = []
        for get_friends in self.friends_patterns_files:
            file = open(get_friends, 'r', encoding='utf-8')
            get_friends_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_friends_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_assign = "_VAR_USERS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in get_friends_strings:
                                    get_friends_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return get_friends_strings

    def get_get_friends_patterns_basic(self):
        get_friends_strings = []
        for get_friends in self.friends_patterns_files:
            file = open(get_friends, 'r', encoding='utf-8')
            get_friends_string = file.read()
            get_friends_strings.append(get_friends_string)
        return get_friends_strings

    def get_follow_patterns_derived(self, python_files):
        follow_strings = []
        for follow_file in self.follow_files:
            file = open(follow_file, 'r', encoding='utf-8')
            follow_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + follow_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in follow_strings:
                                    follow_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in follow_strings:
                                    follow_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return follow_strings

    def get_follow_patterns_basic(self):
        follow_strings = []
        for follow_file in self.follow_files:
            file = open(follow_file, 'r', encoding='utf-8')
            follow_string = file.read()
            follow_strings.append(follow_string)
        return follow_strings

    def get_unfollow_patterns_derived(self, python_files):
        unfollow_strings = []
        for unfollow_file in self.unfollow_patterns_files:
            file = open(unfollow_file, 'r', encoding='utf-8')
            unfollow_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + unfollow_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in unfollow_strings:
                                    unfollow_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in unfollow_strings:
                                    unfollow_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return unfollow_strings

    def get_unfollow_patterns_basic(self):
        unfollow_strings = []
        for unfollow_file in self.unfollow_patterns_files:
            file = open(unfollow_file, 'r', encoding='utf-8')
            unfollow_string = file.read()
            unfollow_strings.append(unfollow_string)
        return unfollow_strings

    def get_get_generic_tweets_patterns_derived(self, python_files):
        get_tweets_strings = []
        for tweets_files in self.tweets_patterns_files:
            file = open(tweets_files, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_tweets_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_assign = "_VAR_TWEETS_ = _VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in get_tweets_strings:
                                    get_tweets_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return get_tweets_strings

    def get_get_generic_tweets_patterns_basic(self):
        get_tweets_strings = []
        for tweets_files in self.tweets_patterns_files:
            file = open(tweets_files, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            get_tweets_strings.append(get_tweets_string)
        return get_tweets_strings

    def get_get_user_tweets_patterns_derived(self, python_files):
        get_user_tweets_strings = []
        for get_user_tweets in self.usertweets_files:
            file = open(get_user_tweets, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_tweets_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in get_user_tweets_strings:
                                    get_user_tweets_strings.append(pattern_call)
                                pattern_assign = "_VAR_TWEETS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in get_user_tweets_strings:
                                    get_user_tweets_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return get_user_tweets_strings

    def get_get_user_tweets_patterns_basic(self):
        get_user_tweets_strings = []
        for get_user_tweets in self.usertweets_files:
            file = open(get_user_tweets, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            get_user_tweets_strings.append(get_tweets_string)
        return get_user_tweets_strings

    def get_like_patterns_derived(self, python_files):
        like_strings = []
        for like_simple_file in self.like_files_simple:
            file = open(like_simple_file, 'r', encoding='utf-8')
            like_simple_string = file.read()
            like_simple_string_2 = "_VAR_MULTI_ = " + like_simple_string
            new_pat_1 = "def _FUN_():\n\t_STAT_MULTI_\n\t" + like_simple_string
            new_pat_2 = "def _FUN_():\n\t_STAT_MULTI_\n\t" + like_simple_string_2
            try:
                fsa1 = Fsa(parser.parse(new_pat_1, first_iter=True, with_ids=True))
                fsa2 = Fsa(parser.parse(new_pat_2, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result1 = fsa1.run(program_tree)
                        result2 = fsa2.run(program_tree)
                        if result1:
                            for res in result1:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in like_strings:
                                    like_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in like_strings:
                                    like_strings.append(pattern_assign)
                        if result2:
                            for res in result2:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in like_strings:
                                    like_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in like_strings:
                                    like_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat_1 + "(or " + new_pat_2 + ")")
        for like_composite_file in self.like_files_composite:
            file = open(like_composite_file, 'r', encoding='utf-8')
            like_composite_string = file.read()
            like_composite_string_2 = "_VAR_MULTI_ = " + like_composite_string
            new_pat_1 = "def _FUN_():\n\t_STAT_MULTI_\n\t" + like_composite_string
            new_pat_2 = "def _FUN_():\n\t_STAT_MULTI_\n\t" + like_composite_string_2
            try:
                fsa1 = Fsa(parser.parse(new_pat_1, first_iter=True, with_ids=True))
                fsa2 = Fsa(parser.parse(new_pat_2, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result1 = fsa1.run(program_tree)
                        result2 = fsa2.run(program_tree)
                        if result1:
                            for res in result1:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in like_strings:
                                    like_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in like_strings:
                                    like_strings.append(pattern_assign)
                        if result2:
                            for res in result2:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in like_strings:
                                    like_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in like_strings:
                                    like_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat_1 + "(or " + new_pat_2 + ")")
        return like_strings

    def get_like_patterns_basic(self):
        like_strings = []
        for like_simple_file in self.like_files_simple:
            file = open(like_simple_file, 'r', encoding='utf-8')
            like_simple_string = file.read()
            like_simple_string_2 = "_VAR_MULTI_ = " + like_simple_string
            like_strings.append(like_simple_string)
            like_strings.append(like_simple_string_2)
        for like_composite_file in self.like_files_composite:
            file = open(like_composite_file, 'r', encoding='utf-8')
            like_composite_string = file.read()
            like_composite_string_2 = "_VAR_MULTI_ = " + like_composite_string
            like_strings.append(like_composite_string)
            like_strings.append(like_composite_string_2)
        return like_strings

    def get_get_tweets_mentions_patterns_derived(self, python_files):
        get_tweets_strings = []
        for get_tweets in self.mentions_files:
            file = open(get_tweets, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_tweets_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in get_tweets_strings:
                                    get_tweets_strings.append(pattern_call)
                                pattern_assign = "_VAR_TWEETS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in get_tweets_strings:
                                    get_tweets_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return get_tweets_strings

    def get_get_tweets_mentions_patterns_derived(self, python_files):
        get_tweets_strings = []
        for get_tweets in self.mentions_files:
            file = open(get_tweets, 'r', encoding='utf-8')
            get_tweets_string = file.read()
            get_tweets_strings.append(get_tweets_string)
        return get_tweets_strings

    def get_retweet_pattern_derived(self, python_files):
        retweet_strings = []
        for retweet_file in self.retweet_files:
            file = open(retweet_file, 'r', encoding='utf-8')
            retweet_string = file.read()
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + retweet_string
            try:
                fsa = Fsa(parser.parse(new_pat, first_iter=True, with_ids=True))
                for f in python_files:
                    program_file = open(f, 'r', encoding='utf-8')
                    program_string = program_file.read()
                    try:
                        program_tree = parser.parse(program_string, with_ids=False, first_iter=True)
                        result = fsa.run(program_tree)
                        if result:
                            for res in result:
                                pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_call not in retweet_strings:
                                    retweet_strings.append(pattern_call)
                                pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in retweet_strings:
                                    retweet_strings.append(pattern_assign)
                    except SyntaxError:
                        logging.error("ERROR PARSING PROGRAM: " + str(f.name))
            except SyntaxError:
                logging.error("ERROR PARSING PATTERN: " + new_pat)
        return retweet_strings

    def get_retweet_pattern_basic(self):
        retweet_strings = []
        for retweet_file in self.retweet_files:
            file = open(retweet_file, 'r', encoding='utf-8')
            retweet_string = file.read()
            retweet_strings.append(retweet_string)
        return retweet_strings

    ########################FSAS##############################################
    ##########################################################################
    ######################################################################
    ######################################################################

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

    def get_blacklist_retweet_fsas_basic(self, python_files):
        blacklist_retweet_strings = []
        retweet_strings = self.get_retweet_pattern_basic()
        get_tweets_strings = self.get_get_generic_tweets_patterns_basic()
        for ret in retweet_strings:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        blacklist_retweet_fsas = []
        for s in blacklist_retweet_strings:
            try:
                blacklist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return blacklist_retweet_fsas

    def get_blacklist_retweet_fsas_derived(self):
        blacklist_retweet_strings = []
        retweet_strings_basic = self.get_retweet_pattern_basic()
        retweet_strings_derived = self.retweet_patterns_derived
        get_tweets_strings_basic = self.get_get_generic_tweets_patterns_basic()
        get_tweets_strings_derived = self.get_generic_tweets_patterns
        for ret in retweet_strings_basic:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_derived:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_basic:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_derived:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        blacklist_retweet_fsas = []
        for s in blacklist_retweet_strings:
            try:
                blacklist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return blacklist_retweet_fsas

    def get_whitelist_retweet_fsas_basic(self):
        whitelist_retweet_strings = []
        retweet_strings = self.get_retweet_pattern_basic()
        get_tweets_strings = self.get_get_generic_tweets_patterns_basic()
        for ret in retweet_strings:
            whitelist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings:
                for whitelistweets in self.tweets_whitelisted_files:
                    tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                    tweetswhitelisted_read = tweetswhitelisted_file.read()
                    whitelist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetswhitelisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        whitelist_retweet_fsas = []
        for s in whitelist_retweet_strings:
            try:
                whitelist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return whitelist_retweet_fsas

    def get_whitelist_retweet_fsas_derived(self):
        whitelist_retweet_strings = []
        retweet_strings_basic = self.get_retweet_pattern_basic()
        retweet_strings_derived = self.retweet_patterns_derived
        get_tweets_strings_basic = self.get_get_generic_tweets_patterns_basic()
        get_tweets_strings_derived = self.get_generic_tweets_patterns
        for ret in retweet_strings_basic:
            whitelist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_derived:
                for whitelistweets in self.tweets_whitelisted_files:
                    tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                    tweetswhitelisted_read = tweetswhitelisted_file.read()
                    whitelist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetswhitelisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            whitelist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_derived:
                for whitelistweets in self.tweets_whitelisted_files:
                    tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                    tweetswhitelisted_read = tweetswhitelisted_file.read()
                    whitelist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetswhitelisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            whitelist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_basic:
                for whitelistweets in self.tweets_whitelisted_files:
                    tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                    tweetswhitelisted_read = tweetswhitelisted_file.read()
                    whitelist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetswhitelisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        whitelist_retweet_fsas = []
        for s in whitelist_retweet_strings:
            try:
                whitelist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return whitelist_retweet_fsas

    def get_mass_retweet_fsa_basic(self):
        retweet_strings = self.get_retweet_pattern_basic()
        get_user_tweets_strings = self.get_get_user_tweets_patterns_basic()
        mass_retweet_strings = []
        for ret in retweet_strings:
            for get_user_tweets_string in get_user_tweets_strings:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        mass_retweet_fsas = []
        for s in mass_retweet_strings:
            try:
                mass_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return mass_retweet_fsas

    def get_mass_retweet_fsa_derived(self):
        retweet_strings_basic = self.get_retweet_pattern_basic()
        retweet_strings_derived = self.retweet_patterns_derived
        get_user_tweets_strings_basic = self.get_get_user_tweets_patterns_basic()
        get_user_tweets_strings_derived = self.user_tweets_patterns_derived
        mass_retweet_strings = []
        for ret in retweet_strings_basic:
            for get_user_tweets_string in get_user_tweets_strings_derived:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            for get_user_tweets_string in get_user_tweets_strings_derived:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            for get_user_tweets_string in get_user_tweets_strings_basic:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        mass_retweet_fsas = []
        for s in mass_retweet_strings:
            try:
                mass_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return mass_retweet_fsas

    def get_indiscriminate_retweet_fsas_basic(self):
        indiscriminate_retweet_strings = self.get_retweet_pattern_basic()
        indiscriminate_retweet_fsas = []
        for s in indiscriminate_retweet_strings:
            try:
                indiscriminate_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return indiscriminate_retweet_fsas

    def get_indiscriminate_retweet_fsas_derived(self):
        indiscriminate_retweet_strings = self.retweet_patterns_derived
        indiscriminate_retweet_fsas = []
        for s in indiscriminate_retweet_strings:
            try:
                indiscriminate_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return indiscriminate_retweet_fsas

    def get_indiscriminate_follow_fsas_basic(self):
        indiscriminate_follow_fsas = []
        indiscriminate_follow_strings = self.get_follow_patterns_basic()
        for s in indiscriminate_follow_strings:
            try:
                indiscriminate_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return indiscriminate_follow_fsas

    def get_indiscriminate_follow_fsas_derived(self):
        indiscriminate_follow_fsas = []
        indiscriminate_follow_strings = self.follow_patterns_derived
        for s in indiscriminate_follow_strings:
            try:
                indiscriminate_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return indiscriminate_follow_fsas

    def get_blacklist_follow_fsas_basic(self):
        blacklist_follow_strings = []
        follow_strings = self.get_follow_patterns_basic()
        get_users_strings = self.get_get_users_patterns_basic()
        for fol in follow_strings:
            blacklist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=False"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings:
                for blacklistusers in self.blacklist_user_files:
                    usersblacklisted_file = open(blacklistusers, 'r', encoding='utf-8')
                    usersblacklisted_read = usersblacklisted_file.read()
                    blacklist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + usersblacklisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            blacklist_follow_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            blacklist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            blacklist_follow_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        blacklist_follow_fsas = []
        for s in blacklist_follow_strings:
            try:
                blacklist_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return blacklist_follow_fsas

    def get_blacklist_follow_fsas_derived(self):
        blacklist_follow_strings = []
        follow_strings_basic = self.get_follow_patterns_basic()
        follow_strings_derived = self.follow_patterns_derived
        get_users_strings_basic = self.get_get_users_patterns_basic()
        get_users_strings_derived = self.get_user_patterns_derived
        for fol in follow_strings_basic:
            blacklist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=False"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings_derived:
                for blacklistusers in self.blacklist_user_files:
                    usersblacklisted_file = open(blacklistusers, 'r', encoding='utf-8')
                    usersblacklisted_read = usersblacklisted_file.read()
                    blacklist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + usersblacklisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            blacklist_follow_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            blacklist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            blacklist_follow_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        for fol in follow_strings_derived:
            blacklist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=False"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings_derived:
                for blacklistusers in self.blacklist_user_files:
                    usersblacklisted_file = open(blacklistusers, 'r', encoding='utf-8')
                    usersblacklisted_read = usersblacklisted_file.read()
                    blacklist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + usersblacklisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            blacklist_follow_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            blacklist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            blacklist_follow_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        for fol in follow_strings_derived:
            blacklist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=False"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings_basic:
                for blacklistusers in self.blacklist_user_files:
                    usersblacklisted_file = open(blacklistusers, 'r', encoding='utf-8')
                    usersblacklisted_read = usersblacklisted_file.read()
                    blacklist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + usersblacklisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            blacklist_follow_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            blacklist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            blacklist_follow_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        blacklist_follow_fsas = []
        for s in blacklist_follow_strings:
            try:
                blacklist_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return blacklist_follow_fsas

    def get_whitelist_follow_fsas_basic(self):
        whitelist_follow_strings = []
        follow_strings = self.get_follow_patterns_basic()
        get_users_strings = self.get_get_users_patterns_basic()
        for fol in follow_strings:
            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=True"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings:
                for whitelistusers in self.whitelist_user_files:
                    userswhitelisted_file = open(whitelistusers, 'r', encoding='utf-8')
                    userswhitelisted_read = userswhitelisted_file.read()
                    whitelist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + userswhitelisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        whitelist_follow_fsas = []
        for s in whitelist_follow_strings:
            try:
                whitelist_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return whitelist_follow_fsas

    def get_whitelist_follow_fsas_derived(self):
        whitelist_follow_strings = []
        follow_strings_basic = self.get_follow_patterns_basic()
        follow_strings_derived = self.follow_patterns_derived
        get_users_strings_basic = self.get_get_users_patterns_basic()
        get_users_strings_derived = self.get_user_patterns_derived
        for fol in follow_strings_basic:
            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=True"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings_derived:
                for whitelistusers in self.whitelist_user_files:
                    userswhitelisted_file = open(whitelistusers, 'r', encoding='utf-8')
                    userswhitelisted_read = userswhitelisted_file.read()
                    whitelist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + userswhitelisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        for fol in follow_strings_derived:
            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=True"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings_derived:
                for whitelistusers in self.whitelist_user_files:
                    userswhitelisted_file = open(whitelistusers, 'r', encoding='utf-8')
                    userswhitelisted_read = userswhitelisted_file.read()
                    whitelist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + userswhitelisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        for fol in follow_strings_derived:
            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=True"
                                            "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
            for get_users in get_users_strings_basic:
                for whitelistusers in self.whitelist_user_files:
                    userswhitelisted_file = open(whitelistusers, 'r', encoding='utf-8')
                    userswhitelisted_read = userswhitelisted_file.read()
                    whitelist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + userswhitelisted_read
                                                    + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)
            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

            whitelist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

            whitelist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)
        whitelist_follow_fsas = []
        for s in whitelist_follow_strings:
            try:
                whitelist_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return whitelist_follow_fsas

    def get_phantom_follow_fsas_basic(self):
        phantom_follow_fsas = []
        phantom_patterns_strings = []
        unfollow_strings = self.get_unfollow_patterns_basic()
        get_friends_strings = self.get_get_friends_patterns_basic()
        for unf in unfollow_strings:
            for getfr in get_friends_strings:
                phantom_patterns_strings.append(
                    getfr + "\n_STAT_MULTI_\nfor _VAR_USER_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + unf)
        for s in phantom_patterns_strings:
            try:
                phantom_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return phantom_follow_fsas

    def get_phantom_follow_fsas_derived(self):
        phantom_follow_fsas = []
        phantom_patterns_strings = []
        unfollow_strings_basic = self.get_unfollow_patterns_basic()
        unfollow_strings_derived = self.unfollow_patterns_derived
        get_friends_strings_basic = self.get_get_friends_patterns_basic()
        get_friends_strings_derived = self.get_friends_patterns_derived
        for unf in unfollow_strings_basic:
            for getfr in get_friends_strings_derived:
                phantom_patterns_strings.append(
                    getfr + "\n_STAT_MULTI_\nfor _VAR_USER_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + unf)
        for unf in unfollow_strings_derived:
            for getfr in get_friends_strings_basic:
                phantom_patterns_strings.append(
                    getfr + "\n_STAT_MULTI_\nfor _VAR_USER_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + unf)
        for unf in unfollow_strings_derived:
            for getfr in get_friends_strings_derived:
                phantom_patterns_strings.append(
                    getfr + "\n_STAT_MULTI_\nfor _VAR_USER_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + unf)
        for s in phantom_patterns_strings:
            try:
                phantom_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return phantom_follow_fsas

    def get_mass_like_fsas_basic(self):
        mass_like_fsas = []
        mass_like_strings = []
        like_strings = self.get_like_patterns_basic()
        get_user_tweets_strings = self.get_get_user_tweets_patterns_basic()
        for like_string in like_strings:
            for get_user_tweets_string in get_user_tweets_strings:
                mass_like_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + like_string)
                for mass_like_string in mass_like_strings:
                    try:
                        mass_like_fsas.append(
                            (Fsa(parser.parse(mass_like_string, first_iter=True, with_ids=True)), mass_like_string))
                    except SyntaxError as e:
                        logging.error("ERROR PARSING PROGRAM: " + str(mass_like_string))
        return mass_like_fsas

    def get_mass_like_fsas_derived(self):
        mass_like_fsas = []
        mass_like_strings = []
        like_strings_basic = self.get_like_patterns_basic()
        like_strings_derived = self.like_patterns_derived
        get_user_tweets_strings_basic = self.get_get_user_tweets_patterns_basic()
        get_user_tweets_strings_derived = self.user_tweets_patterns_derived
        for like_string in like_strings_basic:
            for get_user_tweets_string in get_user_tweets_strings_derived:
                mass_like_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + like_string)
        for like_string in like_strings_derived:
            for get_user_tweets_string in get_user_tweets_strings_derived:
                mass_like_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + like_string)
        for like_string in like_strings_derived:
            for get_user_tweets_string in get_user_tweets_strings_basic:
                mass_like_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + like_string)
        for mass_like_string in mass_like_strings:
            try:
                mass_like_fsas.append(
                    (Fsa(parser.parse(mass_like_string, first_iter=True, with_ids=True)), mass_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(mass_like_string))
        return mass_like_fsas

    def get_indiscriminate_like_fsas_basic(self):
        indiscriminate_like_fsas = []
        indiscriminate_like_strings = self.get_like_patterns_basic()
        for indiscriminate_like_string in indiscriminate_like_strings:
            try:
                indiscriminate_like_fsas.append(
                    (Fsa(parser.parse(indiscriminate_like_string, first_iter=True, with_ids=True)),
                     indiscriminate_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(indiscriminate_like_string))
        return indiscriminate_like_fsas

    def get_indiscriminate_like_fsas_derived(self):
        indiscriminate_like_fsas = []
        indiscriminate_like_strings = self.like_patterns_derived
        for indiscriminate_like_string in indiscriminate_like_strings:
            try:
                indiscriminate_like_fsas.append(
                    (Fsa(parser.parse(indiscriminate_like_string, first_iter=True, with_ids=True)),
                     indiscriminate_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(indiscriminate_like_string))
        return indiscriminate_like_fsas

    def get_blacklist_like_fsas_basic(self):
        blacklist_like_fsas = []
        blacklist_like_strings = []
        like_strings = self.get_like_patterns_basic()
        get_tweets_strings = self.get_get_generic_tweets_patterns_basic()
        for like_string in like_strings:
            blacklist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append(
                "if not any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            blacklist_like_strings.append(
                "if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings:
                blacklist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for blacklistweets in self.tweets_blacklisted_files:
                tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                tweetsblacklisted_read = tweetsblacklisted_file.read()
                blacklist_like_strings.append(tweetsblacklisted_read + "\n_STAT_MULTI\n" + like_string)
        for blacklist_like_string in blacklist_like_strings:
            try:
                blacklist_like_fsas.append(
                    (Fsa(parser.parse(blacklist_like_string, first_iter=True, with_ids=True)), blacklist_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(blacklist_like_string))
        return blacklist_like_fsas

    def get_blacklist_like_fsas_derived(self):
        blacklist_like_fsas = []
        blacklist_like_strings = []
        like_strings_basic = self.get_like_patterns_basic()
        like_strings_derived = self.like_patterns_derived
        get_tweets_strings_basic = self.get_get_generic_tweets_patterns_basic()
        get_tweets_strings_derived = self.get_generic_tweets_patterns
        for like_string in like_strings_basic:
            blacklist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append(
                "if not any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            blacklist_like_strings.append(
                "if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings_derived:
                blacklist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for blacklistweets in self.tweets_blacklisted_files:
                tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                tweetsblacklisted_read = tweetsblacklisted_file.read()
                blacklist_like_strings.append(tweetsblacklisted_read + "\n_STAT_MULTI\n" + like_string)
        for like_string in like_strings_derived:
            blacklist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append(
                "if not any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            blacklist_like_strings.append(
                "if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings_derived:
                blacklist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for blacklistweets in self.tweets_blacklisted_files:
                tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                tweetsblacklisted_read = tweetsblacklisted_file.read()
                blacklist_like_strings.append(tweetsblacklisted_read + "\n_STAT_MULTI\n" + like_string)
        for like_string in like_strings_derived:
            blacklist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            blacklist_like_strings.append(
                "if not any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            blacklist_like_strings.append(
                "if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings_basic:
                blacklist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for blacklistweets in self.tweets_blacklisted_files:
                tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                tweetsblacklisted_read = tweetsblacklisted_file.read()
                blacklist_like_strings.append(tweetsblacklisted_read + "\n_STAT_MULTI\n" + like_string)
        for blacklist_like_string in blacklist_like_strings:
            try:
                blacklist_like_fsas.append(
                    (Fsa(parser.parse(blacklist_like_string, first_iter=True, with_ids=True)), blacklist_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(blacklist_like_string))
        return blacklist_like_fsas

    def get_whitelist_like_fsas_basic(self):
        whitelist_like_fsas = []
        whitelist_like_strings = []
        like_strings = self.get_like_patterns_basic()
        get_tweets_strings = self.get_get_generic_tweets_patterns_basic()
        for like_string in like_strings:
            whitelist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            whitelist_like_strings.append(
                "if _VAR_MULTI_ in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings:
                whitelist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for whitelistweets in self.tweets_whitelisted_files:
                tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                tweetswhitelisted_read = tweetswhitelisted_file.read()
                whitelist_like_strings.append(tweetswhitelisted_read + "\n_STAT_MULTI\n" + like_string)
        for whitelist_like_string in whitelist_like_strings:
            try:
                whitelist_like_fsas.append(
                    (Fsa(parser.parse(whitelist_like_string, first_iter=True, with_ids=True)), whitelist_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(whitelist_like_string))
        return whitelist_like_fsas

    def get_whitelist_like_fsas_derived(self):
        whitelist_like_fsas = []
        whitelist_like_strings = []
        like_strings_basic = self.get_like_patterns_basic()
        like_strings_derived = self.like_patterns_derived
        get_tweets_strings_basic = self.get_get_generic_tweets_patterns_basic()
        get_tweets_strings_derived = self.get_generic_tweets_patterns
        for like_string in like_strings_basic:
            whitelist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            whitelist_like_strings.append(
                "if _VAR_MULTI_ in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings_derived:
                whitelist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for whitelistweets in self.tweets_whitelisted_files:
                tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                tweetswhitelisted_read = tweetswhitelisted_file.read()
                whitelist_like_strings.append(tweetswhitelisted_read + "\n_STAT_MULTI\n" + like_string)
        for like_string in like_strings_derived:
            whitelist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            whitelist_like_strings.append(
                "if _VAR_MULTI_ in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings_basic:
                whitelist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for whitelistweets in self.tweets_whitelisted_files:
                tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                tweetswhitelisted_read = tweetswhitelisted_file.read()
                whitelist_like_strings.append(tweetswhitelisted_read + "\n_STAT_MULTI\n" + like_string)
        for like_string in like_strings_derived:
            whitelist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=True"
                                          "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
            whitelist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
            whitelist_like_strings.append(
                "if _VAR_MULTI_ in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
            for get_tweets in get_tweets_strings_derived:
                whitelist_like_strings.append(get_tweets + "\n_STAT_MULTI_\n" + like_string)
            for whitelistweets in self.tweets_whitelisted_files:
                tweetswhitelisted_file = open(whitelistweets, 'r', encoding='utf-8')
                tweetswhitelisted_read = tweetswhitelisted_file.read()
                whitelist_like_strings.append(tweetswhitelisted_read + "\n_STAT_MULTI\n" + like_string)
        for whitelist_like_string in whitelist_like_strings:
            try:
                whitelist_like_fsas.append(
                    (Fsa(parser.parse(whitelist_like_string, first_iter=True, with_ids=True)), whitelist_like_string))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(whitelist_like_string))
        return whitelist_like_fsas

    def get_blacklist_retweet_fsas_basic(self):
        blacklist_retweet_fsas = []
        blacklist_retweet_strings = []
        retweet_strings = self.get_retweet_pattern_basic()
        get_tweets_strings = self.get_get_generic_tweets_patterns_basic()
        for ret in retweet_strings:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            blacklist_retweet_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + ret)

            blacklist_retweet_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + ret)

            blacklist_retweet_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for s in blacklist_retweet_strings:
            try:
                blacklist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return blacklist_retweet_fsas

    def get_blacklist_retweet_fsas_derived(self):
        blacklist_retweet_fsas = []
        blacklist_retweet_strings = []
        retweet_strings_basic = self.get_retweet_pattern_basic()
        retweet_strings_derived = self.retweet_patterns_derived
        get_tweets_strings_basic = self.get_get_generic_tweets_patterns_basic()
        get_tweets_strings_derived = self.get_generic_tweets_patterns
        for ret in retweet_strings_derived:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            blacklist_retweet_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + ret)

            blacklist_retweet_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + ret)

            blacklist_retweet_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_basic:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_basic:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            blacklist_retweet_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + ret)

            blacklist_retweet_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + ret)

            blacklist_retweet_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_derived:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                             "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
            blacklist_retweet_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + ret)

            blacklist_retweet_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + ret)

            blacklist_retweet_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + ret)
            for get_tweets in get_tweets_strings_derived:
                for blacklistweets in self.tweets_blacklisted_files:
                    tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                    tweetsblacklisted_read = tweetsblacklisted_file.read()
                    blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                     + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for s in blacklist_retweet_strings:
            try:
                blacklist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return blacklist_retweet_fsas

    def get_mass_retweet_fsas_basic(self):
        mass_retweet_fsas = []
        mass_retweet_strings = []
        retweet_strings = self.get_retweet_pattern_basic()
        get_user_tweets_strings = self.get_get_user_tweets_patterns_basic()
        for ret in retweet_strings:
            for get_user_tweets_string in get_user_tweets_strings:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for s in mass_retweet_strings:
            try:
                mass_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return mass_retweet_fsas

    def get_mass_retweet_fsas_derived(self):
        mass_retweet_fsas = []
        mass_retweet_strings = []
        retweet_strings_basic = self.get_retweet_pattern_basic()
        retweet_strings_derived = self.retweet_patterns_derived
        get_user_tweets_strings_basic = self.get_get_user_tweets_patterns_basic()
        get_user_tweets_strings_derived = self.user_tweets_patterns_derived
        for ret in retweet_strings_basic:
            for get_user_tweets_string in get_user_tweets_strings_derived:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            for get_user_tweets_string in get_user_tweets_strings_basic:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for ret in retweet_strings_derived:
            for get_user_tweets_string in get_user_tweets_strings_derived:
                mass_retweet_strings.append(
                    get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)
        for s in mass_retweet_strings:
            try:
                mass_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return mass_retweet_fsas

    def get_indiscriminate_retweet_fsas_basic(self):
        indiscriminate_retweet_fsas = []
        indiscriminate_retweet_strings = self.get_retweet_pattern_basic()
        for s in indiscriminate_retweet_strings:
            try:
                indiscriminate_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return indiscriminate_retweet_fsas

    def get_indiscriminate_retweet_fsas_derived(self):
        indiscriminate_retweet_fsas = []
        indiscriminate_retweet_strings = self.retweet_patterns_derived
        for s in indiscriminate_retweet_strings:
            try:
                indiscriminate_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
            except SyntaxError as e:
                logging.error("ERROR PARSING PROGRAM: " + str(s))
        return indiscriminate_retweet_fsas

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


if __name__ == '__main__':

    main = Main()
    log_file_path = "C:\\Users\\Andrea\\Desktop\\log.txt"

    store_fsas_basic = main.get_store_fsas_basic()
    mimic_fsas_basic = main.get_mimic_fsas_basic()
    constraint_fsas_basic = main.get_constraint_fsas_basic()
    generic_pauses_fsas_basic = main.get_generic_fsas()
    indiscriminate_follow_fsas_basic = main.get_indiscriminate_follow_fsas_basic()
    blacklist_follow_fsas_basic = main.get_blacklist_follow_fsas_basic()
    whitelist_follow_fsas_basic = main.get_whitelist_follow_fsas_basic()
    phantom_follow_fsas_basic = main.get_phantom_follow_fsas_basic()
    indiscriminate_like_fsas_basic = main.get_indiscriminate_like_fsas_basic()
    blacklist_like_fsas_basic = main.get_blacklist_like_fsas_basic()
    whitelist_like_fsas_basic = main.get_whitelist_like_fsas_basic()
    mass_like_fsas_basic = main.get_mass_like_fsas_basic()
    indiscriminate_retweet_fsas_basic = main.get_indiscriminate_retweet_fsas_basic()
    blacklist_retweet_fsas_basic = main.get_blacklist_retweet_fsas_basic()
    whitelist_retweet_fsas_basic = main.get_whitelist_retweet_fsas_basic()
    mass_retweet_fsas_basic = main.get_mass_retweet_fsas_basic()

    for dir in main.dirs:
        try:
            logging.debug("SCANNING PROJECT " + str(dir.name))
            files = list(dir.glob("**/*.py"))

            all_files = files
            types = ["**/^(results_patterns).txt", "**/*.json", "**/*.cfg"]
            for t in types:
                all_files += list(dir.glob(t))

            main.initialize_patterns(files)
            
            store_fsas = store_fsas_basic + main.get_store_fsas_derived()
            mimic_fsas = mimic_fsas_basic + main.get_mimic_fsas_derived()
            constraint_fsas = constraint_fsas_basic + main.get_constraint_fsas_derived()
            generic_pauses_fsas = generic_pauses_fsas_basic
            indiscriminate_follow_fsas = indiscriminate_follow_fsas_basic + main.get_indiscriminate_follow_fsas_derived()
            blacklist_follow_fsas = blacklist_follow_fsas_basic + main.get_blacklist_follow_fsas_derived()
            whitelist_follow_fsas = whitelist_follow_fsas_basic + main.get_whitelist_follow_fsas_derived()
            phantom_follow_fsas = phantom_follow_fsas_basic + main.get_phantom_follow_fsas_derived()
            indiscriminate_like_fsas = indiscriminate_like_fsas_basic + main.get_indiscriminate_like_fsas_derived()
            blacklist_like_fsas = blacklist_like_fsas_basic + main.get_blacklist_like_fsas_derived()
            whitelist_like_fsas = whitelist_like_fsas_basic + main.get_whitelist_like_fsas_derived()
            mass_like_fsas = mass_like_fsas_basic + main.get_mass_like_fsas_derived()
            indiscriminate_retweet_fsas = indiscriminate_retweet_fsas_basic + main.get_indiscriminate_retweet_fsas_derived()
            blacklist_retweet_fsas = blacklist_retweet_fsas_basic + main.get_blacklist_retweet_fsas_derived()
            whitelist_retweet_fsas = whitelist_retweet_fsas_basic + main.get_whitelist_retweet_fsas_derived()
            mass_retweet_fsas = mass_retweet_fsas_basic + main.get_mass_retweet_fsas_derived()

            store_results = []
            mimic_results = []
            constraint_results = []
            generic_pauses_results = []
            indiscriminate_follow_results = []
            blacklist_follow_results = []
            whitelist_follow_results = []
            phantom_follow_results = []
            indiscriminate_like_results = []
            blacklist_like_results = []
            whitelist_like_results = []
            mass_like_results = []
            indiscriminate_retweet_results = []
            blacklist_retweet_results = []
            whitelist_retweet_results = []
            mass_retweet_results = []

            for f in files:
                fi = open(f, 'r', encoding='utf-8')
                feed = fi.read()
                try:
                    feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
                    for fsa in store_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            store_results.append((Module(body=res), fsa[1]))
                    for fsa in mimic_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            mimic_results.append((Module(body=res), fsa[1]))
                    for fsa in constraint_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            constraint_results.append((Module(body=res), fsa[1]))
                    if not mimic_results and not constraint_results:
                        for fsa in generic_pauses_fsas:
                            result = fsa[0].run(feed_tree)
                            for res in result:
                                generic_pauses_results.append((Module(body=res), fsa[1]))
                    for fsa in blacklist_retweet_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            blacklist_retweet_results.append((Module(body=res), fsa[1]))
                    for fsa in whitelist_retweet_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            whitelist_retweet_results.append((Module(body=res), fsa[1]))
                    for fsa in mass_retweet_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            mass_retweet_results.append((Module(body=res), fsa[1]))
                    if not blacklist_retweet_results and not whitelist_retweet_results:
                        for fsa in indiscriminate_retweet_fsas:
                            result = fsa[0].run(feed_tree)
                            for res in result:
                                indiscriminate_retweet_results.append((Module(body=res), fsa[1]))
                    for fsa in blacklist_follow_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            blacklist_follow_results.append((Module(body=res), fsa[1]))
                    for fsa in whitelist_follow_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            whitelist_follow_results.append((Module(body=res), fsa[1]))
                    for fsa in phantom_follow_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            phantom_follow_results.append((Module(body=res), fsa[1]))
                    if not blacklist_follow_results and not whitelist_follow_results:
                        for fsa in indiscriminate_follow_fsas:
                            result = fsa[0].run(feed_tree)
                            for res in result:
                                indiscriminate_follow_results.append((Module(body=res), fsa[1]))
                    for fsa in blacklist_like_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            blacklist_like_results.append((Module(body=res), fsa[1]))
                    for fsa in whitelist_like_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            whitelist_like_results.append((Module(body=res), fsa[1]))
                    for fsa in mass_like_fsas:
                        result = fsa[0].run(feed_tree)
                        for res in result:
                            mass_like_results.append((Module(body=res), fsa[1]))
                    if not blacklist_like_results and not whitelist_like_results:
                        for fsa in indiscriminate_like_fsas:
                            result = fsa[0].run(feed_tree)
                            for res in result:
                                indiscriminate_like_results.append((Module(body=res), fsa[1]))
                    result_file = open(dir.joinpath("results_patterns.txt"), 'a', encoding='utf-8')
                    result_file.truncate(0)
                    result_file.write("STORE PATTERNS:\n")
                    for res in store_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("MIMIC PATTERNS:\n")
                    for res in mimic_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("CONSTRAINT PATTERNS:\n")
                    for res in constraint_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("GENERIC PAUSES PATTERNS:\n")
                    for res in generic_pauses_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("INDISCRIMINATE LIKE PATTERNS:\n")
                    for res in indiscriminate_like_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("BLACKLIST LIKE PATTERNS:\n")
                    for res in blacklist_like_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("WHITELIST LIKE PATTERNS:\n")
                    for res in whitelist_like_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("MASS LIKE PATTERNS:\n")
                    for res in mass_like_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("INDISCRIMINATE FOLLOW PATTERNS:\n")
                    for res in indiscriminate_follow_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("BLACKLIST FOLLOW PATTERNS:\n")
                    for res in blacklist_follow_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("WHITELIST FOLLOW PATTERNS:\n")
                    for res in whitelist_follow_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("PHANTOM FOLLOW PATTERNS:\n")
                    for res in phantom_follow_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("INDISCRIMINATE RETWEET PATTERNS:\n")
                    for res in indiscriminate_retweet_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("BLACKLIST RETWEET PATTERNS:\n")
                    for res in blacklist_retweet_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("WHITELIST RETWEET PATTERNS:\n")
                    for res in whitelist_retweet_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                    result_file.write("MASS RETWEET PATTERNS:\n")
                    for res in mass_retweet_results:
                        write_program_on_file(res[0], result_file)
                        result_file.write("\n")
                        result_file.write(res[1])
                        result_file.write("\n\n")
                except SyntaxError:
                    logging.error("ERROR PARSING PROGRAM: " + str(f.name))
        except BaseException as e:
            logging.debug("ERROR ON PROJECT " + str(dir))
            print(traceback.format_exc())
            logging.error(traceback.format_exc())

# #       except BaseException as e:
#  #          try:
#                logging.error("ERROR ON PROJECT :" + str(dir.name))
#                logging.error(traceback.format_exc())
#                print(traceback.format_exc())
#                print("ERROR ON PROJECT :" + str(dir.name))
#   #         except UnicodeEncodeError as u:
#                log_file = open(log_file_path, 'a', encoding='utf-8')
#                log_file.write("ERROR ON PROJECT :" + str(dir.name))
#                log_file.write("ERROR IN LOG: \n")
#                log_file.write(u)
#                log_file.write("\n")
#                log_file.close()
# except BaseException as e_out:
#   try:
#        logging.error("ERROR ON PROJECT :" + str(dir.name))
#        logging.error(traceback.format_exc())
#        print("ERROR ON PROJECT :" + str(dir.name))
#        print(traceback.format_exc())
#    except UnicodeEncodeError as u:
#        log_file = open(log_file_path, 'a', encoding='utf-8')
#        log_file.write("ERROR ON PROJECT :" + str(dir.name))
#        log_file.write("ERROR IN LOG: \n")
#        log_file.write(u)
#        log_file.write("\n")
#        log_file.close()
