# -*- coding: UTF-8 -*-
 
#只能用在没有PostCode的情况下
#python3 code
import threading
import pymysql
import urllib
import urllib.request
import urllib.error
import zlib
import gzip
from io import StringIO
import chardet

def getMysqlData():
	print('getMysqlData is load')
	#这里去重的函数应该是怎么样的呢
	SQLEXISTS = "SELECT * FROM scrapy_content WHERE id >= 2065"
	# SQLEXISTS = "SELECT COUNT(1) FROM scrapy WHERE title='%s' OR url='%s'"

	lock = threading.RLock()

	conn = pymysql.connect(user='root', passwd='', db='news', host='127.0.0.1')
	# conn.set_character_set('utf8')
	cursor = conn.cursor()
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')

	lock.acquire()
	rowsContent = cursor.execute(SQLEXISTS)
	rows = cursor.fetchall()
	lock.release()
	# print url, self.cursor.fetchall()[0][0]
	#  if rows > 0:
	# print cursor.fetchall(), rows

	# print(rows[0][1], rows[0][4])
	if rowsContent > 0:
		print('data count num is', rowsContent)
		for item in rows:
			print(item[0])
			# print(item[1].encode('latin1').decode('utf-8'))
			# exit()
			make_requests(item[1].encode('latin1').decode('utf-8'), item[4].encode('latin1').decode('utf-8'))
	else:
		print('db is no exists')


def make_requests(subject, message):
	response = [None]
	if (request_dz_dev(response, subject, message)):
		# Success, possibly use response.
		responseText = read_response(response[0])
		print(responseText)
		response[0].close()
	else:
		# Failure, cannot use response.
		pass


def request_dz_dev(response, subject, message):
	response[0] = None
	# try:
	req = urllib.request.Request("http://dz.dev/upload/forum.php?mod=post&action=newthread&fid=2&topicsubmit=yes&infloat=yes&handlekey=fastnewpost&inajax=1")

	req.add_header("Connection", "keep-alive")
	req.add_header("Cache-Control", "max-age=0")
	req.add_header("Origin", "http://dz.dev")
	req.add_header("Upgrade-Insecure-Requests", "1")
	req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36")
	req.add_header("Content-Type", "application/x-www-form-urlencoded")
	req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
	req.add_header("Referer", "http://dz.dev/upload/forum.php?mod=forumdisplay&fid=2")
	req.add_header("Accept-Encoding", "gzip, deflate")
	req.add_header("Accept-Language", "zh-CN,zh;q=0.8")
	req.add_header("Cookie", "XctC_2132_saltkey=PX28DdII; XctC_2132_lastvisit=1501545865; XctC_2132_nofavfid=1; XctC_2132_visitedfid=2; XctC_2132__refer=%252Fupload%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dpm%2526op%253Dchecknewpm%2526rand%253D1501660302; XctC_2132_auth=97b4f3deNAslHw%2BWbSUsSR8W4b8zRh3sc%2B3KO2HHiRUvKQfe%2BjHFBwfcBJa08w4RDhOd%2FppqGTKksOAsfRZU; XctC_2132_lastcheckfeed=1%7C1502027884; XctC_2132_lip=127.0.0.1%2C1502027884; XctC_2132_ulastactivity=6396L94cgGQ%2BYbGo6LzjcDVv%2FNXK5hDAbLWhUSJQ69FEWmDwS7Uo; XctC_2132_onlineusernum=1; XctC_2132_addoncheck_plugin=1; XctC_2132_seccode=3.640cf51428ca315f87; XctC_2132_st_t=1%7C1502193380%7Ce542e9b6f8f5c4c7fe465ce83bff58c7; XctC_2132_forum_lastvisit=D_2_1502193380; XctC_2132_sid=wsJCPp; XctC_2132_smile=1D1; XctC_2132_checkpatch=1; XctC_2132_lastact=1502193418%09forum.php%09ajax")

	# body = "subject=" + subject + "&message=" + message + "&formhash=7e9bb576&usesig=1&posttime=1502193380"

	body = "subject=" + subject + "&message=" + message + "&formhash=7e9bb576&usesig=1&posttime=1502193380"
	print(body)


	response[0] = urllib.request.urlopen(req,  bytes(body, encoding = "utf8"))

	# except urllib.error.URLError as e:
	# 	if not hasattr(e, "code"):
	# 		return False
	# 	response[0] = e
	# except:
	# 	print('http post except')
	# 	return False

	return True

def read_response(response):
	""" Returns the text contained in the response.  For example, the page HTML.  Only handles the most common HTTP encodings."""
	if response.info().get('Content-Encoding') == 'gzip':
		buf = BytesIO(response.read())
		return gzip.GzipFile(fileobj=buf).read().decode('utf8')

	elif response.info().get('Content-Encoding') == 'deflate':
		decompress = zlib.decompressobj(-zlib.MAX_WBITS)
		inflated = decompress.decompress(response.read())
		inflated += decompress.flush()
		return inflated.decode('utf8')

	return response.read().decode('utf8')
getMysqlData()
