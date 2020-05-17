def main():
    filename = "My Clippings.txt"
    data = extract(filename)
    write(data)


def extract(file: str) -> list:
    """
    Parses Kindle Clippings Text File into list of dictionaries
    :param file: Clippings Source
    :return: list of dictionaries of clip data
    """
    # TODO: Implement sorting by book or time
    clips = open("./Data/" + file, "r", encoding="UTF8")
    chunk = []  # Information for one clip
    data = []   # Collected clips data
    for line in clips:
        if line == "==========\n":  # Clip delimeter
            if (res := parse(chunk)) != {}:     # If the clip was only whitespace, skip it
                data.append(res)
            chunk = []
        else:
            chunk.append(line)      # Accrue lines until the delimeter
    return data


def parse(chunk: list) -> dict:
    """
    Unpacks and cleans up the clip data
    :param chunk: list of the relevant clip data
    :return: dictionary of the clip data
    """
    book_and_auth, loc_and_date, _, *clip = (item.strip(" \n") for item in chunk)
    if len(clip := "\n".join(clip).strip(" \n")) == 0:  # Empty Clips
        return {}
    *loc, date = loc_and_date.split(" | ")
    loc = " | ".join([l.strip("- Highlight Bookmark Loc.") for l in loc])
    date = date.strip("Added on")
    # The below logic handles clips from books with no noted author
    book, author = (l[0].strip(" "), l[-1].strip(")")) if len(l := book_and_auth.split("(")) >= 2 else (l[0], "")
    return {"Book": book, "Author": author, "Date": date, "Location": loc, "Clip": clip}


def write(data: list, filename: str = "out.csv") -> bool:
    """
    Writes results to file
    :param data: list of clip data dictionaries
    :param filename: location of output
    :return: True if successful
    """
    # TODO: Filter duplicates?
    out = open("./data/" + filename, "w", encoding="UTF8")
    items = ["Book", "Author", "Date", "Location", "Clip"]
    out.write(",".join(items) + "\n")   # Writing header
    for clip in data:   # Writing each clip
        # Replacing (double quotes -> single quotes), (commas -> semicolons), (newlines -> '\n')
        msg = clip["Clip"].replace("\"", "\'").replace(",", ";").replace("\n", "\\n")
        out.write(",".join(clip[item].replace(",", ";") for item in items[:-1]) + "," + msg + "\n")
    out.close()
    return True


if __name__ == "__main__":
    main()
