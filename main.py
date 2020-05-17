def main():
    filename = "My Clippings.txt"
    data = extract(filename)
    # Can sort by Book, Author, or None. Date, Location, and Clip are unpredictable
    write(data, sort_by="Book", remove_duplicates=True)


def extract(file: str) -> list:
    """
    Parses Kindle Clippings Text File into list of dictionaries
    :param file: Clippings Source
    :return: list of dictionaries of clip data
    """
    # TODO: Extract context from book - this will probably be difficult :)
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
    *location, date = loc_and_date.split(" | ")
    location = " | ".join([loc.strip("- Highlight Bookmark Loc.") for loc in location])
    date = date.strip("Added on")
    # The below logic handles clips from books with no noted author
    book, author = (l[0].strip(" "), l[-1].strip(")")) if len(l := book_and_auth.split("(")) >= 2 else (l[0], "")
    return {"Book": book, "Author": author, "Date": date, "Location": location, "Clip": clip}


def sort_clips(data: list, param="Book") -> list:
    """
    Sorting first by dates would be a little bit more complicated,
    but Python sorts are guaranteed to be stable, so as long as the data was originally ordered
    (which it is, coming from the Kindle text file), we don't have to worry about it!
    :param param: field by which to sort the clips. None results in an unchanged list
    :param data: list of clip data dictionaries
    :return: sorted list of clip data dictionaries
    """
    if param is None:
        return data
    return sorted(data, key=lambda d: d[param])


def write(data: list, filename: str = "out.csv", sort_by: str = "Book", remove_duplicates: bool = True) -> None:
    """
    Writes results to file
    :param sort_by:
    :param remove_duplicates: filter out duplicates? Takes a little longer and ASSUMES A SORTED LIST
    :param data: list of clip data dictionaries
    :param filename: location of output
    :return: True if successful
    """
    if remove_duplicates:
        data = sort_clips(data, param="Book")
    out = open("./data/" + filename, "w", encoding="UTF8")
    items = ["Book", "Author", "Date", "Location", "Clip"]
    out.write(",".join(items) + "\n")   # Writing header
    if remove_duplicates:
        prev = "Lorem Ipsum"
        skips = []
        for i, clip in enumerate(data):  # Writing each clip
            # Replacing (double quotes -> single quotes), (commas -> semicolons), (newlines -> '\n')
            # This is bad practice, modifying data in place. Save space, and I'm being careful (I think :))
            clip["Clip"] = clip["Clip"].replace("\"", "\'").replace(",", ";").replace("\n", "\\n")
            if clip["Clip"] in prev:
                skips.append(i)
            elif prev in clip["Clip"]:
                skips.append(i - 1)
            else:
                prev = clip["Clip"]
        for clip in sort_clips([clip for i, clip in enumerate(data) if i not in skips], param=sort_by):
            line = ",".join(clip[item].replace(",", ";") for item in items) + "\n"
            out.write(line)

    else:
        for clip in data:   # Writing each clip
            # Replacing (double quotes -> single quotes), (commas -> semicolons), (newlines -> '\n')
            msg = clip["Clip"].replace("\"", "\'").replace(",", ";").replace("\n", "\\n")
            line = ",".join(clip[item].replace(",", ";") for item in items[:-1]) + "," + msg + "\n"
            out.write(line)

    out.close()


if __name__ == "__main__":
    main()
