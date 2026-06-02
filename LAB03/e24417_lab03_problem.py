import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
 
# ── helpers ─────────────────────────────────────────────────────────────────
 
def binary_search_iterative(arr, target):
    """Returns (index, iteration_count)."""
    low, high = 0, len(arr) - 1
    iterations = 0
 
    while low <= high:
        iterations += 1
        mid = (low + high) // 2
 
        if arr[mid] == target:
            return mid, iterations
        elif arr[mid] > target:
            high = mid - 1
        else:
            low = mid + 1
 
    return -1, iterations
 
 
def binary_search_recursive(arr, target, low=0, high=None, _count=None):
    """Returns (index, recursive_call_count)."""
    if _count is None:
        _count = [0]
    if high is None:
        high = len(arr) - 1
 
    _count[0] += 1        # count this call
 
    if low > high:
        return -1, _count[0]
 
    mid = (low + high) // 2
 
    if arr[mid] == target:
        return mid, _count[0]
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, low, mid - 1, _count)
    else:
        return binary_search_recursive(arr, target, mid + 1, high, _count)
 
 
# ── parse plot_inputs.txt ────────────────────────────────────────────────────
 
def parse_inputs(path):
    with open(path) as f:
        lines = [l.rstrip('\n') for l in f]
 
    entries = []
    i = 0
    while i < len(lines):
        while i < len(lines) and lines[i].strip() == '':
            i += 1
        if i >= len(lines):
            break
        target = int(lines[i].strip());  i += 1
        size   = int(lines[i].strip());  i += 1
        arr    = list(map(int, lines[i].strip().split()));  i += 1
        entries.append((target, size, arr))
    return entries
 
 
# ── run all inputs ───────────────────────────────────────────────────────────
 
entries = parse_inputs('plot_inputs.txt')
 
input_sizes      = []
iter_counts      = []
rec_call_counts  = []
 
for target, size, arr in entries:
    arr.sort()
 
    _, n_iter  = binary_search_iterative(arr, target)
    _, n_calls = binary_search_recursive(arr, target)
 
    input_sizes.append(size)
    iter_counts.append(n_iter)
    rec_call_counts.append(n_calls)
 
    print(f"n={size:>5}  iter_loops={n_iter:>2}  rec_calls={n_calls:>2}")
 
 
# ── theoretical O(log₂ n) curve ──────────────────────────────────────────────
 
n_range = np.linspace(max(1, min(input_sizes)), max(input_sizes), 400)
log2_curve = np.log2(n_range)
 
 
# ── shared style ─────────────────────────────────────────────────────────────
 
DARK_BG    = '#0f1117'
PANEL_BG   = '#1a1d27'
ACCENT_1   = '#7c9ef7'   # loop-count / iterative  (periwinkle-blue)
ACCENT_2   = '#f97b8b'   # recursive calls          (coral-pink)
LOG_COLOR  = '#ffd166'   # theoretical log₂ n line  (amber)
TEXT_COLOR = '#e0e6f0'
GRID_COLOR = '#2e3249'
 
plt.rcParams.update({
    'figure.facecolor':  DARK_BG,
    'axes.facecolor':    PANEL_BG,
    'axes.edgecolor':    GRID_COLOR,
    'axes.labelcolor':   TEXT_COLOR,
    'axes.titlecolor':   TEXT_COLOR,
    'axes.grid':         True,
    'grid.color':        GRID_COLOR,
    'grid.linewidth':    0.6,
    'xtick.color':       TEXT_COLOR,
    'ytick.color':       TEXT_COLOR,
    'text.color':        TEXT_COLOR,
    'legend.facecolor':  PANEL_BG,
    'legend.edgecolor':  GRID_COLOR,
    'font.family':       'DejaVu Sans',
})
 
 
# ── Plot 1 : Iterative – loop iterations ─────────────────────────────────────
 
fig1, ax1 = plt.subplots(figsize=(9, 5.5))
fig1.patch.set_facecolor(DARK_BG)
 
ax1.plot(n_range, log2_curve,
         color=LOG_COLOR, linewidth=1.5, linestyle='--',
         label='Theoretical O(log₂ n)', zorder=2)
 
ax1.scatter(input_sizes, iter_counts,
            color=ACCENT_1, s=60, zorder=3,
            edgecolors='white', linewidths=0.4,
            label='Measured loop iterations')
 
ax1.set_title('Iterative Binary Search — Loop Iterations vs Input Size',
              fontsize=13, fontweight='bold', pad=14)
ax1.set_xlabel('Input Size  (n)', fontsize=11)
ax1.set_ylabel('Number of Loop Iterations', fontsize=11)
ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax1.legend(fontsize=10, framealpha=0.85)
 
fig1.tight_layout(pad=1.6)
fig1.savefig('iterative_plot.png', dpi=150,
             bbox_inches='tight', facecolor=DARK_BG)
print("\nSaved: iterative_plot.png")
 
 
# ── Plot 2 : Recursive – recursive calls ─────────────────────────────────────
 
fig2, ax2 = plt.subplots(figsize=(9, 5.5))
fig2.patch.set_facecolor(DARK_BG)
 
ax2.plot(n_range, log2_curve,
         color=LOG_COLOR, linewidth=1.5, linestyle='--',
         label='Theoretical O(log₂ n)', zorder=2)
 
ax2.scatter(input_sizes, rec_call_counts,
            color=ACCENT_2, s=60, zorder=3,
            edgecolors='white', linewidths=0.4,
            label='Measured recursive calls')
 
ax2.set_title('Recursive Binary Search — Recursive Calls vs Input Size',
              fontsize=13, fontweight='bold', pad=14)
ax2.set_xlabel('Input Size  (n)', fontsize=11)
ax2.set_ylabel('Number of Recursive Calls', fontsize=11)
ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax2.legend(fontsize=10, framealpha=0.85)
 
fig2.tight_layout(pad=1.6)
fig2.savefig('recursive_plot.png', dpi=150,
             bbox_inches='tight', facecolor=DARK_BG)
print("Saved: recursive_plot.png")