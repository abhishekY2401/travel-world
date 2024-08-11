from app.database.connections.mongo import MongoDB

mongodb: MongoDB = MongoDB()


class Clients:
    mongodb = mongodb.client
