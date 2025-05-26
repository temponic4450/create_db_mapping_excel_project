SELECT TABLE_NAME                                       AS TABLE_NAME 
     , CASE WHEN NVL(TABLE_COMMENT, '-') = '' THEN '-' 
            ELSE NVL(TABLE_COMMENT, '-')      END       AS TABLE_COMMENTS 
  FROM INFORMATION_SCHEMA.TABLES
 WHERE 1=1 
   AND TABLE_SCHEMA = DATABASE()  
 ORDER BY TABLE_NAME 
;



SELECT TBL.TABLE_NAME                                               AS TABLE_NAME 
     , CASE WHEN NVL(TBL.TABLE_COMMENT, '-') = '' THEN '-' 
            ELSE NVL(TBL.TABLE_COMMENT, '-')      END               AS TABLE_COMMENTS 
     , COL.COLUMN_NAME                                              AS COLUMN_NAME      
     , CASE WHEN NVL(COL.COLUMN_COMMENT , '-') = '' THEN '-' 
            ELSE NVL(COL.COLUMN_COMMENT, '-')       END             AS COLUMN_COMMENT 
     , CONCAT(COL.DATA_TYPE, 
              CASE WHEN COL.DATA_TYPE IN ('VARCHAR','CHAR','LONG','CLOB','NCLOB') 
                        THEN CONCAT('(', COL.CHARACTER_MAXIMUM_LENGTH, ')')
                   WHEN COL.DATA_TYPE IN ('DECIMAL', 'ENUM') 
                        THEN CONCAT('(', COL.NUMERIC_PRECISION, ',', COL.NUMERIC_SCALE, ')')
                   ELSE '' END )                                    AS COLUMN_TYPE 
     , CASE WHEN COL_KEY.CONSTRAINT_NAME IS NULL THEN '-' 
            ELSE 'PK' END                                           AS PK
     , CASE WHEN COL.IS_NULLABLE = 'YES' THEN 'NULL' 
            WHEN COL.IS_NULLABLE = 'NO'  THEN 'NOT NULL' 
       END                                                          AS "NULL"
  FROM INFORMATION_SCHEMA.TABLES TBL 
  LEFT JOIN INFORMATION_SCHEMA.COLUMNS COL 
    ON TBL.TABLE_SCHEMA = COL.TABLE_SCHEMA 
   AND TBL.TABLE_NAME = COL.TABLE_NAME 
  LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE COL_KEY 
    ON TBL.TABLE_SCHEMA = COL_KEY.TABLE_SCHEMA 
   AND TBL.TABLE_NAME = COL_KEY.TABLE_NAME 
   AND COL.COLUMN_NAME = COL_KEY.COLUMN_NAME 
 WHERE 1=1 
   AND TBL.TABLE_SCHEMA = DATABASE()  
   AND TBL.TABLE_NAME = '{table_name}' 
 ORDER BY TBL.TABLE_NAME 
        , COL.ORDINAL_POSITION
;
