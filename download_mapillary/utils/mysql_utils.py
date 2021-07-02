# -*- coding: utf-8 -*-

import mysql.connector
import csv
db = ''


def create_db(db_name):
    db = mysql.connector.connect(user="root", password="123456", host="localhost")
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS " + db_name
    cursor.execute(sql)
    db.close()


#数据库连接
def connect_db(db_name):
    try:
        db = mysql.connector.connect(user="root", password="123456", host="localhost", database=db_name)
        print('connected')

        return db
    except Exception as e:
        print(e)


#数据库关闭
def close_sql(db):
    try:
        db.close()
    except Exception as e:
        print(e)


#创建表
def creat_table(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
        db.rollback()


#根据返回值（0,1）判定某表是否存在
def table_exist(db,tablename,database_name):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_NAME='"+tablename+"' and TABLE_SCHEMA='"+database_name+"'")
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)


#数据库查询
def sql_select(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)


def sql_select_with_params(db, sql, params):
    cursor = db.cursor()
    try:
        cursor.execute(sql, params)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)


#单条插入（not userd）
def sql_insert_singel(db,sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


#批量导入
def sql_insert_many(db, sql, values):
    cursor = db.cursor()
    try:
        cursor.executemany(sql, values)
        db.commit()
        print('<----insert done---->')
    except Exception as e:
        if 'truncated' in e:
            print(e)
        db.rollback()

# 更新数据表
def update_table(db, sql, table_name, fields, placeholders, assignments, values):
    cursor = db.cursor()
    try:
        cursor.executemany(sql.format(
                                table=table_name,
                                fields=", ".join(fields),
                                placeholders=", ".join(placeholders),
                                assignments=", ".join(assignments)
                            ), values)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()




# export data from mysql
def export_data(db, output_file_path, sql, params=None):
    cursor = db.cursor()
    try:
        if params is None:
            cursor.execute(sql)
            rows = cursor.fetchall()
        else:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        f = open(output_file_path, 'w')
        csv_file = csv.writer(f, lineterminator='\n')
        csv_file.writerows(rows)
        f.close()

    except Exception as e:
        print(e)
        db.rollback()


# add columns to a table
def add_column(db, sql):
    cur = db.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    # create_db("mapillary")
    db = connect_db("mapillary")

    # year = [2014,2015,2016,2017]
    # for y in year:
    #     for m in range(1,13):
    #         select_sql = "select count(*) from `cambridge_mapillary` where year = %d and month = %d" %(y,m)
    #         result = sql_select(db,select_sql)
    #         print "%d %d %d" % (y,m,result[0][0])

    # output_file_path = '/home/zcq/mysql_output_dir/LA_all_street_points.csv'
    # output_file_path = '/home/zcq/mysql_output_dir/new_Berlin_all_street_points.csv'
    # sql = "select img_key,user_key,lon,lat,captured_at from Berlin"
    # export_data(db, output_file_path, sql)


    sql = "alter table Berlin add cor_lon varchar(30) CHARACTER set utf8 default null, " \
          "add cor_lat varchar(30) CHARACTER set utf8 default null"
    add_column(db, sql)


    close_sql(db)



