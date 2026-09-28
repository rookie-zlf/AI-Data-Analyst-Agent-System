



CREATE TABLE files(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id UUID NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- @block Insert test test file
INSERT INTO files(
    session_id,
    filename,
    file_path
)
VALUES(
    '4c59ceaa-8000-4d9f-948e-9c00e92cac11',
    'sales.csv',
    'data/uploads/4c59ceaa-8000-4d9f-948e-9c00e92cac11_sales.csv'
    );


-- @block Select all files
SELECT * FROM files;


--@block
SELECT * FROM files WHERE id = 1;


--@block
SELECT * FROM files where filename = 'sales.csv';


--@block.  ORDER BY 按照。。。。排序。DESC 降序 ASC 升序

SELECT * FROM files ORDER BY created_at DESC;


--@block LIMIT 限制返回的行数
 SELECT * FROM files ORDER BY created_at DESC LIMIT 4;


--@block  UPDATE 更新数据 SET 设置 WHERE 条件
UPDATE files SET filename = 'new_sales.csv' WHERE id = 1;


--@block.DELETE 删除数据
DELETE FROM files WHERE id =1;



--@block
SELECT id,session_id,filename,file_path,created_at FROM files ORDER BY id DESC LIMIT 5;


--@block
SELECT id, session_id,filename,file_path,created_at FROM files ORDER BY id ;



--@block 新建一张表用来保存AI每次生成的SQL查询语句

CREATE TABLE sql_query_logs(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id UUID,
    sql_text TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--@block 删除表
DROP TABLE sql_query_logs;

--@block 查看数据库中表的信息
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public' 


--@block 记录用户的每一次提问
CREATE TABLE agent_turns(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    turn_id UUID NOT NULL UNIQUE,
    session_id UUID NOT NULL,
    user_message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


----@block 查看数据库中的表
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';


--@block 某次提问过程中，Agent 实际生成并执行了哪些 SQL
CREATE TABLE sql_query_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    turn_id UUID NOT NULL,
    session_id UUID NOT NULL,
    sql_text TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

--@block sql_query_logs引用外键
ALTER TABLE sql_query_logs 
ADD CONSTRAINT fk_sql_query_logs_turn 
FOREIGN KEY (turn_id)
REFERENCES agent_turns(turn_id);

--@block 测试外键约束是否产生作用
INSERT INTO sql_query_logs(
    turn_id,
    session_id,
    sql_text,
    status
)VALUES(
    '11111111-1111-1111-1111-111111111111',
    '05a785b8-2752-4ee6-b65e-a5b33f7ef520',
    'SELECT * FROM files;',
    'success'
);
--@block 
SELECT * 
FROM sql_query_logs;


--@block 
SELECT turn_id 
FROM agent_turns;

--@block 查看表sql_query_logs有哪些外键约束
SELECT constraint_name,
        constraint_type
        FROM information_schema.table_constraints
        WHERE table_schema = 'public'
        and table_name = 'sql_query_logs';

--@block 清空表sql_query_logs
DELETE FROM sql_query_logs;





--@block 查表
SELECT * FROM agent_turns ORDER BY id DESC;


--@block 查表
SELECT * FROM sql_query_logs ORDER BY id DESC;

--@block 添加新列
ALTER TABLE sql_query_logs 
ADD COLUMN source VARCHAR(20);

ALTER TABLE sql_query_logs 
ADD COLUMN tool_name VARCHAR(20);

--@block 更改sql_query_logs更改tool_name字符限制长度
ALTER TABLE sql_query_logs
ALTER COLUMN tool_name TYPE VARCHAR(100);