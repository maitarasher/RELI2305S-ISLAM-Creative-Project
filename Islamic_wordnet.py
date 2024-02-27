from nltk.corpus import stopwords
from collections import defaultdict
import string

class Islamic_Wordnet():
    def __init__(self):
        """
        lexeme is a pairing of a particular word form with its sense -- e.g bright (light) vs bright (idea)
        for "<word>.<pos>.<number>":
        <word> is the word itself
        <pos> is one of the module attributes ADJ, ADJ_SAT, ADV, NOUN or VERB, this WordNet only contains NOUNS (n)
        <number> is the sense number, counting from 0.
        """
        self.lexemes = {'ijtihad': ['ijtihad.n.01','ijtihad.n.02'], #1
                        'jihad': ['jihad.n.01', 'jihad.n.02'], #2
                        'taklid': ['taklid.n.01', 'taklid.n.02'], #3
                        'takfir': ['takfir.n.01', 'takfir.n.01'], #4
                        'ijma': ['ijma.n.01', 'ijma.n.02'], #5
                        'fatwa': ['fatwa.n.01', 'fatwa.02'], #6
                        'mufti': ['mufti.n.01', 'mufti.n.02'], #7
                        'fiqh': ['fiqh.n.01', 'fiqh.n.02'], #8
                        'sharia': ['sharia.n.01','sharia.n.02'], #9
                        'imam': ['imam.n.01','imam.n.02'], #10
                        'walaya': ['walaya.n.01','walaya.n.02'], #11
                        'naf': ['naf.n.01','naf.n.02'], #12
                        'tariqa': ['tariqa.n.01','tariqa.n.02'], #13
                        'sharia': ['sharia.n.01','sharia.n.02']} #14
        self.lexemes_def = {'ijtihad.n.01':['']
                            'ijtihad.n.02':[]
                            'ijtihad.n.01':[]}

        self.lexemes_examples = {}

    def lexemes(self,word):
        if word in self.lexemes:
            return self.lexemes[word]
        return []


wn = Islamic_Wordnet() # Create Islamic_Wordnet object to access the information

def wn_simple_lesk_predictor(context : Context) -> (str,str):
    scores = defaultdict(int)
    lexemes = wn.lexemes(context.lemma, pos=context.pos) # retrieve all lexemes of the word
    for lex in lexemes:
        overlap_score = 0
        overlap_score += overlap(context,wn.lexemes_def(lex)) # add overlap with the sense(lexeme) definition()
        for example in wn.lexemes_examples(lex): # add overlaps with the sense(lexeme) examples
            overlap_score += overlap(context, example)
        scores[lex]=overlap_score
    scores_sorted = sorted(list(zip(scores.keys(), scores.values())),key=lambda x: x[1])[::-1] # Sort in increasing order so lexeme with max overlap occur first on the list
    best_lexeme = scores_sorted[0][0]
    lexemes_def = wn.lexemes_def(best_lexeme)
    return (best_lexeme,lexemes_def)

def overlap(context : Context, sentence) -> int:
    stop_words = stopwords.words('english')
    sen_toks =  tokenize(sentence)
    overlap = (set(sen_toks) & set(context.left_context + context.right_context)) - set(stop_words)
    return len(overlap)

def tokenize(s):
    """
    a naive tokenizer that splits on punctuation and whitespaces.
    """
    s = "".join(" " if x in string.punctuation else x for x in s.lower())
    return s.split()


