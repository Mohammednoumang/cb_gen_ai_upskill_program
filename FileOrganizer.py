from src.main.All_in_one.FileOrganize import FileOrganize
import sys

def main():
    fo = FileOrganize()
    filename = sys.argv[-1]
    fileReader = open(filename)
    curCmd = fileReader.__next__()
    while (curCmd!=None):
        # print(curCmd)
        fo.fileOrganize("C:/Users/nouma/Downloads/TEST/ONE", "C:/Users/nouma/Downloads/TEST/TWO")
        print("done")
        break

if __name__ == "__main__":
    main()