class BaseScraper:
    def fetch(self):
        raise NotImplementedError
    
    def parse(self, html):
        raise NotImplementedError
    
    def normalize(self, data):
        raise NotImplementedError