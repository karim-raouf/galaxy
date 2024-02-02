import pyodbc
from.models import *
import json
import base64
from django.contrib.sessions.base_session import AbstractBaseSession

def create_user_database(username):
    try:
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

        # # Switch to the user database
        cursor.execute(f"USE {username};")

        # Create the galaxy_organization table in the user database
        cursor.execute("""
            
            CREATE TABLE [dbo].[auth_group](
                [id] [int] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](150) NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
            CONSTRAINT [auth_group_name_a6ea08ec_uniq] UNIQUE NONCLUSTERED 
            (
                [name] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            


            CREATE TABLE [dbo].[django_content_type](
                [id] [int] IDENTITY(1,1) NOT NULL,
                [app_label] [nvarchar](100) NOT NULL,
                [model] [nvarchar](100) NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
    



            CREATE TABLE [dbo].[auth_permission](
                [id] [int] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](255) NOT NULL,
                [content_type_id] [int] NOT NULL,
                [codename] [nvarchar](100) NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[auth_permission]  WITH CHECK ADD  CONSTRAINT [auth_permission_content_type_id_2f476e4b_fk_django_content_type_id] FOREIGN KEY([content_type_id])
            REFERENCES [dbo].[django_content_type] ([id])
            

            ALTER TABLE [dbo].[auth_permission] CHECK CONSTRAINT [auth_permission_content_type_id_2f476e4b_fk_django_content_type_id]



            CREATE TABLE [dbo].[auth_group_permissions](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [group_id] [int] NOT NULL,
                [permission_id] [int] NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[auth_group_permissions]  WITH CHECK ADD  CONSTRAINT [auth_group_permissions_group_id_b120cbf9_fk_auth_group_id] FOREIGN KEY([group_id])
            REFERENCES [dbo].[auth_group] ([id])
            

            ALTER TABLE [dbo].[auth_group_permissions] CHECK CONSTRAINT [auth_group_permissions_group_id_b120cbf9_fk_auth_group_id]
            

            ALTER TABLE [dbo].[auth_group_permissions]  WITH CHECK ADD  CONSTRAINT [auth_group_permissions_permission_id_84c5c92e_fk_auth_permission_id] FOREIGN KEY([permission_id])
            REFERENCES [dbo].[auth_permission] ([id])
            

            ALTER TABLE [dbo].[auth_group_permissions] CHECK CONSTRAINT [auth_group_permissions_permission_id_84c5c92e_fk_auth_permission_id]
            
            
            
            
            
            CREATE TABLE [dbo].[galaxy_userstype](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [UserTypeCode] [int] NULL,
                [UserTypeName] [nvarchar](50) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]




            CREATE TABLE [dbo].[galaxy_user](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [password] [nvarchar](128) NULL,
                [last_login] [datetimeoffset](7) NULL,
                [is_superuser] [bit] NOT NULL,
                [username] [nvarchar](128) NULL,
                [first_name] [nvarchar](128) NULL,
                [last_name] [nvarchar](128) NULL,
                [email] [nvarchar](254) NULL,
                [is_staff] [bit] NOT NULL,
                [is_active] [bit] NOT NULL,
                [date_joined] [datetimeoffset](7) NOT NULL,
                [avatar] [nvarchar](100) NULL,
                [user_Type_id] [bigint] NULL,
                [SubscriptionID_id] [bigint] NULL,
                [Birth_Date] [date] NULL,
                [Gender] [int] NULL,
                [Telephone] [nvarchar](100) NULL,
                [Language_id] [bigint] NULL,
                [Psw_Flag] [int] NULL,
                [ip_restricted] [bit] NOT NULL,
                [system_user_active] [bit] NOT NULL,
            CONSTRAINT [galaxy_user_id_3398f6a6_pk] PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            

            ALTER TABLE [dbo].[galaxy_user]  WITH CHECK ADD  CONSTRAINT [galaxy_user_user_Type_id_69e9b74c_fk_galaxy_userstype_id] FOREIGN KEY([user_Type_id])
            REFERENCES [dbo].[galaxy_userstype] ([id])
            

            ALTER TABLE [dbo].[galaxy_user] CHECK CONSTRAINT [galaxy_user_user_Type_id_69e9b74c_fk_galaxy_userstype_id]




            CREATE TABLE [dbo].[django_admin_log](
                [id] [int] IDENTITY(1,1) NOT NULL,
                [action_time] [datetimeoffset](7) NOT NULL,
                [object_id] [nvarchar](max) NULL,
                [object_repr] [nvarchar](200) NOT NULL,
                [action_flag] [smallint] NOT NULL,
                [change_message] [nvarchar](max) NOT NULL,
                [content_type_id] [int] NULL,
                [user_id] [bigint] NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
            

            ALTER TABLE [dbo].[django_admin_log]  WITH CHECK ADD  CONSTRAINT [django_admin_log_content_type_id_c4bce8eb_fk_django_content_type_id] FOREIGN KEY([content_type_id])
            REFERENCES [dbo].[django_content_type] ([id])
            

            ALTER TABLE [dbo].[django_admin_log] CHECK CONSTRAINT [django_admin_log_content_type_id_c4bce8eb_fk_django_content_type_id]
            

            ALTER TABLE [dbo].[django_admin_log]  WITH CHECK ADD  CONSTRAINT [django_admin_log_user_id_c564eba6_fk] FOREIGN KEY([user_id])
            REFERENCES [dbo].[galaxy_user] ([id])
            

            ALTER TABLE [dbo].[django_admin_log] CHECK CONSTRAINT [django_admin_log_user_id_c564eba6_fk]
            

            ALTER TABLE [dbo].[django_admin_log]  WITH CHECK ADD  CONSTRAINT [django_admin_log_action_flag_a8637d59_check] CHECK  (([action_flag]>=(0)))
            

            ALTER TABLE [dbo].[django_admin_log] CHECK CONSTRAINT [django_admin_log_action_flag_a8637d59_check]
            


        
            CREATE TABLE [dbo].[django_session](
                [session_key] [nvarchar](40) NOT NULL,
                [session_data] [nvarchar](max) NOT NULL,
                [expire_date] [datetimeoffset](7) NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [session_key] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
            




            CREATE TABLE [dbo].[django_migrations](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [app] [nvarchar](255) NOT NULL,
                [name] [nvarchar](255) NOT NULL,
                [applied] [datetimeoffset](7) NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            
            CREATE TABLE [dbo].[galaxy_country](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](50) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_currency](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](50) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            
            
            
            
            
            CREATE TABLE [dbo].[galaxy_organization](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [OrganizationName] [nvarchar](50) NULL,
                [CreatedDate] [date] NULL,
                [UserID_id] [bigint] NULL,
                [Address] [nvarchar](100) NULL,
                [Com_Regm] [nvarchar](100) NULL,
                [Cost_Method] [int] NULL,
                [Create_Issue] [bit] NOT NULL,
                [Create_Receive] [bit] NOT NULL,
                [Logo] [nvarchar](100) NULL,
                [Report_B] [nvarchar](100) NULL,
                [Report_H] [nvarchar](100) NULL,
                [SubscriptionID_id] [bigint] NULL,
                [Tax_Reg] [nvarchar](100) NULL,
                [Terms] [nvarchar](max) NULL,
                [Country_id] [bigint] NULL,
                [Currency_id] [bigint] NULL,
                [FacebookLink] [nvarchar](200) NULL,
                [InstagramLink] [nvarchar](200) NULL,
                [OrganizationEmail] [nvarchar](254) NULL,
                [WebsiteLink] [nvarchar](200) NULL,
                [WhatsappLink] [nvarchar](200) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_store](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](50) NULL,
                [org_id_id] [bigint] NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_store]  WITH CHECK ADD  CONSTRAINT [galaxy_store_org_id_id_40c34a9e_fk_galaxy_organization_id] FOREIGN KEY([org_id_id])
            REFERENCES [dbo].[galaxy_organization] ([id])
            

            ALTER TABLE [dbo].[galaxy_store] CHECK CONSTRAINT [galaxy_store_org_id_id_40c34a9e_fk_galaxy_organization_id]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_taxes_charges](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [tax_title] [nvarchar](50) NULL,
                [tax_include] [bit] NOT NULL,
                [default] [bit] NOT NULL,
                [disable] [bit] NOT NULL,
                [min_amount] [numeric](10, 2) NOT NULL,
                [max_amount] [numeric](10, 2) NOT NULL,
                [tax_type] [int] NULL,
                [tax_amount] [int] NULL,
                [rate] [numeric](5, 2) NOT NULL,
                [amount] [numeric](10, 2) NOT NULL,
                [org_id_id] [bigint] NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_taxes_charges]  WITH CHECK ADD  CONSTRAINT [galaxy_taxes_charges_org_id_id_632762ef_fk_galaxy_organization_id] FOREIGN KEY([org_id_id])
            REFERENCES [dbo].[galaxy_organization] ([id])
            

            ALTER TABLE [dbo].[galaxy_taxes_charges] CHECK CONSTRAINT [galaxy_taxes_charges_org_id_id_632762ef_fk_galaxy_organization_id]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_store_tax](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [org_id_id] [bigint] NULL,
                [tax_id_id] [bigint] NULL,
                [store_id_id] [bigint] NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_store_tax]  WITH CHECK ADD  CONSTRAINT [galaxy_store_tax_org_id_id_02e31909_fk_galaxy_organization_id] FOREIGN KEY([org_id_id])
            REFERENCES [dbo].[galaxy_organization] ([id])
            

            ALTER TABLE [dbo].[galaxy_store_tax] CHECK CONSTRAINT [galaxy_store_tax_org_id_id_02e31909_fk_galaxy_organization_id]
            

            ALTER TABLE [dbo].[galaxy_store_tax]  WITH CHECK ADD  CONSTRAINT [galaxy_store_tax_store_id_id_05cc2062_fk_galaxy_store_id] FOREIGN KEY([store_id_id])
            REFERENCES [dbo].[galaxy_store] ([id])
            

            ALTER TABLE [dbo].[galaxy_store_tax] CHECK CONSTRAINT [galaxy_store_tax_store_id_id_05cc2062_fk_galaxy_store_id]
            

            ALTER TABLE [dbo].[galaxy_store_tax]  WITH CHECK ADD  CONSTRAINT [galaxy_store_tax_tax_id_id_4b7e2a9c_fk_galaxy_taxes_charges_id] FOREIGN KEY([tax_id_id])
            REFERENCES [dbo].[galaxy_taxes_charges] ([id])
            

            ALTER TABLE [dbo].[galaxy_store_tax] CHECK CONSTRAINT [galaxy_store_tax_tax_id_id_4b7e2a9c_fk_galaxy_taxes_charges_id]
            
            
            
            
            
            
            
            
            
            CREATE TABLE [dbo].[galaxy_allowedmodule](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [module_code] [int] NULL,
                [UserId_id] [bigint] NOT NULL,
                [module_name] [nvarchar](50) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_allowedmodule]  WITH CHECK ADD  CONSTRAINT [galaxy_allowedmodules_UserId_id_6c612859_fk_galaxy_user_id] FOREIGN KEY([UserId_id])
            REFERENCES [dbo].[galaxy_user] ([id])
            

            ALTER TABLE [dbo].[galaxy_allowedmodule] CHECK CONSTRAINT [galaxy_allowedmodules_UserId_id_6c612859_fk_galaxy_user_id]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_allowedip](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [ip_address] [nvarchar](39) NULL,
                [UserId_id] [bigint] NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_allowedip]  WITH CHECK ADD  CONSTRAINT [galaxy_allowedip_UserId_id_98acef86_fk_galaxy_user_id] FOREIGN KEY([UserId_id])
            REFERENCES [dbo].[galaxy_user] ([id])
            

            ALTER TABLE [dbo].[galaxy_allowedip] CHECK CONSTRAINT [galaxy_allowedip_UserId_id_98acef86_fk_galaxy_user_id]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_timerestriction](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [day_of_week] [nvarchar](10) NULL,
                [start_time] [nvarchar](12) NOT NULL,
                [end_time] [nvarchar](12) NOT NULL,
                [UserID_id] [bigint] NOT NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_timerestriction]  WITH CHECK ADD  CONSTRAINT [galaxy_timerestriction_UserID_id_05daf712_fk_galaxy_user_id] FOREIGN KEY([UserID_id])
            REFERENCES [dbo].[galaxy_user] ([id])
            

            ALTER TABLE [dbo].[galaxy_timerestriction] CHECK CONSTRAINT [galaxy_timerestriction_UserID_id_05daf712_fk_galaxy_user_id]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_department](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](30) NULL,
                [org_id_id] [bigint] NULL,
                [code] [nvarchar](17) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_department]  WITH CHECK ADD  CONSTRAINT [galaxy_department_org_id_id_8947bd37_fk_galaxy_organization_id] FOREIGN KEY([org_id_id])
            REFERENCES [dbo].[galaxy_organization] ([id])
            

            ALTER TABLE [dbo].[galaxy_department] CHECK CONSTRAINT [galaxy_department_org_id_id_8947bd37_fk_galaxy_organization_id]
            
            
            
            
            CREATE TABLE [dbo].[galaxy_category](
                [id] [bigint] IDENTITY(1,1) NOT NULL,
                [name] [nvarchar](30) NULL,
                [department_id] [bigint] NOT NULL,
                [code] [nvarchar](17) NULL,
            PRIMARY KEY CLUSTERED 
            (
                [id] ASC
            )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
            ) ON [PRIMARY]
            

            ALTER TABLE [dbo].[galaxy_category]  WITH CHECK ADD  CONSTRAINT [galaxy_category_department_id_b3fe24f5_fk_galaxy_department_id] FOREIGN KEY([department_id])
            REFERENCES [dbo].[galaxy_department] ([id])
            

            ALTER TABLE [dbo].[galaxy_category] CHECK CONSTRAINT [galaxy_category_department_id_b3fe24f5_fk_galaxy_department_id]
            
            
        """)

        # Re-enable autocommit mode
        cursor.execute("SET IMPLICIT_TRANSACTIONS ON")

        # Close the connections
        cursor.close()
        conn.close()
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"SQL Server Error: {sqlstate}")
    
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
    
    
    
def decode_session_data(raw_session_data):
    try:
        # Extracting the encoded session data
        encoded_data = raw_session_data.split(".")[1]

        # Padding the encoded data if needed
        padding = len(encoded_data) % 4
        if padding:
            encoded_data += '=' * (4 - padding)

        # Decoding base64
        decoded_data = base64.b64decode(encoded_data)

        # Decode JSON
        session_dict = json.loads(decoded_data)

        return session_dict
    except Exception as e:
        # Print the specific error for debugging purposes
        print(f"Error decoding session data: {e}")