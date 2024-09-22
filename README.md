# gatherpass
This tool is meant to periodically scan paste pages and forums for possible leaks. It allows full customization of both, as well as the option to setup conditions for the detection.
## Features
- Notification via [ntfy](https://ntfy.sh/) (**NOTE**: Using the public ntfy server means your notifications are available in cleartext to the public ntfy server. Only use the public server if you are fine with this, otherwise use a self hosted version)
- Scanning pastes or hacker forums for leaks using custom rules and password lists
- Provides tested configurations for quick start
- Uses Google Indexing to search most recent pastes
- Saves result in sqlite3

## What does it really do

Forum threads are scanned with basic python requests and selenium. However, paste pages are dealt with a bit more specifically: It uses the Google search engine, specifically Google Indexing, to search for recent pastes on Google. An example Google query to find the recent pastes from `pastebin.com` after 2024-05-19:
`site:pastebin.com after:2024-05-19`

To successfully gather the data from forums, you will *need* to log in once. Otherwise, you can not use the extra reply functionality of the code. But there are still leaks to find in forums.
## Requirements
1.  `python3.11`
2.  `aspell-*`
3.  `chromium-chromedriver` and the option to open a X window
4.  A list of passwords (sha1 hashed). You can get a list online, from e.g. HIBP:
    1.  Use the [PwnedPasswordsDownloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader) to download HIBP passwords (requires dotnet)
    2.  The password hashes are paired with their frequency in the database. Sort by frequency, then take any amount of hashes from there.
    3.  (Optional) Add custom hashes to password list `echo -n "hello" | sha1sum | awk '{print $1}'c >> password_list.txt` ([source](https://stackoverflow.com/questions/15626073/sha1-password-hash-linux))

## Installation steps
Ubuntu:
```sh
sudo apt install python3 python3-virtualenv sqlite3 aspell-* chromium-chromedriver
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Setup

Before running either of the scripts, it is important to configure the scan by creating a file `conf.json`. This file configures where to scan, and other informations. Here is an example that covers most of the information needed:
```json
{
    "page_list": [
        
        {
            "site": "ideone.com",
            "dl": "plain/"
        },
        {
            "site": "pastebin.ai",
            "dl": "raw/"
        },
        {
            "site": "pastebin.com",
            "dl": "raw/"
        },
        {
            "site": "p.ip.fi",
            "dl": ""
        },
        {   
            "site": "paste.fo",
            "dl": "raw/"
        },
        {
            "site": "www.bitbin.it",
            "dl": "/raw",
            "reverse": true
        }
    ],
    "cookies": {
        "CONSENT": "PENDING+987",
        "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg"
    },
    "separators": [
        ":",
        "|",
        ";"
    ],
    "passlist": "password_list_hashes_3.txt",
    "urls_to_gather": [
        "https://t.me"
    ],
    "forums": [
        {
            "name": "cracked.io",
            "login_uri": "/member.php?action=login",
            "dump_list": "/Forum-Accounts?sortby=started&order=desc&datecut=9999&prefix=0",
            "tid": "topiclist",
            "thanks": "//a[@class='postbit_thanks add_tyl_button']",
            "quote": "postbit_quote",
            "posts": "posts",
            "post_body": "post-set",
            "post_content": "post-content",
            "post_content3": "//div[2]/div[4]/div/div/div[5]/table/tbody/tr/td/div/div/div[1]/div[2]/div[3]/div[2]/div/div[2]",
            "post_content2": "//div[3]/div[4]/div/div/div[3]/table[1]/tbody/tr/td/div/div/div[1]/div[2]/div[3]/div[2]/div/div[2]",
            "post_bottom": "//div[2]/div[4]/div/div/div[5]/table/tbody/tr/td/div/div/div[1]/div[2]/div[4]/div/div/div[2]",
            "reply_body_iframe": "//div[@id='content']/div/div/form/table/tbody/tr[5]/td/div/div/div/iframe",
            "reply_body": "//body/br",
            "reply_post": "//body/div[2]/div[4]/div/div/form/div/input[1]",
            "unlike": "UNLIKE",
            "hidden": "Hidden Content\nYou must reply to this thread to view this content or upgrade your account.\n\nNote: Upgrade your account to see all hidden content on every post without replying and prevent getting banned."
        },
        {
            "name": "cracked.io",
            "login_uri": "/member.php?action=login",
            "dump_list": "/Forum-Combolists--297?sortby=started&order=desc&datecut=9999&prefix=0",
            "tid": "topiclist",
            "thanks": "//a[@class='postbit_thanks add_tyl_button']",
            "quote": "postbit_quote",
            "posts": "posts",
            "post_body": "post-set",
            "post_content": "post-content",
            "post_content3": "//div[2]/div[4]/div/div/div[5]/table/tbody/tr/td/div/div/div[1]/div[2]/div[3]/div[2]/div/div[2]",
            "post_content2": "//div[3]/div[4]/div/div/div[3]/table[1]/tbody/tr/td/div/div/div[1]/div[2]/div[3]/div[2]/div/div[2]",
            "post_bottom": "//div[2]/div[4]/div/div/div[5]/table/tbody/tr/td/div/div/div[1]/div[2]/div[4]/div/div/div[2]",
            "reply_body_iframe": "//div[@id='content']/div/div/form/table/tbody/tr[5]/td/div/div/div/iframe",
            "reply_body": "//body/br",
            "reply_post": "//body/div[2]/div[4]/div/div/form/div/input[1]",
            "unlike": "UNLIKE",
            "hidden": "Hidden Content\nYou must reply to this thread to view this content or upgrade your account.\n\nNote: Upgrade your account to see all hidden content on every post without replying and prevent getting banned."
        }
    ],
    "ratio": 0.0695,
    "user_data": "./chrome-data",
    "user_data_tmp_": "C:/Users/username/AppData/Local/Google/Chrome/User Data",
    "chrome_binary_tmp": "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "chrome_binary": "/usr/bin/chromedriver",
    "ntfy_topic": "https://ntfy.sh/mVwSOeEKHBKoR57y",
    "pastes": "pastes/",
    "threads": "threads/",
    "ignore_list": ["--", "#include", "public", "import", "class", "NULL", "True", "true", "//", "#1"],
    "DEBUG": true,
    "any_pw": false
}
```

After setting everything up, you need to manually log in to the hacker forum you want to scan. The session data will be saved, meaning you will not have to log in again. 

### Variable explanation
Some of these variables you will have to define yourself. If you want to scan a new forum not in this example list, you can determine the variables by going into the HTML code of the forum, right clicking on the appropiate element then select `Copy full XPath`. Make sure to change `/html/body/div` to `//div`.

| Variable | Explanation |
| -------- | ------- |
| page_list | List of paste pages, each using the _site_ and _dl_ parameter |
| cookies | This variable attempts to bypass Google Captchas that usually stop automated requests that use the Google search engine |
| seperators | A list of characters you believe seperate passwords |
| passlist | The filename/path to the file that contains the password list |
| urls_to_gather | A list of URLs that you might want to gather from pastes or forums |
| forums | List of forums to scan |
| ratio | The password to word ratio |
| user_data | The folder to save the chromium session data to |
| chrome_binary | The directory of the chromedriver exe |
| ntfy_topic | The URl of the ntfy topic to post to (Optional) |
| pastes | Folder to save the pastes to (needs to be created in advance) |
| threads | Folder to save threads to (needs to be created in advance) |
| ignore_list | List of passwords to ignore |
| DEBUG | Set this value to true if you wish to have the output of the logging package to your console |
| any_pw | The LeakParser will detect any text as a leak if it has found at least one password from the password list |


For pastes:

| Variable | Explanation |
| -------- | ------- |
| site | URL of paste page, without `https://` |
| dl | the url extension used for getting words and the text of the paste. It is recommended to use any URL extension that results in raw text. PLeasre make sure to use a slash at the end |
| reverse | Some paste pages use the dl extension _after_ the id of the paste, then set this variable |

For forums:

| Variable | Explanation |
| -------- | ------- |
| name | Name of forum, the URL. Withouth `https://` |
| dump_list | Each hacker forum usually has a page with the threads in a list, enter the sub-URL here |
| tid | HTML id of the element that has the list |
| thanks | The path to the button for liking. This button is used to not seem suspicious |
| quote | The ID of the button used for responding |
| posts | ID of the table that has the posts |
| post_body | Body of a post |
| post_content | Content of the post |
| post_bottom | Bottom row of post that usually has the buttons |
| reply_body_iframe | Threads use an iframe for their reply body. This path delivers the path to iframe to switch to |
| reply_body | Body of where to write to |
| reply_post | Button to post the reply |
| unlike | The text on the button if a post has been like before |
| hidden | text that indicates that the content of the post is hidden |

## Running the code

After setting up the configuration, you can then perform scans through a cronjob that runs the script `cron_job.sh`.

In general, there are 2 main functions: 
1. `google_paste_scraper.py`
2. `forum_scraper.py`

You can also write your own main function if you wish to add more logging or if you wish to add this code to any existing code. To e.g. run the Google scraper, these are the necessary imports:
```py
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
```
Then you can initialize objects like this:
```py
# Getting the config object by using the class
config = PassConfig('./conf.json')
# Initialize parser
parser = LeakParser(
    config.get_passlist(), 
    config.get_seperators(),
    config.get_ignore_list(),
    config.get_ratio(),
    config.get_any_pw()
)
# Initialize scraper
scraper = GoogleScraper(
    parser,
    config.get_cookies(),
    today,
    config.get_urls_to_gather(),
    config.get_ntfy_topic(),
    config.get_debug(), 
    'pastes/'
)
# Scan each paste page seperately for pastes
for p in config.get_paste_pages():
    scraper.scrape(parser, p)
```
The scraper takes the day to scan in this specific code. The format used is taken from the `datetime` module:
```py
from datetime import date, timedelta
today = date.today() - timedelta(days=1)
```
Note that the last line subtracts a day from the `date.today()` output. This is because the Google keyword query uses the term `after:` to get newest results. So to get results from the last 24 hours, the day before today is used. 
## TODO
- password heuristic: how big password list? determine how accurate it is in every leak I have, test until each leak is flagged
- forum gathering: replies + subsequent leak gathering
- word splitting
- aktivitätsdiagramm, stakeholder analysis, anforderungsanalyse, stakeholders, sicherheitsforscher, paste sites, software desing, rumspinnnen
- Create script that finds optimal ratio for me lmao, why did i not think of this
- max/min function, easy code
- old ignore list ["--", "#include", "public", "import", "class", "NULL", "True", "true", "//"],