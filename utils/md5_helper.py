from hashlib import md5


class Md5Helper:
    def __init__(self):
        self.hl = md5()

    def encr(self, data: str):
        self.hl.update(data.encode('utf-8'))
        res = self.hl.hexdigest()
        return res
