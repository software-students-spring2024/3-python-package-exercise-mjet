from stop_list import closed_class_stop_words
from collections import Counter
import nltk
import math
import re
import numpy as np

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

def cosine_similarity_arr(vect1, vect2):
    cos_sim = sum(vect1 * vect2) / (sum(vect1**2) * sum(vect2**2)) ** 0.5
    if math.isnan(cos_sim):
        return 0
    else:
        return cos_sim

#increments each word's number of appearances by one if it appears in the updating dictionary 
def update_and_add(initial, update):
    for key in initial.keys():
        if key in update.keys():
            initial[key] += 1
    return initial
            
def tf_idf(target_film, films_in_genre):
    DOCS_IN_CORPUS = len(films_in_genre)
    DOCS_CONCAT = ""
    for film in films_in_genre:
        DOCS_CONCAT += film['overview'] + '\n'
        
    words_docs_concat = nltk.word_tokenize(DOCS_CONCAT)
    unique_word_keys = Counter(words_docs_concat).keys()#list of all unique words in corpus, use to ensure that all vectors are congruent
    dummy_dictionary = dict(zip(unique_word_keys, [0] * len(unique_word_keys)))

    word_present_count = dict(zip(dummy_dictionary.keys(), dummy_dictionary.values())) #dictionary to hold the number of documents in which each word occurs
    term_freq = dict()
    for film in films_in_genre:
        film_words = eliminate_stop(nltk.word_tokenize(film['overview']))
        nr_words = len(film_words)
        unique_words = Counter(film_words)
        film['term_freq'] = dict(zip(dummy_dictionary.keys(), dummy_dictionary.values()))
        film['term_freq'].update(dict(zip(unique_words.keys(), np.array([*unique_words.values()]) / nr_words)))#unpack unique_words from dictionary items

        word_present_count = update_and_add(word_present_count, unique_words)   

    idf = dict(zip(word_present_count.keys(), [math.log(x) for x in DOCS_IN_CORPUS / (np.array([*word_present_count.values()]) + 1)] ) )

    for film in films_in_genre:
        film['tf-idf-vector'] = np.array([*film['term_freq'].values()]) * [math.log(x) for x in DOCS_IN_CORPUS / np.array([*idf.values()])]

    target_film_arr = target_film['tf-idf-vector']
    for film in films_in_genre: 
        film_arr = film['tf-idf-vector']
        film['similarity'] = cosine_similarity_arr(target_film_arr, film_arr)

    films_in_genre.remove(target_film)
    films_in_genre = sorted(films_in_genre, key = lambda x: x['similarity'], reverse = True)
    films_overviews = ''
    for film in films_in_genre:
        films_overviews += f'{film['title']},\tDescription: {film['overview']}\n'

    return films_overviews


