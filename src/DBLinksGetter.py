import MySQLdb

db_user = 'root'
db_password = 'root'
db = 'inlp'

connection = MySQLdb.connect(host="localhost",user=db_user, passwd=db_password,db=db)


def access_db(allCntnt=True,bio=True,dbid=0):
	#Get all the bio or non-bio links generator function
	cur = connection.cursor()
	sql = "SELECT id,link FROM article"
	if not allCntnt:
		sql=sql+" WHERE save=1 AND is_bio = %s AND id>%s ORDER BY id;" % (1 if bio else 0, dbid) # FIXME what about is_bio = -1?
	else:
		sql=sql+" WHERE save=1 AND id>%d ORDER BY id;" % (dbid)
	print sql
	cur.execute(sql)
	rows = cur.fetchall()
	return rows

def get_links(allCntnt=True,bio=True,dbid=0):
	rows = access_db(allCntnt,bio,dbid=dbid)
	return [(row[0],row[1].strip()) for row in rows]

def get_links_gen(allCntnt=True, bio=True,dbid=0):
	rows = access_db(allCntnt,bio,dbid=dbid)
	for row in rows:
		yield (row[0],row[1].strip())

if __name__ == '__main__':
	a = get_links_gen()
	print a.next()
	print a.next()
	print get_links()
	print
	print len(get_links()), len(get_links(False,False))
	for l in get_links_gen():
		print l