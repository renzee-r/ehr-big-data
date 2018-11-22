SELECT DISTINCT
	',|' + medical_specialty + '|: '
	,'[' + STUFF((
		SELECT
			', |' + keyword + '|'
		FROM ehrsample_specialty_keyword esk2
		WHERE esk2.medical_specialty = esk1.medical_specialty
		FOR XML PATH('')
	), 1, 1, '') + ']'
FROM ehrsample_specialty_keyword esk1