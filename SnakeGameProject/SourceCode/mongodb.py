import json
import os
from pymongo import MongoClient

DB_DIR = 'db'
DB_FILE = 'data.json'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # MongoDB localhost connection
db = client['snake_game']
collection = db['game_sessions']

# Function to check if the database location and file exist
def check_database_existence():
    if os.path.exists(DB_DIR) and os.path.isfile(os.path.join(DB_DIR, DB_FILE)):
        # Check if file is not empty
        if os.path.getsize(os.path.join(DB_DIR, DB_FILE)) > 0:
            return True
    return False

# Function to read data from JSON file
def read_data_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to write data to JSON file
def write_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

# Function to store game result in JSON file
def store_game_result(name, score, map_size):
    # Load existing data from JSON file
    data = read_data_from_file(os.path.join(DB_DIR, DB_FILE))
    # Append new game result to data
    data.append({'name': name, 'score': score, 'map_size': map_size})
    # Write updated data back to JSON file
    write_data_to_file(data, os.path.join(DB_DIR, DB_FILE))

# Function to store game result in MongoDB
def store_game_result_to_mongodb(name, score, map_size):
    collection.insert_one({'name': name, 'score': score, 'map_size': map_size})

# Function to initialize the database
def initialize_database():
    if not check_database_existence():
        # Create database directory if it doesn't exist
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        # Create empty data file
        with open(os.path.join(DB_DIR, DB_FILE), 'w') as file:
            json.dump([], file)

# Initialize the database upon script execution
initialize_database()

# Example usage:
# store_game_result("Player1", 100, (10, 10))  # Add data to JSON file
# store_game_result_to_mongodb("Player1", 100, (10, 10))  # Add data to MongoDB
