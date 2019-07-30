"""
To train the word embedding and to train the SIF model, we need to have a huge amount of unlabeled data available.
For our this toy example, we use unlabeled data from the SemEval 2017 Question-Question similarity challenge(Task3)
"""


import gensim.downloader as api

# Generate RAW data (used to create word embedding, and to compute the principal components for SIF)
data = api.load("semeval-2016-2017-task3-subtaskA-unannotated")
subjects = []
for thread in data:
    subject = thread["RelQuestion"]["RelQSubject"]
    subjects.append(subject)

with open(r"./data/semeval-question-corpus.txt", "w+", encoding="UTF-8") as f:
    for subject in subjects:
        f.write(subject + "\n")