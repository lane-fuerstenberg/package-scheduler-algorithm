
class HashTable:
    def __init__(self):
        self.capacity = 16
        self.load_factor = .75
        self.size = 0
        self.hash_table = self.create_buckets()
        self.keys = []

    def create_buckets(self):
        return [[] for _ in range(self.capacity)]

    def put(self, key, value):
        self.keys.append(key)
        hashed_key = self.hash_key(key)
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            bucket_key, bucket_value = record
            if bucket_key == key:
                found_key = True
                break

        if found_key:
            bucket[index] = (key, value)
        else:
            bucket.append((key, value))

        self.size += 1
        if self.size >= self.capacity * self.load_factor:
            self.resize()

    def get(self, key):
        hashed_key = self.hash_key(key)

        bucket = self.hash_table[hashed_key]
        found_key = False
        for index, record in enumerate(bucket):
            bucket_key, bucket_value = record

            if bucket_key == key:
                found_key = True
                break

        if found_key:
            return bucket_value
        else:
            return "No record found"

    def remove(self, key):
        hashed_key = self.hash_key(key)
        self.keys.remove(key)

        bucket = self.hash_table[hashed_key]
        found_key = False
        for index, record in enumerate(bucket):
            bucket_key, bucket_value = record

            if bucket_key == key:
                found_key = True
                break

        if found_key:
            bucket.pop(index)

    def resize(self):
        self.capacity *= 2
        self.size = 0
        self.keys.clear()

        old_hash_table = self.hash_table
        self.hash_table = self.create_buckets()

        for i, bucket in enumerate(old_hash_table):
            for j, record in enumerate(bucket):
                bucket_key, bucket_value = record
                self.put(bucket_key, bucket_value)

    def hash_key(self, key):
        return (11 + hash(key) * 3 ^ 2) % self.capacity

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index >= len(self.keys):
            raise StopIteration

        return self.get(self.keys[self.current_index])

    # def __str__(self):
    #     output = ""
    #     for bucket_list in enumerate(self.hash_table):
    #         for
    #         output += bucket_list + "\r\n\r\n"
    #     #return "".join(str(item) for item in self.hash_table)
