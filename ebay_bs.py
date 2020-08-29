from proxy import getProxy
from bs4 import BeautifulSoup as bs
import requests
import re

import lxml
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# formatter
formatter = logging.Formatter(
    "%(levelname)s - %(asctime)-s - %(filename)s - %(lineno)d --> %(message)s"
)


# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)

# file handler
fh = logging.FileHandler("logs.log", "w")
fh.setLevel(level=logging.DEBUG)
fh.setFormatter(formatter)

# file handler for HTML pages
fhHTML = logging.FileHandler("pages.html", "w")
fhHTML.setLevel(level=logging.CRITICAL)
fhHTML.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fh)
logger.addHandler(fhHTML)

logger.disabled = True


def setup():
    logger.info("Entered Setup")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    }
    logger.debug(f"Created headers: {headers}")
    PROXY = getProxy()
    logger.debug(f"Created proxy: {PROXY}")
    proxies = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }
    logger.info(f"Setup is done: {[headers, proxies]}")
    return [headers, proxies]


def scrape(word, page):
    logger.info("Entered Scrape")
    logger.debug(f"Param passed: {word}, {page}")

    logger.debug("Setting up headers and proxies")
    [headers, proxies] = setup()
    logger.debug("Setup is done")
    logger.debug(f"Headers : {headers}")
    logger.debug(f"Proxies : {proxies}")

    key = word.replace(" ", "+")
    logger.debug(f"Created a keyword from param: {key}")

    url = f"https://www.ebay.com/sch/i.html?_nkw={key}&_pgn={page}"
    logger.debug(f"Url for request: {url}")

    logger.info("Making a request")
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.ok:
        logger.info("Respnose - Ok")
        # time.sleep(10)
        logger.debug("Parssing HTML")
        page = bs(response.text, "lxml")
        logger.info("HTML parssed")
        logger.critical(f"{url}:{page.prettify()}")

        logger.debug("Looking for item divs : <div class='a-section a-spacing-medium'>")
        ul = page.find("ul", "srp-results srp-list clearfix")
        lis = ul.find_all("li", "s-item")
        logger.debug(f"Lis: \n{lis}")
        results = []
        for li in lis:
            item = {}
            imgDiv = li.find("img", "s-item__image-img")
            span = li.find("span", "s-item__price")
            detailsDivs = li.find_all("div", "s-item__detail s-item__detail--primary")
            if imgDiv and span and detailsDivs:
                logger.debug("Elements found. Parsing text")
                imgUrl = imgDiv.attrs["src"]
                title = imgDiv.attrs["alt"]
                price = span.get_text()
                details = [div.find("span").get_text() for div in detailsDivs]

                item["img"] = imgUrl
                item["title"] = title
                item["price"] = price
                item["details"] = details

                logger.debug(f"\nITEM CREATED: \n{item}\n")
                results.append(item)
            else:
                logger.warning(f"Problem in : {url}")
                logger.warning(f"imDiv: {imgDiv}")
                logger.warning(f"span: {span}")
                logger.warning(f"detailsDivs: {detailsDivs}")
                logger.warning("NOT FOUND. CONTINUE SEARCH")
        return results
    else:
        logger.info("Respnose - Failed")
        logger.warning(f"Error code: {response.status_code}")
        return None


# res = scrape("phone case", 1)

# for item in res:
#     print(f"\n{item}\n")

