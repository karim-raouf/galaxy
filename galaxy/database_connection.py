from django.db import connections

def get_database_connection(username):
    connection = connections[username]
    connection.ensure_connection()
    return connection