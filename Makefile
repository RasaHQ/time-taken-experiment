install:
	python -m pip install rasa==2.8.0 rich memo

data:
	python generate-files.py

train:
	python run-training.py

clean:
	rm -rf data
	rm -rf models
	rm traintimes.jsonl

stats:
	python make-stats.py

all: install data train stats
