#TO DO 

#Allow me to put results in and have groups show GF, GA, GD, points, yellow/red cards


import re
from collections import Counter

# ==========================================
# SETTINGS
# ==========================================

INPUT_FILE = "final_draft.txt"
OUTPUT_FILE = "custom_groups.txt"

# ==========================================
# READ FILE
# ==========================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# ==========================================
# PARSE PEOPLE + TEAMS
# ==========================================

team_pattern = r"Tier \d+:\s(.+?)\s\(Rank\s#(\d+)\)"

people_teams = {}
current_person = None

for line in lines:

    line = line.strip()

    # Skip headers
    if (
        not line
        or "WORLD CUP TEAM DRAFT" in line
        or "=" in line
    ):
        continue

    # Person line
    if not line.startswith("Tier"):
        current_person = line
        people_teams[current_person] = []
        continue

    # Team line
    match = re.search(team_pattern, line)

    if match and current_person:
        team_name = match.group(1)
        rank = int(match.group(2))

        people_teams[current_person].append({
            "team": team_name,
            "rank": rank,
            "owner": current_person
        })

# ==========================================
# CREATE TEAM LOOKUP
# ==========================================

team_lookup = {}

for person, teams in people_teams.items():
    for team in teams:
        team_lookup[team["team"]] = team


# ==========================================
# MANUALLY DEFINE GROUPS HERE
# ==========================================

groups = {
    "Group A": [
        "Mexico",
        "South Africa",
        "South Korea",
        "Czechia"
    ],

    "Group B": [
        "Canada",
        "Boznia and Herzegovina",
        "Qatar",
        "Switzerland"
    ],

    "Group C": [
        "Brazil",
        "Morocco",
        "Haiti",
        "Scotland"
    ],

    "Group D": [
        "USA",
        "Paraguay",
        "Australia",
        "Turkiye"
    ],

    "Group E": [
        "Germany",
        "Curacao",
        "Ivory Coast",
        "Ecuador"
    ],

    "Group F": [
        "Netherlands",
        "Japan",
        "Sweden",
        "Tunisia"
    ],

    "Group G": [
        "Belgium",
        "Egypt",
        "Iran",
        "New Zealand"
    ],

    "Group H": [
        "Spain",
        "Cape Verde",
        "Saudi Arabia",
        "Uruguay"
    ],
    
    "Group I": [
        "France",
        "Senegal",
        "Iraq",
        "Norway"
    ],

    "Group J": [
        "Argentina",
        "Algeria",
        "Austria",
        "Jordan"
    ],
  
    "Group K": [
        "Portugal",
        "DR Congo",
        "Uzbekistan",
        "Colombia"
    ],   

    "Group L": [
        "England",
        "Croatia",
        "Ghana",
        "Panama"
    ]

}

# ==========================================
# BUILD OUTPUT
# ==========================================

output = []

output.append("CUSTOM WORLD CUP GROUPS")
output.append("=" * 60)

# Track how many teams each person has
owner_counter = Counter()

for group_name, group_teams in groups.items():

    output.append(f"\n{group_name}")
    output.append("-" * 40)

    for team_name in group_teams:

        if team_name not in team_lookup:
            output.append(f"{team_name} (NOT FOUND)")
            continue

        team = team_lookup[team_name]

        owner_counter[team["owner"]] += 1

        output.append(
            f"{team['team']} "
            f"({team['rank']}) "
            f"- {team['owner']}"
        )

# ==========================================
# VALIDATION CHECK
# ==========================================

#output.append("\n")
#output.append("=" * 60)
#output.append("OWNER VALIDATION")
#output.append("=" * 60)

#all_valid = True
#
#for person in people_teams.keys():
#
#    count = owner_counter[person]
#
#    if count == 4:
#        output.append(f"{person}: OK (4 teams)")
#    else:
#        output.append(
#            f"{person}: ERROR ({count} teams)"
#        )
#        all_valid = False
#
#if all_valid:
#    output.append("\nAll people have exactly 4 teams.")
#else:
#    output.append(
#        "\nWARNING: Some people do not have 4 teams."
#    )

# ==========================================
# SAVE FILE
# ==========================================

output_text = "\n".join(output)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(output_text)
    f.write("\n")

# ==========================================
# PRINT RESULTS
# ==========================================

print(output_text)

print(f"\nGroups saved to '{OUTPUT_FILE}'")
