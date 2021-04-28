sqlite3 ..\stan_db_import\tocc.sqlite ".read dump_db.sql"
del tocc.sqlite
sqlite3 tocc.sqlite ".read db_dump.sql"
