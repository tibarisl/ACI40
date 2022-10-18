import pandas as pd
import dbm
import tweepy
from spacy.pipe_analysis import analyze_pipes

import Modules.pandasmgt
import Modules.twitter_auth
import Modules.databasemgt
import datetime

print("##### Modulo enriquecer tweets")
print("----> Módulo iniciado.")
 
# Autentica a API
api = Modules.twitter_auth.load_api()

#
# Carrega os IDs de tweets ja existentes na tabela "tbl_tweets" e realiza a pesquisa.
#
tweets = []
tweetdictkeys = {'id': None, 'full_text': None, 'screen_name': None, 'created_at': None}
df_current_tweets = Modules.databasemgt.get_df_from_database(sqlquery="SELECT id FROM public.tbl_tweets;")

#
# Remove os tweets já existentes na base
#

try:
    table_v2 = Modules.databasemgt.get_df_from_database(sqlquery="SELECT id FROM public.tbl_tweets_v2;")

    for id in table_v2["id"]:
        df_current_tweets = df_current_tweets[df_current_tweets["id"] != int(id)]

except Exception as error:
    print(f"----> Ocorreu o seguinte erro: {error}")

print(f"----> Removidos tweets já cadastrados . Restantes: {df_current_tweets.__len__()}")

#
# Coleta os tweets no Twitter
#
print(f"----> Coletando itens no Twitter")

count = 0
failed_items_list = []

for tw_id in df_current_tweets["id"]:

    count += 1

    if count > 500:
        break

    print(f"----> Item N: {count}")
    try:
        tweet = api.get_status(tw_id, tweet_mode="extended")
        tweets.append(tweet)

    except Exception as error:
        message = f"----> Tweet:{tw_id} - An exception of type {type(error).__name__} occurred. Arguments: {error.args!r}"
        print(message)
        failed_items_list.append([id, message])

print(f"----> Array com todos os Tweets criado. Qtd itens: {tweets.__len__()}")

print(f"----> Erros identificados: {failed_items_list.__len__()}")
print(f"----> #" + 25 * "#")

count =0
for item in failed_items_list:
    count += 1
    print(f"----> N:{count:<4} - Tweet: {item[1]}")

print(f"----> Criando Dataframe.")

df_tweets = Modules.pandasmgt.create_df_tweets_v2(tweets_keys=tweetdictkeys, tweets=tweets)

print("----> Dataframe criado.")

#
# Insere os tweets do dicionário ao banco de dados
#

#Modules.databasemgt.create_database_table_from_df(df_tweets, 'tbl_tweets_v2')

Modules.databasemgt.write_df_into_database_table(dataframe=df_tweets, pd_parameters='tbl_tweets_v2')

print("----> Tweets inseridos na tabela SQL.")