import psycopg2
from sqlalchemy import create_engine

#
# Gerenciamento de conexões
#

def openconnection():
    """
    Inicia a conexão com o Banco e retorna ela com o objeto connection

    :return:
    """

    connection = psycopg2.connect(user="postgres",
                                 password="@dmin_TCCdatabase2021",
                                 host="127.0.0.1",
                                 port="5432",
                                 database="ACI40")
    return connection

def create_sqlalchemy_engine():
    """
    Cria um motor sqlalchemy para gerenciamento do postgressql

    :return: retorna o engine de manuseio do banco.
    """

    alchemyEngine = create_engine("postgresql:///?User=postgres&;Password=Tib@13248618&Database=ACI40&Server=127.0.0.1&Port=5432")

    return alchemyEngine

#
# Código SQL para gerenciamento de autores
#

def insertautor(id, screen_name, contributors_enabled=None, created_at=None, default_profile=None, default_profile_image=None, description=None, entities=None, favourites_count=None, follow_request_sent=None, followers_count=None, following=None, friends_count=None, geo_enabled=None, has_extended_profile=None, id_str=None, is_translation_enabled=None, is_translator=None, lang=None, listed_count=None, location=None, name=None, notifications=None, profile_background_color=None, profile_background_image_url=None, profile_background_image_url_https=None, profile_background_tile=None, profile_banner_url=None, profile_image_url=None, profile_image_url_https=None, profile_link_color=None, profile_sidebar_border_color=None, profile_sidebar_fill_color=None, profile_text_color=None, profile_use_background_image=None, protected=None, statuses_count=None, time_zone=None, translator_type=None, url=None, utc_offset=None, verified=None, withheld_in_countries=None):

    print(f"##### Função insertautor: {id}, {screen_name}")

    con = openconnection()
    cur = con.cursor()

    try:
        pgsqlquery= "INSERT INTO tbl_autores (contributors_enabled, created_at, default_profile, " \
                    "default_profile_image, description, entities, favourites_count, follow_request_sent, " \
                    "followers_count, following, friends_count, geo_enabled, has_extended_profile, id, id_str, " \
                    "is_translation_enabled, is_translator, lang, listed_count, location, name, notifications, " \
                    "profile_background_color, profile_background_image_url, profile_background_image_url_https, " \
                    "profile_background_tile, profile_banner_url, profile_image_url, profile_image_url_https, " \
                    "profile_link_color, profile_sidebar_border_color, profile_sidebar_fill_color, " \
                    "profile_text_color, profile_use_background_image, protected, screen_name, statuses_count, " \
                    "time_zone, translator_type, url, utc_offset, verified, withheld_in_countries) VALUES (%s, %s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

        valores = (contributors_enabled, created_at, default_profile, default_profile_image, description, entities, favourites_count, follow_request_sent,
                   followers_count, following, friends_count, geo_enabled, has_extended_profile, id, id_str, is_translation_enabled, is_translator, lang,
                   listed_count, location, name, notifications, profile_background_color, profile_background_image_url, profile_background_image_url_https,
                   profile_background_tile, profile_banner_url, profile_image_url, profile_image_url_https, profile_link_color, profile_sidebar_border_color,
                   profile_sidebar_fill_color, profile_text_color, profile_use_background_image, protected, screen_name, statuses_count, time_zone, translator_type,
                   url, utc_offset, verified, withheld_in_countries)

        cur.execute(pgsqlquery, valores)
        con.commit()

        print("----> Insert com sucesso.")

    except (Exception, psycopg2.Error) as error:
        if str(error).find("duplicate key value violates unique constraint")!=-1:
            print("----> Autor já existente.")
        else:
            print("----> Falha ao inserir autor: ", error)


    if con:
        cur.close()
        con.close()
        print("----> Conexão PostgreSQL encerrada.\n")

"""def selectautor():

    print("##### Função selectautor: ")

    con = openconnection()
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM tbl_autores;")
        autores = cur.fetchone()

        print("----> Select realizado com sucesso.")

    except (Exception, psycopg2.Error) as error:
            print("----> Falha ao selecionar registro: ", error)

    if con:
        cur.close()
        con.close()
        print("----> Conexão PostgreSQL encerrada.\n")

    return autores"""

def deleteautor(id):

    print("##### Função deleteautor: ")

    con = openconnection()
    cur = con.cursor()

    try:
        cur.execute("DELETE FROM tbl_autores WHERE id = %s;", (id,))
        con.commit()

        print("----> Exclusão realizada com sucesso.")

    except (Exception, psycopg2.Error) as error:
        print("----> Falha ao remover registro: ", error)

    if con:
        cur.close()
        con.close()
        print("----> Conexão PostgreSQL encerrada.\n")


# Código SQL para gerenciamento de Tweets