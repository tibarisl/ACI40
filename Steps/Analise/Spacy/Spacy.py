from parso import python

from Steps.Analise.Spacy.generate_train_file import generate_training_file

# Gerar arquivo de treino e teste baseado nos dados do DOCCANO

generate_training_file(filepath="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\Doccano\\admin.jsonl",outdir="G:\\Meu Drive\\TCC\\TCC II - Everson Leonardi\\Projeto\\Dados\\TrainFile\\")

#   Executar este comandos no Terminal para criação do arquivo config baseado no base_config
# python -m spacy init fill-config "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\base_config.cfg" "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Dados\Spacy\config.cfg"


#   Executar esta linha de comando no Terminal para rodar os testes.
# python -m spacy train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\config.cfg" --output "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\Spacy\scispacy" --paths.train "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\train.spacy" --paths.dev "G:\Meu Drive\TCC\TCC II - Everson Leonardi\Projeto\Dados\TrainFile\train.spacy"


