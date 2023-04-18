import tweepy

def load_api():
    """
    Este modulo autentica a API do Tweepy com base no arquivo twitter-tokens.txt contido na pasta do projeto.
    :return: Retorna um objeto API com o TweePy
    """

    with open('/Secrets/twitter-tokens.txt') as tfile:
        consumer_key = tfile.readline().strip("\n")
        consumer_secret = tfile.readline().strip("\n")
        access_token = tfile.readline().strip("\n")
        access_token_secret = tfile.readline().strip("\n")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api

#api = carregar_api() <-- Deletar depois