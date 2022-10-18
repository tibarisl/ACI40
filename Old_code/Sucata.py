
####################################################################################################################

for tweet in tweets:
    for key in autordict.keys():
        try:
            aukey = tweet.author._json[key]
            autordict[key].append(aukey)
        except KeyError:
            aukey = ""
            autordict[key].append("")
        except:
            autordict[key] = [aukey]
        print(f"autordict[key]: {autordict[key]} - tweet[key]: {aukey}")

dfautores = pandas.DataFrame.from_dict(autordict)

print(dfautores)

####################################################################################################################

"""
for tweet in tweets:
    print("##### Propriedades do Autor #####")
    print("ID: ", tweet.author.id)
    print("Nome do Autor: ", tweet.author.name)
    print("Tag: @" + tweet.author.screen_name)
    print("Data de ingresso: ", tweet.author.created_at)
    print("Seguidores: ", tweet.author.followers_count)
    print(20*"-")
    print("Data de criação: ", tweet.created_at)
    print("Tweet: ", tweet.text)
    print(50*"-=")
    autor = {
        "id":tweet.author.id,
        "nome":tweet.author.name,
        "tag":tweet.author.screen_name,
        "criado":tweet.author.created_at,
        "qtdseguidores":tweet.author.followers_count,
    }


print(autor)

"""
####################################################################################################################


import psycopg2
import Old_code.databasemgt_old

def criar_tabela_pandas_autores(sql_query):

    print("##### Função selectautor: ")

    con = Old_code.databasemgt_old.openconnection()
    cur = con.cursor()

    try:
        table = pandas.read_sql_query(sql_query, con)

        print("----> Tabela criada.")

    except (Exception, psycopg2.Error) as error:
            print("----> Falha ao criar a tabela pandas: ", error)

    if con:
        cur.close()
        con.close()
        print("----> Conexão PostgreSQL encerrada.\n")

    return table

def pegar_autores():

    dbConnection = Old_code.databasemgt_old.createengine()

    dataFrame = pandas.read_sql("select * from \"tbl_autores\"", dbConnection);

    return dataFrame