import pathlib 
from clumper import Clumper 
from rich.table import Table
from rich.console import Console


from rasa.cli.utils import get_validated_path
from rasa.model import get_model, get_model_subdirectories
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.shared.nlu.training_data.message import Message 
from rasa.shared.nlu.constants import TEXT


console = Console()


def digits(s):
    """grab digits from string"""
    return str("".join([c for c in s if c.isdigit()]))


def load_interpreter(model):
    path_str = str(pathlib.Path(".") / model)
    model = get_validated_path(path_str, "model")
    model_path = get_model(model)
    _, nlu_model = get_model_subdirectories(model_path)
    return RasaNLUInterpreter(nlu_model)


def calculate_sparse_space(model_name):
    interpreter = load_interpreter(model_name).interpreter

    msg = Message(text="demo")
    for component in interpreter.pipeline:
        component.process(msg)

    seq_vecs, sen_vecs = msg.get_sparse_features(TEXT)
    console.log(f"model: {model_name} space: {seq_vecs.features.shape[1]}")

    return str(seq_vecs.features.shape[1])


stats = (Clumper
  .read_jsonl("traintimes.jsonl")
  .mutate(n=lambda d: digits(d["folder"]),
          setting=lambda d: "".join([s for s in d['folder'].replace("data/", "") if s.isalpha()]),
          epochs=lambda d: str(int(digits(d["config"]))),
          time_taken=lambda d: str(d["time_taken"]),
          space_taken=lambda d: str(calculate_sparse_space(d['model'])))
  .sort(lambda d: (d['setting'], int(d['n'])))
  .show()
  .select("setting", "n", "time_taken", "epochs", "space_taken")
  .collect())


table = Table(title="Stats")

table.add_column("Setting", style="cyan")
table.add_column("Datasize", justify="right", style="magenta")
table.add_column("Epochs", justify="right", style="blue")
table.add_column("Time Taken", style="green")
table.add_column("CV Feats", style="green")

for item in stats:
    table.add_row(item["setting"], item["n"], item["epochs"], item["time_taken"], item["space_taken"])


console.print(table)
