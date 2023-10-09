from funcs import show_help, add, get, update_status, export_csv
import sys
import sqlite3

if __name__ == '__main__':
    con = sqlite3.connect('jobs.db')
    # Create the jobs table
    c = con.cursor()
    query = 'CREATE TABLE IF NOT EXISTS jobs (' \
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
            'company_name TEXT NOT NULL, ' \
            'date DATE NOT NULL, ' \
            'job_title TEXT, ' \
            'status TEXT);'
    c.execute(query)
    if len(sys.argv) < 2:
        show_help()
    else:
        try:
            if sys.argv[1] == '-a' or sys.argv[1] == '--add':
                add(con, sys.argv[2], job_title=sys.argv[3])
            elif sys.argv[1] == '-r' or sys.argv[1] == '--remove':
                if len(sys.argv) > 3:
                    add(con, sys.argv[2], date=sys.argv[3], add=False)
                else:
                    add(con, sys.argv[2], add=False)
            elif sys.argv[1] == '-g' or sys.argv[1] == '--get':
                get(con, sys.argv[2])
            elif sys.argv[1] == '-s' or sys.argv[1] == '--show-all':
                get(con, None, get_all=True)
            elif sys.argv[1] == '-u' or sys.argv[1] == '--update':
                update_status(con, sys.argv[2], sys.argv[3], sys.argv[4])
            elif sys.argv[1] == '-o' or sys.argv[1] == '--export':
                file_name = sys.argv[2] if len(sys.argv) >= 3 else "jobs.csv"
                export_csv(con, file_name)
            else:
                print("Unrecognized option, Try again !")
        except Exception as e:
            print(e)
