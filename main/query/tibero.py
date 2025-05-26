import jaydebeapi
import os


def set_tibero_config(object_dicts):
    global TIBERO_DB_URL, TIBERO_DB_JDBC_JAR_PATH, TIBERO_DB_JDBC_DRIVER, TIBERO_DB_USER, TIBERO_DB_PASSWORD
 
    # DB connection information
    TIBERO_DB_URL = f"jdbc:tibero:thin:@//{object_dicts['IP']}:{object_dicts['PORT']}/{object_dicts['SID']}"
    TIBERO_DB_JDBC_JAR_PATH = os.path.join(os.path.dirname(__file__), '..','..', 'jars', 'tibero6-jdbc.jar')
    TIBERO_DB_JDBC_DRIVER = "com.tmax.tibero.jdbc.TbDriver"  # Tibero JDBC 드라이버 클래스
    TIBERO_DB_USER=f"{object_dicts['USER']}"
    TIBERO_DB_PASSWORD=f"{object_dicts['PASSWORD']}"
    TIBERO_SCHEMA=f"{object_dicts['SCHEMA']}"  # Tibero에서는 SCHEMA가 중요하므로 추가
    TIBERO_SID=f"{object_dicts['SID']}"  # Tibero에서는 SID가 필요하지 않지만, 호환성을 위해 추가

    

# 권한 : SELECT ANY DICTIONARY
# TABLE LIST 추출 메서드
def tibero_table_list():
    # DB 연결 정보
    conn = jaydebeapi.connect(
        TIBERO_DB_JDBC_DRIVER,
        TIBERO_DB_URL,
        [TIBERO_DB_USER, TIBERO_DB_PASSWORD],
        TIBERO_DB_JDBC_JAR_PATH
    )
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f"""
                SELECT TABLE_NAME         AS TABLE_NAME
                        , NVL(COMMENTS,'')   AS TABLE_COMMENTS
                    FROM USER_TAB_COMMENTS
                    WHERE 1=1 
                    AND TABLE_NAME NOT IN ('CONVERTCSV')
                    AND TABLE_NAME NOT LIKE 'BIN$%'
                    AND TABLE_TYPE = 'TABLE'
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


def tibero_table_info(table_name):
    # DB 연결 정보 
    conn = jaydebeapi.connect(
        TIBERO_DB_JDBC_DRIVER,
        TIBERO_DB_URL,
        [TIBERO_DB_USER, TIBERO_DB_PASSWORD],
        TIBERO_DB_JDBC_JAR_PATH
    )
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f"""
                    SELECT UTCOL.TABLE_NAME                                         AS TABLE_NAME       
                            , NVL(UTCM.COMMENTS, '-')                                  AS TABLE_COMMENT    
                            , UTCOL.COLUMN_NAME                                        AS COLUMN_NAME      
                            , NVL(UCCM.COMMENTS, '-')                                  AS COLUMN_COMMENT   
                            , UTCOL.DATA_TYPE ||
                            CASE WHEN UTCOL.DATA_TYPE IN ('VARCHAR2','CHAR','NCHAR','NVARCHAR2','LONG','CLOB','NCLOB')
                                        THEN '('||UTCOL.DATA_LENGTH||')'
                                    WHEN UTCOL.DATA_TYPE = 'NUMBER' THEN
                                        CASE WHEN UTCOL.DATA_PRECISION IS NULL THEN ''
                                            ELSE '('||UTCOL.DATA_PRECISION||','||UTCOL.DATA_SCALE||')'
                                        END 
                                    ELSE '' 
                                END                                                     AS COLUMN_TYPE
                            , NVL2(P.PK_COLUMN_NAME, 'PK', '-')                        AS PK
                            , DECODE(UTCOL.NULLABLE, 'Y', 'NULL', 'N', 'NOT NULL')     AS "NULL"
                        FROM USER_TAB_COLUMNS UTCOL
                        LEFT OUTER JOIN USER_COL_COMMENTS UCCM
                            ON UTCOL.TABLE_NAME  = UCCM.TABLE_NAME
                        AND UTCOL.COLUMN_NAME = UCCM.COLUMN_NAME
                        LEFT OUTER JOIN USER_TAB_COMMENTS UTCM
                            ON UTCOL.TABLE_NAME = UTCM.TABLE_NAME
                        LEFT OUTER JOIN (
                                SELECT UCC_PK.TABLE_NAME    AS PK_TABLE_NAME
                                    , UCC_PK.COLUMN_NAME   AS PK_COLUMN_NAME
                                FROM USER_CONS_COLUMNS UCC_PK
                                JOIN USER_CONSTRAINTS UC_PK
                                    ON UCC_PK.CONSTRAINT_NAME = UC_PK.CONSTRAINT_NAME
                                WHERE 1=1 
                                AND UC_PK.CONSTRAINT_TYPE = 'P'
                                ORDER BY UCC_PK.TABLE_NAME
                                ) P
                            ON UTCOL.TABLE_NAME     = P.PK_TABLE_NAME
                        AND UTCOL.COLUMN_NAME    = P.PK_COLUMN_NAME
                        WHERE 1=1
                        AND UTCOL.TABLE_NAME NOT IN ('CONVERTCSV')
                        AND UTCOL.TABLE_NAME NOT LIKE 'BIN$%'
                        AND UTCOL.TABLE_NAME = '{table_name}'
                        ORDER BY UTCOL.TABLE_NAME
                               , UTCOL.COLUMN_ID
                """)
    
    # 결과 가져오기
    table_columns = cursor.fetchall()
    
    # 연결 종료
    cursor.close()
    conn.close()
    
    return table_columns