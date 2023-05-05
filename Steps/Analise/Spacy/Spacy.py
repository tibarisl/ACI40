import pandas
from Steps.Analise.Spacy.generate_train_file import generate_training_file
import spacy
from spacy.cli.train import train as trainsp
import Modules.databasemgt
import dbm
import tweepy
import Modules.pandasmgt
import Modules.twitter_auth
import datetime
import snscrape.modules.twitter as sntwitter
import sys

def gerar_arquivo_treino(sampleNumber):
    # Gerar arquivo de treino e teste baseado nos dados do DOCCANO
    generate_training_file(rdmstate=sampleNumber, filepath="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Doccano\\admin.jsonl", outdir="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\TrainFile\\")


def criar_modelo(resultNumber):

    output_filename = 'G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\TrainFile\\Resultado RS'+ str(resultNumber) + '.txt'

    # Executar este comandos no Terminal para criação do arquivo "config" baseado no "base_config" = Executado apenas uma vez!
    # python -m spacy init fill-config "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\base_config.cfg" "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\config.cfg"

    # Executar esta linha de comando no Terminal para rodar os testes, usando o arquivo .test para o --paths.dev
    #          python -m spacy train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\config.cfg" --output "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\models" --paths.train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\train.spacy" --paths.dev "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\test.spacy"
    #command = 'python -m spacy train "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Spacy\\config.cfg" --output "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Spacy\\models" --paths.train "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\TrainFile\\train.spacy" --paths.dev "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\TrainFile\\test.spacy" > ' + output_filename

    config_path = "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Spacy\\config.cfg"
    output_path = "G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Spacy\\models"

    sys.stdout = open(output_filename, 'w', encoding="utf-8")
    trainsp(config_path, output_path)
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    return


def testar_ner(texto, ner):
    doc = ner(texto)  # input sample text

    lista = list()

    for ent in doc.ents:
        lista.append([ent.text, ent.start_char, ent.end_char, ent.label_])

    return lista
    # spacy.displacy.serve(doc, style="ent")


def verificar_dicionario(texto,tok):

    sql_string = f"""SELECT name FROM public.tbl_mitre_groups;"""

    lista = list()

    df_mitre_groups = Modules.databasemgt.get_df_from_database(sqlquery=sql_string)

    tokens = tok(texto)
    tokens_list = [token.text for token in tokens]

    for group in df_mitre_groups.values:
        if not (' ' in group[0]):
            if group[0].upper() in map(str.upper, tokens_list):
                lista.append(group[0])
        else:
            if group[0].upper() in tokens.text.upper():
                lista.append(group[0])
    return lista


def analisar_posts_SQL(num_posts):

    print("##### def analisar_posts_SQL")
    print("----> iniciado.")

    df_result = pandas.DataFrame(columns=['id', 'full_text', 'screen_name', 'created_at', 'Entidades', 'Threat actor(s)'])

    ner = spacy.load(r"G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\models\model-best")  # load the best model
    tok = spacy.load("en_core_web_lg")


    sql_string = f"""SELECT id,full_text, screen_name,created_at  FROM public.non_trained_tweets limit {num_posts};"""

    try:
        df_tweets = Modules.databasemgt.get_df_from_database(sqlquery=sql_string)



        file = open(f"G:\\Meu Drive\\TCC\TCC II - Everson Leonardi\\Projeto\\Dados\\Analise\\Analise_SQL_txt_{datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')}.txt", "x", encoding="utf-8")
        file_xlsx = (f"G:\\Meu Drive\\TCC\TCC II - Everson Leonardi\\Projeto\\Dados\\Analise\\Analise_SQL_excel_{datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')}.xlsx")

        for index, row in df_tweets.iterrows():
            print()
            file.write("\n")
            print(f"Item {index} de {df_tweets.index.size}")
            file.write(f"Item {index} de {df_tweets.index.size}\n")

            print(f"{10 * '====='}")
            file.write(f"{10 * '====='}\n")

            print(row['id'])
            file.write(str(row['id']))
            file.write("\n")

            print(row['screen_name'])
            file.write(str(row['screen_name']))
            file.write("\n")

            print(row['created_at'])
            file.write(str(row['created_at']))
            file.write("\n")

            print(row['full_text'])
            file.write(row['full_text'])
            file.write("\n")

            print(f"{10 * '-----'}")
            file.write(f"{10 * '-----'}\n")

            ent = testar_ner(row['full_text'], ner)
            print(f"Entidades: ")
            file.write(f"Entidades: ")
            for i in ent:
                print(i)
                file.write(str(i))
                file.write("\n")

            dic = verificar_dicionario(row['full_text'], tok)
            print(f"Threat actor(s): \n")
            file.write(f"Threat actor(s): \n")
            for i in dic:
                print(i)
                file.write(str(i))
            print()
            file.write("\n")


            df_tmp = pandas.Series([row['id'],row['full_text'], row['screen_name'], row['created_at'], ent, dic],index=['id', 'full_text', 'screen_name', 'created_at', 'Entidades', 'Threat actor(s)'])
            df_result = df_result.append(df_tmp, ignore_index=True)

        df_result.to_excel(file_xlsx)

    except dbm.error:
        print(f"----> A tabela 'tbl_tweets_v2' ainda não foi criada.")
    except Exception as error:
        print(f"----> Ocorreu o seguinte erro: {error}")

    print(f"----> Fim da execução. Tweets impressos: {df_tweets.__len__()}")


