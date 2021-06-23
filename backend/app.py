__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
import itertools
import csv
import shutil
import click
import sys
from backend_config import (
    text_length,
    max_docs,
    backend_datafile,
    backend_port,
    backend_workdir,
)
from executors import MyTransformer, DiskIndexer

from jina import Flow, Document

try:
    __import__("pretty_errors")
except ImportError:
    pass

os.environ["JINA_WORKSPACE"] = backend_workdir
os.environ["JINA_PORT"] = os.environ.get("JINA_PORT", str(backend_port))


def trim_string(
    input_string: str, word_count: int = text_length, sep: str = " "
) -> str:
    """
    Trim a string to a certain number of words.
    :param input_string: string to trim
    :param word_count: how many words to trim to
    :param sep: separator between words
    :return: trimmmed string
    """
    sanitized_string = input_string.replace("\\n", sep)
    words = sanitized_string.split(sep)[:word_count]
    trimmed_string = " ".join(words)

    return trimmed_string


def prep_docs(input_file: str, max_docs=max_docs):
    """
    Create DocumentArray consisting of every row in csv as a Document
    :param input_file: Input csv filename
    :return: populated Document Generator
    """

    with open(input_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        input_field = "Description"
        for row in itertools.islice(csv_reader, max_docs):
            input_data = trim_string(row[input_field])
            doc = Document(text=input_data)
            doc.tags = row
            yield doc


indexer_executor = DiskIndexer


def index():
    flow = (
        Flow()
        .add(uses=MyTransformer, parallel=1, name="encoder")
        .add(uses=indexer_executor, workspace=backend_workdir, name="indexer")
    )

    with flow:
        flow.post(
            on="/index",
            inputs=prep_docs(input_file=backend_datafile, max_docs=max_docs),
            request_size=64,
            read_mode="r",
        )


def query_restful():
    flow = (
        Flow()
        .add(uses=MyTransformer, name="encoder")
        .add(uses=indexer_executor, workspace=backend_workdir, name="indexer")
    )

    with flow:
        flow.protocol = "http"
        flow.port_expose = backend_port
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
    workspace = os.environ["JINA_WORKSPACE"]
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
        index()
    if task == "query_restful":
        if not os.path.exists(workspace):
            print(
                f"The directory {workspace} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)
        query_restful()


if __name__ == "__main__":
    main()
