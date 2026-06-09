# benchmark_plot.py
import time
import random
import sys
import matplotlib.pyplot as plt

def merge_sort(arr):
    """
    Perform merge sort on arr.
    Returns: (sorted_arr, comparisons)
    """
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, left_comps = merge_sort(arr[:mid])
    right, right_comps = merge_sort(arr[mid:])

    merged = []
    comps = left_comps + right_comps
    i = j = 0

    while i < len(left) and j < len(right):
        comps += 1 
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged, comps


def quick_sort(arr):
    """
    Perform quick sort (Lomuto partition) on arr.
    Returns: (sorted_arr, comparisons)
    """
    def _quick_sort(a, low, high):
        if low < high:
            p_idx, p_comps = partition(a, low, high)
            left_comps = _quick_sort(a, low, p_idx - 1)
            right_comps = _quick_sort(a, p_idx + 1, high)
            return p_comps + left_comps + right_comps
        return 0

    def partition(a, low, high):
        pivot = a[high]
        i = low - 1
        comps = 0
        for j in range(low, high):
            comps += 1 
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        
        a[i + 1], a[high] = a[high], a[i + 1]
        return i + 1, comps

    total_comps = _quick_sort(arr, 0, len(arr) - 1)
    return arr, total_comps


# We still need this so Quick Sort doesn't crash on worst-case arrays
sys.setrecursionlimit(5000)

def generate_test_data(size, condition):
    if condition == 'Best Case':
        return list(range(size))
    elif condition == 'Worst Case Merge':
        return list(range(size, 0, -1))
    elif condition == 'Average/Best Quick':
        return [random.randint(0, 10000) for _ in range(size)]
    elif condition == 'Worst Case Quick':
        return list(range(size))
    return []

def run_benchmarks_and_plot(sizes):
    # Dictionaries to store data for our plots
    plot_data = {
        'Merge Sort (Best)': {'time': [], 'comps': []},
        'Merge Sort (Worst)': {'time': [], 'comps': []},
        'Quick Sort (Best)': {'time': [], 'comps': []},
        'Quick Sort (Worst)': {'time': [], 'comps': []}
    }

    # Setting up the table header so you can watch the progress
    print(f"{'Algorithm':<20} | {'Case Type':<15} | {'Elements':<10} | {'Time (s)':<15}")
    print("-" * 67)

    for size in sizes:
        scenarios = [
            ('Merge Sort', 'Best Case', generate_test_data(size, 'Best Case'), merge_sort, 'Merge Sort (Best)'),
            ('Merge Sort', 'Worst Case', generate_test_data(size, 'Worst Case Merge'), merge_sort, 'Merge Sort (Worst)'),
            ('Quick Sort', 'Best Case', generate_test_data(size, 'Average/Best Quick'), quick_sort, 'Quick Sort (Best)'),
            ('Quick Sort', 'Worst Case', generate_test_data(size, 'Worst Case Quick'), quick_sort, 'Quick Sort (Worst)')
        ]

        for algo_name, case_type, arr, func, plot_key in scenarios:
            # Measure time
            start = time.perf_counter()
            _, comps = func(arr)
            end = time.perf_counter()
            
            elapsed = end - start
            
            # Print the row for this specific run
            print(f"{algo_name:<20} | {case_type:<15} | {size:<10} | {elapsed:.8f}")
            
            # Store data for plotting
            plot_data[plot_key]['time'].append(elapsed)
            plot_data[plot_key]['comps'].append(comps)

    print("\nCrunching numbers complete! Generating and saving your 8 plots now.")

    # --- Plot 1: Runtime vs Input Size ---
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, plot_data['Merge Sort (Best)']['time'], label='Merge Sort (Best)', marker='o', linestyle='--', markersize=4)
    plt.plot(sizes, plot_data['Merge Sort (Worst)']['time'], label='Merge Sort (Worst)', marker='s', markersize=4)
    plt.plot(sizes, plot_data['Quick Sort (Best)']['time'], label='Quick Sort (Best)', marker='^', linestyle='--', markersize=4)
    plt.plot(sizes, plot_data['Quick Sort (Worst)']['time'], label='Quick Sort (Worst)', marker='x', markersize=4)
    
    plt.title('Performance vs. Input Size (Runtime)')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig('runtime_plot.png', dpi=300) # Saves a nice crisp image
    print("Successfully saved: runtime_plot.png")
    plt.close() # Close the figure to free up memory

    # --- Plot 2: Comparisons vs Input Size ---
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, plot_data['Merge Sort (Best)']['comps'], label='Merge Sort (Best)', marker='o', linestyle='--', markersize=4)
    plt.plot(sizes, plot_data['Merge Sort (Worst)']['comps'], label='Merge Sort (Worst)', marker='s', markersize=4)
    plt.plot(sizes, plot_data['Quick Sort (Best)']['comps'], label='Quick Sort (Best)', marker='^', linestyle='--', markersize=4)
    plt.plot(sizes, plot_data['Quick Sort (Worst)']['comps'], label='Quick Sort (Worst)', marker='x', markersize=4)

    plt.title('Comparisons vs. Input Size')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Comparison Count')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig('comparisons_plot.png', dpi=300)
    print("Successfully saved: comparisons_plot.png")
    plt.close()

if __name__ == "__main__":
    # Generating exactly 20 data points: 50, 100, 150... up to 1000
    test_sizes = [i * 50 for i in range(1, 21)] 
    
    print(f"Starting test with {len(test_sizes)} data points to satisfy the assignment requirements...\n")
    run_benchmarks_and_plot(test_sizes)
    print("\nAll done! Check your folder for the generated image files.")