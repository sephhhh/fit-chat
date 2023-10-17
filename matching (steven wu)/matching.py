def find_matches(user_to_match, firebase):
    users = firebase.get('/Users', "")

    for user in users:
        if 'interests' not in user:
            user['interests'] = []

        common_interests = set(user_to_match["interests"]).intersection(set(user["interests"]))
        interests_score = len(common_interests) / len(user_to_match["interests"])

        user["score"] = 1 + interests_score

    users.sort(key=lambda x: x["score"], reverse=True)

    print("Top 3 matches:")
    for i in range(min(3, len(users))):
        user = users[i]
        print(f"{user['name']}: {user['score']}")
