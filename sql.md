
* ## Unconditional LEFT JOIN

```
...
LEFT JOIN (SELECT MIN(modified) AS first_modified FROM user) ue
ON 1=1

The intention is an unconditional LEFT JOIN, which is different from a CROSS JOIN in that all rows from the left table expression are returned, even if there is no match in the right table expression - while a CROSS JOIN drops such rows from the result. More on joins in the manual.

However:

1=1 is pointless in Postgres and all derivatives including Amazon Redshift. Just use true. This has probably been carried over from another RDBMS that does not support the boolean type properly.

... LEFT JOIN (SELECT  ...) ue ON true

Then again, LEFT JOIN is pointless for this particular subquery with SELECT MIN(modified) FROM user on the right, because a SELECT with an aggregate function (min()) and no GROUP BY clause always returns exactly one row. This case (but not other cases where no row might be found) can be simplified to:

... CROSS JOIN (SELECT MIN(modified) AS first_modified FROM user) ue

Simplification : 

It's simply doing a cross join, which selects all rows from the first table and all rows from the second table and shows as cartesian product, i.e. with all possibilities.

JOIN (LEFT, INNER, RIGHT, etc.) statements normally require an 'ON ..." condition. Putting in 1=1 is like saying "1=1 is always true, do don't eliminate anything".

Reference :
[StackOverFlow Link](https://stackoverflow.com/questions/35374860/join-select-ue-on-1-1)

QUERY PLAN - it is used to check how much memory our query is using, and how much unnecessary records are being accessed.

	EXPLAIN ANALYZE - used when the query starts with SELECT

	ROLLBACK - used when the query starts with INSERT/UPDATE  

```