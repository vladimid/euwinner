"""
Frequency analysis module for lottery number analysis.
Provides reusable functions for analyzing number frequencies in lottery draws.
"""
import csv
import os
from typing import List, Dict, Optional


def load_csv_data(csv_file: str) -> List[Dict]:
    """
    Load CSV data from the specified file.

    Args:
        csv_file: Path to the CSV file

    Returns:
        List of dictionaries representing each draw
    """
    all_rows = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in enumerate(reader):
            # Skip rows with empty DrawNumber
            if not row[1].get('DrawNumber') or row[1]['DrawNumber'].strip() == '':
                continue
            all_rows.append(row[1])
    return all_rows


def get_csv_file_path() -> str:
    """
    Get the path to the lottery draw history CSV file.

    Returns:
        Absolute path to the CSV file
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return str(os.path.join(script_dir, '..', 'tests', 'data', 'lotto-draw-history.csv'))


def analyze_frequency(
    draws: int = 100,
    offset: int = 0,
    number_range: Optional[List[int]] = None
) -> Dict:
    """
    Analyze number frequency from lottery draws.

    Args:
        draws: Number of draws to analyze (default: 100)
        offset: Number of draws to skip from the beginning (default: 0)
        number_range: List of numbers to analyze (default: [1-59])

    Returns:
        Dictionary containing frequency analysis results
    """
    if number_range is None:
        number_range_list: List[int] = list(range(1, 60))
    else:
        number_range_list = number_range

    # Load CSV data
    csv_file = get_csv_file_path()
    all_rows = load_csv_data(csv_file)

    # Validate offset and draws
    if offset < 0:
        raise ValueError("offset must be >= 0")
    if draws <= 0:
        raise ValueError("draws must be > 0")
    if offset >= len(all_rows):
        raise ValueError(f"offset ({offset}) cannot be >= total draws ({len(all_rows)})")

    # Get the draws to analyze
    start_index = offset
    end_index = min(offset + draws, len(all_rows))
    balls_data = all_rows[start_index:end_index]

    if len(balls_data) == 0:
        raise ValueError("No draws available for analysis with given offset and draws parameters")

    # Collect all main balls
    all_balls = []
    for row in balls_data:
        for ball_num in range(1, 7):  # Balls 1-6
            try:
                ball = int(row[f'Ball {ball_num}'])
                all_balls.append(ball)
            except (ValueError, KeyError):
                continue

    # Initialize frequency with specified number range
    frequency = {i: 0 for i in number_range_list}
    for ball in all_balls:
        if ball in frequency:
            frequency[ball] += 1

    # Sort by frequency (descending) then by number
    sorted_freq = sorted(frequency.items(), key=lambda x: (-x[1], x[0]))

    # Calculate statistics
    most_frequent = [num for num, count in sorted_freq[:10] if count > 0]
    least_frequent = [num for num, count in sorted_freq[-10:] if count == 0]
    never_drawn = [num for num, count in frequency.items() if count == 0]

    # Count distribution
    count_by_frequency = {}
    for number, count in frequency.items():
        if count not in count_by_frequency:
            count_by_frequency[count] = 0
        count_by_frequency[count] += 1

    return {
        "draws_analyzed": len(balls_data),
        "offset": offset,
        "number_range": number_range_list,
        "frequency": frequency,
        "sorted_frequency": sorted_freq,
        "most_frequent": most_frequent,
        "least_frequent": least_frequent,
        "never_drawn": sorted(never_drawn),
        "count_by_frequency": count_by_frequency,
        "total_balls_drawn": len(all_balls)
    }

