import spacy

from Steps.Analise.Spacy.generate_train_file import generate_training_file

nlp = spacy.load('en_core_web_md')

# Gerar arquivo de treino baseado nos dados do DOCCANO

generate_training_file(filepath="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\DOCCANO Exported Data\\Fadmin.jsonl",outdir="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\DOCCANO Exported Data\\")

