from datetime import datetime
import sqlite3


def show_help():
    print(
        """
        jobs usage: [options] [<file name> or <job to add>]:
            -s      --show-all  :show all existing jobs
            -a 		--add		:add a new job
            -r		--remove	:remove an existed job
            -g		--get		:retrieve an existed job
            -u		--update	:update status of the job
            
            rejected 	:job status flag
            accepted	:job status flag
            applied	:job status flag
    
        description: The script provides a basic tracking program of jobs applied to.
        when adding a new job, company's name and date should be passed as arguments and job's title is optional.
        when updating job status, company's name and status flag should be passed too. 
        example:
            jobs.py -a Test 'Software engineer' 10/10/2020
            jobs.py -g Test
            jobs.py -r test 10/10/2020
            jobs.py -u Test /10/10/2020 accepted
        """)


def add(con, name, date, job_title=None, add=True):
    """
    con: connection to the database
    name: company's name
    """
    cur = con.cursor()
    if add:
        try:
            cur.execute(f"INSERT INTO jobs VALUES('{datetime.now()}','{name}', '{job_title}', '{date}', 'applied')")
        except sqlite3.OperationalError:
            cur.execute(''' CREATE TABLE jobs(id text, name text, job_title text, date text, status text)''')
            cur.execute(f"INSERT INTO jobs VALUES('{datetime.now()}','{name}', '{job_title}', '{date}', 'applied')")
    else:
        cur.execute(f"DELETE FROM jobs WHERE name = '{name}' AND date = '{date}'")

    con.commit()
    con.close()


def get(con, name, get_all=False):
    cur = con.cursor()
    query = "SELECT * FROM jobs" if get_all else f"SELECT * FROM jobs WHERE name = '{name}'"
    cur.execute(query)
    res = cur.fetchall()
    print("Company\t\tDate\t\tStatus\t\tJob Title")
    for item in res:
        print(f'{item[1]}\t\t{item[3]}\t{item[4]}\t\t{item[2]}')
    con.commit()
    con.close()


def update_status(con, name, date, status):
    cur = con.cursor()
    cur.execute(f"UPDATE jobs SET status = '{status}' WHERE name = '{name}' AND date = '{date}'")
    res = cur.fetchall()
    print(res)
    con.commit()
    con.close()

