# %%
import random

import serializer as se
from config import *

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
users = ["eglu81"]

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
users = ["mizzaro"]
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
users = ["mizzaro", "damiano10", "Micchighel_", "eglu81", "KevinRoitero"]
error_count = 0
duplicate_count = 0
all_users = []
processed_ids = []
print(f"Start at {datetime.now()}")
for user in users:
    print(
        f'\n\n*************************************\nProcessing {user} and his friends\n*************************************')
    serializer = se.Serializer(f'data/{user}')
    with os.scandir(f'data/{user}') as it:
        for entry in it:
            if entry.name.endswith('.json') and not entry.name.endswith('profile.json'):
                print('\n\n******************')
                json = serializer.read_json(f"{entry.name}")
                print(f'\nProcessing {entry.name}, containing {len(json)} users\n******************\n\n')
                for account in json:
                    if account["id"] not in processed_ids:
                        try:
                            print(f'Processing {account["id"]}, user #{len(all_users) + 1}')
                            account_details = api.get_user(account["id"])._json
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
                            processed_ids.append(account_details["id"])
                        except tweepy.TweepError:
                            error_count += 1
                            print("Skipped user because of error")
                    else:
                        duplicate_count += 1
all_users_serializer = se.Serializer('data')
print('\n\n*************************************\n')
all_users_serializer.serialize_json(f"all_users.json", all_users)
print('\n*************************************\n\n')
print(f'Found {error_count} errors and {duplicate_count} duplicates')


# %%

def get_friendship(sourceid, targetid, api):
    kind = ""

    friendship = api.show_friendship(source_id=sourceid, target_id=targetid)

    if not friendship[0].following and not friendship[0].followed_by:
        kind = "none"
    elif not friendship[0].following and friendship[0].followed_by:
        kind = "r_l"
    elif friendship[0].following and not friendship[0].followed_by:
        kind = "l_r"
    else:
        kind = "bi"

    return {
        "source_id": sourceid,
        "target_id": targetid,
        "friendship": kind
    }


accounts = ["mizzaro"]
serializer = se.Serializer('data')
users = serializer.read_json("all_users.json")
edges = []
for account in accounts:
    serializer = se.Serializer(f'data/{account}')
    account_json = serializer.read_json(f"{account}_profile.json")
    account_id = account_json["id"]
    for user in users:
        if user["id"] is not account_id:
            edges.append(get_friendship(account_id, user["id"], api))
            pp.pprint(f"Added friendship between {account} and {user['screen_name']}")
    serializer.serialize_json(f'{account}_friendships.json', edges)

# %%
accounts = ["mizzaro", "damiano10", "eglu81", "KevinRoitero", "Miccighel_"]
json = []
for account in accounts:
    serializer = se.Serializer(f'data/{account}')
    account_friendships = serializer.read_json(f"{account}_friendships.json")
    for friendship in account_friendships:
        json.append(friendship)
serializer = se.Serializer('data')
serializer.serialize_json("all_friendships.json", json)

serializer = se.Serializer('data')
print(len(serializer.read_json("all_users.json")))
