# IDS-ML

## Goal

Build a classifier to classify each host from the dataset as either : 
1) human; 
2) bot;
3) human+bot; 
and report your methodology, results and analysis.

We are free to choose the method to classify but we need to justify our choice of method.

## Datasets

- **Public resolver** : `1.1.1.1` (`one.one.one.one`)
- Some of their DNS traffic has been captured from a vantage point in the network using tcpdump on port `53`.

### Training datasets

1) `webclients_tcpdump.txt` : contains the DNS traces of 120 UNamur hosts browsing several frontpages of the top-1000 Alexa list.
2) `bots_tcpdump.txt` : contains the DNS traces of 120 bots, also in relation to the top-1000 Alexa list.

### Evaluation datasets

They both cintain **human** and **bot** traffic.

- `eval1_tcpdump.txt` : bots and humans are guaranteed to be a separate set of hosts. 
- `eval2_tcpdump.txt` : some hosts emit traffic from a human and from a bot.

#### Lists of bots

- `eval1_botlist.txt` : list of bots
- `eval2_botlist.txt` : list of bots


## Report

The report is located in the [report folder](report/IDS_ML_LUYCKX_BOUHNINE.pdf) .

## Commands

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

For example, in this project, you could use the following command :

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

To do both, run the following command :

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


## Colors

TODO
\begin{itemize}
    \item \textbf{Green} : corresponds to the pre-processing steps. 
    \item \textbf{Blue} : corresponds to the training phase.
    \item \textbf{Red} : corresponds to the evaluation phase.
    \item \textbf{Yellow} : corresponds to saving and loading the model.
    \item \textbf{Purple} : corresponds to every data related to classification and accuracy. We also use light colors to differentiate the different rates during the classification : 
        \begin{enumerate}
            \item \textbf{Light cyan} : corresponds to the detection rate (true positive). 
            \item \textbf{Light red} : corresponds to the false alarm rate (false positive).
            \item \textbf{Light purple} : corresponds to the false negative.
            \item \textbf{Light yellow} : corresponds to the true negative.
        \end{enumerate}
\end{itemize}