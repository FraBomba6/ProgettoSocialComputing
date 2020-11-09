# %%
from config import *

# %%
users = ["mizzaro", "damiano10", "Miccighe", "eglu81", "KevintRoitero"]

for user in users:
    print(f"Processing @{user}")

    user_followers = []

    for item in tweepy.Cursor(
            api.followers,
            screen_name=user,
            skip_status=True,
            include_user_entities=False
    ).items():
        found_follower = {"id": item.id,
                          "name": item.name,
                          "screen_name": item.screen_name,
                          "location": item.location}

        if found_follower not in user_followers:
            user_followers.append(found_follower)

    print(f"Found {len(user_followers)} followers for @{user}")
    serialize_json(data_folder, f"{user}_followers.json", user_followers)
