import re
from collections import defaultdict
from functools import cmp_to_key

def compare(a, b):
    # points
    if a["points"] != b["points"]:
        return b["points"] - a["points"]

    # GD
    gd_a = a["gf"] - a["ga"]
    gd_b = b["gf"] - b["ga"]
    if gd_a != gd_b:
        return gd_b - gd_a

    # GF
    if a["gf"] != b["gf"]:
        return b["gf"] - a["gf"]

    # HEAD TO HEAD
    team_a = a["team"]
    team_b = b["team"]

    h = h2h[team_a][team_b]

    # if no match played, fallback stable
    if h["points"] == 0 and h["gf"] == 0 and h["ga"] == 0:
        return 0

    # H2H points
    if h["points"] != 0:
        return -h["points"]

    # H2H GD
    h2h_gd = h["gf"] - h["ga"]
    if h2h_gd != 0:
        return -h2h_gd

    # H2H GF
    return -(h["gf"])

# ==========================================
# SETTINGS
# ==========================================

INPUT_FILE = "final_draft.txt"
OUTPUT_FILE = "custom_groups_sorted.txt"

SORT_BY = "points"  # change to: "gd", "gf", "ga", "yc", "rc"

# ==========================================
# MATCHES
# ==========================================

matches = [
    ("Mexico", 2, "South Africa", 1),
    ("South Africa", 3, "South Korea", 0)

	]

h2h = defaultdict(lambda: defaultdict(lambda: {
    "points": 0,
    "gf": 0,
    "ga": 0
}))

# ==========================================
# INIT STATS
# ==========================================

stats = defaultdict(lambda: {
    "gf": 0,
    "ga": 0,
    "points": 0,
    "yc": 0,
    "rc": 0
})

# ==========================================
# CALCULATE FROM MATCHES
# ==========================================

for home, hg, away, ag in matches:

    # goals
    stats[home]["gf"] += hg
    stats[home]["ga"] += ag

    stats[away]["gf"] += ag
    stats[away]["ga"] += hg

    # points
    if hg > ag:
        stats[home]["points"] += 3
        h2h[home][away]["points"] += 3
    elif hg < ag:
        stats[away]["points"] += 3
        h2h[away][home]["points"] += 3
    else:
        stats[home]["points"] += 1
        stats[away]["points"] += 1
        h2h[home][away]["points"] += 1
        h2h[away][home]["points"] += 1

    # H2H goals
    h2h[home][away]["gf"] += hg
    h2h[home][away]["ga"] += ag

    h2h[away][home]["gf"] += ag
    h2h[away][home]["ga"] += hg

# ==========================================
# READ FILE
# ==========================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# ==========================================
# PARSE TEAMS + OWNERS
# ==========================================

team_pattern = r"Tier \d+:\s(.+?)\s\(Rank\s#(\d+)\)"

people_teams = {}
current_person = None

for line in lines:
    line = line.strip()

    if (
        not line
        or "WORLD CUP TEAM DRAFT" in line
        or "=" in line
    ):
        continue

    if not line.startswith("Tier"):
        current_person = line
        people_teams[current_person] = []
        continue

    match = re.search(team_pattern, line)

    if match:
        people_teams[current_person].append({
            "team": match.group(1),
            "rank": int(match.group(2)),
            "owner": current_person,

            # ==========================================
            # STATS (EDIT THESE OR IMPORT LATER)
            # ==========================================
            "gf": 0,
            "ga": 0,
            "points": 0,
            "yc": 0,
            "rc": 0,
        })

# ==========================================
# TEAM LOOKUP
# ==========================================

team_lookup = {}
for owner, teams in people_teams.items():
    for t in teams:
        team_lookup[t["team"]] = t

# ==========================================
# ATTACH STATS TO YOUR TEAM LOOKUP
# ==========================================

for team_name, data in team_lookup.items():
    if team_name in stats:
        data.update(stats[team_name])
    else:
        # ensure defaults exist
        data.update({
            "gf": 0,
            "ga": 0,
            "points": 0,
            "yc": 0,
            "rc": 0
        })

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
# SORT KEY FUNCTION
# ==========================================

def sort_key(team):
    if SORT_BY == "points":
        return team["points"]
    elif SORT_BY == "gd":
        return team["gf"] - team["ga"]
    elif SORT_BY == "gf":
        return team["gf"]
    elif SORT_BY == "ga":
        return -team["ga"]  # fewer conceded is better
    elif SORT_BY == "yc":
        return -team["yc"]  # fewer cards is better
    elif SORT_BY == "rc":
        return -team["rc"]
    else:
        return team["points"]

# ==========================================
# BUILD OUTPUT
# ==========================================

output = []
output.append("CUSTOM WORLD CUP GROUPS (SORTED)")
output.append("=" * 60)
output.append(f"Sorted by: {SORT_BY.upper()}")

for group_name, team_names in groups.items():

    output.append(f"\n{group_name}")
    output.append("-" * 40)

    output.append(f"{'Team':<25}{'PTS':>5}{'GF':>5}{'GA':>5}{'GD':>5}{'YC':>5}{'RC':>5}{'Owner':>15}")
    output.append("-" * 80)
    group_teams = []

    for name in team_names:
        if name in team_lookup:
            group_teams.append(team_lookup[name])

    # Sort group
    group_teams.sort(key=cmp_to_key(compare))
    #group_teams.sort(key=sort_key, reverse=True)

    for t in group_teams:
        gd = t["gf"] - t["ga"]

        output.append(
    		f"{t['team']:<25}"
    		f"{t['points']:>5}"
    		f"{t['gf']:>5}"
    		f"{t['ga']:>5}"
    		f"{gd:>5}"
    		f"{t['yc']:>5}"
    		f"{t['rc']:>5}"
    		f"{t['owner']:>15}"
	)

# ==========================================
# SAVE FILE
# ==========================================

output_text = "\n".join(output)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(output_text)
    f.write("\n") 

print(output_text)
print(f"\nSaved to {OUTPUT_FILE}")
