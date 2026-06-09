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


# We have to boost this so Quick Sort doesn't trip over its own shoelaces on worst-case data
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

    # Setting up the table header
    print(f"{'Algorithm':<20} | {'Case Type':<15} | {'Elements':<10} | {'Time (s)':<15}")
    print("-" * 67)

    for size in sizes:
        # Define our four scenarios
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

    # Now let's draw some pretty pictures
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Time Plot
    ax1.plot(sizes, plot_data['Merge Sort (Best)']['time'], label='Merge Sort (Best)', marker='o', linestyle='--')
    ax1.plot(sizes, plot_data['Merge Sort (Worst)']['time'], label='Merge Sort (Worst)', marker='s')
    ax1.plot(sizes, plot_data['Quick Sort (Best)']['time'], label='Quick Sort (Best)', marker='^', linestyle='--')
    ax1.plot(sizes, plot_data['Quick Sort (Worst)']['time'], label='Quick Sort (Worst)', marker='x')
    
    ax1.set_title('Input Size vs Runtime')
    ax1.set_xlabel('Number of Elements')
    ax1.set_ylabel('Time (seconds)')
    ax1.legend()
    ax1.grid(True)

    # Comparison Plot
    ax2.plot(sizes, plot_data['Merge Sort (Best)']['comps'], label='Merge Sort (Best)', marker='o', linestyle='--')
    ax2.plot(sizes, plot_data['Merge Sort (Worst)']['comps'], label='Merge Sort (Worst)', marker='s')
    ax2.plot(sizes, plot_data['Quick Sort (Best)']['comps'], label='Quick Sort (Best)', marker='^', linestyle='--')
    ax2.plot(sizes, plot_data['Quick Sort (Worst)']['comps'], label='Quick Sort (Worst)', marker='x')

    ax2.set_title('Input Size vs Comparisons')
    ax2.set_xlabel('Number of Elements')
    ax2.set_ylabel('Comparison Count')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    print("\nCrunching numbers complete! Opening the plots now.")
    plt.show()

if __name__ == "__main__":
    # Test sizes. I kept them under 1500 to keep Quick Sort from throwing a tantrum on the worst case.
    test_sizes = [100, 250, 500, 750, 1000, 1500] 
    run_benchmarks_and_plot(test_sizes)