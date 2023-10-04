import re
import os
import pandas as pd
from tqdm import tqdm
from q2 import download_audio, cut_audio
from typing import List
from q1 import contains_label


def filter_df(csv_path: str, label: str) -> pd.DataFrame:
    """
    Write a function that takes the path to the processed csv from q1 (in the notebook) and returns a df of only the rows 
    that contain the human readable label passed as argument

    For example:
    get_ids("audio_segments_clean.csv", "Speech")
    """
    # TODO
    df = pd.read_csv(f"{csv_path}")

    filtered_df = df[df["label_names"].str.split('|').apply(lambda x: label in x)]
    return filtered_df


def data_pipeline(csv_path: str, label: str) -> None:
    """
    Using your previously created functions, write a function that takes a processed csv and for each video with the given label:
    (don't forget to create the audio/ folder and the associated label folder!). 
    1. Downloads it to <label>_raw/<ID>.mp3
    2. Cuts it to the appropriate segment
    3. Stores it in <label>_cut/<ID>.mp3

    It is recommended to iterate over the rows of filter_df().
    Use tqdm to track the progress of the download process (https://tqdm.github.io/)

    Unfortunately, it is possible that some of the videos cannot be downloaded. In such cases, your pipeline should handle the failure by going to the next video with the label.
    """
    # TODO
    df = filter_df(csv_path, label)
    # remove whitespace and special characters from column names
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('#', '')

    # mkdir if not exists
    
    if not os.path.exists(f"{label}_raw"):
        os.makedirs(f"{label}_raw")
    if not os.path.exists(f"{label}_cut"):
        os.makedirs(f"{label}_cut")
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            download_audio(row["YTID"], f"{label}_raw/{row['YTID']}")
        except:
            continue
        try:
            cut_audio(f"{label}_raw/{row['YTID']}.mp3", f"{label}_cut/{row['YTID']}.mp3", row["start_seconds"], row["end_seconds"])
        except:
            continue

def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Suppose we now want to rename the files we've downloaded in `path_cut` to include the start and end times as well as length of the segment. While
    this could have been done in the data_pipeline() function, suppose we forgot and don't want to download everything again.

    Write a function that, using regex (i.e. the `re` library), renames the existing files from "<ID>.mp3" -> "<ID>_<start_seconds_int>_<end_seconds_int>_<length_int>.mp3"
    in path_cut. csv_path is the path to the processed csv from q1. `path_cut` is a path to the folder with the cut audio.

    For example
    "--BfvyPmVMo.mp3" -> "--BfvyPmVMo_20_30_10.mp3"

    ## BE WARY: Assume that the YTID can contain special characters such as '.' or even '.mp3' ##
    """
    # TODO
    df = pd.read_csv(csv_path)
    # remove whitespace and special characters from column names
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('#', '')

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            os.rename(f"{path_cut}/{row['YTID']}.mp3", f"{path_cut}/{row['YTID']}_{int(row['start_seconds'])}_{int(row['end_seconds'])}_{int(row['end_seconds']) - int(row['start_seconds'])}.mp3")
        except:
            continue



if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
