__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
import shutil
import sys
import click
from backend_config import (
    max_docs,
    datafile,
    port,
    workdir,
    model
)

from executors.disk_indexer import DiskIndexer
from helper import prep_docs
from jina import Flow

try:
    __import__("pretty_errors")
except ImportError:
    pass


def index(num_docs: int = max_docs):
    """
    Build an index for your search
    :param num_docs: maximum number of Documents to index
    """
    flow = (
        Flow()
        .add(
            uses="jinahub+docker://TransformerTorchEncoder",
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50,
        )
        .add(uses=DiskIndexer, workspace=workdir)
    )

    with flow:
        flow.post(
            on="/index",
            inputs=prep_docs(input_file=datafile, num_docs=num_docs),
            request_size=64,
            read_mode="r",
        )


def query_restful():
    """
    Query your index
    """
    flow = (
        Flow()
        .add(
            uses="jinahub+docker://TransformerTorchEncoder",
            pretrained_model_name_or_path="sentence-transformers/msmarco-distilbert-base-v3",
            name="encoder",
            max_length=50,
        )
        .add(uses=DiskIndexer, workspace=workdir)
    )

    with flow:
        flow.protocol = "http"
        flow.port_expose = port
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query_restful"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=max_docs)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, force: bool):
    workspace = workdir
    if task == "index":
        if os.path.exists(workspace):
            if force:
                shutil.rmtree(workspace)
            else:
                print(
                    f"\n +----------------------------------------------------------------------------------+ \
                        \n |                                   🤖🤖🤖                                         | \
                        \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                        \n |                                   🤖🤖🤖                                         | \
                        \n +----------------------------------------------------------------------------------+"
                )
                sys.exit(1)
        index(num_docs=num_docs)
    if task == "query_restful":
        if not os.path.exists(workspace):
            print(
                f"The directory {workspace} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)
        query_restful()


if __name__ == "__main__":
    main()
