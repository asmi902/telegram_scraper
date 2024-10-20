import csv
import asyncio
import nest_asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# Apply asyncio to work in Jupyter Notebook or other interactive environments
nest_asyncio.apply()

api_id = '28214123'
api_hash = '0d8e7da7edbd6d72a622ea60dfe3ac18'
phone = '+918828000465'

client = TelegramClient('MyApp12345new1234567ab', api_id, api_hash)

async def scrape_members():
    """Scrape members from the chosen Telegram group."""
    print('Connecting to Telegram...')
    await client.start(phone)

    print('Fetching group list...')
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))

    groups = [chat for chat in result.chats if getattr(chat, 'megagroup', False)]

    print('Choose a group to scrape members:')
    for i, group in enumerate(groups):
        print(f'[{i}] - {group.title}')

    g_index = int(input("Enter a number to choose the group: "))
    target_group = groups[g_index]

    print(f'Scraping members from {target_group.title}...')
    all_participants = await client.get_participants(target_group, aggressive=True)

    print('Saving members to CSV...')
    with open("members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'phone', 'group', 'group id'])
        for user in all_participants:
            username = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = (first_name + ' ' + last_name).strip()
            phone = user.phone if user.phone else ""
            writer.writerow([username, user.id, user.access_hash, name, phone, target_group.title, target_group.id])

    print('Members scraped successfully.')


async def fetch_messages(group_name):
    """Fetch messages from the specified Telegram group."""
    print(f'Fetching messages from {group_name}...')

    with open('telegram_messages.csv', 'w', newline='') as csvfile:
        fieldnames = ['sender_id', 'message_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        async for message in client.iter_messages(group_name, limit=100):
            writer.writerow({
                'sender_id': message.sender_id,
                'message_text': message.text or ''
            })
            print(f"Message from {message.sender_id}: {message.text}")

    print('Messages fetched and saved successfully.')


async def main():
    # Connect and scrape members
    await scrape_members()

    # Fetch messages from a specific group
    group_name = 'https://t.me/maalbechenge'  # Replace with the actual public group name or ID
    await fetch_messages(group_name)

    await client.disconnect()  # Ensure the client disconnects properly


# Run the program
asyncio.run(main())
