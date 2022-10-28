from Steps.Analise.Spacy.generate_train_file import generate_training_file
import spacy


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

    print("Done")

#def analisar_posts():


texto = """
There have been increases in global and IOT malware and a rise in encrypted threats as geopolitical strife impact 
cyberattacks. #cyberattacks #cybersecurity #ransomware #malware  https://t.co/G4ToqdvbJE 
https://t.co/D1w9tOPQbd
"""


testar_ner(texto)


