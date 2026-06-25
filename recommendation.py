import math

# ---------- Dataset ----------
movies = ['The Matrix', 'Inception', 'Interstellar', 'The Godfather', 'Pulp Fiction']

# Existing users: each has ratings for the 5 movies (0 = not rated)
users = {
    'User1': [5, 4, 0, 3, 2],
    'User2': [4, 5, 5, 0, 1],
    'User3': [0, 3, 4, 5, 5],
    'User4': [2, 0, 3, 4, 4],
    'User5': [3, 2, 0, 5, 3]
}

print("Existing user ratings (movies × users):")
print("Movie                  ", end="")
for u in users.keys():
    print(f"{u:>10}", end="")
print()
for i, movie in enumerate(movies):
    print(f"{movie:20}", end="")
    for u in users.values():
        print(f"{u[i]:>10}", end="")
    print()

# ---------- Get new user ratings ----------
print("\nNew user: Please rate each movie (0-5), 0 if not watched.")
new_ratings = []
for movie in movies:
    while True:
        try:
            val = input(f"Rate '{movie}' (0-5): ")
            rating = int(val)
            if 0 <= rating <= 5:
                new_ratings.append(rating)
                break
            else:
                print("Must be 0-5.")
        except ValueError:
            print("Please enter a number.")

# ---------- Correlation function (Pearson) ----------
def pearson_correlation(x, y):
    """Compute Pearson correlation between two lists (skip indices where either is 0)."""
    # Filter out pairs where either is 0
    pairs = [(a, b) for a, b in zip(x, y) if a != 0 and b != 0]
    n = len(pairs)
    if n < 2:
        return 0.0
    sum_x = sum(a for a, b in pairs)
    sum_y = sum(b for a, b in pairs)
    sum_x2 = sum(a*a for a, b in pairs)
    sum_y2 = sum(b*b for a, b in pairs)
    sum_xy = sum(a*b for a, b in pairs)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x*sum_x) * (n * sum_y2 - sum_y*sum_y))
    if denominator == 0:
        return 0.0
    return numerator / denominator

# ---------- Compute similarities ----------
similarities = {}
for user, ratings in users.items():
    sim = pearson_correlation(ratings, new_ratings)
    similarities[user] = sim

print("\nSimilarity (correlation) with each existing user:")
for user, sim in similarities.items():
    print(f"  {user}: {sim:.3f}")

# ---------- Generate recommendations ----------
# For each movie that the new user hasn't rated (rating == 0),
# compute weighted average of ratings from similar users (positive correlation)
recommendations = []
for movie_idx, movie in enumerate(movies):
    if new_ratings[movie_idx] == 0:
        weighted_sum = 0.0
        sim_sum = 0.0
        for user, sim in similarities.items():
            if sim > 0:  # Only users with positive correlation
                rating = users[user][movie_idx]  # rating from existing user
                if rating > 0:
                    weighted_sum += sim * rating
                    sim_sum += abs(sim)
        if sim_sum > 0:
            pred_rating = weighted_sum / sim_sum
            recommendations.append((movie, pred_rating))

# Sort by predicted rating descending
recommendations.sort(key=lambda x: x[1], reverse=True)

if recommendations:
    print("\nTop recommendations for you (based on similar users):")
    for movie, score in recommendations[:3]:
        print(f"  {movie} (predicted rating: {score:.2f})")
else:
    print("\nNot enough data to recommend – try rating more movies.")
