import random
import shutil
import sys
import os
import itertools
import csv
from typing import Generator
from jina import Document

from backend_config import (
    text_length,
    max_docs,
)


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


def prep_docs(input_file: str, num_docs: int = max_docs) -> Generator:
    """
    Create generator for every row in csv as a Document
    :param input_file: Input csv filename
    :return: Generator
    """

    with open(input_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        input_field = "Description"
        for row in itertools.islice(csv_reader, num_docs):
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

def deal_with_workspace(dir_name, should_exist: bool = False, force_remove: bool = False):
    if should_exist:
        if not os.path.isdir(dir_name): # It should exist but it doesn't exist
            print(
                f"The directory {dir_name} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)

    if not should_exist: # it shouldn't exist
        if os.path.isdir(dir_name):
            if not force_remove:
                print(
                    f"\n +----------------------------------------------------------------------------------+ \
                        \n |                                   🤖🤖🤖                                         | \
                        \n | The directory {dir_name} already exists. Please remove it before indexing again.  | \
                        \n |                                   🤖🤖🤖                                         | \
                        \n +----------------------------------------------------------------------------------+"
                )
                sys.exit(1)
            else:
                shutil.rmtree(dir_name)

