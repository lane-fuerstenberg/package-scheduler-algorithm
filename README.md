# package-scheduler-algorithm
A school project algorithm designed to receive packages and calculate best path for trucks based on given requirements and utilizing a custom made data structure. In my case I choose a hash table as my data structure.

Details about my hash table:
I modelled my hash table similar to Java's implementation of theirs. The size of the table will be 16 at base, using a single size 16 array at the start. From here each index in this size 16 array will have a “bucket” of values it stores using another array, so that any hash collisions can also be stored into this bucket. When a key attempts to store into a bucket it will store both the key and the value so that in the situation of a hash collision, we can iterate through the bucket and find the matching key. With this system we can store a bunch of similar keys into a singular bucket and not be affected by the hash collisions. Having a high number of hash collisions is bad though so ideally, we attempt to avoid it, the way I decided to avoid hash collisions is to create a smearing function of: (11 + key_hash ^ 2) modulus of hash maps length. This achieved a decent spread of usage in the bucket and worked well enough for my purposes.  Another way we avoid collisions is by utilizing a load factor, in my case I used a load factor of .75, so when the capacity reached around 75% full, we resize the hash_map up a value of base 2 (so 16 > 32 > 64) and then we rehash all the keys already present in the hash_map. This will prevent situations where we have lots of hash collisions because the map is too small, and by rehashing all the keys it makes sure that all the new space being added will be utilized.

Details about my algorithm:
The requirements for this algorithm state that we have 2 drivers with 3 vehicles that have a set of  40 packages they need to deliver. The mileage cannot go above 140 across all vehicles and packages have a number of requirements they need to fulfill on an indidual basis.
Some packages need to be delivered before a set time or have requirements that they must be delivered with other packages. The actual algorithm I implemented was a nearest neighbor insertion algorithm. The idea is to iterate through each package to find the best placement. When iterating through package we will iterate through each truck and then iterate through each insert point in the truck's packages, and at this point we calculate the total added distance for the given insert, on the given truck, with the given package. At the end of each package iteration, we place it into a truck based on the best-found truck and index insertion point combination.

Some sample of what the application looks like on run, it will immediately calculate the given path and then the commands given are just to view details on the path given:

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/12528245-9060-4937-afbb-20eeb8f9fa09)

Using command 1)

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/72415c9f-5c23-43ec-8459-c88d541c5f5f)

Given a time of 8:30)

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/0871a8af-b59c-4b54-bd55-582f025298e6)

Command 2)

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/9f76c65e-3369-4ef9-bcb5-47db8dcde6a5)

Command 3 for each trucks output)

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/07b28b41-c086-4569-ad28-6c2a64681922)

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/4e29161f-0c7f-47cf-8fd8-79b9fe400182)

![image](https://github.com/lane-fuerstenberg/package-scheduler-algorithm/assets/45408948/494f160f-04cd-4cb7-8aea-bf5964182a9c)


