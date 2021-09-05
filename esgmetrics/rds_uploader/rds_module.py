'''
This module contains a class for uploading the data to a SQL relational
database.
'''
import pandas as pd
from sqlalchemy import create_engine


class RdsUploader:
    '''
    This class is used to upload data to a SQL relational database. An engine
    is created using the input information : database_type: str, dbapi: str,
    endpoint: str, port: int, database: str, user: str, password: str

    Attributes:
        database_type (str): It is an attribute that specifies the database
         type of any object
        dbapi (str): It's the library that lets Python connect to the database
         server
        endpoint (str): It's the computation resource that lets you run SQL
         commands on data objects within the Databricks environment
        port (int) : The port on which the database accepts connections
        database (str) : The database name
        user (str): The username that you configured for your database
        password (str): The password that you configured for your database

    '''

    # , database_type: str, dbapi: str, endpoint: str, port:
    def __init__(self):
        # int, database: str, user: str, password: str
        '''
        See help(RdsUploader) for accurate signature
        '''

        database_type = input('database_type : ')
        dbapi = input('dbapi : ')
        endpoint = input('endpoint : ')
        port = input('port : ')
        database = input('database : ')
        user = input('Username : ')
        password = input('Password : ')

        self.database_type = database_type
        self.dbapi = dbapi
        self.endpoint = endpoint
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.engine = create_engine(f"{database_type}+{dbapi}://{user}\
                                    :{password}@{endpoint}:{port}/{database}")

    def send_query(self):
        '''
        This function does the engine execution
        '''
        self.engine.execute()

    def connection_check(self):
        '''
        This function checks the engine connection
        '''
        self.engine.connect()

    def create_table(self, df: pd.DataFrame, table_name: str):
        '''
        This function creates a SQL table from the input pandas
        dataframe

        Args:
            df (pd.DataFrame): Data in Pandas DataFrame format
            table_name (str): Name to be given to the SQL table
        '''
        df.to_sql(table_name, self.engine, if_exists='replace')

    def read_table(self, table_name: str) -> pd.DataFrame:
        '''
        This function reads the SQL table from the database and outputs Pandas
         DataFrame

        Args:
            table_name : Name of the SQL table

        Returns:
            pd.DataFrame: Pandas Dataframe generated from the SQL table
        '''
        df = pd.read_sql_table(table_name, self.engine)
        return df

    @staticmethod
    def add_rows(df: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        '''
        This function add rows from the Pandas DataFrame to the
        input Pandas DataFrame

        Args:
            df (pd.DataFrame): Input data in which rows to be added
            df2 (pd.DataFrame): Data whose rows to be added in df

        Returns:
            pd.DataFrame: Pandas Dataframe
        '''
        df = df.append(df2, ignore_index=True)
        return df

    @staticmethod
    def delete_row(df, labels) -> pd.DataFrame:
        '''
        This function deletes row from the Pandas DataFrame database

        Args:
            df (pd.DataFrame): Input data in which rows to be added
            labels (list) : list of the labels of rows to be deleted

        Returns:
            pd.DataFrame: Pandas Dataframe
        '''
        df1 = df.drop(labels=labels, axis=0, inplace=False)
        return df1
