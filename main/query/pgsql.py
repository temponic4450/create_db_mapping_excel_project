import jaydebeapi
import os

def set_pgsql_config(object_dicts):
    global PGSQL_DB_URL, PGSQL_DB_JDBC_JAR_PATH, PGSQL_DB_JDBC_DRIVER, PGSQL_DB_USER, PGSQL_DB_PASSWORD,PGSQL_SCHEMA, PGSQL_SID
 
    # DB connection information
    PGSQL_DB_URL = f"jdbc:postgresql://{object_dicts['IP']}:{object_dicts['PORT']}/{object_dicts['SID']}"
    PGSQL_DB_JDBC_JAR_PATH = os.path.join(os.path.dirname(__file__), '..','..', 'jars', 'postgresql-42.7.5.jar')
    PGSQL_DB_JDBC_DRIVER = "org.postgresql.Driver"
    PGSQL_DB_USER=f"{object_dicts['USER']}"
    PGSQL_DB_PASSWORD=f"{object_dicts['PASSWORD']}"
    PGSQL_SCHEMA=f"{object_dicts['SCHEMA']}"  # PostgreSQL에서는 SCHEMA가 중요하므로 추가
    PGSQL_SID=f"{object_dicts['SID']}"  # PostgreSQL에서는 SID가 필요하지 않지만, 호환성을 위해 추가



# TABLE LIST 추출 메서드
def pgsql_table_list():
    # DB 연결 정보
    conn = jaydebeapi.connect(
        PGSQL_DB_JDBC_DRIVER,
        PGSQL_DB_URL,
        [PGSQL_DB_USER, PGSQL_DB_PASSWORD],
        PGSQL_DB_JDBC_JAR_PATH
    )
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f"""
                select table_name as table_name
                      , case when obj_description(('"' || table_schema || '"."' || table_name || '"')::regclass, 'pg_class') is null then ''
                             else obj_description(('"' || table_schema || '"."' || table_name || '"')::regclass, 'pg_class') end as table_comments
                from information_schema.tables
               where 1=1
                 and table_schema = '{PGSQL_SCHEMA}'
                 and table_type = 'BASE TABLE'
                 order by table_name
                """
                )    
    
    # 결과 가져오기
    tables = cursor.fetchall()
    
    # 연결 종료
    cursor.close()
    conn.close()
    
    #return [table[0] for table in tables]
    return tables


def pgsql_table_info(table_name):
    # DB 연결 정보 
    conn = jaydebeapi.connect(
        PGSQL_DB_JDBC_DRIVER,
        PGSQL_DB_URL,
        [PGSQL_DB_USER, PGSQL_DB_PASSWORD],
        PGSQL_DB_JDBC_JAR_PATH
    )
    
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f"""
                select c.table_name as table_name
                    , case when obj_description(('"' || c.table_schema || '"."' || c.table_name || '"')::regclass, 'pg_class') is null then '' 
                            else obj_description(('"' || c.table_schema || '"."' || c.table_name || '"')::regclass, 'pg_class') end AS table_comment
                    , c.column_name as column_name
                    , case when col_description(('"' || c.table_schema || '"."' || c.table_name || '"')::regclass, c.ordinal_position) is null then '' 
                            else col_description(('"' || c.table_schema || '"."' || c.table_name || '"')::regclass, c.ordinal_position) end AS column_comment
                    , c.data_type ||
                        case when c.data_type in ('integer','decimal','numeric') then concat('(',c.numeric_precision,',',c.numeric_scale,')') 
                                when c.data_type in ('character varying') and c.character_maximum_length is not null then concat('(',c.character_maximum_length,')')
                                else '' end as data_type
                    , case when tc.constraint_type = 'PRIMARY KEY' then 'PK' 
                            when tc.constraint_type = 'FOREIGN KEY' then 'FK'
                            else '-' end as pk
                    , case when c.is_nullable = 'NO' then 'NOT NULL' 
                            else 'NULL' end as null_check
                    from information_schema.columns c
                    LEFT join information_schema.key_column_usage kcu 
                    on c.table_name = kcu.table_name AND c.column_name = kcu.column_name
                    and kcu.position_in_unique_constraint is null
                    left join information_schema.table_constraints tc 
                    on kcu.constraint_name = tc.constraint_name
                where 1=1 
                    and c.table_schema = '{PGSQL_SCHEMA}'
                    and c.table_name = '{table_name}'
                    order by c.table_name, c.ordinal_position
                """
                )    
    
    # 결과 가져오기
    table_columns = cursor.fetchall()
    
    # 연결 종료
    cursor.close()
    conn.close()
    
    return table_columns