from abc import abstractmethod


class Database:
    client = None

    @abstractmethod
    def init_connection(): ...

    @property
    def client(self):
        return self.client

    def check_health(self):
        if self.client is not None:
            raise Exception("Database not connected..")
        return True
