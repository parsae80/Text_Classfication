import csv
from sklearn.model_selection import train_test_split
import pandas as pd

stopwords = []
with open('PersianStopWords.txt', 'r', encoding='utf-8')as stopWordsList:
    for line in stopWordsList:
        for word in line.split('\n'):
            stopwords.append(word)


persian_alphabet = ['ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر',
                    'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                    'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']

english_alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z')
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
            new_line = line.replace('\t', ',')
            new_line = new_line.replace('\n', '')
            new_line = new_line.split(',')
            news_date.append(new_line[1])
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


#
# features = pd.read_csv('Hamshahri_Corpus.csv')
# # One-hot encode the data using pandas get_dummies
# features = pd.get_dummies(features)
# train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
# # print(test)
# print(train)
