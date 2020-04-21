# get data on pools
import requests
import os
import time
import json
from flask import request, abort
from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode
import re


application = Flask(__name__)
app = application
all_pools = []

def get_db_creds():
    db = os.environ.get("DB", None) or os.environ.get("database", None) or 'pools_db'
    username = os.environ.get("USER", None) or os.environ.get("username", None) or 'root'
    password = os.environ.get("PASSWORD", None) or os.environ.get("password", None) or ''
    hostname = os.environ.get("HOST", None) or os.environ.get("dbhost", None) or 'localhost'
    return db, username, password, hostname

def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    table_ddl = 'CREATE TABLE pools(pool_name char(50) NOT NULL UNIQUE, status char(50) NOT NULL, phone char(50) NOT NULL, pool_type char(50) NOT NULL, PRIMARY KEY(pool_name))'
    cur = getCursor()


    try:
        cur.execute('DROP TABLE pools')
        cur.execute(table_ddl)
        cur.cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

def getCursor():
        db, username, password, hostname = get_db_creds()


        cnx = ''
        try:
            cnx = mysql.connector.connect(user=username, password=password, host=hostname, database=db)

        except Exception as exp:
            print(exp)
            raise

        cur = cnx.cursor()
        cur.cnx = cnx
        return cur

def query_data():

    db, username, password, hostname = get_db_creds()

    print("Inside query_data")
    print("DB: %s" % db)
    print("Username: %s" % username)
    print("Password: %s" % password)
    print("Hostname: %s" % hostname)

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        raise

    cur = cnx.cursor()

    cur.execute("SELECT pool_name FROM pools")
    entries = [dict(pool_name=row[0]) for row in cur.fetchall()]
    return entries

try:
    print("---------" + time.strftime('%a %H:%M:%S'))
    print("Before create_table global")
    create_table()
    print("After create_data global")
except Exception as exp:
    print("Got exception %s" % exp)
    conn = None

@app.route("/static/add_pool", methods=['POST'])
def add_pool():

    # Assignment 4: Insert Pool into database.
    # Extract all the form fields
    print('received request.')
    cur = getCursor()
    pool_name = request.form['pool_name']
    status = request.form['status']
    phone = request.form['phone']
    pool_type = request.form['pool_type']
    print("Pool Name:" + pool_name)
    print("Status:" + status)
    cur.execute("SELECT COUNT(*) FROM pools WHERE pool_name='{}'".format(pool_name))
    result=cur.fetchone()
    print(pool_name, repr(result[0]))
    if result[0] != 0:
        return render_template('pool_added.html')
    #error = validatePool(d2, d3, d4)
    #if error:
        #return error, 400
    cur.execute("INSERT INTO pools(pool_name, status, phone, pool_type) values ('{}', '{}', '{}', '{}')".format(pool_name, status, phone, pool_type))
    cur.cnx.commit()
    print("Returning from addPools")
    return render_template('pool_added.html')

    # Insert into database.


    return render_template('pool_added.html')


@app.route("/pools")
def get_pools():
    # Assignment 4:
    # Query the database to pull all the pools
    # Sample pool -- Delete this from final output.
    cur = getCursor()
    cur.execute("SELECT * FROM pools")
    results=cur.fetchall()
    for pool in results:
        poolDic = {'Name': pool[0], 'Status': pool[1], 'Phone': pool[2], 'Type': pool[3]}
        all_pools.append(poolDic)
    return json.dumps(all_pools)


@app.route("/")
def pool_info_website():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
