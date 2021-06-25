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
    backend_model,
)

from executors.disk_indexer import DiskIndexer
from executors.rankers import ReviewRanker
from executors.encoders import MyTransformer
import random

from jina import Flow, Document

try:
    __import__("pretty_errors")
except ImportError:
    pass


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


def prep_docs(input_file: str, max_docs:int=max_docs):
    """
    Create generator for every row in csv as a Document
    :param input_file: Input csv filename
    :return: Generator
    """

    with open(input_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        input_field = "Description"
        for row in itertools.islice(csv_reader, max_docs):
            # Fix invalid ratings and counts
            if row["Average User Rating"] == "":
                row["Average User Rating"] = random.uniform(0.0, 5.0)
            if row["User Rating Count"] == "":
                row["User Rating Count"] = random.randint(10, 10_000)
            # Set field to encode and index
            input_data = trim_string(f"{row['Name']} - {trim_string(row[input_field])}")
            # Put all of that into a doc
            doc = Document(text=input_data)
            doc.tags = row
            yield doc


def index():
    flow = (
        Flow()
        # .add(uses='jinahub+docker://TransformerTorchEncoder', pretrained_model_name_or_path="sentence-transformers/msmarco-distilbert-base-v3", name="encoder", max_length=50)
        .add(
            uses=MyTransformer,
            pretrained_model_name_or_path=backend_model,
            name="encoder",
        ).add(uses=DiskIndexer, workspace=backend_workdir, name="indexer")
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
        # .add(uses='jinahub+docker://TransformerTorchEncoder', pretrained_model_name_or_path="sentence-transformers/msmarco-distilbert-base-v3", name="encoder", max_length=50)
        .add(
            uses=MyTransformer,
            pretrained_model_name_or_path=backend_model,
            name="encoder",
        ).add(uses=DiskIndexer, workspace=backend_workdir, name="indexer")
        # .add(uses=ReviewRanker, name="ranker")
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
    workspace = backend_workdir
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
