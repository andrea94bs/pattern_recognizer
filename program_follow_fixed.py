from pathlib import *

from fsa.Fsa2 import *
from parse_regex import parser


if __name__ == '__main__':
    # GET PROJECT PATH
    path = 'C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset'
    p = Path(path)

    python_files = []
    python_files += list(p.glob("**/*.py"))

    # GET TWEETS
    path_query_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_tweets\\query"
    p_query_patterns = Path(path_query_patterns)
    query_patterns_files = list(p_query_patterns.glob("*"))

    # BLACKLIST TWEETS
    path_tweetsblacklisted_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_tweets"
    p_tweetsblacklisted_patterns = Path(path_tweetsblacklisted_patterns)
    tweetsblacklisted_files = list(p_tweetsblacklisted_patterns.glob("*"))

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

    # BLACKLIST USERS
    path_blacklist_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_users"
    p_blacklist_user_patterns = Path(path_blacklist_user_patterns)
    blacklist_user_files = list(p_blacklist_user_patterns.glob("*"))

    # BLACKLIST-BASED FOLLOW PATTERNS
    path_blacklist_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\blacklist-based follow"
    p_blacklist_patterns = Path(path_blacklist_patterns)
    blacklist_patterns_files = list(p_blacklist_patterns.glob("*"))

    # UNFOLLOW PATTERNS
    path_unfollow_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\unfollow"
    p_unfollow_patterns = Path(path_unfollow_patterns)
    unfollow_patterns_files = list(p_unfollow_patterns.glob("*"))

    # INDISCRIMINATE FOLLOW PATTERNS
    path_basic_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\indiscrimate follow\\basic"
    p_basic_patterns = Path(path_basic_patterns)
    follow_files = list(p_basic_patterns.glob("*"))

    get_users_strings = []
    for get_followers in followers_patterns_files:
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

    for get_users in users_by_name_files:
        file = open(get_users, 'r', encoding='utf-8')
        get_users_by_name_string = file.read()
        get_users_strings.append(get_users_by_name_string)
        new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_users_by_name_string
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

    for get_users in users_by_query_files:
        file = open(get_users, 'r', encoding='utf-8')
        get_users_by_query_string = file.read()
        get_users_strings.append(get_users_by_query_string)
        new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + get_users_by_query_string
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

    get_friends_strings = []
    for get_friends in friends_patterns_files:
        file = open(get_friends, 'r', encoding='utf-8')
        get_friends_string = file.read()
        get_friends_strings.append(get_friends_string)
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

    follow_strings = []
    for follow_file in follow_files:
        file = open(follow_file, 'r', encoding='utf-8')
        follow_string = file.read()
        follow_strings.append(follow_string)
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

    unfollow_strings = []
    for unfollow_file in unfollow_patterns_files:
        file = open(unfollow_file, 'r', encoding='utf-8')
        unfollow_string = file.read()
        unfollow_strings.append(unfollow_string)
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
                            if pattern_call not in follow_strings:
                                unfollow_strings.append(pattern_call)
                            pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in follow_strings:
                                unfollow_strings.append(pattern_assign)
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

    indiscriminate_follow_strings = []
    for fol in follow_strings:
        indiscriminate_follow_strings.append(fol)

    blacklist_follow_strings = []
    for fol in follow_strings:
        blacklist_follow_strings.append("if _VAR_MULTI_ in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t_VAR_CHECK_=False"
                                        "\n_STAT_MULTI_\nif _VAR_CHECK_:\n\t_STAT_MULTI_\n\t" + fol)
        for get_users in get_users_strings:
            for blacklistusers in blacklist_user_files:
                usersblacklisted_file = open(blacklistusers, 'r', encoding='utf-8')
                usersblacklisted_read = usersblacklisted_file.read()
                blacklist_follow_strings.append(get_users + "\n_STAT_MULTI_\n" + usersblacklisted_read
                                                + "\n_STAT_MULTI_\nfor _VAR_MULTI_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + fol)

    for fol in follow_strings:
        blacklist_follow_strings.append("if not any(_ARGS_):\n\t_STAT_MULTI_\n\t" + fol)

        blacklist_follow_strings.append("if any(_ARGS_):\n\t_STAT_MULTI_\n\tcontinue\n_STAT_MULTI_\n" + fol)

        blacklist_follow_strings.append("if _VAR_MULTI_ not in _VAR_MULTI_:\n\t_STAT_MULTI_\n\t" + fol)

    phantom_patterns_strings = []
    for unf in unfollow_strings:
        for getfr in get_friends_strings:
            phantom_patterns_strings.append(
                getfr + "\n_STAT_MULTI_\nfor _VAR_USER_ in _VAR_USERS_:\n\t_STAT_MULTI_\n\t" + unf)

    indiscriminate_follow_fsas = []
    for s in indiscriminate_follow_strings:
        try:
            indiscriminate_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(s)
            print("error:")
            print(e)
            print(e.text)

    blacklist_follow_fsas = []
    for s in blacklist_follow_strings:
        try:
            blacklist_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(s)
            print("error:")
            print(e)
            print(e.text)

    phantom_follow_fsas = []
    for s in phantom_patterns_strings:
        try:
            phantom_follow_fsas.append((Fsa(parser.parse(s, first_iter=True, with_ids=True)), s))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(s)
            print("error:")
            print(e)
            print(e.text)

    indiscriminate_results = []
    blacklist_results = []
    phantom_results = []

    for f in python_files:
        fi = open(f, 'r', encoding='utf-8')
        feed = fi.read()
        try:
            feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
            for fsa in blacklist_follow_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    blacklist_results.append((Module(body=res), fsa[1]))
            for fsa in phantom_follow_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    phantom_results.append((Module(body=res), fsa[1]))
            if not blacklist_results:
                for fsa in indiscriminate_follow_fsas:
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

    print("PHANTOM:")
    for res in phantom_results:
        print_program(res[0])
        print("\n")
        print(res[1])
# print("PHANTOM PATTERNS")
# for x in phantom_patterns_strings:
#     print(x + "\n")
#
# print("BLACKLIST PATTERNS")
# for x in blacklist_follow_strings:
#     print(x + "\n")
#
# print("INDISCRIMINATE PATTERNS")
# for x in indiscriminate_follow_strings:
#     print(x + "\n")
