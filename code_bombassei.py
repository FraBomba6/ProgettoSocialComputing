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
users = ["mizzaro", "damiano10", "Miccighel_", "eglu81", "KevinRoitero"]
for user in users:
    serializer = se.Serializer(f'data/{user}')
    json = serializer.read_json(f"{user}_followers.json")
    for count in range(0, 5):
        random_follower = random.choice(json)["screen_name"]
        random_follower_followers = []
        for item in tweepy.Cursor(
                api.followers,
                screen_name=random_follower,
                skip_status=True,
                include_user_entities=False
        ).items(10):
            found_follower = item._json
            random_follower_followers.append(found_follower)
        print(f"Found {len(random_follower_followers)} followers for @{random_follower}")
        serializer.serialize_json(f"random_{random_follower}_follower.json", random_follower_followers)

    json = serializer.read_json(f"{user}_following.json")
    for count in range(0, 5):
        random_friend = random.choice(json)["screen_name"]
        random_friend_friends = []
        for item in tweepy.Cursor(
                api.friends,
                screen_name=random_friend,
                skip_status=True,
                include_user_entities=False
        ).items(10):
            found_friend = item._json
            random_friend_friends.append(found_friend)
        print(f"@{random_friend} follows {len(random_friend_friends)} users")
        serializer.serialize_json(f"random_{random_friend}_following.json", random_friend_friends)
