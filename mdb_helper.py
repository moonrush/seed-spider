import pymongo

class Mdb_helper:
    def __init__(self,server_name="mongodb://localhost:27017",db_name="test"):
        server = pymongo.MongoClient(server_name)
        self.db = server[db_name]

    def doc_query_count(self,condition,collection):
        col = self.db[collection]
        num = col.count_documents(condition)
        return num

    def doc_insert(self,condition,collection):
        result = False
        try:
            col = self.db[collection]
            
            col.insert_one(condition)
            result = True
        except Exception as e:
            print(str(e))
        return result