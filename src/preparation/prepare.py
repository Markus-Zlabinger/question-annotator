"""
Run this first. Afterwards, you can start the webservice by executing "application.py"

The preparation includes:
(1) Preprocessing of the questions
(2) Creating of a distance matrix (distances between questions)
(3) The distance matrix is saved and later used by the web application to show related questions
"""
##
import importlib
from gensim.models import FastText
import config
import src.methods as methods
from src.data_io import load_questions, load_training_data
from gensim.parsing.preprocessing import preprocess_documents
import pickle

# Load raw text corpus that is used to train the word embedding model and the SIF model
training = load_training_data(config.PATH_TRAINING_QUESTIONS)
training_tokenized = preprocess_documents(training)

# Load questions that you want to annotate
questions = load_questions(config.PATH_QUESTIONS)
questions_tokenized = preprocess_documents(questions)


# Create FastText embedding using Gensim
# Alternatively, you can use word2vec or pre-trained word embeddings that are publicly available
fasttext_model = FastText(training_tokenized + questions_tokenized, size=100, seed=42, iter=30)
fasttext_model.init_sims(replace=True)  # Normalize

##
importlib.reload(methods)
sif_model = methods.Sif(embedding_vocab=fasttext_model.wv, show_warnings=False)
sif_model.fit(training_tokenized + questions_tokenized)
text_embeddings = sif_model.transform(questions_tokenized)
##

# Return the ranked list of questions with respect to the current candidate question (rowidx)
def get_n_neighbors(rowidx, dmatrix, already_done=set(), n=15):
    row = dmatrix[rowidx]
    neighbors = []
    assert rowidx not in already_done
    for idx, dist in enumerate(row):
        if idx == rowidx:
            continue
        if idx in already_done:
            continue
        neighbors.append((idx, dist))
    neighbors = sorted(neighbors, key=lambda x: x[1])[::-1]
    # return neighbors[:n]
    return neighbors

from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(text_embeddings)
##
rowidx = 7
neighbors = get_n_neighbors(rowidx=rowidx, dmatrix=sim_matrix)
print("===============================")
print("Candidate: {}".format(questions[rowidx]), questions_tokenized[rowidx])
for neighboridx, score in neighbors:
    print(neighboridx, "{}: {}".format(score, questions[neighboridx]), questions_tokenized[neighboridx])
print("===============================")
##

# import numpy as np
# x = np.average([[2,1,2],[2,5, 4]], axis=0)

##


# def initialize_sif(corpus, w2v_model, embedding_method):
#     filename = "~tmp/generated/sif_{}_{}.p".format(embedding_method, len(corpus))
#     if os.path.isfile(filename):
#         return pickle.load(open(filename, "rb"))
#
#     corpus_clean = []
#     for tokenlist in corpus:
#         tmp_list = []
#         for token in tokenlist:
#             if token in w2v_model.wv:
#                 tmp_list.append(token)
#         if len(tmp_list) > 0:
#             corpus_clean.append(tmp_list)
#
#     sif_model = EMBEDDING_MODEL.SifWeighted(show_warnings=False)
#     sif_model.fit(w2v_model.wv, corpus)
#     pickle.dump(sif_model, open(filename, "wb"))
#     return sif_model

# Save distance matrices and questions (in case some questions were removed during preprocessing)

pickle.dump(sim_matrix, open("./data/sim_matrix.p", "wb"))