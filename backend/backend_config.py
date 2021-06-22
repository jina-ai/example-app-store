# in executors.py
backend_model = "sentence-transformers/msmarco-distilbert-base-v3"
backend_top_k = 10

# in app.py
backend_port = 45678
backend_workdir = "workspace"
backend_datafile = "./data/appstore_games-shuffled.csv"
text_length = 50 # How many words to index for each app? Longer = more accurate, shorter = quicker
max_docs = 100 # How many apps to index
random_seed = 42 # Ensure we can replicate shuffling so we get consistent results

# dataset
dataset_url = "https://github.com/alexcg1/ml-datasets/blob/master/nlp/strategy_games/appstore_games.csv?raw=true" 
dataset_filename = 'appstore_games.csv'
