import json
class PassConfig:
    def __init__(self, config_path) -> None:
        self.config = {}
        with open(config_path, "r") as f:
            self.config = json.load(f)
    def get_paste_pages(self) -> None:
        return self.config["page_list"]
    def get_engines(self) -> None:
        return self.config["search_engine"]
    def get_search_terms(self) -> None:
        return self.config["search_term"]
    def get_providers(self) -> None:
        return self.config['providers']
    def get_passlist(self) -> None:
        return self.config['passlist']
    def get_cookies(self) -> None:
        return self.config['cookies']
    def get_seperators(self) -> None:
        return self.config['separators']
    def get_forums(self) -> None:
        return self.config['forums']