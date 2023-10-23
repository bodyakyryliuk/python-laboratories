import json
import sqlite3


connection = sqlite3.connect('database.db')


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def get_column_names(data):
    column_names = set()

    def extract_keys(obj):
        if isinstance(obj, dict):
            column_names.update(obj.keys())
            for value in obj.values():
                extract_keys(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_keys(item)

    extract_keys(data)
    return column_names


def create_table(db_connection, table_name, columns):
    columns_with_types = ', '.join(f'{column} TEXT' for column in columns)
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})'
    cursor = db_connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(create_table_query)


def insert_data(db_connection, table_name, data, columns):
    cursor = db_connection.cursor()

    def insert_rows(obj):
        if isinstance(obj, dict):
            values = [obj.get(column, '') for column in columns]
            cursor.execute(f'INSERT INTO {table_name} VALUES ({",".join(["?"] * len(columns))})', values)
        elif isinstance(obj, list):
            for item in obj:
                insert_rows(item)

    insert_rows(data)
    db_connection.commit()


def db_manager():
    file_path = 'data.json'
    table_name = 'my_table1'

    # Read JSON data from file
    data = read_json_file(file_path)

    # Get column names from the JSON data
    columns = get_column_names(data)

    # Create a connection to the SQLite database
    connection = sqlite3.connect('database.db')

    # Create the table in the database
    create_table(connection, table_name, columns)

    # Insert the data into the table
    insert_data(connection, table_name, data, columns)

    # Close the database connection
    connection.close()


def select_all_rows():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM my_table1")

    # Fetch all rows and column names
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Create a list of dictionaries representing each row
    data = []
    for row in rows:
        row_dict = {}
        for i, value in enumerate(row):
            row_dict[column_names[i]] = value
        data.append(row_dict)

    return data


def main():
    db_manager()
    print(select_all_rows())


if __name__ == '__main__':
    main()