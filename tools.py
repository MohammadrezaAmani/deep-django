import asyncio
import json
import os
from typing import List

import aiofiles

PATH = "."
LANG = "fa"


def source_to_list(code: str) -> List[str]:
    """Convert a Python script to a list of lines."""
    return [i + "\n" for i in code.split("\n")]


def to_ipynb(code: str) -> dict:
    """Convert a Python script to a Jupyter notebook."""

    cells = []
    for code_in_cell in code.split("\n\n\n"):
        cells += [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source_to_list(code_in_cell),
            },
            {"cell_type": "markdown", "metadata": {}, "source": []},
        ]
    return {
        "cells": cells,
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 2,
    }


def load_code(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def to_json(cells: dict) -> str:
    return json.dumps(cells, indent=4)


async def write_ipynb(path: str, ipynb: str):
    async with aiofiles.open(path, mode="w") as f:
        await f.write(ipynb)


async def do_conversion(path: str):
    code = load_code(path)
    cells = to_ipynb(code)
    ipynb = to_json(cells)
    lang = "_" + LANG if LANG else ""
    await write_ipynb(path.replace(".py", lang + ".ipynb"), ipynb)


async def main():
    for root, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(".py"):
                await do_conversion(os.path.join(root, file))


asyncio.run(main())
