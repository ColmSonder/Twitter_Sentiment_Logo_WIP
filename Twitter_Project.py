# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:52:10 2017

@author: HP-Colm
"""

# http://www.kdnuggets.com/2016/06/mining-twitter-data-python-part-2.html
# https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
# http://www.nltk.org/book/ch05.html
# http://nlpforhackers.io/sentiment-analysis-intro/
# http://sentiment.christopherpotts.net/lexicons.html#resources (to add more lexicons later)


import json
import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
stoplist = stopwords.words('english')
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

tweet_store = []
"""with open('python.json', 'r') as f:
        lines = f.readlines() # read only the first tweet/line
        for line in lines:
            tweet = json.loads(line) # load it as Python dict
            tweet_text = tweet["u'text'"]
            tweet_store.append(tweet_text)"""
            
with open('python.json', 'r') as f:
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        tweet_text = tweet['text']
        tweet_store.append(tweet_text)
        
            
    
"""with open('python.json', 'r') as f:
        line = f.readline() # read only the first tweet/line
        tweet = json.loads(line) # load it as Python dict
        #print(json.dumps(tweet, indent=4)) # pretty-print
        tweet_text = tweet['text']
        tweet_store.append(tweet_text)"""


def text_prep(x):
    from bs4 import BeautifulSoup
    b_strip = BeautifulSoup(x, 'lxml')

# kill all script and style elements
    for script in b_strip(["script", "style"]):
        script.extract()    # rip it out

# get text
    text = b_strip.get_text()

# break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
# (')aphostophe  replacement (ie)   you're --> you are  
# ( basic dictionary lookup : master dictionary present in a hidden block of code)
    #https://drive.google.com/file/d/0B1yuv8YaUVlZZ1RzMFJmc1ZsQmM/view
    # Aphost lookup dict
    APPO = {
            "aren't" : "are not",
            "can't" : "cannot",
            "couldn't" : "could not",
            "didn't" : "did not",
            "doesn't" : "does not",
            "don't" : "do not",
            "hadn't" : "had not",
            "hasn't" : "has not",
            "haven't" : "have not",
            "he'd" : "he would",
            "he'll" : "he will",
            "he's" : "he is",
            "i'd" : "I would",
            "i'd" : "I had",
            "i'll" : "I will",
            "i'm" : "I am",
            "isn't" : "is not",
            "it's" : "it is",
            "it'll":"it will",
            "i've" : "I have",
            "let's" : "let us",
            "mightn't" : "might not",
            "mustn't" : "must not",
            "shan't" : "shall not",
            "she'd" : "she would",
            "she'll" : "she will",
            "she's" : "she is",
            "shouldn't" : "should not",
            "that's" : "that is",
            "there's" : "there is",
            "they'd" : "they would",
            "they'll" : "they will",
            "they're" : "they are",
            "they've" : "they have",
            "we'd" : "we would",
            "we're" : "we are",
            "weren't" : "were not",
            "we've" : "we have",
            "what'll" : "what will",
            "what're" : "what are",
            "what's" : "what is",
            "what've" : "what have",
            "where's" : "where is",
            "who'd" : "who would",
            "who'll" : "who will",
            "who're" : "who are",
            "who's" : "who is",
            "who've" : "who have",
            "won't" : "will not",
            "wouldn't" : "would not",
            "you'd" : "you would",
            "you'll" : "you will",
            "you're" : "you are",
            "you've" : "you have",
            "'re": " are",
            "wasn't": "was not",
            "we'll":" we will",
            "didn't": "did not",
            "tryin'":"trying"
            }

# handle encoding on "text" table item so that table can be exported
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    from nltk import word_tokenize, WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize((text))
    words=[APPO[word] if word in APPO else word for word in words]
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in stoplist]
    return str(' '.join(words))

def pos_tagger(x):
    token =nltk.word_tokenize((x))
    tagged = nltk.pos_tag(token)
    return (tagged)

def hashtag_ext(x):
    ext = [i for i in x.split() if i.startswith("#")]
    return(ext)        

def hashtag_rem(x):
    rem = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x).split())
    return(rem)
    
def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

# take list of tweets and put into data frame              
tweet_df = pd.DataFrame({'tweet': tweet_store})
# extract hashtags into their own column on the datafrome, for later analysis as following lines of code strip them out ahead of POS tagging
tweet_df['hashtags'] = tweet_df['tweet'].apply(lambda row: hashtag_ext(row))
# remove # as text prep puts a space inbetween # and hastag name, SHOULD FIX THIS
tweet_df['tweet_strpd'] = tweet_df['tweet'].apply(lambda row: hashtag_rem((row))) 
# text prep and pop into new column
tweet_df['tweet_prepd'] = tweet_df['tweet_strpd'].apply(lambda row: text_prep (row))
   
# add a column of POS tagged tweet
tweet_df['tweet_tagged'] = tweet_df['tweet_strpd'].apply(lambda row: pos_tagger(row))

def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None

def swn_polarity(x):
    """
    Return a sentiment polarity: 0 = negative, 1 = positive
    """
 
    sentiment = 0.0
    tokens_count = 0
    
    for word, tag in x:
        wn_tag = penn_to_wn(tag)
        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV, wn.VERB):
            continue
        
        lemma = lemmatizer.lemmatize(word, pos=wn_tag)
        if not lemma:
            continue
        
        synsets = wn.synsets(lemma, pos=wn_tag)
        if not synsets:
            continue
 
    # Take the first sense, the most common
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
 
        sentiment += swn_synset.pos_score() - swn_synset.neg_score()
        tokens_count += 1
 
    # judgment call ? Default to positive or negative
    if not tokens_count:
        return 0
 
    # sum greater than 0 => positive sentiment
    if sentiment >= 0:
        return sentiment
 
    # negative sentiment
    return 0


# https://github.com/dipanjanS/text-analytics-with-python/blob/master/Chapter-7/sentiment_analysis_unsupervised_lexical.py

def swn_polarity_2(review, verbose=False):
    
    # tokenize and POS tag text tokens
    text_tokens = nltk.word_tokenize(review)
    tagged_text = nltk.pos_tag(text_tokens)
    pos_score = neg_score = token_count = obj_score = 0
    # get wordnet synsets based on POS tags
    # get sentiment scores if synsets are found
    for word, tag in tagged_text:
        ss_set = None
        if 'NN' in tag and swn.senti_synsets(word, 'n'):
            ss_set = swn.senti_synsets(word, 'n')[0]
        elif 'VB' in tag and swn.senti_synsets(word, 'v'):
            ss_set = swn.senti_synsets(word, 'v')[0]
        elif 'JJ' in tag and swn.senti_synsets(word, 'a'):
            ss_set = swn.senti_synsets(word, 'a')[0]
        elif 'RB' in tag and swn.senti_synsets(word, 'r'):
            ss_set = swn.senti_synsets(word, 'r')[0]
        # if senti-synset is found        
        if ss_set:
            # add scores for all found synsets
            pos_score += ss_set.pos_score()
            neg_score += ss_set.neg_score()
            obj_score += ss_set.obj_score()
            token_count += 1
    
    # aggregate final scores
    final_score = pos_score - neg_score
    norm_final_score = round(float(final_score) / token_count, 2)
    #final_sentiment = 1 if norm_final_score >= 0 else 0
        
    return norm_final_score    


tweet_df['tweet_swntagged_swn_polarity'] = tweet_df['tweet_tagged'].apply(lambda row: swn_polarity(row))
#tweet_df['tweet_swntagged_compute_score'] = tweet_df['tweet_tagged'].apply(lambda row: compute_score(row))
tweet_df['tweet_swntagged_swn_polarity_2'] = tweet_df['tweet_strpd'].apply(lambda row: swn_polarity_2(row, verbose=False))
#final_sentiment = analyze_sentiment_sentiwordnet_lexicon(tweet_df['tweet_strpd'], verbose=False)
tweet_df.to_excel('C:\Users\HP-Colm\Documents\Python Scripts\AIB Twitter Project/tweet_df.xlsx', sheet_name='Sheet1')
