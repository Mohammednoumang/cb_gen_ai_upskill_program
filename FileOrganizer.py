import sys

def main():
    filename = sys.argv[-1]
    fileReader = open(filename)
    curCmd = fileReader.__next__()
    while (curCmd!=None):
        print(curCmd)
        break

if __name__ == "__main__":
    main()