from pathlib import *

from fsa.Fsa2 import *
from parse_regex import parser


def run():
    index = 1

    # RETRIEVE PYTHON FILES TO SCAN LOOKING FOR PATTERNS
    path = 'C:\\Users\\Andrea\\PycharmProjects\\inspect_def\\' + input("Inserisci percorso progetto: ").replace("/",
                                                                                                                "\\")
    p = Path(path)
    python_files = []
    python_files += list(p.glob("**/*.py"))

    # GET FOLLOWERS
    path_followers_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\followers"
    p_followers_patterns = Path(path_followers_patterns)
    followers_patterns_files = list(p_followers_patterns.glob("*"))

    # GET USER
    path_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\search_users\\single"
    p_user_patterns = Path(path_user_patterns)
    user_files = list(p_user_patterns.glob("*"))

    # BLACKLIST USERS
    path_blacklist_user_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\blacklist_users"
    p_blacklist_user_patterns = Path(path_blacklist_user_patterns)
    blacklist_user_files = list(p_blacklist_user_patterns.glob("*"))

    # PHANTOM FOLLOW PATTERNS
    path_phantom_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\phantom_follow"
    p_phantom_patterns = Path(path_phantom_patterns)
    phantom_patterns_files = list(p_phantom_patterns.glob("*"))

    # BLACKLIST-BASED FOLLOW PATTERNS
    path_blacklist_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\blacklist-based follow"
    p_blacklist_patterns = Path(path_blacklist_patterns)
    blacklist_patterns_files = list(p_blacklist_patterns.glob("*"))

    # UNFOLLOW PATTERNS
    path_unfollow_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\unfollow"
    p_unfollow_patterns = Path(path_unfollow_patterns)
    unfollow_patterns_files = list(p_unfollow_patterns.glob("*"))

    # INDISCRIMINATE FOLLOW PATTERNS
    path_basic_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\parse_follow\\pattern_programs\\indiscrimate follow\\basic"
    p_basic_patterns = Path(path_basic_patterns)
    basic_patterns_files = list(p_basic_patterns.glob("*"))

    basic_fsas = []

    index_patterns_to_extract = 1

    basic_follow_strings = []
    unfollow_strings = []
    get_followers_strings = []
    get_user_strings = []
    blacklist_users_strings = []

    for k in basic_patterns_files:
        pat = open(k, 'r', encoding='utf-8')
        pat = pat.read()
        basic_follow_strings.append(pat)

    for u in unfollow_patterns_files:
        pat = open(u, 'r', encoding='utf-8')
        pat = pat.read()
        unfollow_strings.append(pat)

    for fol in followers_patterns_files:
        pat = open(fol, 'r', encoding='utf-8')
        pat = pat.read()
        get_followers_strings.append(pat)

    for blus in blacklist_user_files:
        pat = open(blus, 'r', encoding='utf-8')
        pat = pat.read()
        blacklist_users_strings.append(pat)

    basic_fsa_feed = []
    for i in range(0, len(basic_follow_strings)):
        b = basic_follow_strings[i]
        if b not in basic_fsa_feed:
            basic_fsa_feed.append(b)
        new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + b
        new_pat_tree = parser.parse(new_pat, first_iter=True, with_ids=True)
        fsa_to_try = Fsa(new_pat_tree)
        for f in python_files:
            to_scan = open(f, 'r', encoding='utf-8')
            try:
                program_tree = parser.parse(to_scan.read(), first_iter=True)
                result = fsa_to_try.run(copy.deepcopy(program_tree))
                if result:
                    for res in result:
                        pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                        if pattern_call not in basic_follow_strings:
                            basic_follow_strings.append(pattern_call)
                            basic_fsa_feed.append(pattern_call)
                        pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                        if pattern_assign not in basic_follow_strings:
                            basic_follow_strings.append(pattern_assign)
                            basic_fsa_feed.append(pattern_assign)
            except SyntaxError as e:
                print("ERROR PARSING FILE: ", end=' ')
                print(f)
                print("error:")
                print(e)
                print(e.text)

    # #
    # #
    #

    search_followers_blacklist_feed = []
    for i in range(0, len(get_followers_strings)):
        getfol = get_followers_strings[i]
        for j in range(0, len(blacklist_users_strings)):
            new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + getfol + "\n\t" + blacklist_users_strings[j]
            try:
                new_pat_tree = parser.parse(new_pat, first_iter=True, with_ids=True)
                fsa_to_try = Fsa(new_pat_tree)
                for f in python_files:
                    to_scan = open(f, 'r', encoding='utf-8')
                    try:
                        program_tree = parser.parse(to_scan.read(), first_iter=True)
                        result = fsa_to_try.run(copy.deepcopy(program_tree))
                        if result:
                            for res in result:
                                pattern_call = "_VAR_USERS_." + res.name + "(_ARGS_)"
                                if pattern_call not in basic_follow_strings:
                                    search_followers_blacklist_feed.append(pattern_call)
                                pattern_assign = "_VAR_USERS_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                                if pattern_assign not in basic_follow_strings:
                                    search_followers_blacklist_feed.append(pattern_assign)
                    except SyntaxError as e:
                        print("ERROR PARSING FILE: ", end=' ')
                        print(f)
                        print("error:")
                        print(e)
                        print(e.text)
            except SyntaxError as e:
                print("ERROR PARSING PATTERN: ", end=' ')
                print(new_pat)
                print("error:")
                print(e)
                print(e.text)

    unfollow_fsa_feed = []
    for i in range(0, len(unfollow_strings)):
        u = unfollow_strings[i]
        new_pat = "def _FUN_():\n\t_STAT_MULTI_\n\t" + u
        try:
            new_pat_tree = parser.parse(new_pat, first_iter=True, with_ids=True)
            fsa_to_try = Fsa(new_pat_tree)
            for f in python_files:
                to_scan = open(f, 'r', encoding='utf-8')
                try:
                    program_tree = parser.parse(to_scan.read(), first_iter=True)
                    result = fsa_to_try.run(copy.deepcopy(program_tree))
                    if result:
                        for res in result:
                            if u in unfollow_fsa_feed:
                                unfollow_fsa_feed.remove(u)
                            pattern_call = "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_call not in unfollow_strings:
                                unfollow_strings.append(pattern_call)
                            if pattern_call not in unfollow_fsa_feed:
                                unfollow_fsa_feed.append(pattern_call)
                            pattern_assign = "_VAR_MULTI_ = " + "_VAR_MULTI_." + res.name + "(_ARGS_)"
                            if pattern_assign not in unfollow_strings:
                                unfollow_strings.append(pattern_assign)
                            if pattern_assign not in unfollow_fsa_feed:
                                unfollow_fsa_feed.append(pattern_assign)
                    else:
                        if u not in unfollow_fsa_feed:
                            unfollow_fsa_feed.append(u)
                except SyntaxError as e:
                    print("ERROR PARSING File: ", end=' ')
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING PATTERN: ", end=' ')
            print(new_pat)
            print("error:")
            print(e)
            print(e.text)

    patterns_placeholder_substituted = []
    for blpat in blacklist_patterns_files:
        pat = open(blpat, 'r', encoding='utf-8')
        pat_str = pat.read()
        pat.close()
        pat = open(blpat, 'r', encoding='utf-8')
        pat_lines = pat.readlines()
        last = pat_lines[-1]
        for st in basic_fsa_feed:
            splitted = st.split("\n")
            to_insert = pat_str.replace("(FOLLOW_PLACEHOLDER)", splitted[0])
            if len(splitted) > 1:
                for line in splitted[1:]:
                    to_insert += "\n" + " " * last.count(" ") + line
            patterns_placeholder_substituted.append(to_insert)
            # print(to_insert)

    for g in search_followers_blacklist_feed:
        for basic in basic_fsa_feed:
            patterns_placeholder_substituted.append(g + "\n" + "_STAT_MULTI_" + "\n"
                                                    + "for _VAR_USER_ in _VAR_USERS_:" +
                                                    "\n\t" + "_STAT_MULTI_" +
                                                    "\n\t" + basic)
    blacklist_fsas = []
    for pattern_placeholder_substituted in patterns_placeholder_substituted:
        try:
            blacklist_fsas.append((Fsa(parser.parse(pattern_placeholder_substituted, with_ids=True, first_iter=True)),
                                   pattern_placeholder_substituted))
        except SyntaxError as e:
            print("ERROR PARSING PATTERN: ", end=' ')
            print(pattern_placeholder_substituted)
            print("error:")
            print(e)
            print(e.text)

    patterns_placeholder_substituted = []
    for unpat in phantom_patterns_files:
        pat = open(unpat, 'r', encoding='utf-8')
        pat_str = pat.read()
        pat.close()
        pat = open(unpat, 'r', encoding='utf-8')
        pat_lines = pat.readlines()
        last = pat_lines[-1]
        for st in unfollow_fsa_feed:
            splitted = st.split("\n")
            to_insert = pat_str.replace("(UNFOLLOW_PLACEHOLDER)", splitted[0])
            if len(splitted) > 1:
                for line in splitted[1:]:
                    to_insert += "\n" + " " * last.count(" ") + line
            patterns_placeholder_substituted.append(to_insert)

    unfollow_fsas = []
    for pattern_placeholder_substituted in patterns_placeholder_substituted:
        try:
            unfollow_fsas.append((Fsa(parser.parse(pattern_placeholder_substituted, with_ids=True, first_iter=True)),
                                  pattern_placeholder_substituted))
        except SyntaxError as e:
            print("ERROR PARSING PATTERN: ", end=' ')
            print(pattern_placeholder_substituted)
            print("error:")
            print(e)
            print(e.text)

    basic_fsas = []
    for basic in basic_fsa_feed:
        try:
            basic_fsas.append((Fsa(parser.parse(basic, with_ids=True, first_iter=True)), basic))
        except SyntaxError as e:
            print("ERROR PARSING PATTERN: ", end=' ')
            print(basic)
            print("error:")
            print(e)
            print(e.text)

    results = []
    results_blacklist = []
    results_unfollow = []
    for f in python_files:
        to_scan = open(f, 'r', encoding='utf-8')
        to_scan_read = to_scan.read()
        try:
            fsa_feed = parser.parse(to_scan_read, first_iter=True)
            to_scan.close()
            for fsa in blacklist_fsas:
                result_fsa = fsa[0].run(copy.deepcopy(fsa_feed))
                if result_fsa:
                    for r in result_fsa:
                        results_blacklist.append((Module(body=r), fsa[1]))
            for fsa in unfollow_fsas:
                result_fsa = fsa[0].run(copy.deepcopy(fsa_feed))
                if result_fsa:
                    for r in result_fsa:
                        results_unfollow.append((Module(body=r), fsa[1]))
            if not results_blacklist:
                for fsa in basic_fsas:
                    result = fsa[0].run(copy.deepcopy(fsa_feed))
                    if result:
                        for r in result:
                            results.append((Module(body=r), fsa[1]))
        except SyntaxError as e:
            print("ERROR: ", end='')
            print(f)
            print(e)
            print(e.text)

    # return results
    print("BASIC:")
    for res in results:
        print(res[1])
        print_program(res[0])
        print("\n")
    print("BLACKLIST:\n")
    for res in results_blacklist:
        print(res[1])
        print_program(res[0])
        print("\n")
    print("UNFOLLOW:\n")
    for res in results_unfollow:
        print(res[1])
        print_program(res[0])
    #   for x in basic_fsa_feed:
    #       print(x)
    #       print("\n")
    return results, results_blacklist, results_unfollow
