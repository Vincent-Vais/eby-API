import json
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


def getProxy():
    try:
        # proxy addresses are stored in json file {proxies: [arr of prox]}
        with open("proxies.json") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error, {e}")
    # first run, file has not been created yet
    except FileNotFoundError:
        data = loadProxies()
    proxies = data["proxies"]
    # each time the scrapper is run proxy is popped from arr so gotta check
    if len(proxies) == 0:
        proxies = loadProxies()
    # we do not want to repaeat proxy addresses
    proxy = proxies.pop(0)
    # store updated array back in file
    updateProxiesJSON(proxies)
    return proxy


def loadProxies():
    req_proxy = RequestProxy()
    proxies = req_proxy.get_proxy_list()  # this will create proxy list
    data = {"proxies": [proxy.get_address() for proxy in proxies]}
    return data


def updateProxiesJSON(p):
    with open("proxies.json", "w") as f:
        json.dump({"proxies": p}, f)
