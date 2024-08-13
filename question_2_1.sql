-- Create table 'tree'
CREATE TABLE tree (
	id			INT,
	parent_id	INT
)

-- Insert data to table 'tree'
INSERT INTO tree (id, parent_id) VALUES
	('1', '4'),
	('2', '4'),
	('3', '7'),
	('4', '5'),
	('5', '7'),
	('6', '5'),
	('7', NULL),
	('8', '7'),
	('9', '8'),
	('10', '9'),
	('11', '8'),
	('12', '6'),
	('13', '12'),
	('14', '12'),
	('15', '2')



--1. Determine the type of each node
SELECT 
	t.id,
	CASE 
		WHEN (t.parent_id IS NULL) THEN 'root'
		WHEN (t.id NOT IN (SELECT t1.parent_id FROM tree AS t1 WHERE t.id = t1.parent_id)) THEN 'leaf'
		ELSE 'inner'
	END AS type_node
FROM tree AS t


--2. List all descendents of a node and itself
WITH RECURSIVE descendants AS (
	SELECT 
		id,
		id AS root_id
	FROM tree

	UNION ALL
	
	SELECT
		t.id,
		d.root_id
	FROM tree AS t
	INNER JOIN descendants d 
		ON t.parent_id = d.id 
)

SELECT
	root_id,
	STRING_AGG(id::text, ',') AS descendant_list
FROM descendants
GROUP BY root_id
ORDER BY root_id
