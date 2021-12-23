from .utils import return_hash
import requests
import json
import os

class Collection(object):
  """
  Induvisual json dump. Inner level after Bucket.\n
  :param name: str - name of collection\n
  :param parent_bucket: Bucket - parent bucket of this collection\n
  :param id: str - id of collection\n
  :id: str - id of collection\n
  :url: str - url of collection\n
  """
  def __init__(self, parent_bucket, name, id) -> None:
    """
    Constructs a Collection object\n
    :param name: str - name of collection\n
    :param parent_bucket: Bucket - parent bucket of this collection\n
    :param id: str - id of collection
    """
    self.name = name
    self.parent_bucket = parent_bucket
    self.bucket_id = parent_bucket.id
    self.id = id
    
    self.url = f'https://jsonbase.com/{self.bucket_id}/{self.id}'
    
  def __repr__(self) -> str:
    """
    Prints a representation of the Collection object
    """
    return f'<Collection {self.name} id:{self.id}>'
  
  def get(self) -> dict | list:
    """
    Gets the collection data from jsonbase\n
    
    Returns\n
    The data that was retrieved from the collection
    """
    url = f'https://jsonbase.com/{self.bucket_id}/{self.id}'
    response = requests.get(url)
    return response.json()
  
  def put(self, data: list | dict) -> dict | list:
    """
    Puts the supplied data into the collection in jsonbase\n
    :param data: dict | list - data to put into the collection\n
    
    Returns\n
    The data that was put into the collection
    """
    url = f'https://jsonbase.com/{self.bucket_id}/{self.id}'
    response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
    return response.json()
  
  def append(self, data: list | dict) -> dict | list:
    """
    Note: Only works if this collection is a list. This is not the same as put. This will append the data to the collection.\n
    Appends the supplied data to the collection in jsonbase\n
    :param data: dict | list - data to append to the collection\n
    
    Returns\n
    The data that was appended to the collection
    """
    url = f'https://jsonbase.com/{self.bucket_id}/{self.id}'
    _data = self.get()
    _data.append(data)
    response = requests.post(url, json=_data, headers={'Content-Type': 'application/json'})
    return _data
  
  def find(self, filter: dict) -> list | dict:
    """
    Note: Only works if this collection is a list.\n
    Finds documents in the collection that match the given filter\n
    :param filter: dict - key values to match\n
    
    Returns\n
    documents that match the given filter
    """
    _data = self.get()
    _filtered = []
    for doc in _data:
      add = True
      for k, v in filter.items():
        if doc.get(k) != v:
          add = False
      if add:
        _filtered.append(doc)
    return _filtered
    
class Bucket(object):
  """
  Outer Level of the json dump.\n
  :param CLIENT_SECRET: str - the client secret, this is used as the salt for hashing url endpoints\n
  :param bucket_name: str - the name of the bucket\n
  :param config_file: str - the path to the config file, defaults to ./db.config.json\n
  :id: str - id of bucket\n
  :config: dict - the loaded config file\n
  :collections: dict[str, Collection] - the collections in the bucket\n
  :url: str - url of bucket\n
  """
  def __init__(self, CLIENT_SECRET, bucket_name, config_file='db.config.json') -> None:
    """
    Constructs a Bucket object\n
    :param CLIENT_SECRET: str - the client secret, this is used as the salt for hashing url endpoints\n
    :param bucket_name: str - the name of the bucket\n
    :param config_file: str - the path to the config file, defaults to ./db.config.json\n
    """
    self.SALT = CLIENT_SECRET
    self.name = bucket_name
    self.id = return_hash(self.name, self.SALT)
    
    self._config_file_path = config_file
    self.config = self.setup_config(config_file)
    
    self.collections = self._load_collections()
    self.url = 'https://jsonbase.com/' + self.id

  def setup_config(self, config_file='db.config.json') -> dict:
    """
    Sets up the config file for the bucket\n
    :param config_file: str - the path to the config file, defaults to ./db.config.json\n
    """
    if os.path.exists(config_file):
      print('Config file already exists')
      return json.load(open(config_file))
    config = {self.name: {'id': self.id, 'collections': []}}
    json.dump(config, open(config_file, 'w'), indent=2)
    return config
    
  def get(self, collection_name: str) -> dict | list:
    """
    Gets the collection data from jsonbase\n
    Alternative to Collection.get()\n
    Returns\n
    Data that was retrieved from the collection
    """
    collection = self.collections.get(collection_name)
    return collection.get()

  def put(self, collection_name: str, data: list | dict) -> dict | list:
    """
    Put the supplied data into the collection in jsonbase\n
    Alternative to Collection.put()\n
    Returns\n
    Data that was put into the collection
    """
    collection = self.collections.get(collection_name)
    return collection.put(data)
  
  def append(self, collection_name: str, data: list | dict) -> dict | list:
    """
    Note: Only works if the collection is a list\n
    Appends the supplied data to the collection\n
    :param collection_name: str - the name of the collection\n
    :param data: dict | list - the data to append to the collection\n
    Returns\n
    The data that was appended to the collection
    """
    collection = self.collections.get(collection_name)
    return collection.append(data)
  
  def find(self, collection_name: str, filter: dict) -> list | dict:
    """
    Note: Only works if this collection is a list.\n
    Finds documents in the collection that match the given filter\n
    :param collection_name: str - the name of the collection\n
    :param filter: dict - key values to match\n
    Returns\n
    documents that match the given filter
    """
    collection = self.collections.get(collection_name)
    return collection.find(filter)
  
  def create_collection(self, collection_name: str) -> Collection:
    """
    Creates a collection in the bucket\n
    :param collection_name: str - the name of the collection\n
    Returns\n
    Collection that was created
    """
    collection_id = return_hash(collection_name, self.SALT)
    collection = Collection(self, collection_name, collection_id)
    self._add_collection_to_config(collection)
    return collection
  
  def get_collection(self, collection_name: str) -> Collection:
    """
    Gets the collection from the bucket\n
    Returns\n
    Collection matching the name
    """
    return self.collections.get(collection_name)
  
  def print_map(self) -> None:
    """
    Prints a depiction of the bucket and its enclosed collections\n
    """
    print(f'{self.name}: {self.id[:5:]}...{self.id[-5::]}\n' + '\n'.join(f'    ◟{collection.name}: {collection.id[:5:]}...{collection.id[-5::]}' for collection in self.collections.values()))
    
  def _load_collections(self) -> dict[str, Collection]:
    """
    Internal Method, Loads the collections from the loaded config\n
    Returns\n
    Collections dict
    """
    return {
      collection['name']: Collection(self, collection['name'], collection['id']) 
      for collection in self.config[self.name]['collections']
    }
    
  def _add_collection_to_config(self, collection: Collection) -> None:
    """
    Internal method, adds the collection to the config file and updates loaded config\n
    :param collection: Collection - the collection to add to the config\n
    """
    collection_data = {'name': collection.name, 'id': collection.id}
    
    self.config[self.name]['collections'].append(collection_data)
    self.collections = self._load_collections()
    
    config = json.load(open(self._config_file_path))
    if collection_data not in config[self.name]['collections']: 
      config[self.name]['collections'].append(collection_data)
    json.dump(config, open(self._config_file_path, 'w'), indent=2)
    
  def __repr__(self):
    """
    Prints a representation of the Bucket object
    """
    return f'<Bucket {self.name} id:{self.id}>'