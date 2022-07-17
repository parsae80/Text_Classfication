import csv
from sklearn.model_selection import train_test_split
import pandas as pd

stopwords = []
with open('PersianStopWords.txt', 'r', encoding='utf-8')as stopWordsList:
    for line in stopWordsList:
        for word in line.split('\n'):
            stopwords.append(word)



full_body_news = []
news_category = []
news_date = []
news_did = []
news_body = ""
is_first_did = True
with open('Hamshahri-Sample.txt', 'r', encoding='utf-8') as hCorpus:
    for line in hCorpus:
        line = line.replace('\t', ',')
        new_line = ""
        if line.strip().startswith(".DID") or is_first_did or not line:
            if is_first_did:
                is_first_did = False

            if news_body != '':
                full_body_news.append(news_body)
            news_body = ""
            new_line = line.replace('\t', ',')
            new_line = new_line.replace('\n', '')
            new_line = new_line.split(',')
            news_did.append(new_line[1])

        elif line.startswith(".Cat"):
            new_line = line.replace('\t', ',')
            new_line = new_line.replace('\n', '')
            new_line = new_line.split(',')
            news_category.append(new_line[1])
        elif line.startswith('.Date'):
            continue
        else:
            news_body_temp = ''
            news_body_temp += line.strip()
            for word in news_body_temp.split(' '):
                if word in stopwords:
                    news_body_temp = news_body_temp.replace(word, '')

            news_body += news_body_temp
news_cat_body_list = list(zip(news_category, full_body_news))


# because of dealing with non-ASCII characters, we need to specify the character encoding in the open() function
with open('Hamshahri_Corpus.csv', 'w', encoding='utf-8')as hCorpusCSV:
    writer = csv.writer(hCorpusCSV)
    # write a row to the csv file
    writer.writerow(news_cat_body_list)


news_category_list = []
with open('Hamshahri-Categories.txt','r', encoding='utf-8')as hCats:
    for line in hCats:
        for word in line.split(' '):
            if word not in news_category_list and word != '\n' and word != '':
                news_category_list.append(word)

tokens = []


def tokenize_corpus(corpus):
    for line in full_body_news:
        for word in line.split(' '):
            if len(word) > 1:
                if word not in stopwords:
                    tokens.append(word)

    return tokens

tokenized_corpus = tokenize_corpus(full_body_news)
vocabulary = []
for word in tokenized_corpus:
    if word not in vocabulary and word is not '':
        vocabulary.append(word)
