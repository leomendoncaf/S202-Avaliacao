import pymongo


class Database:
    def __init__(self, database, collection, dataset):
        connectionString = "mongodb+srv://root:root@cluster0.yzftv.mongodb.net/test"
        self.clusterConnection = pymongo.MongoClient(
            connectionString,
            tlsAllowInvalidCertificates=True # CASO OCORRA O ERRO [SSL_INVALID_CERTIFICATE]
        )
        self.db = self.clusterConnection[database]
        self.collection = self.db[collection]
        self.dataset = dataset

    def resetDatabase(self):
        self.db.drop_collection(self.collection)
        self.collection.insert_many(self.dataset)