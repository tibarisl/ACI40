import pandas

text = []
new_json_file = []

df = pandas.read_json(path_or_buf="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Doccano\\admin.jsonl", lines=True, )
print(df)

for line in df:
    print(line)

#for line in text:
#    if "[]" in line.label:
#        print(line)

#temp_tweets = []
#for tweet in tweets:
#    if tweet.full_text.__len__() >= min_tweet_text_len:
#        temp_tweets.append(tweet)
#tweets = temp_tweets.copy()


#df = pd.read_json('data.json')
#print(df.to_string())