def analisar_posts_Twitter(num_posts):

    print("##### def analisar_posts_Twitter")
    print("----> iniciado.")

    # Autentica a API
    api = Modules.twitter_auth.load_api()

    # Parametros do Tweepy Cursor
    itemcount = num_posts
    #search_words = '("THREAT" OR "MALWARE" OR "VIRUS" OR "ATTACK" OR "VULNERABILITY") AND ("IOT" OR "CPS" OR "SCADA" OR "INDUSTRY 4.0")'
    search_words = "ATTACK AND IOT"
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

    # Cria um Daframe para adicionar os resultados.
    df_result = pandas.DataFrame(columns=['id', 'full_text', 'screen_name', 'created_at', 'Entidades', 'Threat actor(s)'])

    ner = spacy.load(r"G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\models\model-best")  # load the best model
    tok = spacy.load("en_core_web_lg")


    # Pegar as propriedades dos Tweets
    tweetdictkeys = {'id': None, 'full_text': None, 'screen_name': None, 'created_at': None}

    try:
        df_tweets = Modules.pandasmgt.create_df_tweets_v2(tweets_keys=tweetdictkeys, tweets=tweets)

        file = open(f"G:\\Meu Drive\\TCC\TCC II - Everson Leonardi\\Projeto\\Dados\\Analise\\Analise_Twitter_txt_{datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')}.txt", "x", encoding="utf-8")
        file_xlsx = (f"G:\\Meu Drive\\TCC\TCC II - Everson Leonardi\\Projeto\\Dados\\Analise\\Analise_Twitter_excel_{datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')}.xlsx")

        for index, row in df_tweets.iterrows():
            print()
            file.write("\n")
            print(f"Item {index} de {df_tweets.index.size}")
            file.write(f"Item {index} de {df_tweets.index.size}\n")

            print(f"{10 * '====='}")
            file.write(f"{10 * '====='}\n")

            print(row['id'])
            file.write(str(row['id']))
            file.write("\n")

            print(row['screen_name'])
            file.write(str(row['screen_name']))
            file.write("\n")

            print(row['created_at'])
            file.write(str(row['created_at']))
            file.write("\n")

            print(row['full_text'])
            file.write(row['full_text'])
            file.write("\n")

            print(f"{10 * '-----'}")
            file.write(f"{10 * '-----'}\n")

            ent = testar_ner(row['full_text'], ner)
            print(f"Entidades: ")
            file.write(f"Entidades: ")
            for i in ent:
                print(i)
                file.write(str(i))
                file.write("\n")

            dic = verificar_dicionario(row['full_text'], tok)
            print(f"Threat actor(s): \n")
            file.write(f"Threat actor(s): \n")
            for i in dic:
                print(i)
                file.write(str(i))
            print()
            file.write("\n")

            df_tmp = pandas.Series([row['id'], row['full_text'], row['screen_name'], row['created_at'], ent, dic],
                                   index=['id', 'full_text', 'screen_name', 'created_at', 'Entidades',
                                          'Threat actor(s)'])
            df_result = df_result.append(df_tmp, ignore_index=True)
        df_result.to_excel(file_xlsx)
    except dbm.error:
        print(f"----> A tabela 'tbl_tweets_v2' ainda não foi criada.")
    except Exception as error:
        print(f"----> Ocorreu o seguinte erro: {error}")

    print(f"----> Fim da execução. Tweets impressos: {df_tweets.__len__()}")

def analisar_posts_Twitter_v2(num_posts):

    api = Modules.twitter_auth.load_api()

    from datetime import datetime, timedelta

    data_inicio = datetime.now() - timedelta(days=180)
    data_inicio = data_inicio.strftime('%Y-%m-%d')

    string_de_pesquisa = '("Attack" AND "Industry 4" until:2021-01-01 since:2020-07-01)'

    tweetdictkeys = {'id': None, 'full_text': None, 'screen_name': None, 'created_at': None}

    tweets = []

    try:
        for tweet in sntwitter.TwitterSearchScraper(string_de_pesquisa).get_items():

            # print(vars(tweet))
            # break
            if len(tweets) == 2:
                break
            else:
                tweets.append([tweet.date, tweet.username, tweet.content])



        df_tweets = Modules.pandasmgt.create_df_tweets_v2(tweets_keys=tweetdictkeys, tweets=tweets)

        for index, row in df_tweets.iterrows():
            print()
            #file.write("\n")
            print(f"Item {index} de {df_tweets.index.size}")
            #file.write(f"Item {index} de {df_tweets.index.size}\n")

            print(f"{10 * '====='}")
            #file.write(f"{10 * '====='}\n")

            print(row['id'])
            #file.write(str(row['id']))
            #file.write("\n")

            print(row['screen_name'])
            #file.write(str(row['screen_name']))
            #file.write("\n")

            print(row['created_at'])
            #file.write(str(row['created_at']))
            #file.write("\n")

            print(row['full_text'])
            #file.write(row['full_text'])
            #file.write("\n")

            print(f"{10 * '-----'}")
            #file.write(f"{10 * '-----'}\n")

            ent = testar_ner(row['full_text'], ner)
            print(f"Entidades: ")
            #file.write(f"Entidades: ")
            for i in ent:
                print(i)
                #file.write(str(i))
                #file.write("\n")

            dic = verificar_dicionario(row['full_text'], tok)
            print(f"Threat actor(s): \n")
            #file.write(f"Threat actor(s): \n")
            for i in dic:
                print(i)
                #file.write(str(i))
            print()
            #file.write("\n")

            #df_tmp = pandas.Series([row['id'], row['full_text'], row['screen_name'], row['created_at'], ent, dic],
            #                       index=['id', 'full_text', 'screen_name', 'created_at', 'Entidades',
            #                              'Threat actor(s)'])
            #df_result = df_result.append(df_tmp, ignore_index=True)

    except dbm.error:
        print(f"----> A tabela 'tbl_tweets_v2' ainda não foi criada.")
    except Exception as error:
        print(f"----> Ocorreu o seguinte erro: {error}")