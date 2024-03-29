from django.conf import settings
import sys
from django.db.models import Model
from django.apps import apps
import random, string, time


class MongoConnection(Model):
    collection_name = ''
    OTHER_DB = False

    def __init__(self):
        if self.OTHER_DB:
            self.collection = settings.OTHER_DB[self.collection_name]
        else:
            self.collection = settings.DB[self.collection_name]


class GMBaseModel(MongoConnection):
    collection_name = ""
    OTHER_DB = False

    def get_unique_id(self):
        cur_time_str = str(int(time.time() * 1000000.0))
        id_int = int('9'+cur_time_str[9:-5]+''.join(random.choice(string.digits) for _ in range(3))+cur_time_str[13:])
        return self.data_exist_check(id_int)

    def data_exist_check(self, id):
        if self.collection.find_one({'id':id}):
            id+=1
            return self.data_exist_check(id)
        return id

    def count(self):
        return self.collection.count()

    def find(self, match, project=None, sort=None):
        return self.collection.find(match, project, sort=sort)

    def find_one(self, match, sort=None, project=None):
        if sort:
            return self.collection.find_one(match, project, sort=sort)
        else:
            return self.collection.find_one(match, project)

    def find_one_and_update(self, match, data, sort=None, upsert=True):
        if sort:
            return self.collection.find_one_and_update(match, {"$set": data}, upsert=upsert, return_document=True, sort=sort)
        else:
            return self.collection.find_one_and_update(match, {"$set": data}, upsert=upsert, return_document=True)

    def find_one_and_update_alt(self, match, data, sort=None, upsert=True):
        if sort:
            return self.collection.find_one_and_update(match, data, upsert=upsert, return_document=True, sort=sort)
        else:
            return self.collection.find_one_and_update(match, data, upsert=upsert, return_document=True)
    
    def update_one(self, match, data):
        self.collection.update_one(match, {'$set': data})

    def update(self, match, data):
        self.collection.update_one(match, data)

    def update_alt(self, match, data, upsert=True):
        self.collection.update_one(match, data, upsert=upsert)

    def update_many(self, match, data, upsert=True):
        self.collection.update_many(match, data, upsert)

    def insert_one(self, data):
        return self.collection.insert(data)

    def insert_many(self, data):
        return self.collection.insert_many(data)

    def delete_many(self, match):
        self.collection.delete_many(match)

    def bulk_write(self, data):
        self.collection.bulk_write(data)

    def aggregateVerbose(self, query, single=False):
        result = self.collection.aggregate(query)
        if single:
            try:
                return result.next()
            except StopIteration:
                return None
        else:
            return result

    def aggregate(self, match=None, sort=None, skip=None, limit=None, project=None, with_oid=False):
        aggregate = []
        aggregate.append({'$match': match}) if match else None
        aggregate.append({'$sort': sort}) if sort else None
        if with_oid:
            aggregate.append({ '$addFields': {'oid': {'$toString': "$_id"}}})
        aggregate.append({'$project': project}) if project else aggregate.append({'$project': {'_id' : 0}})
        aggregate.append({'$skip': skip}) if skip else None
        aggregate.append({'$limit': limit}) if limit else None
        
            
        return self.collection.aggregate(aggregate)

    def aggregate_with_lookup(self, match=None, sort=None, skip=None, limit=None, project=None, lookups=[], single=False):
        aggregate = []
        aggregate.append({'$match': match}) if match else None
        aggregate.append({'$sort': sort}) if sort else None
        
        for lookup in lookups:
            # collection_object = lookup.get('collection_object')
            collection_object = apps.get_model(app_label=lookup.get("collection").split('.')[0], model_name=lookup.get("collection").split('.')[1])()
            lookup_field1 = self.collection_name+"__"+lookup.get("lookup_field1")
            pipeline_match = None
            pipeline_match_extra = None
            if lookup.get('lookup_field2'):
                pipeline_match=["$"+lookup.get("lookup_field2"), "$$"+lookup_field1]
            if lookup.get('pipeline_match'):
                pipeline_match_extra = lookup.get('pipeline_match')
            l = {
                'from': collection_object.collection_name,
                "let": {lookup_field1: {"$ifNull" : ["$"+lookup.get("lookup_field1"), None]}},
                'pipeline': collection_object.getPipeline(match=pipeline_match, match_extra=pipeline_match_extra, sort=lookup.get("sort"), project=lookup.get("project"), skip=lookup.get("skip"), limit=lookup.get("limit"), lookups=lookup.get('lookups', [])),
                'as': lookup.get("as", collection_object.collection_name)
            }
            aggregate.append({'$lookup': l}) if l else None
            if lookup.get("unwind"):
                unwind = {'path' : "$"+lookup.get("as", collection_object.collection_name)}
                if lookup.get("unwind_preserve"):
                    unwind['preserveNullAndEmptyArrays'] = True
                aggregate.append({'$unwind': unwind})
            # print("aggregate", aggregate)
        aggregate.append({'$project': project}) if project else aggregate.append({'$project': {'_id' : 0}})
        aggregate.append({'$skip': skip}) if skip else None
        aggregate.append({'$limit': limit}) if limit else None
        
        result = self.collection.aggregate(aggregate)
        if single:
            try:
                return result.next()
            except StopIteration:
                return None
        else:
            return result

    def getPipeline(self, match=None, match_extra=None, sort=None, skip=None, limit=None, project=None, lookups=[]):
        pipeline = []
        if match:
            if match_extra:
                match_list = [{"$eq": match}]
                match_list.extend([{"$eq": match_extra}])
                pipeline.append({'$match': {"$expr": {"$and": match_list}}}) if match else None
            else:
                pipeline.append({'$match': {"$expr": {"$eq": match}}}) if match else None
        elif match_extra:
            pipeline.append({'$match': {"$expr": {"$eq": match_extra}}}) if match else None            
        # pipeline.append({'$match': {"$expr": {"$eq": match}}}) if match else None
        pipeline.append({'$sort': sort}) if sort else None
        
        for lookup in lookups:
            # collection_object = lookup.get('collection_object')
            collection_object = apps.get_model(app_label=lookup.get("collection").split('.')[0], model_name=lookup.get("collection").split('.')[1])()
            lookup_field1 = self.collection_name+"__"+lookup.get("lookup_field1")
            pipeline_match = None
            pipeline_match_extra = None
            if lookup.get('lookup_field2'):
                pipeline_match=["$"+lookup.get("lookup_field2"), "$$"+lookup_field1]
            if lookup.get('pipeline_match'):
                pipeline_match_extra = lookup.get('pipeline_match')
            l = {
                'from': collection_object.collection_name,
                "let": {lookup_field1: {"$ifNull" : ["$"+lookup.get("lookup_field1"), None]}},
                'pipeline': collection_object.getPipeline(match=pipeline_match, match_extra=pipeline_match_extra, sort=lookup.get("sort"), project=lookup.get("project"), skip=lookup.get("skip"), limit=lookup.get("limit"), lookups=lookup.get('lookups', [])),
                'as': lookup.get("as", collection_object.collection_name)
            }
            pipeline.append({'$lookup': l}) if l else None
            if lookup.get("unwind"):
                unwind = {'path' : "$"+lookup.get("as", collection_object.collection_name)}
                if lookup.get("unwind_preserve"):
                    unwind['preserveNullAndEmptyArrays'] = True
                pipeline.append({'$unwind': unwind})
            print("pipeline", l)

        pipeline.append({'$project': project}) if project else pipeline.append({'$project': {'_id' : 0}})
        pipeline.append({'$skip': skip}) if skip else None
        pipeline.append({'$limit': limit}) if limit else None

        
        return pipeline