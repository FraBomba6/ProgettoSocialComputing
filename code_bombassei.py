# %%
from config import *
import ProgettoSocialComputing.serializer as se

# %%
users = ["eglu81"]

for user in users:
    print(f"Processing @{user}")

    user_followers = []

    for item in tweepy.Cursor(
            api.followers,
            screen_name=user,
            skip_status=True,
            include_user_entities=False
    ).items():
        found_follower = item._json

        if found_follower not in user_followers:
            user_followers.append(found_follower)

    print(f"Found {len(user_followers)} followers for @{user}")
    serializer = se.Serializer('followers')
    serializer.serialize_json(f"{user}_followers.json", user_followers)
