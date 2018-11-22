BEGIN TRAN

UPDATE ehrsample_specialty
SET keywords = SUBSTRING(keywords, 0, CHARINDEX('NOTE' COLLATE SQL_Latin1_General_CP1_CS_AS, keywords))
OUTPUT INSERTED.*
FROM ehrsample_specialty
WHERE keywords COLLATE SQL_Latin1_General_CP1_CS_AS LIKE '%NOTE%'

--COMMIT TRAN
--ROLLBACK TRAN