import pandas as pd
import dbm
import tweepy
import Modules.pandasmgt
import Modules.twitter_auth
import Modules.databasemgt
import datetime

print("##### Modulo coletartweets")
print("----> Módulo iniciado.")

# Autentica a API
api = Modules.twitter_auth.load_api()

# Parametros do Tweepy Cursor
itemcount = 20
search_words = '("THREAT" OR "MALWARE" OR "VIRUS" OR "ATTACK" OR "VULNERABILITY") AND ("IOT" OR "CPS" OR "SCADA" OR "INDUSTRY 4.0")'
tweet_filter = " -filter:retweets"
search_query = search_words + tweet_filter

print(f"----> Parametros carregados: {search_query} - Qtd Itens: {itemcount}")

# Pesquisa os Tweets conforme String de pesquisa

print("----> Pesquisando Tweets.....")

tweets = []

set_of_tweets = tweepy.Cursor(api.search, q=search_query, tweet_mode='extended', lang='en').items(itemcount)

for tweet in set_of_tweets:
    tweets.append(tweet)

print(f"----> Pesquisa concluida. Itens identificados: {tweets.__len__()}")

#
# Remove os tweets que não atendem os requisitos.
#

num_followers = 1000
num_tweets = 1000
created_until = 2020
min_tweet_text_len = 30

temp_tweets = []
for tweet in tweets:
    if tweet.author.followers_count > num_followers:
        temp_tweets.append(tweet)
tweets = temp_tweets.copy()

print(f"----> Removidos 'followers_count' < {num_followers} . Restantes: {tweets.__len__()}")

temp_tweets = []
for tweet in tweets:
    if tweet.author.statuses_count > num_tweets:
        temp_tweets.append(tweet)
tweets = temp_tweets.copy()

print(f"----> Removidos 'statuses_count' < {num_tweets}. Restantes: {tweets.__len__()}")

temp_tweets = []
for tweet in tweets:
    if tweet.author.created_at <= datetime.datetime(2019, 6, 1):
        temp_tweets.append(tweet)
tweets = temp_tweets.copy()

print(f"----> Removidos 'created_at' > {created_until}. Restantes: {tweets.__len__()}")

temp_tweets = []
for tweet in tweets:
    if tweet.full_text.__len__() >= min_tweet_text_len:
        temp_tweets.append(tweet)
tweets = temp_tweets.copy()

print(f"----> Removidos tweets com menos de {min_tweet_text_len} caracteres. Restantes: {tweets.__len__()}")

print("----> Remoção dos tweets baseados nos requisitos mínimos concluída.")

#
# Pegar as propriedades dos Tweets
#

tweetdictkeys = {'id': None, 'full_text': None, 'created_at': None}

#
# Criar o dataframe com Tweets
#

df_tweets = Modules.pandasmgt.create_df_tweets(tweets_keys=tweetdictkeys, tweets=tweets)

print(f"----> Criação do dicionário com Tweets. Qtd: {df_tweets.__len__()}")

#
# Remove os tweets já existentes na base
#

try:
    df_current_tweets = Modules.databasemgt.get_df_from_database(sqlquery="SELECT id FROM public.tbl_tweets;")

    for id in df_current_tweets["id"]:
        df_tweets = df_tweets[df_tweets["id"] != int(id)]

except dbm.error:
    print(f"----> A tabela 'tbl_tweets' ainda não foi criada.")
except Exception as error:
    print(f"----> Ocorreu o seguinte erro: {error}")

print(f"----> Removidos tweets já cadastrados . Restantes: {df_tweets.__len__()}")

#
# Insere os tweets do dicionário ao banco de dados
#

# Modules.databasemgt.create_database_table_from_df(df_autores, 'tbl_novos_autores')

Modules.databasemgt.write_df_into_database_table(dataframe=df_tweets, pd_parameters='tbl_tweets_test')

print("----> Autores inseridos na tabela SQL.")

# write_df_into_database_table(dataframe = pd.DataFrame, pd_parameters = str):

#
# Imprime os autores no Pandas
#
print(df_tweets[['id']])



