# get data on pools
import requests
import os
import time
import json
from flask import request, abort
from flask import Flask, render_template
import re
import xml.etree.ElementTree as ET

source = "https://raw.githubusercontent.com/devdattakulkarni/elements-of-web-programming/master/data/austin-pool-timings.xml"

data = requests.get(source)

root = ET.fromstring(data.text)


app = Flask(__name__)



"""
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
"""


@app.route("/pools")
def get_pools():
    all_pools = []
    # Assignment 4:
    # Query the database to pull all the pools
    #cur = getCursor()
    #cur.execute("SELECT * FROM pools")
    #results=cur.fetchall()
    """
    for pool in results:
        poolDic = {'Name': pool[0], 'Status': pool[1], 'Phone': pool[2], 'Type': pool[3]}
        all_pools.append(poolDic)
        """
    """
    pool = {}
    pool['Name'] = 'Barton Springs'
    pool['Type'] = 'Community'
    pool['Status'] = 'Open'
    pool['Weekday'] = '9-5'
    pool['Weekend'] = 'Closed'
    """
# parses the xml file
    for pool in root.findall('row'):
        pool_name = ''
        pool_type = ''
        status = ''
        weekday = ''
        weekend = ''
        try:
            pool_name = pool.find('pool_name').text
            pool_type = pool.find('pool_type').text
            status = pool.find('status')
            if status is not None:
                status = status.text
            weekday = pool.find('weekday')
            if weekday is not None:
                weekday = weekday.text
            weekend = pool.find('weekend')
            if weekend is not None:
                weekend = weekend.text


        except AttributeError:
            print(pool)
            import traceback
            traceback.print_exc()
            continue

        all_pools.append({"Name":pool_name, "Type": pool_type, "Status": status, "Weekday": weekday, "Weekend": weekend})
    return json.dumps(all_pools)


@app.route("/")
def pool_info_website():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
