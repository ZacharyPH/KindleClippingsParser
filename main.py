def main():
    filename = "My Clippings 1.txt"
    extract(filename)


def extract(file):
    # TODO: Implement sorting by book or time
    clips = open("./Data/" + file, "r", encoding="UTF8")
    chunk = []
    data = []
    for line in clips:
        if line == "==========\n":
            if (res := parse(chunk)) != {}:
                data.append(res)
            chunk = []
        else:
            chunk.append(line)
    write(data)


def parse(chunk):
    book_and_auth, loc_and_date, _, *clip = (item.strip(" \n") for item in chunk)
    if len(clip := "\n".join(clip).strip(" \n")) == 0:
        print("Empty clip...")
        return {}
    *loc, date = loc_and_date.split(" | ")
    loc = " | ".join([l.strip("- Highlight Bookmark Loc.") for l in loc])
    date = date.strip("Added on")
    book, author = (l[0].strip(" "), l[-1].strip(")")) if len(l := book_and_auth.split("(")) >= 2 else (l[0], "")
    return {"Book": book, "Author": author, "Date": date, "Location": loc, "Clip": clip}


def write(data, filename="out1.csv"):
    # TODO: Filter duplicates
    out = open("./data/" + filename, "w", encoding="UTF8")
    items = ["Book", "Author", "Date", "Location", "Clip"]
    out.write(",".join(items) + "\n")
    for clip in data:   # TODO: Cleanup .split / .join pairs with .replace for escaping commas
        msg = clip["Clip"].replace(",", "\\,").replace("\"", "\'")
        if len(msg.strip(" ")) == 0:    # Empty clip
            continue    # TODO: Now obsolete, I think
        out.write(",".join(clip[item].replace(",", "\\,") for item in items[:-1]) + "," + msg + "\n")
    out.close()


if __name__ == "__main__":
    main()
