__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import click # For command line arguments
from backend_config import max_docs, datafile, port, workdir, model # Import basic settings

from executors.disk_indexer import DiskIndexer # Import disk-based Executor
from helper import prep_docs, deal_with_workspace # Import helper functions
from jina import Flow # To build Executors into a pipeline

try:
    __import__("pretty_errors") # Show nicer error output if pretty_errors package installed
except ImportError:
    pass


def index(num_docs: int = max_docs):
    """
    Build an index for your search
    :param num_docs: maximum number of Documents to index
    """
    # Build a Flow with 2 Executors, to encode and index the text
    flow = (
        Flow()
        .add(
            uses="jinahub+docker://TransformerTorchEncoder", # Download from Jina Hub
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50, # Maximum number of tokens to encode
        )
        .add(uses=DiskIndexer, workspace=workdir)
    )

    with flow:
        flow.post(
            on="/index",
            inputs=prep_docs(input_file=datafile, num_docs=num_docs), # Generator to create Documents from dataset
            request_size=64,
            read_mode="r",
        )


def query_restful():
    """
    Query your indexed data
    """
    flow = (
        Flow()
        .add(
            uses="jinahub+docker://TransformerTorchEncoder",
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50,
        )
        .add(uses=DiskIndexer, workspace=workdir, name="indexer")
    )

    with flow:
        flow.protocol = "http"  # Activate REST gateway
        flow.port_expose = port  # Set gateway port
        flow.block()  # Keep Flow open


# Set up command line arguments
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
        # Check if workspace with indexed data already exists. If so, warn user or delete
        deal_with_workspace(dir_name=workspace, should_exist=False, force_remove=force)

        # Run index fn
        index(num_docs=num_docs)

    if task == "query_restful":
        # Check if workspace with indexed data already exists. If not, warn user
        deal_with_workspace(dir_name=workspace, should_exist=True)

        # Run query fn
        query_restful()


if __name__ == "__main__":
    main()
