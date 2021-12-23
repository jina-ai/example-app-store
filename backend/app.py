__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import click
from config import max_docs, datafile, port, workdir, MODEL

from helper import prep_docs, deal_with_workspace
from jina import Flow

try:
    __import__("pretty_errors")
except ImportError:
    pass

flow = (
    Flow()
    .add(
        name="encoder",
        # uses="jinahub://SpacyTextEncoder/v0.3",
        uses="jinahub://TransformerTorchEncoder/v0.3",
        # uses_with={"model_name": MODEL},
        install_requirements=True,
        force=True
    )
    .add(
        name="indexer",
        uses="jinahub://SimpleIndexer/v0.11",
        uses_with={"index_file_name": "index"},
        install_requirements=True,
        force=True
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
            show_progress=True
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
