The Kensington website doesn't have an "email when back in stock button" so I made an alternative.

Notes:
- Run `pip3 install -r requirements.txt` to install dependencies
- Create a `.env` file containing your SMTP email and password and keep it secure
- If you don't have Firefox, you can use Chrome, but may need the chromewebdriver if not already setup
- Can easily be adapted to check stock of other products/retailers, just update the product URL and "Where to Buy" text, replacing with text that only appears when the product is available
- Update the absolute paths in 'main.sh' based on where your code is stored. Crontab will not work otherwise
- Example cron job could be `0 * * * * bash /home/artfvl/Documents/code/kensington-stock-checker/main.sh` this will run once per hour in the background

