import pandas as pd

from parser import parse_data
from setup import setup_output_dir
from data_processing import process_data
from report_generation import generate_report


def Resonance() -> None:

    # TODO: extract these from argparse

    raw_filename: str = "test"
    messenger: str = "Telegram"
    output_dir: str = "output"

    print("Setting up the output directory...")

    setup_output_dir(output_dir)

    print("Done.")


    parse_data(raw_filename, messenger, output_dir) 

    data: pd.DataFrame = pd.read_csv(output_dir + "/data.csv")



    final_data = process_data(data, output_dir)



    generate_report(final_data, output_dir)





