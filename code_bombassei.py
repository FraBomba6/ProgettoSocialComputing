# %%
from config import *
import ProgettoSocialComputing.serializer as se

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
    serializer = se.Serializer('followers')
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
    serializer = se.Serializer('following')
    serializer.serialize_json(f"{user}_following.json", user_friends)
