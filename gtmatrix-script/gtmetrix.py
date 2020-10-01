#! /usr/bin/python3.6
import os
import json
import time
import csv

URL = 'https://gtmetrix.com/api/0.1/test'

with open('gtmetrix.csv', mode='w') as gt_file:
    gt_add = csv.writer(gt_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    gt_add.writerow(["Site", "Region", "PageSpeed", "YSlow", "Requests", "PageSize (MB)", "LoadTime (Sec.)"])

with open("/home/admin/gtmetrix/account.json") as account:
    acc = json.loads(account.read())

    for check in acc['clients']:

        email = check['email']
        api = check['api']
        site = check['site']
        name = check['name']
        region = check['region']
        print(site)
        cmd1 = 'curl --user {0}:{1} --form url={2} --form x-metrix-adblock=0 {3} > code.json'.format(email, api, site, URL)
        os.system(cmd1)
        with open("code.json", "r") as read_file:
            data = json.load(read_file)
            gt_id = data["test_id"]
            time.sleep(50)
            cmd2 = "curl --user {0}:{1} {2}/{3} > report.json".format(email, api, URL, gt_id)
            os.system(cmd2)
            with open("report.json") as f:
                data = json.loads(f.read())
                pagespeed = data["results"]["pagespeed_score"]
                yslow = data["results"]["yslow_score"]
                requests = data["results"]["page_elements"]
                pagesize = round(data["results"]["page_bytes"]/1048576, 2)
                loadtime = data["results"]["page_load_time"]/1000
                with open('gtmetrix.csv', mode='a') as gt_file:
                    gt_put = csv.writer(gt_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    gt_put.writerow([site, region, pagespeed, yslow, requests, pagesize, loadtime])

os.system('python3 /home/admin/gtmetrix/send.py')
