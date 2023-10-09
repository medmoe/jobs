import csv
import sqlite3
from datetime import datetime


def show_help():
    print(
        """
        jobs usage: [options] [<file name> or <job to add>]:

            Options:
                -s, --show-all       : Show all existing jobs
                -a, --add            : Add a new job
                -r, --remove         : Remove an existing job
                -g, --get            : Retrieve an existing job
                -u, --update         : Update status of a job
                -o, --export         : Export data to CSV file

            Status Flags:
                rejected             : Job status flag
                accepted             : Job status flag
                applied              : Job status flag

        Description:
            The script provides a basic tracking program for jobs applied to. 
            When adding a new job, the company's name, and the job's title should be passed.
            When updating job status, the company's name and date should be passed.

        Examples:
            jobs.py -a Test 'Software engineer' 10/10/2020
            jobs.py -g Test
            jobs.py -r Test 10/10/2020
            jobs.py -u Test 10/10/2020 accepted
            jobs.py -o output.csv
        """
    )


def add(con, name, job_title=None, add=True):
    """
    con: connection to the database
    name: company's name
    """
    cur = con.cursor()
    insertion_query = 'INSERT INTO jobs (company_name, date, job_title, status) VALUES (?, ?, ?, ?)'
    if add:
        cur.execute(insertion_query, (name, datetime.now().date(), job_title, 'applied'))
    else:
        cur.execute(f"DELETE FROM jobs WHERE company_name = '{name}'")

    con.commit()
    con.close()


def get(con, name, get_all=False):
    cur = con.cursor()
    query = "SELECT * FROM jobs" if get_all else f"SELECT * FROM jobs WHERE name = '{name}'"
    cur.execute(query)
    res = cur.fetchall()
    print("Company\t\tDate\t\tStatus\t\tJob Title")
    for item in res:
        print(f'{item[1]:<10}\t{item[2]:<10}\t{item[4]:<10}\t{item[3]:<10}')
    con.commit()
    con.close()


def update_status(con, name, date, status):
    cur = con.cursor()
    cur.execute(f"UPDATE jobs SET status = '{status}' WHERE name = '{name}' AND date = '{date}'")
    res = cur.fetchall()
    print(res)
    con.commit()
    con.close()


def export_csv(con, file_name):
    cur = con.cursor()
    cur.execute('SELECT * FROM jobs')
    rows = cur.fetchall()

    # Write to CSV
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([description[0] for description in cur.description])  # write headers
        for row in rows:
            writer.writerow(row)
    con.commit()
    con.close()
    print("done!")
