# sustainlp2020-energy

## Install

1. create a virtual python3 environment: `virtualenv .env -p python3.7`, then activate it: `source .env/bin/activate`

2. follow [official doc](https://pytorch.org/get-started/locally/) to install PyTorch
(tested with torch==1.6.0 with CUDA 10.1)

3. `pip install -r requirements.txt`

## Usage

(see `scripts.sh` for more comprehensive usage examples)

- log power using the WattsUp meter: `python wattsup.py -l -o sample.log`
- (optional) plot power and energy (needs to `pip install PyQt5 matplotlib`): `python plot.py sample.log sample.png`

- `random_select_questions.py`: random question selection.
- `run_energy_squad.py`: benchmarking inference on SQuAD.
- `compute_efficiency_info.py`: extract energy from the experiment-impact-tracker.
- `compute_wattsup_energy.py`: extract energy from the wattsup log.

## Sample data
see [raw_sample_logs.zip](https://github.com/csarron/sustainlp2020-energy/releases/download/v1.0/raw_sample_logs.zip)

## Cite

```bib
@inproceedings{cao-etal-2020-towards,
    title = "Towards Accurate and Reliable Energy Measurement of {NLP} Models",
    author = "Cao, Qingqing  and
      Balasubramanian, Aruna  and
      Balasubramanian, Niranjan",
    booktitle = "Proceedings of SustaiNLP: Workshop on Simple and Efficient Natural Language Processing",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.sustainlp-1.19",
    pages = "141--148",
    abstract = "Accurate and reliable measurement of energy consumption is critical for making well-informed design choices when choosing and training large scale NLP models. In this work, we show that existing software-based energy estimations are not accurate because they do not take into account hardware differences and how resource utilization affects energy consumption. We conduct energy measurement experiments with four different models for a question answering task. We quantify the error of existing software-based energy estimations by using a hardware power meter that provides highly accurate energy measurements. Our key takeaway is the need for a more accurate energy estimation model that takes into account hardware variabilities and the non-linear relationship between resource utilization and energy consumption. We release the code and data at https://github.com/csarron/sustainlp2020-energy.",
}
```

## FAQ

- Q1: Why am I not getting errors using the experiment-impact-tracker library?
see [possible bug](https://github.com/Breakend/experiment-impact-tracker/pull/21)

- Q2: this require hardware power meter setup, I don't have one, what should I do?
we are exploring more user-friendly and more accurate energy estimation methods, stay tuned!


