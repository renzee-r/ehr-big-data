SELECT DISTINCT
	medical_specialty
	,TRIM(splt2.value) AS keyword
FROM ehrsample_specialty
CROSS APPLY STRING_SPLIT(keywords, ',') splt
CROSS APPLY STRING_SPLIT(splt.value, '/') splt2
WHERE 1=1
--AND splt2.value LIKE '[^a-zA-Z0-9]'
AND TRIM(splt2.value)  <> ''
