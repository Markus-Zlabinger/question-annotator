"""
For this sample program, we used the standard GenSim preprocesser.

You can, however, modify the preprocessing pipeline at will.

"""

from gensim.parsing.preprocessing import preprocess_string

def text2tokens(text):
    return preprocess_string(text)

