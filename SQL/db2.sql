SELECT NAME              AS TABLE_NAME
     , NVL(REMARKS,'')   AS TABLE_COMMENTS
  FROM SYSIBM.SYSTABLES
 WHERE 1=1 
   AND CREATOR = CURRENT SCHEMA 
   AND TYPE = 'T'  
 ORDER BY TABLE_NAME
 ;
 
 

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
;