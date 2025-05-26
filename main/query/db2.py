import jaydebeapi
import os


def set_db2_config(object_dicts):
    global DB2_DB_URL, DB2_DB_JDBC_JAR_PATH, DB2_DB_JDBC_DRIVER, DB2_DB_USER, DB2_DB_PASSWORD
 
    # DB connection information
    DB2_DB_URL = f"jdbc:db2://{object_dicts['IP']}:{object_dicts['PORT']}/{object_dicts['SID']}"
    DB2_DB_JDBC_JAR_PATH = os.path.join(os.path.dirname(__file__), '..','..', 'jars', 'jcc-11.5.9.0.jar')
    DB2_DB_JDBC_DRIVER = "com.ibm.db2.jcc.DB2Driver"
    DB2_DB_USER=f"{object_dicts['USER']}"
    DB2_DB_PASSWORD=f"{object_dicts['PASSWORD']}"
    DB2_SCHEMA=f"{object_dicts['SCHEMA']}" 
    DB2_SID=f"{object_dicts['SID']}" 

    
# 권한 : SELECT ANY DICTIONARY
# TABLE LIST 추출 메서드   
def db2_table_list():
    # DB 연결 정보
    conn = jaydebeapi.connect(
        DB2_DB_JDBC_DRIVER,
        DB2_DB_URL,
        [DB2_DB_USER, DB2_DB_PASSWORD],
        DB2_DB_JDBC_JAR_PATH
    )
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f"""
                   SELECT NAME              AS TABLE_NAME
                        , NVL(REMARKS,'')   AS TABLE_COMMENTS
                    FROM SYSIBM.SYSTABLES
                    WHERE 1=1 
                    AND CREATOR = CURRENT SCHEMA 
                    AND TYPE = 'T'  
                    ORDER BY TABLE_NAME
                """
                )    
    
    # 결과 가져오기
    tables = cursor.fetchall()
    
    # 연결 종료
    cursor.close()
    conn.close()
    
    #return [table[0] for table in tables]
    return tables


# TABLE INFO 추출 메서드
def db2_table_info(table_name):
    # DB 연결 정보 
    conn = jaydebeapi.connect(
        DB2_DB_JDBC_DRIVER,
        DB2_DB_URL,
        [DB2_DB_USER, DB2_DB_PASSWORD],
        DB2_DB_JDBC_JAR_PATH
    )
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f"""
                   SELECT TBL.NAME                                             AS TABLE_NAME
                        , NVL(TBL.REMARKS,'-')                                 AS TABLE_COMMENTS
                        , COL.NAME                                             AS COLUMN_NAME 
                        , NVL(COL.REMARKS,'-')                                 AS COLUMN_COMMENTS
                        , TRIM(COL.COLTYPE) || 
                        CASE WHEN COL.COLTYPE IN ('VARCHAR','CHAR', 'LONG', 'DECFLOAT', 'GRAPHIC', 'VARGRAPH') THEN '('||COL.LENGTH||')'
                                WHEN COL.COLTYPE = 'DECIMAL' THEN '('||COL.LENGTH||','||COL.SCALE||')'
                                ELSE '' END                                     AS COLUMN_TYPE
                        , NVL2(COL.KEYSEQ, 'PK', '-')                          AS PK
                        , DECODE(COL.NULLS, 'Y', 'NULL', 'N', 'NOT NULL')      AS "NULL"
                    FROM SYSIBM.SYSTABLES TBL 
                    LEFT JOIN SYSIBM.SYSCOLUMNS COL 
                        ON TBL.CREATOR = COL.TBCREATOR 
                    AND TBL.NAME = COL.TBNAME 
                    WHERE 1=1
                    AND TBL.CREATOR = CURRENT SCHEMA 
                    AND TBL.TYPE = 'T'  
                    AND TBL.NAME = '{table_name}'      
                    ORDER BY TBL.NAME
                            , COL.COLNO
                """)
    
    # 결과 가져오기
    table_columns = cursor.fetchall()
    
    # 연결 종료
    cursor.close()
    conn.close()
    
    return table_columns