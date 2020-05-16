def main():
    filename = "My Clippings 0.txt"
    extract(filename)


def extract(file):
    clips = open("./Data/" + file, "r", encoding="UTF8")
    chunk = []
    for line in clips:
        if line == "==========\n":
            parse(chunk)
            chunk = []
        else:
            chunk.append(line)


def parse(chunk):
    print("Chunk:\n", chunk)
    pass


if __name__ == "__main__":
    main()
