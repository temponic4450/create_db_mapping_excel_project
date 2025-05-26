import openpyxl
import os
import sys
from main.work.excel import create_list_sheet,  create_table_sheet
from main.query.oracle import set_oracle_config
from main.query.pgsql import set_pgsql_config
from main.query.tibero import set_tibero_config
from main.query.db2 import set_db2_config


def create_excel_file(object_dicts):
    # setting dictionary

        config_dicts = {
            "RDBMS" : object_dicts["RDBMS"],
            "IP" : object_dicts["IP"],
            "PORT" : object_dicts["PORT"],
            "SID" : object_dicts["SID"],
            "SCHEMA" : object_dicts["SCHEMA"],
            "USER" : object_dicts["USER"],
            "PASSWORD" : object_dicts["PASSWORD"]
        }
        
        # if not exists, create the save path
        save_path = object_dicts["SAVE_PATH"]
        if not os.path.exists(save_path):
            os.makedirs(save_path)


        # set RDBMS 
        SELECT_RDBMS = object_dicts["RDBMS"]

        # Check if the RDBMS is supported
        if SELECT_RDBMS == "Oracle":
            # Set the configuration for database connection
            set_oracle_config(config_dicts)  
        elif SELECT_RDBMS == "PostgreSQL":
            # Set the configuration for PostgreSQL database connection
            set_pgsql_config(config_dicts)
        elif SELECT_RDBMS == "MSSQL":
            raise NotImplementedError("MSSQL is not supported yet.")
        elif SELECT_RDBMS == "mariaDB":
            raise NotImplementedError("mariaDB is not supported yet.")
        elif SELECT_RDBMS == "Tibero":
            set_tibero_config(config_dicts)  # Assuming you have a function to set Tibero config
        elif SELECT_RDBMS == "DB2(LUW)":
            set_db2_config(config_dicts)
            

        # Create a new workbook and select the active worksheet
        workbook = openpyxl.Workbook()
        
        create_list_sheet(workbook, SELECT_RDBMS) # Call the function to create the list
        
        create_table_sheet(workbook, save_path, SELECT_RDBMS) # Call the function to create the table

        
        
