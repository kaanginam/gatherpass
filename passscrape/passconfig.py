import json
"""
Helper class to deal with config as well as deal with
undefined values
"""
class PassConfig:
    def __init__(self, config_path) -> None:
        self.config = {}
        with open(config_path, "r") as f:
            self.config = json.load(f)
    def get_paste_pages(self) -> list:
        return self.get_key("page_list")
    def get_passlist(self) -> str:
        return self.get_key('passlist')
    def get_cookies(self) -> dict:
        return self.get_key('cookies')
    def get_seperators(self) -> list:
        return self.get_key('separators')
    def get_forums(self) -> list:
        return self.get_key('forums')
    def get_ratio(self) -> float:
        return self.get_key('ratio')
    def get_urls_to_gather(self) -> list:
        return self.get_key('urls_to_gather')
    def get_user_data_dir(self) -> str:
        return self.get_key('user_data')
    def get_chrome_binary(self) -> str:
        return self.get_key('chrome_binary')
    def get_ntfy_topic(self) -> str:
        return self.get_key('ntfy_topic')
    def get_db_conn_str(self) -> str:
        return self.get_key('db_conn_str')
    def get_ignore_list(self) -> list:
        return self.get_key('ignore_list')
    def get_debug(self) -> bool:
        return self.get_key('DEBUG')
    def get_any_pw(self) -> bool:
        return self.get_key('any_pw')
    def get_key(self, key):
        try:
            value = self.config[key]
            if value:
                return value
        except KeyError:
            return ''