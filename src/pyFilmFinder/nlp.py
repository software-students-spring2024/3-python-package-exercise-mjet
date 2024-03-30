import math
import re
from stop_list import closed_class_stop_words

abstracts_no_stop = closed_class_stop_words

def cosine_similarity_arr(vect1, vect2):
    cos_sim = sum(vect1 * vect2) / (sum(vect1**2) * sum(vect2**2)) ** 0.5
    if math.isnan(cos_sim):
        return 0
    else:
        return cos_sim

IDF = dict()
def idf(word):
    try:
        idf_score = IDF[word]

        return idf_score
    except:
        docs_containing = 0
        for abstract in abstracts_no_stop:
            try:
                abstract_words = abstracts_no_stop[abstract]
                if (abstracts_no_stop[abstract][word] > 0):
                    docs_containing+=1

                TERM_FREQ[f'{abstract}{word}'] = abstract_words[word] / len(abstract_words)   
            except: #word is not present
                TERM_FREQ[f'{abstract}{word}'] = 0  
        
        idf_score = np.log(DOCS_IN_CORPUS / (docs_containing + 1)) #avoid div by 0
        IDF[word] = idf_score
        return idf_score
    

def eliminate_stop(words):
    no_stop = dict()
    for i in range(len(words)):
        if (words[i] not in closed_class_stop_words and (re.findall('\d|\.|\,|\!|\?', words[i]) == [])): #index is not in list of stopwords                    
            word = words[i]
            try:
                no_stop[word]+=1
            except:#new word
                no_stop[word]=1
            
    return no_stop