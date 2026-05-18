#!/usr/bin/env python3
"""fib.py: Measure recursive and iterative Fibonacci runtimes, save to CSV, and plot."""

import time
import csv
import matplotlib.pyplot as plt

def fib_recursive(n):
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def main():
    # 3. Data Collection Setup
    # Test input sizes: n = 5, 10, 15, ..., 40
    n_values = list(range(5, 41, 5)) 
    trials = 5
    csv_filename = "fib_results.csv"
    
    results = []

    for n in n_values:
        print(f"Testing n = {n:2} ...", end=" ", flush=True)
        total_time_r = 0.0
        total_time_i = 0.0

        for _ in range(trials):
            # Recursive timing
            start = time.perf_counter()
            fib_recursive(n)
            total_time_r += (time.perf_counter() - start)

            # Iterative timing
            start = time.perf_counter()
            fib_iterative(n)
            total_time_i += (time.perf_counter() - start)

        avg_time_r_ms = (total_time_r / trials) * 1000
        avg_time_i_ms = (total_time_i / trials) * 1000

        results.append((n, avg_time_r_ms, avg_time_i_ms))
        print("Done.")

    # Save to CSV
    print(f"\nSaving results to '{csv_filename}'...")
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["n", "Average_Recursive_Time_ms", "Average_Iterative_Time_ms"])
        writer.writerows(results)

    # 4. Plotting
    print("Generating plot...")
    n_data = [row[0] for row in results]
    r_data = [row[1] for row in results]
    i_data = [row[2] for row in results]

    plt.figure(figsize=(10, 6))
    
    # Plot both lines
    plt.plot(n_data, r_data, marker='o', color='red', label='Recursive')
    plt.plot(n_data, i_data, marker='s', color='blue', label='Iterative')

    # Apply required labels and legend
    plt.xlabel('n')
    plt.ylabel('Time in milliseconds')
    plt.title('Average Fibonacci Runtime: Recursive vs. Iterative')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the plot as an image and then show it
    plt.savefig('fib_plot.png')
    plt.show()

if __name__ == "__main__":
    main()