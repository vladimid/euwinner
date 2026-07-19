#!/usr/bin/env python3
import csv
import sys
import os

# Parse parameters
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file = os.path.join(script_dir, '..', 'tests', 'data', 'lotto-draw-history.csv')

# Read the CSV file to get all rows
all_rows = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in enumerate(reader):
        # Skip rows with empty DrawNumber
        if not row[1].get('DrawNumber') or row[1]['DrawNumber'].strip() == '':
            continue
        all_rows.append(row[1])

# Determine which draws to analyze
balls_data = []

if len(sys.argv) == 1:
    # No parameters: use most recent 26 draws
    num_draws = 26
    balls_data = all_rows[:num_draws]
    analysis_type = f"most recent {num_draws} draws"

elif len(sys.argv) == 2:
    # One parameter: use most recent N draws
    num_draws = int(sys.argv[1])
    balls_data = all_rows[:num_draws]
    analysis_type = f"most recent {num_draws} draws"

elif len(sys.argv) == 3:
    # Two parameters: M (DrawNumber) and N (number of draws before it)
    target_draw_number = int(sys.argv[1])
    num_draws = int(sys.argv[2])

    # Find the target draw
    target_index = None
    for i, row in enumerate(all_rows):
        if int(row['DrawNumber']) == target_draw_number:
            target_index = i
            break

    if target_index is None:
        print(f"Error: Draw number {target_draw_number} not found in CSV file")
        sys.exit(1)

    # Get N draws after the target (since CSV is in reverse chronological order)
    start_index = target_index + 1
    end_index = start_index + num_draws
    balls_data = all_rows[start_index:end_index]

    if len(balls_data) == 0:
        print(f"Error: Not enough previous draws. Need {num_draws} but only {len(all_rows) - target_index - 1} available.")
        sys.exit(1)

    # Get the actual draw numbers for display
    draw_numbers = [row['DrawNumber'] for row in balls_data]
    analysis_type = f"{num_draws} draws before draw {target_draw_number}: {', '.join(draw_numbers)}"

else:
    print("Usage: python number_frequency.py [M] [N]")
    print("  No parameters: analyze most recent 26 draws")
    print("  One parameter N: analyze most recent N draws")
    print("  Two parameters M N: analyze N draws before draw M")
    sys.exit(1)

print("=" * 80)
print(f"NUMBER FREQUENCY ANALYSIS - {analysis_type.capitalize()}")
print("=" * 80)
print()

# Collect all main balls
all_balls = []
for row in balls_data:
    for ball_num in range(1, 7):  # Balls 1-6
        ball = int(row[f'Ball {ball_num}'])
        all_balls.append(ball)

# Initialize frequency with all numbers 1-59 with count 0
frequency = {i: 0 for i in range(1, 60)}
for ball in all_balls:
    frequency[ball] += 1

# Print all numbers sorted by frequency (descending), then by number
print("FREQUENCY OF ALL NUMBERS (1-59) - Sorted by Frequency (Descending)")
print("-" * 80)
sorted_freq = sorted(frequency.items(), key=lambda x: (-x[1], x[0]))

for number, count in sorted_freq:
    odd_even = "Odd " if number % 2 == 1 else "Even"
    half = "1-30" if number <= 30 else "31-59"
    print(f"   Number {number:2d}: {count:2d} times  ({odd_even}, {half})")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)

# Count how many numbers appear 0 times, 1 time, 2+ times, etc.
count_by_frequency = {}
for number, count in frequency.items():
    if count not in count_by_frequency:
        count_by_frequency[count] = 0
    count_by_frequency[count] += 1

for freq in sorted(count_by_frequency.keys()):
    num_count = count_by_frequency[freq]
    print(f"   {num_count:2d} numbers drawn exactly {freq} time(s)")

print()

# Find numbers never drawn
never_drawn = [num for num, count in frequency.items() if count == 0]
if never_drawn:
    print(f"Numbers NEVER drawn (0 times): {sorted(never_drawn)}")
else:
    print("All numbers have been drawn at least once!")

print()
print("=" * 80)
