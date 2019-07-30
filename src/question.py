class Question:
    qid = None
    text = None
    text_tokens = None

    def __init__(self, qid, text):
        self.qid = qid
        self.text = text
        #self.text_tokens = text_tokens

    def __repr__(self):
        return self.text
