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


@app.route("/pools")
def get_pools():
    all_pools = []

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
