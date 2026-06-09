# simple_sort.py
import time

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


if __name__ == "__main__":
    # Our highly scientific, hardcoded test subject
    hardcoded_input = [42, 17, 89, 33, 11, 105, 2, 77]
    print(f"Original Array: {hardcoded_input}\n")

    # --- Merge Sort Test ---
    start_time = time.perf_counter()
    sorted_merge, merge_comps = merge_sort(hardcoded_input.copy())
    end_time = time.perf_counter()
    
    print("--- Merge Sort ---")
    print(f"Sorted: {sorted_merge}")
    print(f"Comparisons: {merge_comps}")
    print(f"Time: {end_time - start_time:.8f} seconds\n")

    # --- Quick Sort Test ---
    start_time = time.perf_counter()
    sorted_quick, quick_comps = quick_sort(hardcoded_input.copy())
    end_time = time.perf_counter()
    
    print("--- Quick Sort ---")
    print(f"Sorted: {sorted_quick}")
    print(f"Comparisons: {quick_comps}")
    print(f"Time: {end_time - start_time:.8f} seconds")
