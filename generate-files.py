import pathlib 
import subprocess

import pandas as pd
from rich.console import Console
from taipo.common import dataframe_to_nlu_file

df = pd.read_csv('outofscope-intent-classification-dataset.csv')

def remove_outliers(df):
    return df.loc[lambda d: d['label'] != 'oos']

def add_label_row_number(df):
    return (df
        .assign(n=1, label_row_id=lambda d: d.groupby("label")
        .transform(lambda d: d.cumsum())['n'])
        .drop(columns=['n'])
    )

if __name__ == "__main__":
    console = Console()
    console.log("starting.")
    df_tagged = df.pipe(remove_outliers).pipe(add_label_row_number)

    for size in [10, 25, 50]:
        write_df = df_tagged.loc[lambda d: d['label_row_id'] <= size].assign(intent=lambda d: d['label'])
        clean_write_paths = [f"data/clean-{size}/clean.yml", f"data/typod-{size}/clean.yml", f"data/dupli-{size}/clean.yml"]

        # First create the normal .yml files
        for path in clean_write_paths:
            pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
            dataframe_to_nlu_file(write_df, path)
            console.log(f"created {path}")
        
        # Next, create the typo .yml files
        cmd = f"python -m taipo keyboard augment data/typod-{size}/clean.yml data/typod-{size}/typod.yml"
        subprocess.run(cmd.split(" "))
        console.log(f"created data/typod-{size}/typod.yml")

        # Finally, create the duplicated.yml files
        concat_df = write_df.assign(text=lambda d: ["stopword " + t for t in d['text']])
        dataframe_to_nlu_file(concat_df, f"data/dupli-{size}/clean.yml")
        console.log(f"created data/dupli-{size}/dupli.yml")
    console.log("done!")
