from Steps.Analise.Spacy.generate_train_file import generate_training_file
import spacy
import Modules.databasemgt
import dbm
import tweepy
import Modules.pandasmgt
import Modules.twitter_auth


def gerar_arquivo_treino():
    # Gerar arquivo de treino e teste baseado nos dados do DOCCANO
    generate_training_file(filepath="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Doccano\\admin.jsonl", outdir="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\TrainFile\\")


def criar_modelos():
    return

    #   Executar este comandos no Terminal para criação do arquivo "config" baseado no "base_config"
    # python -m spacy init fill-config "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\base_config.cfg" "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\config.cfg"
    #   Executar esta linha de comando no Terminal para rodar os testes.
    # Usando o mesmo arquivo .train para o --paths.dev
    # python -m spacy train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\config.cfg" --output "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\models" --paths.train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\train.spacy" --paths.dev "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\train.spacy"
    # Usando o arquivo .test para o --paths.dev
    # python -m spacy train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\config.cfg" --output "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\models" --paths.train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\train.spacy" --paths.dev "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\test.spacy"


def testar_ner(texto):
    nlp1 = spacy.load(r"G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\models\model-best")  #load the best model
    doc = nlp1(texto)  # input sample text

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

    # spacy.displacy.serve(doc, style="ent")

def analisar_posts_SQL(num_posts):

    print("##### def analisar_posts_SQL")
    print("----> iniciado.")

    try:
        df_tweets = Modules.databasemgt.get_df_from_database(sqlquery=f"SELECT id,full_text FROM public.tbl_tweets_v2 order by random() limit {num_posts};")

        for index, row in df_tweets.iterrows():
            print()
            print()
            print(f"{10 * '====='}")
            print(row['id'])
            print(row['full_text'])
            print(f"{10 * '-----'}")
            testar_ner(row['full_text'])

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

    # Pegar as propriedades dos Tweets
    tweetdictkeys = {'id': None, 'full_text': None, 'screen_name': None, 'created_at': None}

    try:
        df_tweets = Modules.pandasmgt.create_df_tweets_v2(tweets_keys=tweetdictkeys, tweets=tweets)

        for index, row in df_tweets.iterrows():
            print()
            print()
            print(f"{10 * '====='}")
            print(row['id'])
            print(row['full_text'])
            print(f"{10 * '-----'}")
            testar_ner(row['full_text'])

    except dbm.error:
        print(f"----> A tabela 'tbl_tweets_v2' ainda não foi criada.")
    except Exception as error:
        print(f"----> Ocorreu o seguinte erro: {error}")

    print(f"----> Fim da execução. Tweets impressos: {df_tweets.__len__()}")


#
#   BLOCO DE TESTES
#

#gerar_arquivo_treino()

texto = """
IoT Botnets Fuels DDoS Attacks – Are You Prepared?: The increased proliferation of IoT devices paved the way for 
the rise of IoT botnets that amplifies DDoS attacks today. This is a dangerous warning that the possibility of a 
sophisticated DDoS attack… https://t.co/8RNZLyTB3r https://t.co/kJ0ztEVSiA
"""

#testar_ner(texto)

#analisar_posts_SQL(num_posts=30)
#analisar_posts_Twitter(num_posts=20)