import json
import requests

class NotAuthorizedException(BaseException):
    pass

class IncorrectAuthInfoException(Exception):
    pass

class RequestErroredException(Exception):
    pass

def make_url(url, params):
    url += '?'
    for k,v in params.iteritems():
        url += "%s=%s&" % (k, v)
    return url[:-1]

def parse_url(url):
    params = {}
    params_str = url.split('#')[1]
    for pair in params_str.split('&'):
        kv = pair.split('=')
        params[kv[0]] = kv[1]
    return params

def list_to_str(lst): # translates list elements into comma-separated string
    string = ''
    for item in lst:
        string += item
        string += ','
    return string[:-1] # striping last comma

class VkApi:
    __auth_vars = {
        "client_id": int(),
        "scope": str(),
        "redirect_uri": "https://oauth.vk.com/blank.html",
        "display": "popup",
        "v": "5.5",
        "response_type": "token"
    }
    __auth_url = "https://oauth.vk.com/authorize"
    __api_endpoint = "https://api.vk.com/method/%s"
    __authorized = False
    __access_token = str()

    def __init__(self, client_id=0, scope=[], access_token='', console_auth=True, keep_token=False, try_loading_token=False):
        if try_loading_token and self.__load_auth_info():
            self.__authorized = True

        if access_token:
            self.__access_token = access_token
            self.__authorized = True

        elif client_id and scope:
            self.__auth_vars["client_id"] = client_id
            self.__auth_vars["scope"] = list_to_str(scope)
            if console_auth:
                self.__console_auth()

        else:
            raise IncorrectAuthInfoException()

        if keep_token:
            self.__save_auth_info()

    def __console_auth(self):
        print "### %s ###" % self.get_auth_url()
        print "### Please, open this URL in your browser and authorize ###"
        response = parse_url(raw_input(">>> Resulting URL: "))
        self.__access_token = response["access_token"]
        self.__authorized = True

    def __save_auth_info(self):
        with open("auth.json", "w") as file:
            json.dump({"access_token": self.__access_token}, file)

    def __load_auth_info(self):
        try:
            with open("auth.json", "r") as file:
                info = json.load(file)
                self.__access_token = info["access_token"]
                return True
        except:
            return False


    def set_token(self, access_token):
        self.__access_token = access_token
        self.__authorized = True

    def get_token(self):
        return self.__access_token

    def is_authorized(self):
        return self.__authorized

    def get_auth_url(self):
        return make_url(self.__auth_url, self.__auth_vars)


    def request(self, api_method, data={}):
        if not self.__authorized:
            raise NotAuthorizedException()
        data["access_token"] = self.__access_token
        url = self.__api_endpoint % api_method
        r = requests.get(url, params=data)
        try:
            return r.json()["response"]
        except KeyError:
            raise RequestErroredException(r.json()['error']['error_msg'])