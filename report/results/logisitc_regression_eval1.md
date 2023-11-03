
#### LOGISTIC REGRESSION #### For Eval 1


```
All features :

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 11.11111111111111 %
False negative rate : 0.0 %
True negative rate : 88.88888888888889 %
Accuracy : 90.0 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  12 
Number of false negative :  0 
Number of true negative :  96 
####

#### Classification report : 

## Bot : 

Precision: 0.5
Recall: 1.0
F1-Score: 0.6666666666666666
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.8888888888888888
F1-Score: 0.9411764705882353
Support: 108.0 
 
## Weighted avg : 

Precision: 0.95
Recall: 0.9
F1-Score: 0.9137254901960784
Support: 120.0 
####
```

--------------------
```
Only misc features : 

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 24.074074074074073 %
False negative rate : 0.0 %
True negative rate : 75.92592592592592 %
Accuracy : 78.33333333333333 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  26 
Number of false negative :  0 
Number of true negative :  82 
####

#### Classification report : 

## Bot : 

Precision: 0.3157894736842105
Recall: 1.0
F1-Score: 0.4799999999999999
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.7592592592592593
F1-Score: 0.8631578947368421
Support: 108.0 
 
## Weighted avg : 

Precision: 0.931578947368421
Recall: 0.7833333333333333
F1-Score: 0.8248421052631579
Support: 120.0 
####
```
---------------------
```
Only time features :

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 6.481481481481481 %
False negative rate : 0.0 %
True negative rate : 93.51851851851852 %
Accuracy : 94.16666666666667 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  7 
Number of false negative :  0 
Number of true negative :  101 
####

#### Classification report : 

## Bot : 

Precision: 0.631578947368421
Recall: 1.0
F1-Score: 0.7741935483870968
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.9351851851851852
F1-Score: 0.9665071770334929
Support: 108.0 
 
## Weighted avg : 

Precision: 0.9631578947368421
Recall: 0.9416666666666667
F1-Score: 0.9472758141688532
Support: 120.0 
####
```

---------------------

```
Only numbers features : 

####
False alarm rate and detection rate...
Detection rate : 58.333333333333336 %
False alarm rate : 4.62962962962963 %
False negative rate : 41.66666666666667 %
True negative rate : 95.37037037037037 %
Accuracy : 91.66666666666666 %
####
Total host :  120 
Number of true positive :  7 
Number of false positive :  5 
Number of false negative :  5 
Number of true negative :  103 
####

#### Classification report : 

## Bot : 

Precision: 0.5833333333333334
Recall: 0.5833333333333334
F1-Score: 0.5833333333333334
Support: 12.0 
 
## Human : 

Precision: 0.9537037037037037
Recall: 0.9537037037037037
F1-Score: 0.9537037037037037
Support: 108.0 
 
## Weighted avg : 

Precision: 0.9166666666666666
Recall: 0.9166666666666666
F1-Score: 0.9166666666666666
Support: 120.0 
####
```

---------------------

```
### Combination 1: High-Level Behavioral Traits
Average number of dots in a domain
Number of requests in a session
Frequency of repeated requests in a short time frame
Type of requests queried by hosts

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 2.7777777777777777 %
False negative rate : 0.0 %
True negative rate : 97.22222222222221 %
Accuracy : 97.5 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  3 
Number of false negative :  0 
Number of true negative :  105 
####

#### Classification report : 

## Bot : 

Precision: 0.8
Recall: 1.0
F1-Score: 0.888888888888889
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.9722222222222222
F1-Score: 0.9859154929577464
Support: 108.0 
 
## Weighted avg : 

Precision: 0.98
Recall: 0.975
F1-Score: 0.9762128325508607
Support: 120.0 
####
```

---------------------

```
### Combination 2: Domain Interaction and Traffic Patterns
Number of unique domains
Average counts
Average time between requests
Average of request length
Type of responses received by hosts

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 13.88888888888889 %
False negative rate : 0.0 %
True negative rate : 86.11111111111111 %
Accuracy : 87.5 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  15 
Number of false negative :  0 
Number of true negative :  93 
####

#### Classification report : 

## Bot : 

Precision: 0.4444444444444444
Recall: 1.0
F1-Score: 0.6153846153846153
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.8611111111111112
F1-Score: 0.9253731343283582
Support: 108.0 
 
## Weighted avg : 

Precision: 0.9444444444444444
Recall: 0.875
F1-Score: 0.894374282433984
Support: 120.0 
####
```


---------------------

```
### Combination 3: Response-Based and Session Duration Features
Average of response length
Average time for a session
Average time between requests
Frequency of repeated requests in a short time frame

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 10.185185185185185 %
False negative rate : 0.0 %
True negative rate : 89.81481481481481 %
Accuracy : 90.83333333333333 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  11 
Number of false negative :  0 
Number of true negative :  97 
####

#### Classification report : 

## Bot : 

Precision: 0.5217391304347826
Recall: 1.0
F1-Score: 0.6857142857142856
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.8981481481481481
F1-Score: 0.9463414634146341
Support: 108.0 
 
## Weighted avg : 

Precision: 0.9521739130434782
Recall: 0.9083333333333333
F1-Score: 0.9202787456445993
Support: 120.0 
####
```

---------------------

```
### Combination 4: Detailed Request and Response Patterns
Type of requests queried by hosts
Type of responses received by hosts
Average of request length
Average of response length

####
False alarm rate and detection rate...
Detection rate : 100.0 %
False alarm rate : 24.074074074074073 %
False negative rate : 0.0 %
True negative rate : 75.92592592592592 %
Accuracy : 78.33333333333333 %
####
Total host :  120 
Number of true positive :  12 
Number of false positive :  26 
Number of false negative :  0 
Number of true negative :  82 
####

#### Classification report : 

## Bot : 

Precision: 0.3157894736842105
Recall: 1.0
F1-Score: 0.4799999999999999
Support: 12.0 
 
## Human : 

Precision: 1.0
Recall: 0.7592592592592593
F1-Score: 0.8631578947368421
Support: 108.0 
 
## Weighted avg : 

Precision: 0.931578947368421
Recall: 0.7833333333333333
F1-Score: 0.8248421052631579
Support: 120.0 
####

```

---------------------
