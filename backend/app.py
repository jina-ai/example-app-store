__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import click
from config import max_docs, datafile, port, workdir

from helper import prep_docs, deal_with_workspace
from jina import Flow

try:
    __import__("pretty_errors")
except ImportError:
    pass

flow = (
    Flow()
    .add(
        name="app_store_encoder",
        uses="jinahub://TransformerTorchEncoder",
        install_requirements=True
    )
    .add(
        name="app_store_indexer",
        uses="jinahub://SimpleIndexer/",
        uses_with={"index_file_name": "index", "default_top_k": 12},
        # uses_metas={"workspace": "workspace"},
        volumes="./workspace:/workspace/workspace",
        install_requirements=True
    )
)

def index(num_docs: int = max_docs):
    """
    Build an index for your search
    :param num_docs: maximum number of Documents to index
    """

    with flow:
        flow.post(
            on="/index",
            inputs=prep_docs(input_file=datafile, num_docs=num_docs),
            request_size=64,
            read_mode="r",
        )


def search():
    """
    Query your index
    """
    with flow:
        flow.protocol = "http"
        flow.port_expose = port
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=max_docs)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, force: bool):
    if task == "index":
        deal_with_workspace(dir_name=workdir, should_exist=False, force_remove=force)
        index(num_docs=num_docs)

    if task == "search":
        deal_with_workspace(dir_name=workdir, should_exist=True)
        search()


if __name__ == "__main__":
    main()
