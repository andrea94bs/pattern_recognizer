from builtins import SyntaxError
from pathlib import *
from fsa.Fsa2 import *
from parse_regex import parser


def run_store():
    # GET PROJECT PATH
    path = 'C:\\Users\\Andrea\\PycharmProjects\\inspect_def\\' + input("Inserisci percorso progetto: ").replace("/",
                                                                                                                "\\")

    p = Path(path)

    python_files = []
    python_files += list(p.glob("**/*.py"))

    # GET FOLLOWERS
    path_followers_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\followers"
    p_followers_patterns = Path(path_followers_patterns)
    followers_patterns_files = list(p_followers_patterns.glob("*"))

    # GET FRIENDS
    path_friends_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\friends"
    p_friends_patterns = Path(path_friends_patterns)
    friends_patterns_files = list(p_friends_patterns.glob("*"))

    # GET USER BY NAME
    path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\by_name"
    p_user_patterns = Path(path_user_patterns)
    users_by_name_files = list(p_user_patterns.glob("*"))

    # GET USERS BY QUERY
    path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\by_query"
    p_user_patterns = Path(path_user_patterns)
    users_by_query_files = list(p_user_patterns.glob("*"))

    # GET USER TWEETS
    path_usertweets_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\user_tweets"
    p_usertweets_patterns = Path(path_usertweets_patterns)
    usertweets_files = list(p_usertweets_patterns.glob("*"))

    # GET TWEETS
    path_tweets_pattern = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\query"
    p_tweets_patterns = Path(path_tweets_pattern)
    tweets_patterns_files = list(p_tweets_patterns.glob("*"))

    # STORE
    path_store_pattern = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\store_patterns"
    p_store_patterns = Path(path_store_pattern)
    store_patterns_files = list(p_store_patterns.glob("*"))

    get_tweets_strings = []
    for tweets_files in (tweets_patterns_files + usertweets_files):
        file = open(tweets_files, 'r', encoding='utf-8')
        get_tweets_string = file.read()
        # print("GETTING PATTERN STRING [GET TWEET]:")
        # print(get_tweets_string)
        get_tweets_strings.append(get_tweets_string)
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
                            # print("NEW PATTERN FOR GETTING TWEETS:")
                            # print(pattern_assign)
                            if pattern_assign not in get_tweets_strings:
                                get_tweets_strings.append(pattern_assign)
                except SyntaxError as e:
                    print("ERROR PARSING ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING ")
            print(new_pat)
            print("error:")
            print(e)
            print(e.text)

    get_users_strings = []
    for get_followers in (
            followers_patterns_files + friends_patterns_files + users_by_name_files + users_by_query_files):
        file = open(get_followers, 'r', encoding='utf-8')
        get_followers_string = file.read()
        get_users_strings.append(get_followers_string)
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
                except SyntaxError as e:
                    print("ERROR PARSING: ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(new_pat)
            print("error:")
            print(e)
            print(e.text)

    store_strings = []
    for store_file in (store_patterns_files):
        file = open(store_file, 'r', encoding='utf-8')
        store_string = ""
        for s in file.readlines():
            store_string = store_string + s
        store_strings.append(store_string)
        try:
            fsa = Fsa(parser.parse(store_string, first_iter=True, with_ids=True))
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
                except SyntaxError as e:
                    print("ERROR PARSING: ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(store_string)
            print("error:")
            print(e)
            print(e.text)

    store_strings_patterns = []
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
            print("ERROR PARSING: ")
            print(store_strings_pattern)
            print("error:")
            print(e)
            print(e.text)

    results = []
    for f in python_files:
        fi = open(f, 'r', encoding='utf-8')
        feed = fi.read()
        try:
            feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
            for fsa in fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    results.append((Module(body=res), fsa[1]))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(f)
            print("error:")
            print(e)
            print(e.text)

    for res in results:
        print_program(res[0])
        print("\n")
        print(res[1])
        pass
