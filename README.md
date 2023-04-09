# Youtube-Database

## To build the database:
```bash
psql -d postgres -U isdb -f initialize.sql
```

Then, run `python <query-file-name>` to use queries, for example:
```bash
python complex_query_1.py
```
