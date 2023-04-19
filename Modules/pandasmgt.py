import pandas as pd
import datetime

def create_df_authors(author_keys, tweets):
    print("##### Função create_df_authors: ")

    dicionario = author_keys.copy()

    for tweet in tweets:
        if dicionario["id"] is None or not tweet.author._json["id"] in dicionario["id"]:
            print(f"----> Novo autor no dicionario: {tweet.author._json['id']}")
            cont = 0
            for key in dicionario.keys():
                cont += 1
                try:
                    aukey = tweet.author._json[key]
                    dicionario[key].append(aukey)
                except KeyError:
                    aukey = ""
                    dicionario[key].append("")
                except:
                    dicionario[key] = [aukey]
                print(f"----> N:{cont:<4}:{dicionario.__len__():<4} - Autor[key]: {key:<25} - Valor[key]: {aukey}")
            print("----> " + 50 * "=#")
        else:
            print(f"----> {tweet.author._json['id']} ja esta no dicionario")

    author_df = pd.DataFrame.from_dict(data=dicionario)

    print("----> Dicionario concluido. Retornando data frame.\n")

    return author_df


def create_df_tweets(tweets_keys, tweets):
    print("##### Função create_df_tweets: ")

    dicionario = tweets_keys.copy()

    for tweet in tweets:
        if dicionario["id"] is None or not tweet._json["id"] in dicionario["id"]:
            cont = 0
            for key in dicionario.keys():
                cont += 1
                try:
                    twkey = tweet._json[key]
                    dicionario[key].append(twkey)
                except KeyError as error:
                    twkey = ""
                    dicionario[key].append("")
                except AttributeError as error:
                    dicionario[key] = [twkey]
                except Exception as error:
                    template = f"An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(error).__name__, error.args)
                    print(message)
                finally:
                    print(f"----> N:{cont:<4}:{dicionario.__len__():<4} - Tweet[key]: {key:<25} - Valor[key]: {twkey}")
            print("----> " + 50 * "=#")
        else:
            print(f"----> {tweet._json['id']} ja está no dicionario")

    tweets_df = pd.DataFrame.from_dict(data=dicionario)

    print("----> Dicionario concluido. Retornando data frame.\n")

    return tweets_df


def create_df_tweets_v2(tweets_keys, tweets):
    print("##### Função create_df_tweets_v2: ")

    dicionario = tweets_keys.copy()

    for tweet in tweets:
        if dicionario["id"] is None or not tweet._json["id"] in dicionario["id"]:
            cont = 0
            for key in dicionario.keys():
                cont += 1
                try:
                    if key == "screen_name":
                        twkey = tweet._json["user"][key]
                        if dicionario[key] == None:
                            dicionario[key] = [twkey]
                        else:
                            dicionario[key].append(twkey)
                    elif key == "created_at":
                        twkey = datetime.datetime.strftime(datetime.datetime.strptime(tweet._json[key],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
                        dicionario[key].append(twkey)
                    else:
                        twkey = tweet._json[key]
                        dicionario[key].append(twkey)
                except KeyError as error:
                    twkey = ""
                    dicionario[key].append("")

                except AttributeError as error:
                    dicionario[key] = [twkey]
                except Exception as error:
                    template = f"An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(error).__name__, error.args)
                    print(message)
                finally:
                    print(f"----> N:{cont:<4}:{dicionario.__len__():<4} - Tweet[key]: {key:<25} - Valor[key]: {twkey}")
            print("----> " + 50 * "=#")
        else:
            print(f"----> {tweet._json['id']} ja está no dicionario")

    tweets_df = pd.DataFrame.from_dict(data=dicionario)

    print("----> Dicionario concluido. Retornando data frame.\n")

    return tweets_df


def remove_df_items(dataframe=pd.DataFrame, column_name=str, comparation_string=str, value=object):

    print("##### Função remove_df_items: ")

    if comparation_string == "<":
        new_dataframe = dataframe[dataframe[column_name] >= value]
    elif comparation_string == ">":
        new_dataframe = dataframe[dataframe[column_name] <= value]
    elif comparation_string == "==":
        new_dataframe = dataframe[dataframe[column_name] != value]
    elif comparation_string == "!=":
        new_dataframe = dataframe[dataframe["column_name"] == value]
    else:
        raise Exception("Valor do parametro 'value' nao é válido")

    return new_dataframe
