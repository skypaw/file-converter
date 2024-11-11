import argparse
import logging
import os.path
import pathlib

PARSER = argparse.ArgumentParser(
    "main.py", description="Converting txt file to utf-8 encoding", add_help=True
)
logger = logging.getLogger("converter")
logger.setLevel("INFO")

KEYWORDS = ["Full Name", "Social Security Number", "Telephone Number"]


class FileNotTxtException(Exception):
    pass


def parse_arguments() -> dict[str, pathlib.Path]:
    PARSER.add_argument(
        "-i",
        "--input",
        type=pathlib.Path,
        required=True,
        help="path to the input.txt file, example ./foo.txt",
    )
    PARSER.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        required=True,
        help="path to the output file, example ./bar.txt",
    )
    return PARSER.parse_args().__dict__


def check_file_exists(arguments) -> None:
    if not arguments["input"].is_file():
        raise FileNotFoundError
    if arguments["output"].is_file():
        raise FileExistsError


def check_extensions(arguments) -> None:
    extension_input = os.path.splitext(arguments["input"])[-1]
    extension_output = os.path.splitext(arguments["output"])[-1]
    if not extension_input == ".txt" or not extension_output == ".txt":
        raise FileNotTxtException


class ConvertFile:
    def __init__(self, arguments):
        self.arguments = arguments

    def __input_generator(self):
        for line in open(file=self.arguments["input"], mode="r", errors="ignore"):
            yield line

    def __filter_keywords(self, line):
        for keyword in KEYWORDS:
            position = line.find(keyword)


    def process(self):
        with open(file=self.arguments["output"], mode="wb") as output:
            for line in self.__input_generator():
                encoded = line.encode("utf-8", errors="ignore")
                output.write(encoded)


if __name__ == "__main__":
    args = parse_arguments()
    try:
        check_file_exists(args)
    except FileNotFoundError:
        logger.error(f"Input file does not exists, {PARSER.print_help()}")
    except FileExistsError:
        logger.error(f"Output file exists, {PARSER.print_help()}")

    try:
        check_extensions(args)
    except FileNotTxtException:
        logger.error(f"File extension has to be .txt, {PARSER.print_help()}")

    cf = ConvertFile(args)
    cf.process()
