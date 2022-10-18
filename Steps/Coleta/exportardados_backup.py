import pandas as pd
import dbm
import tweepy
import Modules.pandasmgt
import Modules.twitter_auth
import Modules.databasemgt
import datetime


#
# Exporta os dados para CSV prontos para o DOCCANO.
#

exp_directory = "D:\\Dados_TCC\\"
file_name = "tweets_bkp.csv"

try:
    #df_tweets = Modules.databasemgt.get_df_from_database(sqlquery="SELECT id, full_text FROM public.tbl_tweets;")
    df_tweets = Modules.databasemgt.get_df_from_database(sqlquery="SELECT * FROM public.tbl_tweets;")

    df_tweets.to_csv(path_or_buf=exp_directory + file_name, sep=';', na_rep='', header=True, index=False, mode='w', encoding="utf-8",
                     quotechar='"', date_format=None, doublequote=True, decimal='.', errors='strict')

except dbm.error:
    print(f"----> A tabela 'tbl_tweets' ainda não foi criada?")
except Exception as error:
    print(f"----> Ocorreu o seguinte erro: {error}")

print(f"----> Exportação finalizada.")
print(f"----> Tweets extraidos: {df_tweets.__len__()}")
print(f"----> Diretório: {exp_directory + file_name}")
