# IDS-ML

## Goal

Build a classifier to classify each host from the dataset as either : 
1) human; 
2) bot;
3) human+bot; 
and report your methodology, results and analysis.

We are free to choose the method to classify but we need to justify our choice of method.

## Datasets

- **Public resolver** : `1.1.1.1`
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


## Commands


