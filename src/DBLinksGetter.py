import MySQLdb

db_user = 'root'
db_password = ''
db = 'INLP_schema'

connection = MySQLdb.connect(host="localhost",user=db_user, passwd=db_password,db=db)

def get_links(bio=True):
	#Get all the bio or non-bio links
	cur = connection.cursor()
	#sql = "SELECT id, link FROM article WHERE save = 1 and LENGTH(content) < 2 ORDER BY id;"
	sql = "SELECT link FROM article WHERE is_bio = %s;" % (1 if bio else 0)
	cur.execute(sql)
	rows = cur.fetchall()
	return [row[0].strip() for row in rows]

def get_links_gen(bio=True):
	#Get all the bio or non-bio links generator function
	cur = connection.cursor()
	sql = "SELECT link FROM article WHERE is_bio = %s;" % (1 if bio else 0) # FIXME what about is_bio = -1?
	cur.execute(sql)
	rows = cur.fetchall()
	for row in rows:
		yield row[0].strip()

if __name__ == '__main__':
	a = get_links_gen()
	print a.next()
	print a.next()
	print get_links()
	print
	print len(get_links()), len(get_links(False))
	for l in get_links_gen():
		print l