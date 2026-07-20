#!/usr/bin/env python3
import sys
from frequency_analyzer import analyze_frequency, load_csv_data, get_csv_file_path

def main():
    """CLI interface for number frequency analysis"""
    
    # Parse parameters
    if len(sys.argv) == 1:
        # No parameters: use most recent 26 draws
        num_draws = 26
        offset = 0
        analysis_type = f"most recent {num_draws} draws"
    
    elif len(sys.argv) == 2:
        # One parameter: use most recent N draws
        num_draws = int(sys.argv[1])
        offset = 0
        analysis_type = f"most recent {num_draws} draws"
    
    elif len(sys.argv) == 3:
        # Two parameters: M (DrawNumber) and N (number of draws before it)
        target_draw_number = int(sys.argv[1])
        num_draws = int(sys.argv[2])
        
        # Load data to find the target draw
        csv_file = get_csv_file_path()
        all_rows = load_csv_data(csv_file)
        
        # Find the target draw
        target_index = None
        for i, row in enumerate(all_rows):
            if int(row['DrawNumber']) == target_draw_number:
                target_index = i
                break
        
        if target_index is None:
            print(f"Error: Draw number {target_draw_number} not found in CSV file")
            sys.exit(1)
        
        # Calculate offset (number of draws after the target)
        offset = target_index + 1
        
        if offset + num_draws > len(all_rows):
            print(f"Error: Not enough previous draws. Need {num_draws} but only {len(all_rows) - offset} available.")
            sys.exit(1)
        
        # Get the actual draw numbers for display
        draw_numbers = [all_rows[i]['DrawNumber'] for i in range(offset, offset + num_draws)]
        analysis_type = f"{num_draws} draws before draw {target_draw_number}: {', '.join(draw_numbers)}"
    
    else:
        print("Usage: python number_frequency.py [M] [N]")
        print("  No parameters: analyze most recent 26 draws")
        print("  One parameter N: analyze most recent N draws")
        print("  Two parameters M N: analyze N draws before draw M")
        sys.exit(1)
    
    # Perform the analysis
    result = analyze_frequency(draws=num_draws, offset=offset)
    frequency = result["frequency"]
    sorted_freq = result["sorted_frequency"]
    count_by_frequency = result["count_by_frequency"]
    never_drawn = result["never_drawn"]
    
    # Print results
    print("=" * 80)
    print(f"NUMBER FREQUENCY ANALYSIS - {analysis_type.capitalize()}")
    print("=" * 80)
    print()
    
    print("FREQUENCY OF ALL NUMBERS (1-59) - Sorted by Frequency (Descending)")
    print("-" * 80)
    
    for number, count in sorted_freq:
        odd_even = "Odd " if number % 2 == 1 else "Even"
        half = "1-30" if number <= 30 else "31-59"
        print(f"   Number {number:2d}: {count:2d} times  ({odd_even}, {half})")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    for freq in sorted(count_by_frequency.keys()):
        num_count = count_by_frequency[freq]
        print(f"   {num_count:2d} numbers drawn exactly {freq} time(s)")
    
    print()
    
    if never_drawn:
        print(f"Numbers NEVER drawn (0 times): {never_drawn}")
    else:
        print("All numbers have been drawn at least once!")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
