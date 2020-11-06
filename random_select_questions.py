#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Qingqing Cao, https://awk.ai/, Twitter@sysnlp"

import argparse
import json
import random
from pathlib import Path


def main(args):
    input_file = Path(args.input_file)
    num = args.num
    output_file = input_file.with_suffix(f'.{num}{input_file.suffix}')
    with open(input_file) as f:
        d = json.load(f)

    total = 0
    for article in d['data']:
        for paragraph in article['paragraphs']:
            total += len(paragraph['qas'])

    idx = list(range(total))
    random.shuffle(idx)
    idx_select = set(idx[:num])
    no = 0
    new_article = []
    for article in d['data']:
        new_para = []
        title = article["title"]
        for paragraph in article['paragraphs']:
            context = paragraph['context']
            new_qas = []
            for qa in paragraph['qas']:
                # question = qa['question']
                if no in idx_select:
                    # selected
                    new_qas.append(qa)
                no += 1
            if new_qas:
                new_para.append({'context': context, 'qas': new_qas})
        if new_para:
            new_article.append({'title': title, 'paragraphs': new_para})
    new_data = {'data': new_article, 'version': '1.1'}
    with open(output_file, 'w') as f:
        f.write(json.dumps(new_data))
    new_num = 0
    for article in new_data['data']:
        for paragraph in article['paragraphs']:
            new_num += len(paragraph['qas'])
    assert new_num == num, 'not consistent, please check dataset'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str,
                        help="input dataset file")
    parser.add_argument("-n", "--num", default=1000, type=int,
                        help="number of examples to select", )
    main(parser.parse_args())
