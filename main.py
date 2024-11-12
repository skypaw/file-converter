import argparse
import logging
import os.path
import pathlib

PARSER = argparse.ArgumentParser(
    "main.py", description="Converting txt file to utf-8 encoding", add_help=True
)
logger = logging.getLogger("converter")
logger.setLevel("INFO")


class FileNotTxtException(Exception):
    pass


class FileOutsideWorkingDirException(Exception):
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


def check_path(path) -> None:
    path_split = os.path.splitext(path)
    extension_input = path_split[-1]

    if not extension_input == ".txt":
        raise FileNotTxtException
    if ".." in path_split[0] or "~" in path_split[0]:
        raise FileOutsideWorkingDirException


class ConvertFile:
    def __init__(self, arguments):
        self.__arguments = arguments
        self.__keywords = []
        self.__load_keywords()

    def __input_generator(self):
        for line in open(file=self.__arguments["input"], mode="r", errors="ignore"):
            yield line

    def __load_keywords(self):
        for keyword in open(
                file=pathlib.Path("filter-keywords.txt"), mode="r", errors="ignore"
        ):
            self.__keywords.append(keyword)

    def __filter_keywords(self, line):
        for keyword in self.__keywords:
            position = line.find(keyword)

    def process(self):
        with open(file=self.__arguments["output"], mode="wb") as output:
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
        check_path(args["input"])
        check_path(args["output"])
    except FileNotTxtException:
        logger.error(f"File extension has to be .txt, {PARSER.print_help()}")
    except FileOutsideWorkingDirException:
        logger.error(
            f"Potential path traversal, input has to be in file-converter dir, {PARSER.print_help()}"
        )

    cf = ConvertFile(args)
    cf.process()
