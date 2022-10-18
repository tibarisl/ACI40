import datetime
import Old_code.databasemgt_old

# Código para manipulação de dicionários de atutores:

def criardicionarioautor(dicionariocomkeys, tweets):

    """
    Criar um dicionário de autores baseando nas chaves e tweets passados como parametro.

    :param dicionariocomkeys:
    :param tweets:
    :return:
    """

    print("##### Função criardicionarioautor: ")

    dicionario = dicionariocomkeys.copy()

    for tweet in tweets:
        if dicionario["id"] == None or not tweet.author._json["id"] in dicionario["id"]:
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

    print("----> Dicionario concluido.\n")

    return dicionario

def inserirautoresnobanco(dicionáriocomautores):

    print("##### Função inserirautoresnobanco: ")

    qtdautores = dicionáriocomautores["id"].__len__()
    indice = 0

    while indice < qtdautores:
            Old_code.databasemgt_old.insertautor(
                dicionáriocomautores["id"][indice],
                dicionáriocomautores["screen_name"][indice],
                dicionáriocomautores["contributors_enabled"][indice],
                dicionáriocomautores["created_at"][indice],
                None, #dicionáriocomautores["default_profile"][indice],
                None, #dicionáriocomautores["default_profile_image"][indice],
                dicionáriocomautores["description"][indice],
                None, #dicionáriocomautores["entities"][indice],
                dicionáriocomautores["favourites_count"][indice],
                None, #dicionáriocomautores["follow_request_sent"][indice],
                dicionáriocomautores["followers_count"][indice],
                None, #dicionáriocomautores["following"][indice],
                dicionáriocomautores["friends_count"][indice],
                None, #dicionáriocomautores["geo_enabled"][indice],
                None, #dicionáriocomautores["has_extended_profile"][indice],
                dicionáriocomautores["id_str"][indice],
                None, #dicionáriocomautores["is_translation_enabled"][indice],
                None, #dicionáriocomautores["is_translator"][indice],
                None, #dicionáriocomautores["lang"][indice],
                dicionáriocomautores["listed_count"][indice],
                dicionáriocomautores["location"][indice],
                dicionáriocomautores["name"][indice],
                dicionáriocomautores["notifications"][indice],
                None, #dicionáriocomautores["profile_background_color"][indice],
                None, #dicionáriocomautores["profile_background_image_url"][indice],
                None, #dicionáriocomautores["profile_background_image_url_https"][indice],
                None, #dicionáriocomautores["profile_background_tile"][indice],
                None, #dicionáriocomautores["profile_banner_url"][indice],
                None, #dicionáriocomautores["profile_image_url"][indice],
                None, #dicionáriocomautores["profile_image_url_https"][indice],
                None, #dicionáriocomautores["profile_link_color"][indice],
                None, #dicionáriocomautores["profile_sidebar_border_color"][indice],
                None, #dicionáriocomautores["profile_sidebar_fill_color"][indice],
                None, #dicionáriocomautores["profile_text_color"][indice],
                None, #dicionáriocomautores["profile_use_background_image"][indice],
                None, #dicionáriocomautores["protected"][indice],
                dicionáriocomautores["statuses_count"][indice],
                None, #dicionáriocomautores["time_zone"][indice],
                None, #dicionáriocomautores["translator_type"][indice],
                dicionáriocomautores["url"][indice],
                None, #dicionáriocomautores["utc_offset"][indice],
                dicionáriocomautores["verified"][indice],
                None, #dicionáriocomautores["withheld_in_countries"][indice]
            )
            indice += 1

    print("----> Funcão encerrada.\n")


# Código para manipulação de dicionários de tweets:



# Código para manipulação de qualquer dicionáro:

def deletaritemdicionario(dicionario, identificador, valor, operador="igual"):
    """
    Deleta um item do dicionário baseado nos parametros.

    :param dicionario:
    :param identificador:
    :param valor:           < Para este deve ser passado a variavel do tipo a ser comparado.
    :param operador:
    :return:
    """

    print(f"##### Função deletaritemdicionario: {identificador}, {valor}, {operador}")

    novodicionario = dicionario.copy()
    lista = []
    indice = 0
    itemremovido = ""

    for item in dicionario[identificador]:

        # Altera o tipo da variavel para o o mesmo do parametro
        if type(valor) is datetime.datetime:
            item = datetime.datetime.strptime(item, '%a %b %d %H:%M:%S +0000 %Y')
        elif type(valor) is int:
            item = int(item)
        elif type(valor) is float:
            item = float(item)
        elif type(valor) is str:
            item = str(item)
        elif type(valor) is bool:
            item = bool(item)

        if operador == "menor":
            if item < valor:
                lista.append(indice)
            indice += 1
        elif operador == "maior":
            if item > valor:
                lista.append(indice)
            indice += 1
        else:
            if item == valor:
                lista.append(indice)
            indice += 1

    lista.sort(reverse=True)

    print("----> Linhas encontradas (Dec): " + str(lista))

    for pos in lista:
        for key in dicionario.keys():
                if  key == "id": itemremovido = str(novodicionario[key][pos])
                del novodicionario[key][pos]
        print(f"----> Item removido: Linha - {pos:<4} : " + itemremovido)

    print("----> Exclusao finalizada.")

    return novodicionario

def verificakey(dictkeycomvalor):
    try:
        return dictkeycomvalor
    except KeyError:
        return None
    except Exception as error:
        print(f"----> Ocorreu o seguinte erro: {error}")