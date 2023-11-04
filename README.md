# ICYBM201 : Flagging suspicious hosts from DNS traces

## Authors and ULB matricules
- LUYCKX Marco 496283
- BOUHNINE Ayoub 500048

## Introduction

This README provides an overview of our project, which aims to build a classifier to distinguish network hosts as either human, bot or a combination of both. The document outlines the project's objectives, datasets used, available commands and an overview of the project's structure.


## Goal

Build a classifier to classify each host from the dataset as either : 
1) human; 
2) bot;
3) human+bot; 

and report our methodology, results and analysis.

We are free to choose the method to classify but we need to justify our choice of method.

As specified in the project statement, we tried to follow as much as possible the **pep0008** style guide.

## Report

⚠️⚠️⚠️ Detailed information, methodology, results and analysis can be found in the [project report](report/IDS_ML_LUYCKX_BOUHNINE.pdf).


## Datasets

### Public resolver data

The project focuses only on data from a public resolver with the following details :
- **IP address** : `1.1.1.1` (`one.one.one.one`)
- **Data source** : DNS traffic captured via tcpdump on port `53`

### Training datasets

The training data includes two datasets :
1. `webclients_tcpdump.txt` : Contains DNS traces from 120 UNamur hosts browsing various top-1000 Alexa-listed websites.
2. `bots_tcpdump.txt` : Contains DNS traces from 120 bots, also interacting with top-1000 Alexa-listed websites.

### Evaluation datasets

They both contain **human** and **bot** traffic.

1. `eval1_tcpdump.txt` : bots and humans are guaranteed to be a separate set of hosts. 
2. `eval2_tcpdump.txt` : some hosts emit traffic from a human and from a bot.

#### Lists of bots

For evaluation, two lists of known bot hosts are used :
- `eval1_botlist.txt`
- `eval2_botlist.txt`

## Commands

Do not forget to install the requirements before running the scripts ! You can do it by running the following command :
First, create a virtual environment and activate it :

```bash
python3 -m venv .venv && source .venv/bin/activate
```

Finally, install the requirements :
```bash
pip3 install -r requirements.txt
```
--- 

First of all, navigate to the `scripts` folder :

```bash 
cd scripts
```

In the next commands, `<algo>` can be replaced by `decision_tree`, `logistic_regression`, `neural_networks`, `random_forest` or `knn`. 

---
To train the model, run the following command :

```bash
python3 train.py \
--webclients ../training_datasets/tcpdumps/webclients_tcpdump.txt \
--bots ../training_datasets/tcpdumps/bots_tcpdump.txt \
--algo <algo> \
--output ../trained_models/<algo>/trained_model_<algo>.pkl
```

For example, you could use the following command :

```bash
python3 train.py \
--webclients ../training_datasets/tcpdumps/webclients_tcpdump.txt \
--bots ../training_datasets/tcpdumps/bots_tcpdump.txt \
--algo logistic_regression \
--output ../trained_models/logistic_regression/trained_model_logistic_regression.pkl
```

---

To evaluate the model, run the following command :

```bash
python3 eval.py \
--trained_model ../trained_models/<algo>/trained_model_<algo>.pkl \
--dataset ../evaluation_datasets/tcpdumps/eval1_tcpdump.txt \
--output ../suspicious_hosts/suspicious_hosts.txt
```

For example, in this project, you could use the following command :

```bash
python3 eval.py \
--trained_model ../trained_models/logistic_regression/trained_model_logistic_regression.pkl \
--dataset ../evaluation_datasets/tcpdumps/eval1_tcpdump.txt \
--output ../suspicious_hosts/suspicious_hosts.txt
```

---

To do both at the same time, run the following command :

```bash
python3 main.py \
--webclients ../training_datasets/tcpdumps/webclients_tcpdump.txt \
--bots ../training_datasets/tcpdumps/bots_tcpdump.txt \
--algo <algo> \
--trained_model ../trained_models/<algo>/trained_model_<algo>.pkl \
--dataset ../evaluation_datasets/tcpdumps/eval1_tcpdump.txt \
--output ../suspicious_hosts/suspicious_hosts.txt 
```

For example, in this project, you could use the following command :

```bash
python3 main.py \
--webclients ../training_datasets/tcpdumps/webclients_tcpdump.txt \
--bots ../training_datasets/tcpdumps/bots_tcpdump.txt \
--algo logistic_regression \
--trained_model ../trained_models/logistic_regression/trained_model_logistic_regression.pkl \
--dataset ../evaluation_datasets/tcpdumps/eval1_tcpdump.txt \
--output ../suspicious_hosts/suspicious_hosts.txt 
```

### Diagrams

First, starting for the root directory of the project, navigate to the `scripts/utils/diagrams/` directory :

```bash
cd scripts/utils/diagrams/
```

To create plots related to algorithms, run the following command :

```bash
python3 diagram_algo.py
```

To create plots related to metrics, run the following command :

```bash
python3 diagram_metrics.py
```



## Colors

When running the scripts, we use colors to differentiate the different steps of the process :
- **Green** : corresponds to the pre-processing steps.
- **Blue** : corresponds to the training phase.
- **Red** : corresponds to the evaluation phase.
- **Yellow** : corresponds to saving and loading the model.
- **Purple** : corresponds to every data related to classification and accuracy. 

- We also use light colors to differentiate the different rates during the classification :
    1. **Light cyan** : corresponds to the detection rate (true positive).
    2. **Light red** : corresponds to the false alarm rate (false positive).
    3. **Light purple** : corresponds to the false negative.
    4. **Light yellow** : corresponds to the true negative.


## Structure of the project

- `diagrams` : contains the diagrams produced for in the report.
- `docs` : contains the articles that we need to read for the project. TODO REMOVE THIS ONE
- `evaluation_datasets` : contains the evaluation datasets given by the professor and the botlists.
- `report` : contains the report of the project.
- `scripts` : contains the scripts used to train and evaluate the models.
  - `features` : contains the 3 scripts (time, misc and numbers) used to create the new features based on the aggregated raw features.
  - `utils` : 
    - `colors.py` : contains the colors used in the scripts.
    - `constants.py` : contains the constants used in the scripts.
    - `features.py` : contains the functions used to orchestrate everything related to the features.
    - `parsing_dns_trace.py` : contains the functions used to parse the DNS traces.
    - `saving_and_loading.py` : contains the functions used to save and load the models.
    - `diagrams` :
      - `diagram_algo.py` : contains the functions used to create the diagrams related to the algorithms.
      - `diagram_metrics.py` : contains the functions used to create the diagrams related to the metrics.   
  - `eval.py` : contains the functions used to evaluate the models.
  - `main.py` : contains the functions used to both do the training and evaluation of the models.
  - `train.py` : contains the functions used to train the models.
- `suspicious_hosts` : contains the suspicious hosts found by the models.
- `trained_models` : contains the trained models. There is a subdirectory for each algorithm.
- `training_datasets` : contains the training datasets given by the professor.

---


