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



@app.route("/static/add_pool", methods=['POST'])
def add_pool():

    # Assignment 4: Insert Pool into database.
    # Extract all the form fields
    print('received request.')
    #cur = getCursor()
    pool_name = request.form['pool_name']
    status = request.form['status']
    phone = request.form['phone']
    pool_type = request.form['pool_type']
    print("Pool Name:" + pool_name)
    print("Status:" + status)
    #cur.execute("SELECT COUNT(*) FROM pools WHERE pool_name='{}'".format(pool_name))
    result=cur.fetchone()
    print(pool_name, repr(result[0]))
    if result[0] != 0:
        print("I made it to here!")
        return render_template('pool_added.html')
    #error = validatePool(d2, d3, d4)
    #if error:
        #return error, 400
    #cur.execute("INSERT INTO pools(pool_name, status, phone, pool_type) values ('{}', '{}', '{}', '{}')".format(pool_name, status, phone, pool_type))
    #cur.cnx.commit()
    print("Returning from addPools")
    return render_template('pool_added.html')


@app.route("/pools")
def get_pools():
    all_pools = []
    # Assignment 4:
    # Query the database to pull all the pools
    #cur = getCursor()
    #cur.execute("SELECT * FROM pools")
    #results=cur.fetchall()
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
