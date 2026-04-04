import sys


def read_source(source_file):
    with open(source_file, "r") as f:
        return f.read()


if __name__ == "__main__":
    source = read_source(sys.argv[1])
    print(source)
