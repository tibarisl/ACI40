import Steps.Analise.Spacy.Spacy as analise


for i in range(11, 31):

    print("##### Criando arquivo de treino randomico número:" + str(i))
    analise.gerar_arquivo_treino(sampleNumber=i)

    print("##### Criando modelo de número:" + str(i))
    analise.criar_modelo(resultNumber=i)

#analise.analisar_posts_SQL(num_posts=5000)

#analise.analisar_posts_Twitter(num_posts=1000)

#analise.analisar_posts_Twitter_v2(num_posts=1000)

