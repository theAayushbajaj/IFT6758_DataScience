import json
import pandas as pd


def count_labels(labels: str) -> int:
    """
    Given a string of unparsed labels, return the number of distinct labels.

    For example:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> 3
    """
    # TODO
    return len(labels.split(","))


def convert_id(ID: str) -> str:
    """
    Create a function that takes in a label ID (e.g. "/m/09x0r") and returns the corresponding label name (e.g. "Speech")

    To do so, make use of the `json` library and the `data/ontology.json` file, a description of the file can be found
    at https://github.com/audioset/ontology

    While reading the file each time and looping through the elements to find a match works well enough for our
    purposes, think of ways this process could be sped up if say this function needed to be run 100000 times.
    """
    # TODO
    file_location = "data/ontology.json"
    with open(file_location, 'r') as file:
        ontology_json = json.load(file)
        for element in ontology_json:
            if element["id"] == ID:
                return element["name"]           
    return None

def convert_ids(labels: str) -> str:
    """
    Using convert_id() create a function that takes the label columns (i.e a string of comma-separated label IDs)
    and returns a string of label names, separated by pipes "|".

    For example:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> "Music|Skateboard|Speech"
    """
    # TODO
    Ids = labels.split(",")
    names = [convert_id(id) for id in Ids]
    return "|".join(names)


def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Create a function that takes a Series of strings where each string is formatted as above 
    (i.e. "|" separated label names like "Music|Skateboard|Speech") and returns a Series with just
    the values that include `label`.

    For example, given the label "Music" and the following Series:
    "Music|Skateboard|Speech"
    "Voice|Speech"
    "Music|Piano"

    the function should just return
    "Music|Skateboard|Speech"
    "Music|Piano"

    WARNING: Using .contains is not enough here
    """
    # TODO
    filtered_series = labels[labels.str.split('|').apply(lambda x: label in x)]
    return filtered_series


def get_conditional_proportion(labels: pd.Series, label_1: str, label_2: str) -> float:
    """
    Create a function that, given a Series as described above, returns the proportion of rows
    with label_1 that also have label_2. Make use of the function you created above.

    For example, suppose the Series has 1000 values, of which 120 have label_1. If 30 of the 120
    have label_2, your function should return 0.25.
    """
    # TODO
    label_1_series = contains_label(labels, label_1)

    # Filter the label_1 series for rows containing label_2
    label_1_and_label_2_series = contains_label(label_1_series, label_2)

    # Calculate the proportion
    proportion = float(len(label_1_and_label_2_series) / len(label_1_series))# if len(label_1_series) > 0 else 0.0

    return proportion


if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])
    print(contains_label(series, "Music"))
    print(get_conditional_proportion(series, "Music", "Piano"))
