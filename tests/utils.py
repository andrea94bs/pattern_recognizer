from pathlib import *

if __name__ == '__main__':
    p ="C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset\\https___github_com_vicosurge_twitterino_bot"
    path_dir_1 = p
    p_dir_1 = Path(path_dir_1)
    files_1 = list(p_dir_1.glob("**/*.py"))

    words = ['follow', 'create', 'write', 'sleep', 'retweet', 'fav', 'dump', 'store', 'save', 'destroy', 'unfollow']

    for file in files_1:
        f = open(file, 'r', encoding='utf-8').read().lower()
        for word in words:
            if word in f:
                print(word)
                print(file)
