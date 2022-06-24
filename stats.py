from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

import emoji


extract = URLExtract()


def fetchstats(selected_user, df):

    #se o usuário selecionado for um usuário específico, faça alterações no dataframe, caso contrário, não faça alterações

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # contando o número de arquivos de mídia compartilhados

    mediaommitted = df[df['Message'] == '<Media omitted>']

    # Numero de links compartilhados 

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), mediaommitted.shape[0], len(links)


# Usuario mais ocupado ( nivel do grupo) 

def fetchbusyuser(df):

    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()

    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, newdf


def createwordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500,
                   min_font_size=10, background_color='white')

    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return df_wc


# obter as palavras mais comuns, isso retornará um dataframe de palavars mais comuns


def getcommonwords(selecteduser, df):

    # getting the stopwords

    file = open('stop_hinglish.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df[(df['User'] != 'Group Notification') |
              (df['User'] != '<Media omitted>')]

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


def getemojistats(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojidf


def monthtimeline(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))

    temp['Time'] = time

    return temp


def monthactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Month'].value_counts()


def weekactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Day_name'].value_counts()
