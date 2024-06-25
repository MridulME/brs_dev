import config as c
from table_reader import connect_to_mysql

def get_data():
    book_df, user_df = connect_to_mysql()
    return book_df, user_df


