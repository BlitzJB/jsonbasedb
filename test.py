from jsonbasedb import *

"""
A bunch of simple tests to ensure the working of the library.
Not intended to be unit tests, but rather a quick way to ensure things are set.
"""

bucket = Bucket('CLIENT_SECRET', 'testing_bucket')
print(bucket)

collection1 = bucket.create_collection('testing_collection')
collection2 = bucket.create_collection('testing_collection2')
print(collection1)
print(bucket.get_collection('testing_collection'))

collection1.put({'key': 'value'})
collection2.put([{'key': 'value'}])

print(bucket.get('testing_collection'))
print(bucket.get('testing_collection2'))

print(collection1.get())
print(collection2.get())

bucket.print_map()
print(bucket.config)

print(bucket.url)
print(collection1.url)
