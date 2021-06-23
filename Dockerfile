FROM pytorch/pytorch:latest

COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt

WORKDIR "backend"

RUN python get_data.py

ENTRYPOINT ["python", "app.py"]

LABEL author="Alex C-G (alex.cg@jina.ai)"
LABEL type="app"
LABEL kind="example"
LABEL avatar="None"
LABEL description="App store example using Jina"
LABEL documentation="https://github.com/alexcg1/jina-app-store-example"
LABEL keywords="[NLP, app store, text, jina, example, search]"
LABEL license="apache-2.0"
LABEL name="jina-appstore-search-5k"
LABEL platform="linux/amd64"
LABEL update="None"
LABEL url="https://github.com/alexcg1/jina-app-store-example"
LABEL vendor="Jina AI Limited"
LABEL version="0.4.1"
