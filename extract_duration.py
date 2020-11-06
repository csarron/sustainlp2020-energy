#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Qingqing Cao, https://awk.ai/, Twitter@sysnlp"

import argparse
import parse
from pathlib import Path


def main(args):
    input_file = Path(args.input_file)
    suffix = "end" if args.end else "start"
    out_dir = Path(args.out_dir)
    for line in open(input_file):
        batch_size = next(parse.findall("b-{}/", line))[0]
        iteration = next(parse.findall("-t{}.log", line))[0]
        time = next(parse.findall(".log:{:ta} -", line))[0]
        output_file = out_dir.joinpath(
            f'b-{batch_size}', f't{iteration}-{suffix}.txt')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = '{}-{}-{}-{}-{}-{}'.format(
            time.year, time.month, time.day, time.hour, time.minute,
            time.second)
        output_file.write_text(timestamp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str,
                        help="input dataset file")
    parser.add_argument("-o", "--out_dir", type=str, required=True,
                        help="output dir")
    parser.add_argument("-e", "--end", action="store_true",
                        help="start or end, start by default", )
    main(parser.parse_args())
