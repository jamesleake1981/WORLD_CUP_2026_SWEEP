import random

# =====================================================
# WORLD CUP TEAMS WITH RANKINGS
# Lower number = better team
# =====================================================

teams = [
    {"team": "France", "rank": 1},
    {"team": "Spain", "rank": 2},
    {"team": "Argentina", "rank": 3},
    {"team": "England", "rank": 4},
    {"team": "Portugal", "rank": 5},
    {"team": "Brazil", "rank": 6},
    {"team": "Netherlands", "rank": 7},
    {"team": "Morocco", "rank": 8},
    {"team": "Belgium", "rank": 9},
    {"team": "Germany", "rank": 10},
    {"team": "Croatia", "rank": 11},
    {"team": "Colombia", "rank": 13},

    {"team": "Senegal", "rank": 14},
    {"team": "Mexico", "rank": 15},
    {"team": "USA", "rank": 16},
    {"team": "Uruguay", "rank": 17},
    {"team": "Japan", "rank": 18},
    {"team": "Switzerland", "rank": 19},
    {"team": "Iran", "rank": 21},
    {"team": "Turkiye", "rank": 22},
    {"team": "Ecuador", "rank": 23},
    {"team": "Austria", "rank": 24},
    {"team": "South Korea", "rank": 25},
    {"team": "Australia", "rank": 27},
    
    {"team": "Algeria", "rank": 28},
    {"team": "Egypt", "rank": 29},
    {"team": "Canada", "rank": 30},
    {"team": "Norway", "rank": 31},
    {"team": "Panama", "rank": 33},
    {"team": "Ivory Coast", "rank": 34},
    {"team": "Sweden", "rank": 38},
    {"team": "Paraguay", "rank": 40},
    {"team": "Czechia", "rank": 41},
    {"team": "Scotland", "rank": 43},
    {"team": "Tunisia", "rank": 44},
    {"team": "DR Congo", "rank": 46},

    {"team": "Uzbekistan", "rank": 50},
    {"team": "Qatar", "rank": 55},
    {"team": "Iraq", "rank": 57},
    {"team": "South Africa", "rank": 60},
    {"team": "Saudi Arabia", "rank": 61}, 
    {"team": "Jordan", "rank": 63},
    {"team": "Boznia and Herzegovina", "rank": 65},
    {"team": "Cape Verde", "rank": 69},
    {"team": "Ghana", "rank": 74},
    {"team": "Curacao", "rank": 82},
    {"team": "Haiti", "rank": 83},
    {"team": "New Zealand", "rank": 85},
]

# =====================================================
# PEOPLE
# =====================================================

people = [
    "James",
    "Natalie",
    "Nora",
    "Briony",
    "Laura",
    "Andrea",
    "Tom",
    "Linda",
    "Chistine",
    "Kirsty",
    "Paul",
    "Friend"
]

# =====================================================
# SETTINGS
# =====================================================

OUTPUT_FILE = "world_cup_draft_results.txt"

# Optional:
# random.seed(42)

# =====================================================
# VALIDATION
# =====================================================

if len(teams) != 48:
    raise ValueError("Need exactly 48 teams.")

if len(people) != 12:
    raise ValueError("Need exactly 12 people.")

# =====================================================
# SPLIT INTO TIERS
# =====================================================

tiers = {
    "Tier 1": teams[0:12],
    "Tier 2": teams[12:24],
    "Tier 3": teams[24:36],
    "Tier 4": teams[36:48],
}

# Shuffle each tier independently
for tier in tiers.values():
    random.shuffle(tier)

# =====================================================
# ASSIGN TEAMS
# =====================================================

assignments = {}

for i, person in enumerate(people):
    assignments[person] = {
        "Tier 1": tiers["Tier 1"][i],
        "Tier 2": tiers["Tier 2"][i],
        "Tier 3": tiers["Tier 3"][i],
        "Tier 4": tiers["Tier 4"][i],
    }

# =====================================================
# BUILD OUTPUT
# =====================================================

output = []

output.append("WORLD CUP TEAM DRAFT")
output.append("=" * 60)

for person, picks in assignments.items():
    output.append(f"\n{person}")

    for tier_name, data in picks.items():
        output.append(
            f"  {tier_name}: {data['team']} "
            f"(Rank #{data['rank']})"
        )

# =====================================================
# PRINT RESULTS
# =====================================================

output_text = "\n".join(output)

print(output_text)

# =====================================================
# SAVE TO FILE
# =====================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(output_text)
    f.write("\n")

print(f"\nResults saved to '{OUTPUT_FILE}'")
