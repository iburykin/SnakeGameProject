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

# Function to store game result in MongoDB
def store_game_result(name, score, map_size):
    collection.insert_one({'name': name, 'score': score, 'map_size': map_size})

# Function to initialize the database with JSON data
def initialize_database_from_file(filename):
    if check_database_existence():
        data = read_data_from_file(filename)
        if data:  # Check if data is not empty
            collection.insert_many(data)

# Function to dump data to JSON upon application closure
def dump_data_to_file(filename):
    data = list(collection.find())
    write_data_to_file(data, filename)

# Function to initialize the database
def initialize_database():
    if not check_database_existence():
        # Create database directory if it doesn't exist
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        # Create empty data file
        with open(os.path.join(DB_DIR, DB_FILE), 'w') as file:
            json.dump([], file)
    else:
        initialize_database_from_file(os.path.join(DB_DIR, DB_FILE))


# Initialize the database upon script execution
initialize_database()
