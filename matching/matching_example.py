users = [
    {"name": "Alice", "interests": ["hiking", "reading", "music", "swimming"]},
    {"name": "Bob", "interests": ["traveling", "photography", "cooking", "basketball", "hiking"]},
    {"name": "Henry", "interests": ["basketball", "hiking", "tennis", "soccer", "cards"]},
]

user_to_match = {"name": "Steven", "interests": ["reading", "board games", "cooking", "swimming"]}

for user in users:
    common_sports = set(user_to_match["interests"]).intersection(set(user["interests"]))
    user["common_sports"] = common_sports

for user in users:
    sports_score = len(user["common_sports"]) / len(user_to_match["interests"])
    user["score"] = sports_score

users.sort(key=lambda x: x["score"], reverse=True)

print("Top 3 matches:")
for i in range(3):
    if i >= len(users):
        break
    user = users[i]
    print(f"{i+1}){user['name']}: {user['score']}")
