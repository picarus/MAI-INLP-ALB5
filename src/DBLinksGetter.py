import MySQLdb

db_user = 'root'
db_password = 'root'
db = 'inlp'

connection = MySQLdb.connect(host="localhost",user=db_user, passwd=db_password,db=db)


def access_db(allCntnt=True,bio=True):
	#Get all the bio or non-bio links generator function
	cur = connection.cursor()
	sql = "SELECT link FROM article"
	if not allCntnt:
		sql=sql+" WHERE is_bio = %s;" % (1 if bio else 0) # FIXME what about is_bio = -1?
	cur.execute(sql)
	rows = cur.fetchall()
	return rows

def get_links(allCntnt=True,bio=True):
	rows = access_db(allCntnt,bio)
	return [row[0].strip() for row in rows]

def get_links_gen(allCntnt=True, bio=True):
	rows = access_db(allCntnt,bio)
	for row in rows:
		yield row[0].strip()

if __name__ == '__main__':
	a = get_links_gen()
	print a.next()
	print a.next()
	print get_links()
	print
	print len(get_links()), len(get_links(False,False))
	for l in get_links_gen():
		print l