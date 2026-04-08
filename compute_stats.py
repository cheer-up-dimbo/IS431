import csv
import pathlib
import collections

path = pathlib.Path(r'c:\Users\zakir\Downloads\BoxBunny 4301 (Responses) - Form responses 1.csv')
rows = list(csv.reader(path.open(encoding='utf-8-sig', newline='')))
headers = rows[0]
g_idx = 1

# Extract boxer and support rows
boxer_rows = [r for r in rows[1:] if len(r) > g_idx and r[g_idx] == 'Boxer at Boxing Gyms']
support_rows = [r for r in rows[1:] if len(r) > g_idx and r[g_idx] in ['Coach', 'Boxing Gym Owner', 'Parents of Young Boxers']]

print("="*80)
print("BOXER ANALYSIS")
print(f"n = {len(boxer_rows)}")
print("")

# Boxer themes
boxer_themes = {
    'Lack of Training Partners': ['partner', 'sparring partner', 'training partner', 'no sparring'],
    'Slow Progress': ['slow progress', 'faster advancement', 'advance more quickly', 'progress', 'plateau', 'faster skill'],
    'Injury-Prone': ['injur', 'risk of injuries', 'heavy sparring', 'hurt'],
    'Limited Coaching Attention': ['coaching attention', 'coaching', 'feedback', 'coach', 'guidance'],
    'Time Commitment': ['time commitment', 'schedule', 'balancing', 'availability', 'work/school', 'time availability'],
    'Unmotivated': ['unmotivated', 'motivation', 'disciplined', 'stay consistent', 'staying consistent', 'struggle'],
    'Tracking Progress': ['track progress', 'measure progress', 'quantify', 'benchmark', 'progress over time'],
}

# Combine all text from each boxer
boxer_texts = []
for r in boxer_rows:
    text = ' | '.join(cell.lower() for cell in r if cell.strip())
    boxer_texts.append(text)

# Count respondents per theme
bo_counts = {}
for theme, kws in boxer_themes.items():
    bo_counts[theme] = sum(any(kw in text for kw in kws) for text in boxer_texts)

# Print sorted by prevalence
print("Theme Counts (respondents mentioning theme):")
for theme, count in sorted(bo_counts.items(), key=lambda x: -x[1]):
    pct = round(count / len(boxer_rows) * 100, 1)
    print(f"  {theme:35s}: {count:2d} ({pct:5.1f}%)")

print("\n" + "="*80)
print("SUPPORT STAKEHOLDER ANALYSIS")
print(f"n = {len(support_rows)}")
print("")

# Check how many answered the drill ranking question
drill_cols = [23, 24, 25, 26, 27, 28]
with_drill_responses = sum(1 for r in support_rows if len(r) > 28 and any(r[c].strip() for c in drill_cols))
print(f"Respondents with drill rankings: {with_drill_responses}")

# Extract drill rankings 
drill_labels = ['Pad Work', 'Sparring', 'Defense Drills', 'Technique Drills', 'Bag Work']
drill_data = {label: [] for label in drill_labels}

for r in support_rows:
    if len(r) > 28:
        for i, label in enumerate(drill_labels):
            rank_str = r[23 + i].strip()
            if rank_str:
                # Parse the rank
                try:
                    if '(Requires more attention)' in rank_str or '1 (Requires more attention)' in rank_str:
                        rank = 1
                    elif '(Requires less attention)' in rank_str or '6 (Requires less attention)' in rank_str:
                        rank = 6
                    else:
                        # Extract first number
                        for word in rank_str.split():
                            if word.isdigit():
                                rank = int(word)
                                break
                        else:
                            continue
                    drill_data[label].append(rank)
                except:
                    pass

print("\nDrill Priority Rankings (lower rank = more attention needed):")
avg_ranks = {}
for label in drill_labels:
    if drill_data[label]:
        avg = round(sum(drill_data[label]) / len(drill_data[label]), 2)
        avg_ranks[label] = (avg, len(drill_data[label]))
        print(f"  {label:20s}: avg_rank = {avg:4.2f} (n={len(drill_data[label])})")

print("\nRanked by priority (ascending = more attention):")
for label, (avg, n) in sorted(avg_ranks.items(), key=lambda x: x[1][0]):
    pct_of_respondents = round(n / len(support_rows) * 100, 1)
    print(f"  {label:20s}: avg={avg:4.2f} ({n} respondents, {pct_of_respondents}% of support group)")

print("\n" + "="*80)
print("DATA FOR CHART UPDATES")
print("")
print("Boxer pie data (sorted by count):")
sorted_boxer = sorted(bo_counts.items(), key=lambda x: -x[1])
values = [count for theme, count in sorted_boxer]
labels = [theme for theme, count in sorted_boxer]
print(f"  labels = {labels}")
print(f"  values = {values}")

print("\nSpport stakeholder drill data (sorted by avg_rank - most urgent first):")
sorted_drills = sorted(avg_ranks.items(), key=lambda x: x[1][0])
print(f"  labels = {[label for label, _ in sorted_drills]}")
print(f"  avg_ranks = {[avg for _, (avg, n) in sorted_drills]}")
