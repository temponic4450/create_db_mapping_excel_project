-- table list
 select table_name as table_name
                      , case when obj_description(('"' || table_schema || '"."' || table_name || '"')::regclass, 'pg_class') is null then ''
                             else obj_description(('"' || table_schema || '"."' || table_name || '"')::regclass, 'pg_class') end as table_comments
                from information_schema.tables
               where 1=1
                 and table_schema = '{PGSQL_SCHEMA}'
                 and table_type = 'BASE TABLE'
                 order by table_name
;



-- table 명세서
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