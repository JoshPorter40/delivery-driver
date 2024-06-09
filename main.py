# Author: Joshua Porter
# Email: jpor284@wgu.edu
# Student ID: 010543847

# Hashmap was created using a video my instructor Preety Khatri sent me via her course introductory email and the video
# is available in course tips: https://www.youtube.com/watch?v=9HFbhPscPU0&ab_channel=OggiAI-ArtificialIntelligenceToday
import csv
from datetime import timedelta

class HashMap:

    def __init__(self):
        # Sets the size of the array to 64 and sets every cell equal to None to create a list with a fixed length
        self.size = 64
        self.map = [None] * self.size

    def get_hash(self, key):
        # Takes a key and calculates the index for that key and then returns the index
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def add(self, key, value):
        # Gets the index and passes in the list created from key_value
        key_hash = self.get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            # Check if index empty, and adds key_value to the map at that index
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                # Checks if key has a match and will then update that value. If there is no match, then add the value
                if pair[0] == key:
                    pair[1] = value
                    return true
                self.map[key_hash].append(key_value)
                return True

    def get(self, key):
        # For cells that are not None, loop through until the keys match and return the value. If not found, return none
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        # Locate the key, check if cell is None, if not None, find index and them remove it
        key_hash = self.get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    def print(self):
        # Prints every non None cell in array
        for item in self.map:
            if item is not None:
                print(str(item))

class Package:
    def __init__(self, packageID, address, city, state, zip, deadline, weight, reqs):
        # Creates a package object
        self.packageID = int(packageID)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = int(weight)
        self.reqs = reqs
        self.status = "At hub"
        self.loadingTime = None
        self.deliveryTime = None

    def load_package_data(filename):
        # Reads in the data from the specified csv file and calls add function to add data to packageData hashmap
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                package = Package(*row)
                package.add_package(packageData)

    def add_package(self, hashMap):
        # Adds package to packageData hashmap
        key = self.packageID
        hashMap.add(key, self)

    def update_status(self, current_time):
        # Updates the status of the package based on the current time
        if self.deliveryTime is not None and current_time >= self.deliveryTime:
            self.status = "Delivered"
        elif self.loadingTime is not None and current_time >= self.loadingTime:
            self.status = "En route"
        else:
            self.status = "At hub"

    def __str__(self):
        # Returns a string representation of the package object
        return (f"Package ID: {self.packageID}\n"
                f"Address: {self.address}\n"
                f"City: {self.city}\n"
                f"State: {self.state}\n"
                f"Zip: {self.zip}\n"
                f"Deadline: {self.deadline}\n"
                f"Weight: {self.weight}\n"
                f"Status: {self.status}\n"
                f"Loading Time: {self.loadingTime}\n"
                f"Delivery Time: {self.deliveryTime}\n")

class Truck:
    def __init__(self, startTime = None, packageID = [], mileage = 0):
        # Initialize the Truck object with optional parameters startTime, packageID list, and mileage
        self.startTime = startTime
        self.packageID = packageID
        self.mileage = mileage
        self.currentLocation = 0
        self.currentTime = startTime

def load_distance_data(distanceData, filename):
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # Convert the row to a list of floats and handles empty strings
            distance_row = []
            for value in row:
                if value:
                    distance_row.append(float(value))
                else:
                    distance_row.append(0.0)  # Treat missing values as 0.0
            distanceData.append(distance_row)
    # Makes the matrix symmetrical
    n = len(distanceData)
    for i in range(n):
        for j in range(i + 1, n):
            # Sets each pair of corresponding elements to the maximum value for symmetry
            distanceData[i][j] = distanceData[j][i] = max(distanceData[i][j], distanceData[j][i])

def load_address_data(addressData, filename):
    # Reads a CSV file containing address data and appends each address to the addressData list
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row:
                address = row[2]
                addressData.append(address)

def distance_between(address1Index, address2Index, distanceData):
    # Returns the distance between two addresses using their indices in the addressData list and the distanceData
    return distanceData[address1Index][address2Index]

