from builtins import SyntaxError
from pathlib import *
from fsa.Fsa2 import *
from parse_regex import parser


def run_pauses():
    # GET PROJECT PATH
    path = 'C:\\Users\\Andrea\\PycharmProjects\\inspect_def\\' + input("Inserisci percorso progetto: ").replace("/",
                                                                                                                "\\")
    p = Path(path)

    python_files = []
    python_files += list(p.glob("**/*.py"))

    all_files = []
    types = ["**/*.py", "**/*.txt", "**/*.json", "**/*.cfg"]
    for t in types:
        all_files += list(p.glob(t))

    path_pause_patterns = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\generic"
    p_pause_patterns = Path(path_pause_patterns)
    pause_files = list(p_pause_patterns.glob("*"))

    path_pause_large = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\large"
    p_pause_large = Path(path_pause_large)
    pauses_large_file = list(p_pause_large.glob("*"))

    path_pause_little = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\little"
    p_pause_little = Path(path_pause_little)
    pauses_little_file = list(p_pause_little.glob("*"))

    path_time_little = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\time_assignment_little"
    p_time_little = Path(path_time_little)
    time_little_file = list(p_time_little.glob("*"))

    path_time_large = "C:\\Users\\Andrea\\PycharmProjects\\Patterns\\pause_pattern\\time_assignment_large"
    p_time_large = Path(path_time_large)
    time_large_file = list(p_time_large.glob("*"))

    pauses_large_strings = []
    for pauses_large in time_large_file:
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
                            # print("NEW PATTERN FOR GETTING TWEETS:")
                            # print(pattern_assign)
                            if new_pattern not in pauses_large_strings:
                                pauses_large_strings.append(new_pattern)
                except SyntaxError as e:
                    print("ERROR PARSING ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING ")
            print(new_pattern)
            print("error:")
            print(e)
            print(e.text)
    for p in pauses_large_file:
        file = open(p, 'r', encoding='utf-8')
        pauses_large_strings.append(file.read())



    pauses_little_strings = []
    for pauses_little in time_little_file:
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
                except SyntaxError as e:
                    print("ERROR PARSING ")
                    print(f)
                    print("error:")
                    print(e)
                    print(e.text)
        except SyntaxError as e:
            print("ERROR PARSING ")
            print(new_pattern)
            print("error:")
            print(e)
            print(e.text)
    for p in pauses_little_file:
        file = open(p, 'r', encoding='utf-8')
        pauses_little_strings.append(file.read())

    generic_pauses = []
    for pause in pause_files:
        file = open(pause, 'r', encoding='utf-8')
        generic_pauses.append(file.read())


    constraint_strings = []
    for pause in generic_pauses:
        constraint_strings.append("if _VAR_1 < _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
        constraint_strings.append("if _VAR_1 <= _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
        constraint_strings.append("if _VAR_1 >= _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
        constraint_strings.append("if _VAR_1 > _VAR_2 and EVERY:\n\t_STAT_MULTI_\n\t" + pause)
    for little in pauses_little_strings:
        constraint_strings.append(little)

    mimic_fsas = []
    for pause_string in pauses_large_strings:
        try:
            mimic_fsas.append(
                (Fsa(parser.parse(pause_string, first_iter=True, with_ids=True)), pause_string))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(pause_string)
            print("error:")
            print(e)
            print(e.text)

    constraint_fsas = []
    for constraint_string in constraint_strings:
        try:
            constraint_fsas.append(
                (Fsa(parser.parse(constraint_string, first_iter=True, with_ids=True)), constraint_string))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(constraint_string)
            print("error:")
            print(e)
            print(e.text)

    generic_fsas = []
    for generic_pause in generic_pauses:
        try:
            generic_fsas.append(
                (Fsa(parser.parse(generic_pause, first_iter=True, with_ids=True)), generic_pause))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(generic_pause)
            print("error:")
            print(e)
            print(e.text)

    mimic_results = []
    constraint_results = []
    generic_results  = []
    for f in python_files:
        fi = open(f, 'r', encoding='utf-8')
        feed = fi.read()
        try:
            feed_tree = parser.parse(feed, first_iter=True, with_ids=False)
            for fsa in mimic_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    mimic_results.append((Module(body=res), fsa[1]))
            for fsa in constraint_fsas:
                result = fsa[0].run(feed_tree)
                for res in result:
                    constraint_results.append((Module(body=res), fsa[1]))
            if not mimic_results and not constraint_results:
                for fsa in generic_fsas:
                    result = fsa[0].run(feed_tree)
                    for res in result:
                        generic_results.append((Module(body=res), fsa[1]))
        except SyntaxError as e:
            print("ERROR PARSING: ")
            print(f)
            print("error:")
            print(e)
            print(e.text)

    print("MIMIC:")
    for res in mimic_results:
        print_program(res[0])
        print("\n")
        print(res[1])
        pass

    print("CONSTRAINTS:")
    for res in constraint_results:
        print_program(res[0])
        print("\n")
        print(res[1])

    print("GENERIC:")
    for res in generic_results:
        print_program(res[0])
        print("\n")
        print(res[1])
