from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
from dotenv import load_dotenv
import smtplib
import ssl
import logging

load_dotenv()
FORMAT = '%(levelname)s:%(asctime)s - %(message)s'
logging.basicConfig(filename='/home/artfvl/Documents/code/kensington-stock-checker/process.log',
                    encoding='utf-8', level=logging.INFO, format=FORMAT)


product_name = 'Kensington Slimblade Pro'
product_url = 'https://www.kensington.com/en-gb/p/products/control/trackballs/slimblade-pro-trackball-1/'  # Target product
# product_url = 'https://www.kensington.com/en-gb/p/products/control/trackballs/slimblade-trackball/' # Known in-stock product for testing

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
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
        logging.info("Product is available.")
    except Exception:
        logging.exception("Item in stock, email failed.")
else:
    logging.info("Item not in stock, no email sent.")
driver.close()
