import pyodbc
from.models import *



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

    # Switch to the user database
    cursor.execute(f"USE {username};")

    # Create the galaxy_organization table in the user database
    cursor.execute("""
        CREATE TABLE galaxy_organization (
            id BIGINT PRIMARY KEY,
            OrganizationName NVARCHAR(50),
            CreatedDate DATE,
            UserID_id BIGINT,
            Address NVARCHAR(100),
            Com_Regm NVARCHAR(100),
            Cost_Method INT,
            Create_Issue BIT NOT NULL,
            Create_Receive BIT NOT NULL,
            Logo NVARCHAR(100),
            Report_B NVARCHAR(100),
            Report_H NVARCHAR(100),
            SubscriptionID_id BIGINT,
            Tax_Reg NVARCHAR(100),
            Terms NVARCHAR(MAX),
            Country_id BIGINT,
            Currency_id BIGINT,
            Tax_id BIGINT,
            FacebookLink NVARCHAR(200),
            InstagramLink NVARCHAR(200),
            OrganizationEmail NVARCHAR(254),
            WebsiteLink NVARCHAR(200),
            WhatsappLink NVARCHAR(200)
        );
    """)

    # Re-enable autocommit mode
    cursor.execute("SET IMPLICIT_TRANSACTIONS ON")

    # Close the connections
    cursor.close()
    conn.close()
    
def delete_user_database(username):
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
    cursor.execute(f"DROP DATABASE {username};")

    # Re-enable autocommit mode
    cursor.execute("SET IMPLICIT_TRANSACTIONS ON")

    # Close the connections
    cursor.close()
    conn.close()