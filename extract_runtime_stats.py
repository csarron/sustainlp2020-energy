#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Qingqing Cao, https://awk.ai/, Twitter@sysnlp"

import argparse
import numpy as np

from natsort import natsorted
from pathlib import Path
from experiment_impact_tracker.utils import load_data_into_frame


def one_entry(log_dir):
    df, json_array = load_data_into_frame(log_dir)
    cpu_load = []
    mem = []
    gpu_load = []
    gpu_mem = []
    for item in json_array:
        cpu_load.append(item['average_relative_cpu_utilization'])
        mem.append(item['absolute_mem_percent_usage'])
        all_gpus = item['per_gpu_average_estimated_utilization_absolute']
        gl_list = [g['sm'] for g in all_gpus.values()]
        gl = sum(gl_list)
        if gl > 0:
            gpu_load.append(gl)
        gm_list = [g['mem'] for g in all_gpus.values()]
        gm = sum(gm_list)
        if gm > 0:
            gpu_mem.append(gm)
    cl = np.mean(cpu_load)
    gl = np.mean(gpu_load)
    cm = np.mean(mem)
    gm = np.mean(gpu_mem)
    # print(f'cpu_load={cl}, mem={cm}, gpu_load={gl}, gpu_mem={gm}')
    # return eff_data['total_power']
    return cl, cm, gl, gm


def main(args):
    log_parent_path = Path(args.log_parent_dir)
    log_dirs = {x.name: one_entry(x) for x in log_parent_path.iterdir()
                if x.is_dir()}
    for x, val in natsorted(log_dirs.items()):
        cl, cm, gl, gm = val
        print(f"{x[1:]}, {cl}, {cm}, {gl}, {gm} ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_parent_dir", type=str,
                        help="parent dir of the dir containing log files "
                             "from experiment_imapct_tracker")
    main(parser.parse_args())
