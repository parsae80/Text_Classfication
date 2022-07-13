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
    count = 0;
    for line in hCorpus:
        line = line.replace('\t', ',')
        new_line = ""
        if (line.strip().startswith(".DID") or is_first_did):
            if is_first_did:
                is_first_did = False
            count += 1
            if count == 2:
                full_body_news.append(news_body)
                news_body = ""
                count = 0
            new_line = line.replace('\t', ',')
            new_line = new_line.replace('\n', '')
            new_line = new_line.split(',')
            news_did.append(new_line[1])
            # if is_first_did:
            #   is_first_did = False
        elif (line.startswith(".Cat")):
            new_line = line.replace('\t', ',')
            new_line = new_line.replace('\n', '')
            new_line = new_line.split(',')
            news_category.append(new_line[1])
        elif (line.startswith('.Date')):
            new_line = line.replace('\t', ',')
            new_line = new_line.replace('\n', '')
            new_line = new_line.split(',')
            news_date.append(new_line[1])
        else:
            news_body += line.strip()
            news_cat_body_list = list(zip(news_category, full_body_news))

print(news_did)
