import pandas
import tweepy
import Modules.twitter_auth
import Old_code.dicionariomgt_old
import datetime

print("##### Modulo indetificarfontes")
print("----> Módulo iniciado.")

# Autentica a API
api = Modules.twitter_auth.load_api()

# Parametros do Tweepy Cursor
itemcount = 100
search_words = "#opendir"
tweet_filter = " -filter:retweets"
search_query = search_words, tweet_filter

print(f"----> Parametros carregados: {search_query}")

# Pesquisa os Tweets conforme String de pesquisa

print("----> Pesquisando Tweets.....")

tweets = []

for tweet in tweepy.Cursor(api.search, q=search_query).items(itemcount):
    tweets.append(tweet)

print(f"----> Pesquisa concluida. Itens identificados: {tweets.__len__()}")

# Pega todas as propriedades do autor

autordictkeys = {'id': None, 'id_str': None, 'name': None, 'screen_name': None, 'location': None,
                 'description': None, 'url': None, 'entities': None, 'protected': None, 'followers_count': None,
                 'friends_count': None, 'listed_count': None, 'created_at': None, 'favourites_count': None, 'utc_offset': None,
                 'time_zone': None, 'geo_enabled': None, 'verified': None, 'statuses_count': None, 'lang': None,
                 'contributors_enabled': None, 'is_translator': None, 'is_translation_enabled': None, 'profile_background_color': None, 'profile_background_image_url': None,
                 'profile_background_image_url_https': None, 'profile_background_tile': None, 'profile_image_url': None, 'profile_image_url_https': None, 'profile_banner_url': None,
                 'profile_link_color': None, 'profile_sidebar_border_color': None, 'profile_sidebar_fill_color': None, 'profile_text_color': None, 'profile_use_background_image': None,
                 'has_extended_profile': None, 'default_profile': None, 'default_profile_image': None, 'following': None, 'follow_request_sent': None,
                 'notifications': None, 'translator_type': None, 'withheld_in_countries': None}

print(f"----> Biblioteca de autores criada.")

# Remoção das chaves que não vao ser utilizadas

#del autordictkeys['contributors_enabled']
#del autordictkeys['created_at']
del autordictkeys['default_profile']
del autordictkeys['default_profile_image']
#del autordictkeys['description']
#del autordictkeys['entities']
#del autordictkeys['favourites_count']
del autordictkeys['follow_request_sent']
#del autordictkeys['followers_count']
del autordictkeys['following']
#del autordictkeys['friends_count']
del autordictkeys['geo_enabled']
del autordictkeys['has_extended_profile']
#del autordictkeys['id']
#del autordictkeys['id_str']
del autordictkeys['is_translation_enabled']
del autordictkeys['is_translator']
del autordictkeys['lang']
#del autordictkeys['listed_count']
#del autordictkeys['location']
#del autordictkeys['name']
#del autordictkeys['notifications']
del autordictkeys['profile_background_color']
del autordictkeys['profile_background_image_url']
del autordictkeys['profile_background_image_url_https']
del autordictkeys['profile_background_tile']
if "profile_banner_url" in autordictkeys: del autordictkeys['profile_banner_url']
del autordictkeys['profile_image_url']
del autordictkeys['profile_image_url_https']
del autordictkeys['profile_link_color']
del autordictkeys['profile_sidebar_border_color']
del autordictkeys['profile_sidebar_fill_color']
del autordictkeys['profile_text_color']
del autordictkeys['profile_use_background_image']
del autordictkeys['protected']
#del autordictkeys['screen_name']
#del autordictkeys['statuses_count']
del autordictkeys['time_zone']
del autordictkeys['translator_type']
#del autordictkeys['url']
del autordictkeys['utc_offset']
#del autordictkeys['verified']
del autordictkeys['withheld_in_countries']

print("----> Remoção das chaves indesejadas concluida.")

# Cria o dicionário com autores
autorcolec = Old_code.dicionariomgt_old.criardicionarioautor(autordictkeys, tweets)

print(f"----> Criação do dicionário com autores. Qtd: {autorcolec.__len__()}")

# Remove os autores que não atendem os requisitos.
autorcolec = Old_code.dicionariomgt_old.deletaritemdicionario(autorcolec, "followers_count", 5000, "menor")
autorcolec = Old_code.dicionariomgt_old.deletaritemdicionario(autorcolec, "statuses_count", 1000, "menor")
autorcolec = Old_code.dicionariomgt_old.deletaritemdicionario(autorcolec, "created_at", datetime.datetime(2020, 10, 13), "maior")

print("----> Remoção dos autores baseados nos requisitos mínimos concluída.")

# Insere os autores do dicionário ao banco de dados
Old_code.dicionariomgt_old.inserirautoresnobanco(autorcolec)

# Imprime os autores no Pandas
dfautorescolec = pandas.DataFrame.from_dict(autorcolec)
print(dfautorescolec[['id', 'screen_name', 'followers_count', 'created_at']])