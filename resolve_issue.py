json = dict()

idList = []


for account in accounts:
    serializer = se.Serializer(f"data/{account}")
    with os.scandir(f"data/{account}") as it:
        for entry in it:
                if entry.name.endswith("followers.json") or entry.name.endswith("follower.json") or entry.name.endswith("following.json")