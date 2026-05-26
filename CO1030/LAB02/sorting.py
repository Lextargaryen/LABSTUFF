import random
import time


def create_rand_data(size):
    """Create a list of given size populated with random data."""
    return [random.randint(0, 100) for _ in range(size)]


def create_worst_data(size):
    """Create a list of given size in worst-case order (reverse sorted)."""
    return list(range(size, 0, -1))


def create_best_data(size):
    """Create a list of given size in best-case order (already sorted)."""
    return list(range(size))


def is_sorted(data):
    """Check if the list is sorted in ascending order."""
    for i in range(1, len(data)):
        if data[i] < data[i - 1]:
            return False
    return True


def display(data):
    """Display the list."""
    print("=======")
    print("  ".join(str(x) for x in data))
    print("=======")


# ----------------------------------------------------------
#     Implementation of sorting algorithms
# ----------------------------------------------------------

def bubble_sort(data):

    n = len(data)
    for i in range(n):
        s = False
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:

                data[j], data[j + 1] = data[j + 1], data[j]
                s = True
        if not s:
            break
    return data


def selection_sort(data):

    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j

        data[i], data[min_idx] = data[min_idx], data[i]
    return data


def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data


# ----------------------------------------------------------

if __name__ == "__main__":
    # Create arrays of different sizes, populate with data, and
    # measure the time taken by each algorithm to sort the array.
    
    test_sizes = [500, 1000, 2000]
    
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort)
    ]
    
    data_scenarios = [
        ("Random Data", create_rand_data),
        ("Best Case", create_best_data),
        ("Worst Case", create_worst_data)
    ]

    print(f"{'Algorithm':<16} | {'Scenario':<14} | {'Size':<6} | {'Time (Seconds)'}")
    print("-" * 60)

    for algo_name, algo_func in algorithms:
        for scenario_name, data_func in data_scenarios:
            for size in test_sizes:
                # 1. Generate the data
                data = data_func(size)
                
                # 2. Start the clock
                start_time = time.perf_counter()
                
                # 3. Sort
                algo_func(data)
                
                # 4. Stop the clock
                end_time = time.perf_counter()
                
                # Verify that it actually sorted correctly (sanity check)
                if not is_sorted(data):
                    print(f"Uh oh! {algo_name} failed to sort the data!")
                    continue
                
                time_taken = end_time - start_time
                
                print(f"{algo_name:<16} | {scenario_name:<14} | {size:<6} | {time_taken:.6f}")
        print("-" * 60)

test1 = [1,9,2,1,1,52,74,3,0,-1,5,-6]
test2 = [5,2,7,-5,6,85,-85,84,1,0,0,5]

print("bubble")
print(bubble_sort(test1))

print("selection")
print(selection_sort(test1))

print("insertion")
print(insertion_sort(test1))


