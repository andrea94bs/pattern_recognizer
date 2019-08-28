from git import Repo

list = open("C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset13.txt")
i = 0

for url in list.readlines():
    try:
        Repo.clone_from(url.strip(),
                        "C:\\Users\\Andrea\\Documents\\University\\Magistrale\\Tesi\\Bot\\Patterns_test\\dataset\\" + url.replace(
                            "/", "_").replace(":", "_").replace("-", "_").replace(".", "_").strip()
                        )
        i += 1
    except Exception as e:
        print("error cloning " + url)
        print(e)
