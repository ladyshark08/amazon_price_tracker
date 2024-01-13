import requests
from bs4 import BeautifulSoup
from pprint import pprint
import smtplib
import os

my_email = ""
password = os.environ.get("PASSWORD")

url = ("https://www.amazon.ca/dp/B0B8TC6KWF/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0B8TC6KWF&pd_rd_w=0z6rX&content-id"
       "=amzn1.sym.75a1cf77-5ca0-4d60-94bd-a9c2c988c"
       "1c3&pf_rd_p=75a1cf77-5ca0-4d60-94bd-a9c2c988c1c3&pf_rd_r=2AJTJ2W8PKDKSA9Y570M&pd_rd_wg=Z2Icp&pd_rd_r=6e441af3"
       "-1b9f"
       "-4e9f-b39c-bb5671cbc549")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept-Language": "en-US,en;q=0.5",
    "sec-fetch_dest": "document"
}

response = requests.get(url=url, headers=headers)
webpage = response.text

soup = BeautifulSoup(webpage, "lxml")
price = soup.select_one(selector=".a-offscreen").text
title = soup.select_one(selector="#productTitle").text.strip()
price = price.replace("$", "")
price_fig = price.split(".")
final_price = int(price_fig[0])


if final_price < 200:
    with smtplib.SMTP("smtp.gmail.com", port=587) as new_connect:
        new_connect.starttls()
        message = f'Subject: Amazon Price Alert\n\nHello,\n\n{title} is now ${final_price}\n\n{url}'
        new_connect.login(user=my_email, password=password)
        new_connect.sendmail(from_addr=my_email, to_addrs="",
                             msg=message)
