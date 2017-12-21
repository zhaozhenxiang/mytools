#!/usr/bin/python3
#coding=utf-8
import pymysql
import configInfo

#获取链接
def __getCursor():        
    configInstance = configInfo.configInfo()
    # 打开数据库连接
    db = pymysql.connect(configInstance.get('mysql', 'host'),configInstance.get('mysql', 'user'),configInstance.get('mysql', 'password'),configInstance.get('mysql', 'database'),charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    return cursor, db
#获取数据
def loadMysqlData(limitCount):
    (cursor, db) = __getCursor()
    # SQL 查询语句
    sql = 'SELECT * FROM `video_download` WHERE `status` = 0  order by `id` asc limit 0, %d'
    try:
        # 执行SQL语句
        cursor.execute(sql % (limitCount))
        # 获取所有记录列表
        results = cursor.fetchall()    
    except:
        results = ()
        print ("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return results

#打印数据
# print(loadMysqlData(1))

def updateRows(rows):
    if 0 == len(rows):
        print('updateRows的实参为空')
        return
    (cursor, db) = __getCursor()    
    # SQL 更新语句
    sql = "UPDATE `video_download` SET `start_down_time` = '%s', \
    `downloaded_time` = '%s', `status` = %d, `video_path` = '%s', \
    `sub_title_path` = '%s', `merge_path` = '%s' \
     where `id` = %d"
    for item in rows:
        try:
            # 执行SQL语句
            cursor.execute(sql % (item[0], item[1], item[2], db.escape_string(item[3]), db.escape_string(item[4]), db.escape_string(item[5]), item[6]))
            
            # cursor.execute(sql % (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
            # 提交到数据库执行
            db.commit()
        except pymysql.Error as e:
            # 发生错误时回滚
            db.rollback()            
            db.close()
            print(e)
            return False
            # 关闭数据库连接
    
    db.close()
    return True

#更新数据
# updateData = [('2017-08-29 14:14:00', '2017-08-29 14:14:00', 1, 'asd', 'asd', 'asd', 1)]
# print(updateRows(updateData))




