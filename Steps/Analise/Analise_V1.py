import Steps.Analise.Spacy.Spacy as analise

# Analises basedas ou no Twitter ou nos itens do Banco de dados.

analise.analisar_posts_SQL(num_posts=5000)

#analise.analisar_posts_Twitter_v2(num_posts=1000)

# Gera as 30 simulações para a tabela.
#for i in range(1, 31):

#    print("##### Criando arquivo de treino randomico número:" + str(i))
#    analise.gerar_arquivo_treino(sampleNumber=12)

#    print("##### Criando modelo de número:" + str(i))
#    analise.criar_modelo(resultNumber=12)

# Gera o modelo com 0.99 -- Modificado diretamente na função generate_training_file
#analise.gerar_arquivo_treino(sampleNumber=12)
#analise.criar_modelo(resultNumber=12)
#analise.analise_Manual_posts_SQL(100)

