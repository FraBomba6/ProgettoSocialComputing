# %%
import random
from config import *
import serializer as se

# %%
users = ["eglu81"]

for user in users:
    print(f"Processing @{user}")

    user_friends = []

    for item in tweepy.Cursor(
            api.followers,
            screen_name=user,
            skip_status=True,
            include_user_entities=False
    ).items():
        found_friend = item._json
        user_friends.append(found_friend)

    print(f"Found {len(user_friends)} followers for @{user}")
    serializer = se.Serializer('./followers')
    serializer.serialize_json(f"{user}_followers.json", user_friends)

# %%
users = ["damiano10", "eglu81", "KevinRoitero", "Miccighel_", "mizzaro"]

for user in users:
    print(f"Processing @{user}")

    user_friends = []

    for item in tweepy.Cursor(
            api.friends,
            screen_name=user,
            skip_status=True,
            include_user_entities=False
    ).items():
        found_friend = item._json
        user_friends.append(found_friend)

    print(f"@{user} follows {len(user_friends)} users")
    serializer = se.Serializer('./following')
    serializer.serialize_json(f"{user}_following.json", user_friends)

# %%
users = ["damiano10", "eglu81", "KevinRoitero", "Miccighel_", "mizzaro"]
for user in users:
    serializer = se.Serializer(f'data/{user}')
    json = serializer.read_json(f"{user}_followers.json")
    for count in range(0, 5):
        random_follower = random.choice(json)
        random_follower_screenName = random_follower["screen_name"]
        random_follower_id = random_follower["id"]
        random_follower_followers = []
        for item in tweepy.Cursor(
                api.followers,
                screen_name=random_follower_screenName,
                skip_status=True,
                include_user_entities=False
        ).items(10):
            found_follower = item._json
            random_follower_followers.append(found_follower)
        print(f"Found {len(random_follower_followers)} followers for @{random_follower_screenName}")
        serializer.serialize_json(f"random_{random_follower_id}_follower.json", random_follower_followers)

    json = serializer.read_json(f"{user}_following.json")
    for count in range(0, 5):
        random_friend = random.choice(json)
        random_friend_screenName = random_friend["screen_name"]
        random_friend_id = random_friend["id"]
        random_friend_friends = []
        for item in tweepy.Cursor(
                api.friends,
                screen_name=random_friend_screenName,
                skip_status=True,
                include_user_entities=False
        ).items(10):
            found_friend = item._json
            random_friend_friends.append(found_friend)
        print(f"@{random_friend_screenName} follows {len(random_friend_friends)} users")
        serializer.serialize_json(f"random_{random_friend_id}_following.json", random_friend_friends)

# %%
users = ["damiano10", "eglu81", "KevinRoitero", "Miccighel_", "mizzaro"]
processed_ids = []
for user in users:
    serializer = se.Serializer(f'data/{user}')
    with os.scandir(f'data/{user}') as it:
        for entry in it:
            if entry.name.endswith('.json') and not entry.name.endswith('profile.json'):
                json = serializer.read_json(f"{entry.name}")
                for account in json:
                    if account["id"] not in processed_ids:
                        processed_ids.append(account["id"])
all_users = []
range_end = len(processed_ids)//100
for i in range(0, range_end + 1):
    start_index = i*100
    end_index = start_index + 100
    if i == range_end:
        end_index = len(processed_ids)
    users_chunk = api.lookup_users(processed_ids[start_index:end_index])
    for user_obj in users_chunk:
        account_details = user_obj._json
        useful_account_details = {
            "id": account_details["id"],
            "name": account_details["name"],
            "screen_name": account_details["screen_name"],
            "description": account_details["description"],
            "followers_count": account_details["followers_count"],
            "friends_count": account_details["friends_count"],
            "profile_image_url_https": account_details["profile_image_url_https"]
        }
        all_users.append(useful_account_details)
serializer = se.Serializer(f'data')
serializer.serialize_json(f"all_users.json", all_users)

# %%