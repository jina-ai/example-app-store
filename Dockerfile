FROM jinaai/jina:2.0-py38

ARG docs_to_index=100

COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get -y install wget git && pip install -r requirements.txt && python get_data.py && python app.py -t index -n $docs_to_index

ENTRYPOINT ["python", "app.py" , "-t", "query_restful"]

LABEL author="Alex C-G (alex.cg@jina.ai)"
LABEL type="app"
LABEL kind="example"
LABEL avatar="None"
LABEL description="App store example using Jina"
LABEL documentation="https://github.com/alexcg1/jina-app-store-example"
LABEL keywords="[NLP, app store, text, jina, example, search, transformers, torch]"
LABEL license="apache-2.0"
LABEL name="jina-appstore-search"
LABEL platform="linux/amd64"
LABEL update="None"
LABEL url="https://github.com/alexcg1/jina-app-store-example"
LABEL vendor="Jina AI Limited"
LABEL version="0.6.6"
