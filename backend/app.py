import os
import itertools
from pprint import pprint
from jina import Flow, Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap
from jina.parsers.helloworld import set_hw_chatbot_parser
import csv
from backend_config import backend_port, backend_workdir, backend_datafile, text_length, max_docs
from executors import MyTransformer, MyIndexer

try:
    __import__("pretty_errors")
except ImportError:
    pass


def trim_string(input_string: str, word_count: int = text_length, sep: str = " ") -> str:
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


def run_appstore_flow(inputs, args) -> None:
    """
    Execute the app store example. Indexes data and presents REST endpoint
    :param inputs: Documents or DocumentArrays to input
    :args: arguments like port, workdir, etc
    :return: None
    """

    # Create Flow and add
    #   - MyTransformer (an encoder Executor)
    #   - MyIndexer (a simple indexer Executor)
    flow = (
        Flow()
        .add(uses=MyTransformer, parallel=args.parallel)
        # .add(uses=EmbeddingIndexer)
        # .add(uses=KeyValueIndexer)
        .add(uses=MyIndexer, workspace=args.workdir)
    )
    # flow = Flow.load_config('flows/index.yml')

    # Open the Flow
    with flow:
        # Start index pipeline, taking inputs then printing the processed DocumentArray
        flow.post(on="/index", inputs=inputs)

        # Start REST gateway so clients can query via Streamlit or other frontend (like Jina Box)
        flow.use_rest_gateway(backend_port)

        # Block the process to keep it open. Otherwise it will just close and no-one could connect
        flow.block()


if __name__ == "__main__":

    # Get chatbot's default arguments
    args = set_hw_chatbot_parser().parse_args()

    # Change a few things
    args.workdir = backend_workdir

    # Convert the csv file to a DocumentArray
    docs = prep_docs(input_file=backend_datafile)

    # Run the Flow
    run_appstore_flow(inputs=docs, args=args)
