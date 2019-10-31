import sent2vec
from nltk import TweetTokenizer
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
import data_io
import config
from  more_itertools import unique_everseen

SENT2VEC_MODEL = "/newstorage2/zlabinger/embeddings/twitter_unigrams.bin"

model = sent2vec.Sent2vecModel()
model.load_model(SENT2VEC_MODEL)

##
tokenizer = TweetTokenizer()

def tokenize_questions(question):
    return tokenizer.tokenize(question)

# Copied from https://github.com/epfml/sent2vec/blob/master/tweetTokenize.py
def convert2sent2vec(tweet):
    tweet = tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '<url>', tweet)
    tweet = re.sub('(\@[^\s]+)', '<user>', tweet)
    try:
        tweet = tweet.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        pass
    return tweet


def get_raw_questions():
    q = []
    with open("./sample-questions.txt", "r") as f:
        for line in f:
            q.append(line.strip())
    return q

def sentences2vector(sents):
    prepared_sents = []
    for sent in sents:
        tokenized = tokenize_questions(sent)
        sent2vecformat = convert2sent2vec(" ".join(tokenized))
        prepared_sents.append(sent2vecformat)
    return model.embed_sentences(prepared_sents)


questions_raw = pd.read_csv("./data/sample-questions.txt")
questions = questions_raw["question"].tolist()
questions_ids = questions_raw["qid"].apply(str).tolist()
questions_embedded = sentences2vector(questions)
# questions_tokenized = [tokenize_questions(q) for q in questions_raw]
# questions_preprocessed = [convert2sent2vec(" ".join(q)) for q in questions_tokenized]
# questions_embedded = model.embed_sentences(questions_preprocessed)
##
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

answers = pd.read_csv("./data/sample-answers-html.txt")
answers_clean = [cleanhtml(a) for a in answers["answer"]]

answer_sentences = []
answer_sentences_labels = []
for aid, answer in zip(answers["aid"], answers["answer"]):
    answer_clean = cleanhtml(answer)
    sentences = sent_tokenize(answer_clean)
    answer_sentences.extend(sentences)
    answer_sentences_labels.extend(len(sentences) * [aid])

answer_sentences_embedded = sentences2vector(answer_sentences)


# sentences_list = [for for sentences_answer in sentences_list]
##

suffix = ""
if "wiki_unigrams" in SENT2VEC_MODEL:
    suffix = "_wiki"

q2q_simmat = cosine_similarity(questions_embedded)
q2q_simmat = pd.DataFrame(q2q_simmat, index=questions_ids, columns=questions_ids)
q2q_simmat.to_csv("./data/q2q_simmat.csv", index=True, header=True)
##
q2s_simmat = cosine_similarity(questions_embedded, answer_sentences_embedded)
df = pd.DataFrame(q2s_simmat, index=questions_ids)

answer_labels = list(unique_everseen(answer_sentences_labels))
answer_sentences_labels = np.array(answer_sentences_labels)
new_data = []
for answer_label in answer_labels:
    mask = answer_sentences_labels == answer_label
    cols = df.iloc[:,mask].values.tolist()
    new_data.append(cols)
q2s_simmat = pd.DataFrame(new_data, columns=questions_ids, index=answer_labels).transpose().copy()
q2s_simmat.to_csv("./data/q2s_simmat.csv", index=True, header=True)
##

# x = pd.read_csv("./data/q2s_simmat.csv", index_col=0, header=0)
# x.index = x.index.astype("str")
# x.columns = x.columns.astype("str")
##
#q2q_simmat.loc["0", "0"]

# q2s_simmat = cosine_similarity(questions_embedded, answer_sentences_embedded)
#
#
#
# q2s_simmat = pd.DataFrame(q2s_simmat, index=questions_ids)
#
# # q2s_simmat = pd.DataFrame(q2s_simmat, index=questions_ids), columns=answer_sentences_labels)
#
# q2q_simmat.to_csv("./data/q2q_simmat.csv", index=True, header=True)
# q2s_simmat.to_csv("./data/q2s_simmat.csv", index=True, header=True)
#
# x = pd.read_csv("./data/q2s_simmat.csv", index_col=0, header=0)

# data_io.save_similarity_matrix(q2q_simmat, config.)

# np.savetxt("./sim_matrix{}.txt".format(suffix), sim_matrix)
# np.savetxt("./vectors{}.txt".format(suffix), questions_embedded)
##
