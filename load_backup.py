#! ./venv/bin/python
#import psycopg2
import subprocess
import glob
import os

def run_sql_file(path):
    # dumps may have duplicates
    subprocess.run([
            "psql",
            "-h",  "localhost",
            "-p", "5432",
            "-U", "postgres",
            "-d", "postgres",
            "-w",  # no pass prompt,
            "-f", path
    ])

# List files
files = [
    f for f in glob.glob("./dumps/**/*")
]

# Sort files by reverse modification time, so we get the most recent structure
files = sorted(files, key=lambda f: os.path.getmtime(f), reverse=True)

print("Creating table")
run_sql_file("./create_scraper_table.sql")


print("Restoring dumps", files)

for idx, f in enumerate(files):
    print("Restoring file", f)
    # Run
    subprocess.run([
        "pg_restore",
        "--verbose",
        # Old version, did not provide a safe structure:
        # db structure is taken from the latest dump
        # other wise we take only data into consideration
        #"--clean" if idx == 0 else "--data-only",#"--clean", # Do NOT clean otherwise only the last dump is used
        "--data-only", # we expect the table to be created
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


print("Remove dups")
run_sql_file("./remove_dups.sql")

exit(0)
