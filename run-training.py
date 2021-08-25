import time
import datetime as dt
import pathlib
from argparse import Namespace
from memo import memfile, memlist

from rich.console import Console
from rasa.model_training import train_nlu

data = []


@memfile("traintimes.jsonl")
@memlist(data)
def run_training(folder, config):
    stamp = dt.datetime.now()
    tic = time.time()
    train_nlu(config=config, nlu_data=folder, output=f"model-{folder}.tar.gz")
    toc = time.time() 
    return {'time_taken': toc - tic, 'timestamp': str(stamp), 'model': f"model-{folder}.tar.gz"}


if __name__ == "__main__": 
    console = Console()
    console.log("starting.")

    for folder in pathlib.Path("data").glob("*"):
        for config in pathlib.Path(".").glob("config*.yml"):
            console.log(f"training folder {folder} with {config} file.")
            run_training(folder=str(folder), config=str(config))
    console.log("done!")
    console.log(data)
