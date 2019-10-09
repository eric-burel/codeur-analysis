#! ./venv/bin/python
import psycopg2
import subprocess
subprocess.run(
    "pg_restore --verbose --clean --no-acl --no-owner -h localhost -p 5432 -U postgres -P admin123 -d postgres latest.dump",
    shell=True
)
