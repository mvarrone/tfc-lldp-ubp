import os
import shutil
import sys


def deploy():
    path1 = "D://Documentos//Mati//tfc//frontend//dist"  # compiled dist folder
    path2 = "C://nginx-1.21.6//projects//tfc//dist"  # nginx project folder

    value_1 = os.path.isdir(path1)
    if not value_1:
        print("\ndist folder not found at tfc/frontend\n")
        sys.exit(0)

    value_2 = os.path.isdir(path2)
    if value_2:
        mydir = path2
        try:
            shutil.rmtree(mydir)
            shutil.move(path1, path2)
            print("\nDone\n")
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        try:
            result = shutil.move(path1, path2)
            print("\nDone\n")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    deploy()
