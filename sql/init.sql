



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
SELECT id, session_id,filename,file_path,created_at FROM files ORDER BY id DESC LIMIT 5;