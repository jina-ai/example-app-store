import os
from pprint import pprint
import pretty_errors
from jina.types.arrays.memmap import DocumentArrayMemmap
from jina import Flow, Document, DocumentArray
from jina.parsers.helloworld import set_hw_chatbot_parser
import csv
from appstore_config import my_port, my_workdir

if __name__ == "__main__":
    from executors import MyTransformer, MyIndexer
else:
    from .executors import MyTransformer, MyIndexer


def trim_string(input_string, word_count=50, sep=" "):
    sanitized_string = input_string.replace("\\n", sep).replace("\\u2022", sep)
    words = sanitized_string.split(sep)[:word_count]
    output = " ".join(words)

    return output


def prep_docs(input_file, max_docs=1000):
    # docs = DocumentArrayMemmap("./mem_map")
    # docs.clear()
    docs = DocumentArray()
    with open(input_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        input_field = "Description"
        for row in csv_reader:
            input_data = trim_string(row[input_field])
            doc = Document(text=input_data)
            doc.tags = row
            # del doc.tags[input_field]
            # doc = Document(content="foo")
            docs.extend([doc])

    # docs.prune()
    return docs


def run_appstore(inputs, args):
    """
    Execute the app store example.

    :param args: arguments passed from CLI
    """

    f = (
        Flow()
        .add(uses=MyTransformer, parallel=args.parallel)
        .add(uses=MyIndexer, workspace=args.workdir)
    )

    # # index it!
    with f:
        f.post(on="/index", inputs=inputs, on_done=print)
        f.use_rest_gateway(args.port_expose)
        f.block()


if __name__ == "__main__":

    args = set_hw_chatbot_parser().parse_args()
    args.port_expose = my_port
    args.workdir = my_workdir

    docs = prep_docs(input_file="./data/1000.csv")

    run_appstore(inputs=docs, args=args)
