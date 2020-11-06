#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Qingqing Cao, https://awk.ai/, Twitter@sysnlp"

import argparse
import numpy as np

from experiment_impact_tracker.utils import gather_additional_info
from experiment_impact_tracker.utils import load_initial_info
from pathlib import Path

from natsort import natsorted


def one_energy(log_dir):
    sys_data = load_initial_info(log_dir)
    eff_data = gather_additional_info(sys_data, log_dir)
    return eff_data['total_power']


def main(args):
    log_parent_path = Path(args.log_parent_dir)
    energy = {x.name: one_energy(x) for x in log_parent_path.iterdir()
              if x.is_dir()}
    for x, val in natsorted(energy.items()):
        print(f"{x[1:]}, {val * 3.6e6} ")
    print(f"found {len(energy)} logs")
    avg = np.mean(list(energy.values()))
    std = np.std(list(energy.values()))
    print(f'{log_parent_path} energy avg (kwh): {avg:.5f}')
    print(f'{log_parent_path} energy std (kwh): {std:.5f}')
    print(f'{log_parent_path} energy avg (J): {avg * 3.6e6:.2f}')
    print(f'{log_parent_path} energy std (J): {std * 3.6e6:.2f}')
    print(f'{log_parent_path} energy std (%): {std * 100 / avg:.2f}')
    if args.num_examples:
        per_ex_avg = avg / args.num_examples
        per_ex_std = std / args.num_examples
        print(f"{log_parent_path} per example energy")
        print(f"avg (J), std (J), std ratio (%)")
        print(f"{per_ex_avg * 3.6e6:.1f}, {per_ex_std * 3.6e6:.1f}, "
              f"{per_ex_std * 100 / per_ex_avg:.1f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_parent_dir", type=str,
                        help="parent dir of the dir containing log files "
                             "from experiment_imapct_tracker")
    parser.add_argument("-n", "--num_examples", default=0, type=int,
                        help="number of examples to get "
                             "average energy per example ",
                        )
    main(parser.parse_args())
