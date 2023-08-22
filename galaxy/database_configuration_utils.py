from django.conf import settings
from django.db import connections

def update_database_configuration(username):
    # Update the 'DATABASES' setting
    settings.DATABASES[username] = {
        'ENGINE': 'mssql',
        'NAME': username,
        'USER': 'sa',
        'PASSWORD': 'Ka@12?34#',
        'HOST': 'DESKTOP-F9VA3BH\SQLEXPRESS',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
    }

    # Create a Django database connection for the user database
    connections.databases[username] = settings.DATABASES[username]