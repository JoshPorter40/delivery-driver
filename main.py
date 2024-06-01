# Hashmap was created using a video my instructor Preety Khatri sent me via her course introductory email and the video
# is available in course tips: https://www.youtube.com/watch?v=9HFbhPscPU0&ab_channel=OggiAI-ArtificialIntelligenceToday
import csv

class HashMap:

    def __init__(self):
        # sets the size of the array to 64 and sets every cell equal to None to create a list with a fixed length
        self.size = 64
        self.map = [None] * self.size

    def _get_hash(self, key):
        # takes a key and calculates the index for that key and then returns the index
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def add(self, key, value):
        # gets the index and passes in the list created from key_value
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            # check if index empty, and adds key_value to the map at that index
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                # checks if key has a match and will then update that value. If there is no match, then add the value
                if pair[0] == key:
                    pair[1] = value
                    return true
                self.map[key_hash].append(key_value)
                return True

    def get(self, key):
        # for cells that are not None, loop through until the keys match and return the value. If not found, return none
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        # locate the key, check if cell is None, if not None, find index and them remove it
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    def print(self):
        # prints every non None cell in array
        for item in self.map:
            if item is not None:
                print(str(item))

class Package:
    def __init__(self, packageID, address, city, state, zip, deadline, weight, reqs):
        #creates a package object
        self.packageID = int(packageID)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = int(weight)
        self.reqs = reqs

    def loadPackageData(filename):
        # reads in the data from the specified csv file and calls add function to add data to packageData hashmap
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                package = Package(*row)
                package.add_package(packageData)

    def add_package(self, hashMap):
        # adds package to packageData hashmap
        key = self.packageID
        hashMap.add(key, self)

class Truck:
    def __init__(self, startTime, packageID, mileage):
        self.startTime = startTime
        self.packageID = packageID
        self.mileage = mileage

packageData = HashMap()
Package.loadPackageData('packageCSV.csv')

for i in range(1,41):
    package = packageData.get(i)
    if package:
        print("Package Details:")
        print("Package ID:", package.packageID)
        print("Address:", package.address)
        print("City:", package.city)
        print("Weight:", package.weight, "\n")




