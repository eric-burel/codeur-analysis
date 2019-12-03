#! ./venv/bin/python
import psycopg2
import subprocess
import glob


# List files
files = glob.glob("./dumps/*")
print("Restoring dumps", files)

for f in files:
    print("Restoring file", f)
    # Run
    subprocess.run([
        "pg_restore",
        "--verbose",
        "--clean",
        "--no-acl",
        "--no-owner",
        "-h",  "localhost",
        "-p", "5432",
        "-U", "postgres",
        "-d", "postgres",
        "-w",  # no pass prompt,
        "-t", "scraper_codeurproject",
        f
    ])

exit(0)