def deliver_packages(truck, packageData, distanceData, addressData):
    # delivers the packages using the nearest neighbor algorithm
    # Initialize total mileage and current location and time of the truck
    total_mileage = 0
    currentLocation = truck.currentLocation
    currentTime = truck.currentTime

    # Loop until there are packages remaining to deliver
    while truck.packageID:
        # Initialize variables to find the nearest package
        min_distance = float('inf')
        nearest_package_id = None
        nearest_package = None
        nearest_address_index = None

        # Iterate through each package remaining in the truck
        # If N is the number of packages in the truck, M is the number of addresses
        # The nested loops iterate through each package in the truck and each address in the addressData list
        #  resulting in a time complexity of O(N*M)
        for package_id in truck.packageID:
            # Get package details from packageData hashmap
            package = packageData.get(package_id)
            # Find the index of the package address in the addressData list
            address_index = addressData.index(package.address)
            # Calculate the distance between the truck's current location and the package address
            distance = distance_between(currentLocation, address_index, distanceData)

            # Update minimum distance and nearest package details if a closer package is found
            if distance < min_distance:
                min_distance = distance
                nearest_package_id = package_id
                nearest_package = package
                nearest_address_index = address_index

        if nearest_package:
            # Calculate travel time to reach the nearest package
            travel_time = timedelta(hours=min_distance / 18)
            # Update current time and total mileage
            currentTime += travel_time
            total_mileage += min_distance
            # Update truck's mileage and package delivery information
            truck.mileage += min_distance
            nearest_package.deliveryTime = currentTime
            nearest_package.loadingTime = truck.startTime  # Set the loading time when the package is being delivered
            nearest_package.update_status(currentTime)
            # Remove the delivered package from the truck's package list
            truck.packageID.remove(nearest_package_id)
            # Update truck's current location to the address of the delivered package
            currentLocation = nearest_address_index

    # Update truck's current location and time and return total mileage
    truck.current_location = currentLocation
    truck.current_time = currentTime
    return total_mileage

# creates packageData hashmap, loads package data, creates distanceData & addressData list, loads distanceData & addressData
packageData = HashMap()
Package.load_package_data('packageCSV.csv')
distanceData = [] # Initialize an empty list to hold the distances
load_distance_data(distanceData, 'distanceCSV.csv')
addressData = []  # Initialize an empty list to hold the addresses
load_address_data(addressData, 'addressCSV.csv')

# Create trucks and set their start times and package IDs
truck1 = Truck(startTime=timedelta(hours=8, minutes=0), packageID=[1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40])
truck2 = Truck(startTime=timedelta(hours=9, minutes=5), packageID=[2, 3, 5, 6, 8, 18, 22, 25, 26, 28, 32, 33, 36, 38])
truck3 = Truck(startTime=timedelta(hours=10, minutes=20), packageID=[4, 7, 9, 10, 11, 12, 17, 21, 23, 24, 27, 35, 39])

# Calculates the total mileage traveled by each truck and stores it in that truck's total_mileage variable
# Rounds the total mileage for each truck to 2 decimal places
total_mileage_truck1 = deliver_packages(truck1, packageData, distanceData, addressData)
total_mileage_truck1 = round(total_mileage_truck1, 2)
total_mileage_truck2 = deliver_packages(truck2, packageData, distanceData, addressData)
total_mileage_truck2 = round(total_mileage_truck2, 2)
total_mileage_truck3 = deliver_packages(truck3, packageData, distanceData, addressData)
total_mileage_truck3 = round(total_mileage_truck3, 2)
# Calculates the total mileage traveled by all trucks combined and store it in total_mileage to 2 decimal places
total_mileage = total_mileage_truck1 + total_mileage_truck2 + total_mileage_truck3
total_mileage = round(total_mileage, 2)


class Main:
    # The Command Line Interface
    print("Western Governors University Parcel Service (WGUPS)")
    print(f"The total mileage for the route is: {total_mileage}\n")

    # User is prompted to enter 'time' if they want to check the package status by time. Otherwise, the program exits.
    text = input("To check status by time, please type 'time'. (All other entries will close the program): \n")

    def view_package_status(packageData, current_time, package_id=None):
        # View the delivery status of all packages or a single package at the specified time
        if package_id:
            package = packageData.get(package_id)
            if package:
                package.update_status(current_time)  # Update package status based on current time
                print(package)
            else:
                print(f"Package ID {package_id} not found.")
        else:
            for package_id in range(1, 41):  # Assuming package IDs are from 1 to 40
                package = packageData.get(package_id)
                if package:
                    package.update_status(current_time)  # Update package status based on current time
                    print(package)

    # Prompt the user to enter the time
    if text.lower() == "time":
        time_input = input("Enter the time (HH:MM format): \n")
        try:
            # Convert the user input into hours and minutes
            hours, minutes = map(int, time_input.split(":"))
            # Create a timedelta object representing the specified time
            current_time = timedelta(hours=hours, minutes=minutes)

            # Ask the user if they want to see a single package or all packages
            package_option = input("To check a single package, type 'single'. To check all packages, type 'all': \n")

            if package_option.lower() == "single":
                package_id_input = input("Enter the package ID: ")
                try:
                    package_id = int(package_id_input)
                    # Call the function to view the status of the specified package
                    view_package_status(packageData, current_time, package_id)
                except ValueError:
                    print("Invalid package ID. Please enter a numeric value.")
            elif package_option.lower() == "all":
                # Call the function to view the status of all packages at the specified time
                view_package_status(packageData, current_time)
            else:
                print("Invalid option. Exiting...")
        except ValueError:
            # Handle invalid time format
            print("Invalid time format. Please enter time in HH:MM format.")
    else:
        # Exit the program if the user doesn't want to check status by time
        print("Exiting...")
