import pyodbc

def create_user_database(username):
    # Connect to the SQL Server database
    conn = pyodbc.connect(
        'DRIVER={SQL Server};' 
        'SERVER=DESKTOP-F9VA3BH\SQLEXPRESS;'
        'DATABASE=users;'
        'UID=sa;'
        'PWD=Ka@12?34#;' 
    )
    
    conn.autocommit = True
    cursor = conn.cursor()

    # Disable autocommit mode explicitly
    cursor.execute("SET IMPLICIT_TRANSACTIONS OFF")

    # Create a new database for the user
    cursor.execute(f"CREATE DATABASE {username};")

    # Re-enable autocommit mode
    cursor.execute("SET IMPLICIT_TRANSACTIONS ON")

    # Close the connections
    cursor.close()
    conn.close()