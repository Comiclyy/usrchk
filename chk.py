import random
import requests
import threading
import time
import json

# Function to check if the webpage has content
def check_webpage(url):
    response = requests.get(url)
    if "Couldn't find any profile with name" in response.text:
        return False
    return True

# Function to check if a username contains special characters and has at least 3 characters
def is_valid_username(username):
    # Check if the username has only letters, digits, underscores, and has at least 3 characters
    return len(username) >= 3 and (username.isalnum() or '_' in username)

# Read wordlist file path from config.json
with open('chk.json', 'r') as config_file:
    config = json.load(config_file)
    wordlist_path = config.get('wordlist', 'wordlists/wordlist-1k.txt')

# Read words from the specified wordlist file
with open(wordlist_path, 'r') as wordlist_file:
    wordlist = wordlist_file.read().splitlines()

    if len(wordlist) > 10000:
        print("WARNING: LARGE FILE, MAY TAKE LONGER THAN EXPECTED (Over 10k)")

    # Initialize lists to store available and blocked usernames
    available_usernames = []
    blocked_usernames = []

    # Function to check a single word
    def check_word(random_word):
        # Construct the URL
        url_to_check = f"https://api.mojang.com/users/profiles/minecraft/{random_word}"
        
        # Check if the webpage has content
        if not check_webpage(url_to_check):
            # Check if the username is valid
            if is_valid_username(random_word):
                available_usernames.append(random_word)
            else:
                blocked_usernames.append(random_word)

    # Measure time to complete
    start_time = time.time()

    # Use threading to check words concurrently
    threads = []
    for random_word in wordlist:
        thread = threading.Thread(target=check_word, args=(random_word,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time

    # Print available usernames
    print("Available usernames:")
    for word in available_usernames:
        print(word)

    print(f"Time taken: {total_time} seconds")
