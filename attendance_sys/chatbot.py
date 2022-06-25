# install and import various libraries like NLTK,RANDOM,STRING,SKLEARN,

import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Here main database file is attached on which we are going to process our chatbot.
# Right now we are using simple text file as database and it is accessed by its path address.
f = open("./static/meaec.txt", "rt")
raw = f.read()
raw = raw.lower()

# def update(fromuser):
#     fu = open("C:\\chatbot\\questions.txt", "rt")
#     file = fu.write(fromuser)


sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)
# sent_tokens[:]
# word_tokens[:]


# now pre-processing of text file
# ----pre-processing ----
# Lematization :

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


# Remove punctuations
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Now core function of Chatbot

# ---Code for initial response---

GREETING_INPUT = ("hello", "hi", "hii", "hey buddy", "hey", "what's up", "wassup")
GREETING_RESPONSES = ("Hi there...", "hey,how can I help you...", "glad you are here! how may can i help you...")
ENDING = ("bye", "thanks", "thank you")


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUT:
            return random.choice(GREETING_RESPONSES)


# print(greeting("Heyy good morning"))

# the words need to be encoded as integers or floating point values
# for use as input to a machine learning algorithm, called feature extraction (or vectorization).
# find the similarity between words entered by the user and the words in the corpus.
# This is the simplest possible implementation of a chatbot.


# Generating response:
# define a function response which searches the user’s utterance for one or more known keywords
# and returns one of several possible responses. If it doesn't find the input matching any of the keywords,
# it returns a response:” I am sorry! I don’t understand you”
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)

    # Learn vocabulary and idf, return term-document matrix
    # Returns X : Tf-idf-weighted sparse matrix, [n_samples, n_features]

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    # print (tfidf.shape)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = vals.argsort()[0][-2]

    flat = vals.flatten()

    flat.sort()
    req_tfidf = flat[-2]

    #    user_response = user_response.lower()
    if user_response.lower() in GREETING_INPUT:
        robo_response = greeting(user_response)
        return robo_response
    
    if user_response.lower() in GREETING_INPUT:
        robo_response = response.f
        return robo_response


    elif user_response.lower() in ENDING:
        robo_response = "You are Welcome..I hope your queries get satisfied..HAVE A NICE DAY 😀"
        return robo_response

    elif req_tfidf == 0:
        robo_response = robo_response + "I am sorry! I don't understand you"
        #        update(user_response)
        return robo_response

    else:
        greeting(user_response)
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


def get_bot_response(msg):
    userText = msg  # get data from input,we write js  to index.html
    s = response(userText)
    sent_tokens.remove(userText)
    return str(s)
