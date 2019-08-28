from pathlib import *

from fsa.Fsa2 import *
from parse_regex import parser


def run_ret():
    # GET PROJECT PATH
    path = 'C:\\Users\\Andrea\\PycharmProjects\\inspect_def\\' + input("Inserisci percorso progetto: ").replace("/",
                                                                                                                "\\")
    p = Path(path)

    python_files = []
    python_files += list(p.glob("**/*.py"))

    # GET TWEETS
    path_query_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\query"
    p_query_patterns = Path(path_query_patterns)
    query_patterns_files = list(p_query_patterns.glob("*"))

    # GET MENTIONS
    path_mentions_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\mentions"
    p_mentions_patterns = Path(path_mentions_patterns)
    mentions_files = list(p_mentions_patterns.glob("*"))

    # GET USER TWEETs
    path_usertweets_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\user_tweets"
    p_usertweets_patterns = Path(path_usertweets_patterns)
    usertweets_files = list(p_usertweets_patterns.glob("*"))

    # STREAM
    path_stream_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\stream"
    p_stream_patterns = Path(path_stream_patterns)
    stream_files = list(p_stream_patterns.glob("*"))

    # BLACKLIST TWEETS
    path_tweetsblacklisted_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_tweets"
    p_tweetsblacklisted_patterns = Path(path_tweetsblacklisted_patterns)
    tweetsblacklisted_files = list(p_tweetsblacklisted_patterns.glob("*"))

    # RETWEET
    path_retweet_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\retweet"
    p_retweet_patterns = Path(path_retweet_patterns)
    retweet_files = list(p_retweet_patterns.glob("*"))

    get_tweets_strings = []
    for get_tweets in query_patterns_files:
        file = open(get_tweets, 'r', encoding='utf-8')
        get_tweets_string = file.read()
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
                            pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_call not in get_tweets_strings:
                                get_tweets_strings.append(pattern_call)
                            pattern_assign = "_VAR_TWEETS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in get_tweets_strings:
                                get_tweets_strings.append(pattern_assign)
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

    for get_tweets in mentions_files:
        file = open(get_tweets, 'r', encoding='utf-8')
        get_tweets_string = file.read()
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
                            pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_call not in get_tweets_strings:
                                get_tweets_strings.append(pattern_call)
                            pattern_assign = "_VAR_TWEETS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in get_tweets_strings:
                                get_tweets_strings.append(pattern_assign)
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

    get_user_tweets_strings = []
    for get_user_tweets in usertweets_files:
        file = open(get_user_tweets, 'r', encoding='utf-8')
        get_tweets_string = file.read()
        get_user_tweets_strings.append(get_tweets_string)
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
                                get_user_tweets_strings.append(pattern_call)
                            pattern_assign = "_VAR_TWEETS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in get_user_tweets_strings:
                                get_user_tweets_strings.append(pattern_assign)
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

    retweet_strings = []
    for retweet_file in retweet_files:
        file = open(retweet_file, 'r', encoding='utf-8')
        retweet_string = file.read()
        retweet_strings.append(retweet_string)
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

    indiscriminate_retweet_strings = []
    for ret in retweet_strings:
        indiscriminate_retweet_strings.append(ret)

    blacklist_retweet_strings = []
    for ret in retweet_strings:
        blacklist_retweet_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                         "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + ret)
        for get_tweets in get_tweets_strings:
            for blacklistweets in tweetsblacklisted_files:
                tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                tweetsblacklisted_read = tweetsblacklisted_file.read()
                blacklist_retweet_strings.append(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                                                 + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)

    mass_retweet_strings = []
    for ret in retweet_strings:
        for get_user_tweets_string in get_user_tweets_strings:
            mass_retweet_strings.append(
                get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + ret)

    for ret in retweet_strings:
        blacklist_retweet_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + ret)

        blacklist_retweet_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + ret)

        blacklist_retweet_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + ret)

    indiscriminate_retweet_fsas = []
    for s in indiscriminate_retweet_strings:
        try:
            indiscriminate_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(s)
            print("error:")
            print(e)
            print(e.text)

    blacklist_retweet_fsas = []
    for s in blacklist_retweet_strings:
        try:
            blacklist_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(s)
            print("error:")
            print(e)
            print(e.text)

    mass_retweet_fsas = []
    for s in mass_retweet_strings:
        try:
            mass_retweet_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(s)
            print("error:")
            print(e)
            print(e.text)

    indiscriminate_results = []
    blacklist_results = []
    mass_results = []

    for f in python_files:
        fi = open(f, 'r', encoding='utf-8')
        feed = fi.read()
        try:
            feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
            for fsa in blacklist_retweet_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    blacklist_results.append((Module(body=res), fsa[1]))
            for fsa in mass_retweet_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    mass_results.append((Module(body=res), fsa[1]))
            if not blacklist_results:
                for fsa in indiscriminate_retweet_fsas:
                    result = fsa[0].run(feed_tree)
                    for res in result:
                        indiscriminate_results.append((Module(body=res), fsa[1]))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(f)
            print("error:")
            print(e)
            print(e.text)

    print("INDISCRIMINATE:")
    for res in indiscriminate_results:
        print_program(res[0])
        print("\n")
        print(res[1])

    print("BLACKLIST:")
    for res in blacklist_results:
        print_program(res[0])
        print("\n")
        print(res[1])

    print("MASS:")
    for res in mass_results:
        print_program(res[0])
        print("\n")
        print(res[1])
