from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
from dotenv import load_dotenv
import smtplib
import ssl
import logging

load_dotenv()
logging.basicConfig(filename='error.log',
                    encoding='utf-8', level=logging.DEBUG)


product_name = 'Kensington Slimblade Pro'
product_url = 'https://www.kensington.com/en-gb/p/products/control/trackballs/slimblade-pro-trackball-1/'  # Target product
# product_url = 'https://www.kensington.com/en-gb/p/products/control/trackballs/slimblade-trackball/' # Known in-stock product for testing

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)
driver.get(product_url)

port = 587
# SMTP setup (option 2) https://support.google.com/a/answer/176600?hl=en
smtp_server = 'smtp.gmail.com'
smtp_email = os.getenv('SMTP_EMAIL')
# Create app password https://support.google.com/accounts/answer/185833?hl=en#zippy=%2Cwhy-you-may-need-an-app-password
smtp_password = os.getenv('SMTP_PASSWORD')

# For different retailers, the wording can be adjusted to match their "in stock" identifier
if "Where to Buy" in driver.page_source:
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(smtp_email, smtp_password)
        message = 'Subject: {} in Stock!\n\n{}'.format(
            product_name, product_url)

        server.sendmail(
            smtp_email,
            smtp_email,
            message
        )
        print("Product is available.")
    except Exception:
        logging.exception("Email Failed")

driver.close()
