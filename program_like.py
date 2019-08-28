from builtins import SyntaxError
from pathlib import *
from fsa.Fsa2 import *
from parse_regex import parser


def run_like():
    # GET PROJECT PATH
    path = 'C:\\Users\\Andrea\\PycharmProjects\\inspect_def\\' + input("Inserisci percorso progetto: ").replace("/",
                                                                                                                "\\")
    p = Path(path)

    python_files = []
    python_files += list(p.glob("**/*.py"))

    # GET TWEETS
    path_tweets_pattern = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\query"
    p_tweets_patterns = Path(path_tweets_pattern)
    tweets_patterns_files = list(p_tweets_patterns.glob("*"))

    # BLACKLIST TWEETS
    path_tweetsblacklisted_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_tweets"
    p_tweetsblacklisted_patterns = Path(path_tweetsblacklisted_patterns)
    tweetsblacklisted_files = list(p_tweetsblacklisted_patterns.glob("*"))

    # GET USER BY NAME
    path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\by_name"
    p_user_patterns = Path(path_user_patterns)
    users_by_name_files = list(p_user_patterns.glob("*"))

    # GET USERS BY QUERY
    path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\by_query"
    p_user_patterns = Path(path_user_patterns)
    users_by_query_files = list(p_user_patterns.glob("*"))

    # BLACKLIST USERS
    path_blacklist_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_users"
    p_blacklist_user_patterns = Path(path_blacklist_user_patterns)
    blacklist_user_files = list(p_blacklist_user_patterns.glob("*"))

    # GET USER TWEETs
    path_usertweets_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\user_tweets"
    p_usertweets_patterns = Path(path_usertweets_patterns)
    usertweets_files = list(p_usertweets_patterns.glob("*"))

    # LIKE
    path_like_patterns_simple = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\like\\simple"
    p_like_patterns_simple = Path(path_like_patterns_simple)
    like_files_simple = list(p_like_patterns_simple.glob("*"))

    path_like_patterns_composite = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\like\\composite"
    p_like_patterns_composite = Path(path_like_patterns_composite)
    like_files_composite = list(p_like_patterns_composite.glob("*"))

    get_tweets_strings = []
    for tweets_files in tweets_patterns_files:
        file = open(tweets_files, 'r', encoding='utf-8')
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
                            pattern_assign = "_VAR_TWEETS_ = _VAR_MULTI_." + res.name + "(_ARGS_)"
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

    get_user_tweets_strings = []
    for get_user_tweets in usertweets_files:
        file = open(get_user_tweets, 'r', encoding='utf-8')
        get_tweets_string = file.read()
        # print("GETTING PATTERN [GET USER'S TWEETS]")
        # print(get_tweets_string)
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
                            # print("FOUND NEW PATTERN:")
                            # print(pattern_call)
                            if pattern_call not in get_user_tweets_strings:
                                get_user_tweets_strings.append(pattern_call)
                            pattern_assign = "_VAR_TWEETS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            # print("FOUND NEW PATTERN:")
                            # print(pattern_assign)
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

    like_strings = []
    for like_simple_file in like_files_simple:
        file = open(like_simple_file, 'r', encoding='utf-8')
        like_simple_string = file.read()
        like_simple_string_2 = "_VAR_MULTI_ = " + like_simple_string
        # print("GETTING PATTERN [PUT LIKE]")
        # print(like_simple_string + "\n" + like_simple_string_2)
        like_strings.append(like_simple_string)
        like_strings.append(like_simple_string_2)
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
                                # print("FOUND NEW PATTERN:")
                                # print(like_simple_string)
                                # print(new_pat_1)
                                # print(new_pat_2)
                                # print(pattern_call)
                                like_strings.append(pattern_call)
                            pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in like_strings:
                                # print("FOUND NEW PATTERN:")
                                # print(pattern_assign)
                                like_strings.append(pattern_assign)
                    if result2:
                        for res in result2:
                            pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_call not in like_strings:
                                # print("FOUND NEW PATTERN:")
                                # print(like_simple_string)
                                # print(new_pat_1)
                                # print(new_pat_2)
                                # print(pattern_call)
                                like_strings.append(pattern_call)
                            pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in like_strings:
                                # print("FOUND NEW PATTERN:")
                                # print(pattern_assign)
                                like_strings.append(pattern_assign)
                except SyntaxError as e:
                    print("ERROR PARSING: ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(new_pat_1 + "\n" + new_pat_2)
            print("error:")
            print(e)
            print(e.text)

    for like_composite_file in like_files_composite:
        file = open(like_composite_file, 'r', encoding='utf-8')
        like_composite_string = file.read()
        like_composite_string_2 = "_VAR_MULTI_ = " + like_composite_string
        # print("GETTING PATTERN [PUT LIKE]")
        # print(like_composite_string + "\n" + like_composite_string_2)
        like_strings.append(like_composite_string)
        like_strings.append(like_composite_string_2)
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
                                # print("FOUND NEW PATTERN:")
                                # print(like_simple_string)
                                # print(new_pat_1)
                                # print(new_pat_2)
                                # print(pattern_call)
                                like_strings.append(pattern_call)
                            pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in like_strings:
                                # print("FOUND NEW PATTERN:")
                                # print(pattern_assign)
                                like_strings.append(pattern_assign)
                    if result2:
                        for res in result2:
                            pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_call not in like_strings:
                                # print("FOUND NEW PATTERN:")
                                # print(like_simple_string)
                                # print(new_pat_1)
                                # print(new_pat_2)
                                # print(pattern_call)
                                like_strings.append(pattern_call)
                            pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in like_strings:
                                # print("FOUND NEW PATTERN:")
                                # print(pattern_assign)
                                like_strings.append(pattern_assign)
                except SyntaxError as e:
                    print("ERROR PARSING: ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(new_pat_1 + "\n" + new_pat_2)
            print("error:")
            print(e)
            print(e.text)

    indiscriminate_like_strings = []
    for ind_like_string in like_strings:
        # print("INDISCRIMINATE LIKE PATTERN:")
        # print(ind_like_string)
        indiscriminate_like_strings.append(ind_like_string)

    blacklist_like_strings = []
    for like_string in like_strings:
        # print("BLACKLIST LIKE PATTERN")
        # print("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
        #       "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
        blacklist_like_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI\n\t_VAR_CHECK_=False"
                                      "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + like_string)
        # print("BLACKLIST LIKE PATTERN")
        # print("if not any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
        blacklist_like_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + like_string)
        # print("BLACKLIST LIKE PATTERN")
        # print("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
        blacklist_like_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + like_string)
        # print("BLACKLIST LIKE PATTERN")
        # print("if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
        blacklist_like_strings.append(
            "if _VAR_MULTI_ not in _VAR_MULTI_ and _EVERY_:\n\t_STAT_MULTI_\n\t" + like_string)
        for get_tweets in get_tweets_strings:
            for blacklistweets in tweetsblacklisted_files:
                tweetsblacklisted_file = open(blacklistweets, 'r', encoding='utf-8')
                tweetsblacklisted_read = tweetsblacklisted_file.read()
                # print("BLACKLIST LIKE PATTERN")
                # print(get_tweets + "\n_STAT_MULTI_\n" + tweetsblacklisted_read
                #       + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + like_string)

    mass_like_strings = []
    for like_string in like_strings:
        for get_user_tweets_string in get_user_tweets_strings:
            mass_like_strings.append(
                get_user_tweets_string + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_TWEETS_:\n\t_STAT_MULTI_\n\t" + like_string)

    indiscriminate_like_fsas = []
    for indiscriminate_like_string in indiscriminate_like_strings:
        try:
            indiscriminate_like_fsas.append(
                (Fsa(parser.parse(indiscriminate_like_string, first_iter=True, with_ids=True)),
                 indiscriminate_like_string))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(indiscriminate_like_string)
            print("error:")
            print(e)
            print(e.text)

    blacklist_like_fsas = []
    for blacklist_like_string in blacklist_like_strings:
        try:
            blacklist_like_fsas.append(
                (Fsa(parser.parse(blacklist_like_string, first_iter=True, with_ids=True)), blacklist_like_string))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(blacklist_like_string)
            print("error:")
            print(e)
            print(e.text)

    mass_like_fsas = []
    for mass_like_string in mass_like_strings:
        try:
            mass_like_fsas.append(
                (Fsa(parser.parse(mass_like_string, first_iter=True, with_ids=True)), mass_like_string))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(mass_like_string)
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
            for fsa in blacklist_like_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    blacklist_results.append((Module(body=res), fsa[1]))
            for fsa in mass_like_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    mass_results.append((Module(body=res), fsa[1]))
            if not blacklist_results:
                for fsa in indiscriminate_like_fsas:
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
        pass

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
