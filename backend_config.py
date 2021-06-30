# in executors.py
model = "sentence-transformers/msmarco-distilbert-base-v3" # Language model will we use to "understand" the text
top_k = 10 # How many results will a query return?

# in app.py
port = 45678 # Port for REST query gateway
workdir = "workspace" # Directory where we will store the index
datafile = "./data/appstore_games-shuffled.csv" # Processed datafile
text_length = 50 # How many words to index for each app? Longer = more accurate, shorter = quicker
max_docs = 3000 # How many apps to index. Can override with "-n" flag

# dataset
dataset_url = "https://github.com/alexcg1/ml-datasets/blob/master/nlp/strategy_games/appstore_games.csv?raw=true" # URL to download dataset
dataset_filename = 'appstore_games.csv' # Original dataset filename
random_seed = 42 # Ensure we can replicate shuffling so we get consistent results
