import json
class PassConfig:
    def __init__(self, config_path) -> None:
        self.config = {}
        # TODO: use standard values if a variable/key undefined
        with open(config_path, "r") as f:
            self.config = json.load(f)
    def get_paste_pages(self) -> list:
        return self.get_key("page_list")
    def get_engines(self) -> list:
        return self.get_key("search_engine")
    def get_search_terms(self) -> list:
        return self.get_key("search_term")
    def get_providers(self) -> list:
        return self.get_key('providers')
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
    def get_use_azure(self) -> bool:
        return self.get_key('use_azure')
    def set_use_azure(self, t) -> None:
        self.config['use_azure'] = t
    def get_key(self, key):
        try:
            value = self.config[key]
            if value:
                return value
        except KeyError:
            return ''