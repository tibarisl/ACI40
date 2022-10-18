from sqlalchemy import create_engine
import pandas as pd

def create_sqlalchemy_engine():

    sqlalchemy_engine = create_engine('postgresql://postgres:admin_TCCdatabase2021@localhost:5432/ACI40')

    return sqlalchemy_engine

def get_df_from_database(sqlquery):

    engineSQL = create_sqlalchemy_engine()
    connection = engineSQL.connect()
    table_dataframe = pd.read_sql_query(sqlquery, con=connection)

    connection.close()

    return table_dataframe

def create_database_table_from_df(dataframe = pd.DataFrame, pd_parameters = str):

    engineSQL = create_sqlalchemy_engine()
    connection = engineSQL.connect()
    dataframe.to_sql(pd_parameters, engineSQL)

    connection.close()

def write_df_into_database_table(dataframe = pd.DataFrame, pd_parameters = str):

    engineSQL = create_sqlalchemy_engine()
    connection = engineSQL.connect()

    dataframe.to_sql(pd_parameters, engineSQL, if_exists='append', chunksize=1000, index=False)

    connection.close()
