# Youtube-Database

## To build the database:
```bash
psql -d postgres -U isdb -f initialize.sql
```

Then, run the following to use queries:
```bash
python <query-file-name>
e.g. python complex_query_1.py
```
