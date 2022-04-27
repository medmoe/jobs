from funcs import show_help, add, get, update_status
import sys
import sqlite3

if __name__ == '__main__':
	con = sqlite3.connect('jobs.db')
	if len(sys.argv) < 2:
		show_help()
	else:
		try:
			if sys.argv[1] == '-a' or sys.argv[1] == '--add':
				add(con, sys.argv[2], sys.argv[4], job_title=sys.argv[3])
			elif sys.argv[1] == '-r' or sys.argv[1] == '--remove':
				add(con, sys.argv[2], sys.argv[3], add=False)
			elif sys.argv[1] == '-g' or sys.argv[1] == '--get':
				get(con, sys.argv[2])
			elif sys.argv[1] == '-s' or sys.argv[1] == '--show-all':
				get(con, None, get_all=True)
			elif sys.argv[1] == '-u' or sys.argv[1] == '--update':
				update_status(con, sys.argv[2], sys.argv[3], sys.argv[4])
			else:
				print("Unrecognized option, Try again !")
		except Exception as e:
			show_help()

