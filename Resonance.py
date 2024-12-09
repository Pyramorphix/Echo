import pandas as pd

from parser import parse_data
from data_processing import process_data


def Resonance() -> None:

    # TODO: extract these from argparse

    raw_filename: str = "test"
    messenger: str = "Telegram"
    output_dir: str = "output"

    parse_data(raw_filename, messenger, output_dir) 

    data: pd.DataFrame = pd.read_csv(output_dir + "/data.csv")



    # Testing some stuff before making it clean
    # TODO: make these separate functions



    process_data(data)


