import requests
import time
import re

# OAuth token
SLACK_TOKEN = 'ENTER YOUR SLACK TOKEN HERE'

# Channel ID
CHANNEL_ID = 'C080P6M4DKL'

def get_channel_messages(channel_id, user_id):
    """Fetch messages from a specific channel and filter by user."""
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}',
        'Content-Type': 'application/json'
    }
    url = 'https://slack.com/api/conversations.history'
    params = {
        'channel': CHANNEL_ID,
        'limit': 1000
    }
    all_messages = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data.get('ok'):
            print("Failed to retrieve messages:", data.get('error'))
            break
        messages = data.get('messages', [])
        user_messages = [msg for msg in messages if msg.get('user') == user_id]
        all_messages.extend(user_messages)
        next_cursor = data.get('response_metadata', {}).get('next_cursor')
        if not next_cursor:
            break
        params['cursor'] = next_cursor
        time.sleep(1)
    return all_messages

def get_user_id_by_email(email):
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}',
        'Content-Type': 'application/json'
    }
    url = 'https://slack.com/api/users.lookupByEmail'
    params = {'email': email}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if not data.get('ok'):
        print(f"Error: {data.get('error')}")
        return None
    return data['user']['id']

def check_bot_channel_access(channel_id):
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }
    url = 'https://slack.com/api/conversations.info'
    params = {'channel': channel_id}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if not data.get('ok'):
        print(f"Error: {data.get('error')}")
        return False
    return data['channel'].get('is_member', False)

def extract_passcode(text):
    match = re.search(r"is\s'(.+?)'\.", text)
    if match:
        return match.group(1)
    else:
        return None

def get_passwords():
    # Find email of user to grab messages from
    email = 'joearrowsmith0@gmail.com'
    USER_ID = get_user_id_by_email(email)
    if USER_ID:
        print(f"User ID for {email}: {USER_ID}")
    else:
        print("User not found")
        return []
    messages = get_channel_messages(CHANNEL_ID, USER_ID)
    passwords = []
    for message in messages:
        text = message['text'] if isinstance(message['text'], str) else ' '.join(message['text'])
        password = extract_passcode(text)
        if password:
            passwords.append(password)
    passwords.reverse()
    return passwords

print(get_passwords())