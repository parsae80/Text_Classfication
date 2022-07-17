import csv
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from torch import nn
from torch.nn import functional as F
from torch.optim import Adam
from tqdm import tqdm
import gc

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


# because of dealing with non-ASCII characters, we need to specify the character encoding in the open() function
with open('Hamshahri_Corpus.csv', 'w', encoding = 'utf-8')as hCorpusCSV:
    writer = csv.writer(hCorpusCSV)
    # write a row to the csv file
    writer.writerow(news_cat_body_list)
    
 import pandas as pd

df = pd.DataFrame(news_cat_body_list, columns = ['Category', 'NewsBody'])
headerList = ['Cat', 'Body']
  
# converting data frame to csv
df.to_csv("/content/Hamshahri_Corpus.csv", header=headerList, index=False)
  
# display modified csv file
news_df = pd.read_csv("/content/Hamshahri_Corpus.csv")
X = news_df.loc[:,"Body"]
y = news_df.loc[:,"Cat"]
X_vector=TfidfVectorizer().fit_transform(X)
X_train, X_test, y_train, y_test=train_test_split(X_vector,y,test_size=0.2, random_state=42)


embed_len = 50
hidden_dim = 50
n_layers= 8

class RNNClassifier(nn.Module):
    def __init__(self):
        super(RNNClassifier, self).__init__()
        self.embedding_layer = nn.Embedding(num_embeddings=128, embedding_dim=embed_len)
        self.rnn = nn.RNN(input_size=embed_len, hidden_size=hidden_dim, num_layers=n_layers,
                          batch_first=True, nonlinearity="relu", dropout=0.2)

    def forward(self, X_batch):
        embeddings = self.embedding_layer(X_batch)
        output, hidden = self.rnn(embeddings, torch.randn(n_layers, len(X_batch), hidden_dim))
        return self.linear(output[:,-1])
    

 
def CalcValLossAndAccuracy(model, loss_fn, val_loader):
    with torch.no_grad():
        Y_shuffled, Y_preds, losses = [],[],[]
        for X, Y in val_loader:
            preds = model(X)
            loss = loss_fn(preds, Y)
            losses.append(loss.item())

            Y_shuffled.append(Y)
            Y_preds.append(preds.argmax(dim=-1))

        Y_shuffled = torch.cat(Y_shuffled)
        Y_preds = torch.cat(Y_preds)

        print("Valid Loss : {:.3f}".format(torch.tensor(losses).mean()))
        print("Valid Acc  : {:.3f}".format(accuracy_score(Y_shuffled.detach().numpy(), Y_preds.detach().numpy())))


def TrainModel(model, loss_fn, optimizer, train_loader, val_loader, epochs=10):
    for i in range(1, epochs+1):
        losses = []
        for X, Y in tqdm(train_loader):
            Y_preds = model(X)

            loss = loss_fn(Y_preds, Y)
            losses.append(loss.item())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print("Train Loss : {:.3f}".format(torch.tensor(losses).mean()))
        CalcValLossAndAccuracy(model, loss_fn, val_loader)
        

epochs = 15
learning_rate = 1e-3

loss_fn = nn.CrossEntropyLoss()
rnn_classifier = RNNClassifier()
optimizer = Adam(rnn_classifier.parameters(), lr=learning_rate)

TrainModel(rnn_classifier, loss_fn, optimizer, train_loader, test_loader, epochs)
