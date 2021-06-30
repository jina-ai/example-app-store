# AI-powered app store search

![](./video.gif)

This is a simple example to show how to build an AI-powered search engine for an app store using the [Jina](https://github.com/jina-ai/jina/) framework. It indexes and searches a subset of the [17K Mobile Strategy Games dataset](https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games) from Kaggle.

## Instructions

### Prerequisites

- You have a Mac or Linux system
- You have Python 3.7 or later installed, and have some basic Python knowledge
- You understand basic git and terminal usage

### Clone this repo

```shell
git clone git@github.com:alexcg1/jina-app-store-example.git
cd jina-app-store-example
```

### Create a virtual environment

We wouldn't want our project clashing with our system libraries, now would we?

```shell
virtualenv env --python=python3.8 # Python versions >= 3.7 work fine
source env/bin/activate
```

### Install everything

Make sure you're in your virtual environment first!

```shell
pip install -r requirements.txt
```

### Increase your swap space (optional)

We're dealing with big language models and quite long text passages. Macs can apparently dynamically allocate swap space, but on Manjaro Linux I manually created and activated a swapfile. Otherwise my computer with 16gb of RAM will just freeze up while indexing.

```shell
# Don't bother if you're on a Mac or have loads of memory
cd /tmp
dd if=/dev/zero of=swapfile bs=1M count=10240 status=progress
chmod 600 swapfile
mkswap swapfile
swapon swapfile
```

You'll need to do this after every reboot. Or you can [read the instructions](https://wiki.archlinux.org/title/Swap#Manually) to mount it at startup.

### Download dataset

```shell
python get_data.py
```

This command creates a directory called `data` and downloads the [17K Mobile Strategy Games dataset](https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games) into it. It then shuffles it to ensure we get a diverse range of apps to search through.

💡 **Tip**: We shuffle using a fixed random seed of `42`, so every shuffle will be the same. Want a different shuffle? Change it in [`backend_config.py`](./backend/backend_config.py)

### Index your data

```shell
python app.py -t index -n 1000
```

💡 **Tip**: Use `-n` to specify number of apps to index

### Search your data

`app.py` accepts an input query via a REST gateway:

```shell
python app.py -t query_restful
```

### Start the front end

In another terminal:

```sh
git clone https://github.com/alexcg1/jina-app-store-frontend.git
cd jina-app-store-frontend
virtualenv env
source env/bin/activate
pip install -r requirements.txt
streamlit app.py
```

Then open http://localhost:8501 in your browser

### Search from the terminal

```shell
curl --request POST -d '{"top_k":10,"mode":"search","data":["hello world"]}' -H 'Content-Type: application/json' 'http://0.0.0.0:45678/search'
```

Where `hello world` is your query.

The results should be a big chunk of JSON containing the matching apps. Or at least something close to matching. By default we're only indexing 1,000 apps from a list that's a few years old (since this is just an example) so don't be surprised if your search for a specific title doesn't come up.

💡 **Tip**: For cleaner formatting, pipe the contents of the above command into [`jq`](https://stedolan.github.io/jq/) by adding `| jq` to the end of the command.

## FAQ

### Why this dataset?

It contains a lot of metadata, including (working) links to icons. I want to build a nice front-end to show off the search experience so graphical assets are vital. Plus stuff like ratings, descriptions, the works.

### The download/purchase buttons don't do anything

This is just a demo search engine. It has no functionality beyond that. 

### How can I change basic settings?

Edit `backend/backend_config.py`

### What are all these files?

After cloning, downloading the dataset and indexing data, you'll see a lot of files. We're only concerned about the `backend` folder since that's where all the Jina magic happens. Don't worry if you don't see all of these right away. Sometimes they'll only appear after downloading the dataset or indexing.

|       | Filename                      | What is it?                                       |
|-------|-------------------------------|---------------------------------------------------|
| 📂    | `data`                        | Folder for storing downloaded dataset             |
| -- 📄 | `appstore_games.csv`          | Original dataset                                  |
| -- 📄 | `appstore_games_shuffled.csv` | Processed dataset that we'll index                |
| 📂    | `executors`                   | Folder to store Executors we write ourself        |
| -- 📄 | `disk_indexer.py`             | Executor to build an on-disk index                |
| 📂    | `workspace`                   | Folder to store indexed data                      |
| 📄    | `app.py`                      | Our main program file                             |
| 📄    | `backend_config.py`           | Basic config settings                             |
| 📄    | `get_data.py`                 | Script to retrieve dataset                        |
| 📄    | `helper.py`                   | Helper functions go here to ensure clean `app.py` |

You may also see several `__pycache__` folders with `.pyc` files. Don't worry about these. [They're explained here](https://stackoverflow.com/a/16869074) if you really want to know.


