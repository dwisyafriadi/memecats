import json
import requests
import time
from colorama import init, Fore, Style

def get_new_token(query_id):
    payload = {
        "initData": query_id,
        "inviteCode": "",
        "groupId": ""
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://app.memecats.xyz",
        "priority": "u=1, i",
        "referer": "https://app.memecats.xyz"
    }

    url = "https://api.memecats.xyz/auth/login"

    for attempt in range(3):
        print(f"\r{Fore.YELLOW + Style.BRIGHT}Mendapatkan token dengan query_id: {query_id}...", end="", flush=True)
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"\r{Fore.GREEN + Style.BRIGHT}Success Created Token", end="", flush=True)
            response_json = response.json()
            if response_json and 'data' in response_json:
                return response_json['data'].get('token')  # Return the token if available
            else:
                print(f"\r{Fore.RED + Style.BRIGHT}Token Not Found: {response_json}", flush=True)
                break
        else:
            print(f"\r{Fore.RED + Style.BRIGHT}Gagal mendapatkan token, percobaan {attempt + 1}: {response.json()}", flush=True)
            time.sleep(1)  # Wait before the next attempt

    print(f"\r{Fore.RED + Style.BRIGHT}Gagal mendapatkan token setelah 3 percobaan.", flush=True)
    return None

def clear_tasks(token, target):
    url = "https://api.memecats.xyz/task/list"  # Adjust if needed
    payload = {
        "target": target,
        "address": "",  # Assuming address is required as per your API example
        "_token": token
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    print(f"\r{Fore.YELLOW + Style.BRIGHT}Clearing tasks for {target}...", end="", flush=True)

    # First attempt to clear tasks
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        
        # Log the full response for debugging
        print(f"\nResponse: {json.dumps(response_json, indent=2)}")

        if response_json['code'] == 302:
            print(f"\r{Fore.YELLOW + Style.BRIGHT}Waiting for tasks to complete...", end="", flush=True)
            # Polling until the task is complete
            while True:
                time.sleep(5)  # Wait for some time before checking again
                response = requests.post(url, headers=headers, json=payload)
                response_json = response.json()
                
                # Log the full response for debugging
                print(f"\nResponse: {json.dumps(response_json, indent=2)}")

                if response_json['code'] == 0:
                    print(f"\r{Fore.GREEN + Style.BRIGHT}Tasks cleared successfully", end="", flush=True)
                    # Check if 'data' is a dict before accessing
                    if isinstance(response_json['data'], dict):
                        print(f"\nUsername: {response_json['data']['username']}, Coins: {response_json['data']['coin']}")
                    else:
                        print(f"\nData is not in the expected format: {response_json['data']}")
                    return response_json
                elif response_json['code'] != 302:
                    print(f"\r{Fore.RED + Style.BRIGHT}Failed to clear tasks: {response_json}", flush=True)
                    return None
        elif response_json['code'] == 0:
            print(f"\r{Fore.GREEN + Style.BRIGHT}Tasks cleared successfully", end="", flush=True)
            # Check if 'data' is a dict before accessing
            if isinstance(response_json['data'], dict):
                print(f"\nUsername: {response_json['data']['username']}, Coins: {response_json['data']['coin']}")
            else:
                print(f"\nData is not in the expected format: {response_json['data']}")
            return response_json
    else:
        print(f"\r{Fore.RED + Style.BRIGHT}Failed to clear tasks: {response.json()}", flush=True)
        return None



# Main function to process all queries
def process_queries():
    with open('query.txt', 'r') as file:
        query_ids = file.readlines()
    query_ids = [id.strip() for id in query_ids if id.strip()]

    for query_id in query_ids:
        token = get_new_token(query_id)
        if token:
            print(f"\nGet Token: {token}")
            clear_tasks(token, "twitter")
            clear_tasks(token, "channel")
        else:
            print(f"\n{Fore.RED + Style.BRIGHT}Tidak ada token yang diperoleh untuk query: {query_id}")

    print(f"\n{Fore.GREEN + Style.BRIGHT}Proses selesai untuk semua query.")

# Call the main function to start processing
process_queries()