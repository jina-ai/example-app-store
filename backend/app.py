import os
from pprint import pprint
import pretty_errors
from jina import Flow, Document, DocumentArray
from jina.parsers.helloworld import set_hw_chatbot_parser
import csv
from backend_config import my_port, my_workdir, my_datafile
from executors import MyTransformer, MyIndexer


def trim_string(input_string, word_count=50, sep=" "):
    sanitized_string = input_string.replace("\\n", sep).replace("\\u2022", sep)
    words = sanitized_string.split(sep)[:word_count]
    output = " ".join(words)

    return output


def prep_docs(input_file):
    docs = DocumentArray()
    with open(input_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        input_field = "Description"
        for row in csv_reader:
            input_data = trim_string(row[input_field])
            doc = Document(text=input_data)
            doc.tags = row
            docs.extend([doc])

    return docs


def run_appstore(inputs, args):
    """
    Execute the app store example.
    """

    f = (
        Flow()
        .add(uses=MyTransformer, parallel=args.parallel)
        .add(uses=MyIndexer, workspace=args.workdir)
    )

    with f:
        f.post(on="/index", inputs=inputs, on_done=print)
        f.use_rest_gateway(args.port_expose)
        f.block()


if __name__ == "__main__":

    args = set_hw_chatbot_parser().parse_args()
    args.port_expose = my_port
    args.workdir = my_workdir

    docs = prep_docs(input_file=my_datafile)

    run_appstore(inputs=docs, args=args)
