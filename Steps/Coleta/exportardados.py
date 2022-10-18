import pandas as pd
import dbm
import tweepy
import Modules.pandasmgt
import Modules.twitter_auth
import Modules.databasemgt
import datetime


#
# Exporta os dados para CSV prontos para o DOCCANO e análise.
#

########## CSV RawData ##########

exp_directory = "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Export de Tweets para processamento\\"
file_name = "tweets_rawdata " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S') + ".csv"

try:
    df_tweets = Modules.databasemgt.get_df_from_database(sqlquery="SELECT * FROM public.tbl_tweets_v2;")

    df_tweets.to_csv(path_or_buf=exp_directory + file_name, sep=';', na_rep='', header=True, index=False, mode='w', encoding="utf-8",
                     quotechar='"', date_format=None, doublequote=True, decimal='.', errors='strict')

except dbm.error:
    print(f"----> A tabela 'tbl_tweets' ainda não foi criada?")
except Exception as error:
    print(f"----> Ocorreu o seguinte erro: {error}")

print(f"----> Exportação finalizada para Análise.")
print(f"----> Tweets extraidos: {df_tweets.__len__()}")

########## CSV DOCCANO ##########

file_name_doc = "tweets_DOCCANO " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S') + ".json"

try:
    df_tweets = Modules.databasemgt.get_df_from_database(sqlquery="SELECT * FROM public.tbl_tweets_v2;")

    #df_tweets.to_csv(path_or_buf=exp_directory + file_name_doc, sep=';', na_rep='', header=True, index=False, mode='w', encoding="utf-8",
    #                 quotechar='"', date_format=None, doublequote=True, decimal='.', errors='strict')

    df_tweets.to_json(path_or_buf=exp_directory + file_name_doc, orient="records")

except Exception as error:
    print(f"----> Ocorreu o seguinte erro: {error}")

print(f"----> Exportação finalizada para o DOCCANO.")
print(f"----> Tweets extraidos: {df_tweets.__len__()}")

print(f"----> Diretório: {exp_directory + file_name}")


