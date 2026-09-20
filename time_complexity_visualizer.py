import base64, random, time
from heapq import merge
from pathlib import Path
from flask import Flask, jsonify, request
from matplotlib.figure import Figure

app = Flask(__name__)

def linear_search(a, target=-1):
    for i, x in enumerate(a):
        if x == target: return i
    return -1

def binary_search(a, target=-1):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target: return mid
        if a[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

def bubble_sort(a):
    a = a[:]
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]

def nested_loops(a):
    for _ in a:
        for _ in a: pass

def selection_sort(a):
    a = a[:]
    for i in range(len(a)):
        m = min(range(i, len(a)), key=a.__getitem__)
        a[i], a[m] = a[m], a[i]

def merge_sort(a):
    if len(a) < 2: return a
    mid = len(a) // 2
    return list(merge(merge_sort(a[:mid]), merge_sort(a[mid:])))

def quick_sort(a):
    if len(a) < 2: return a
    p, rest = a[0], a[1:]
    return quick_sort([x for x in rest if x < p]) + [p] + quick_sort([x for x in rest if x >= p])

ALGOS = {f.__name__: f for f in [linear_search, binary_search, bubble_sort, nested_loops,
                                 selection_sort, merge_sort, quick_sort]}

def time_complexity_visualizer(algorithm, n_min, n_max, n_step):
    sizes, times = list(range(n_min, n_max + 1, n_step)), []
    for n in sizes:
        data = random.sample(range(n), n) if "sort" in algorithm.__name__ else list(range(n))
        start = time.perf_counter()
        algorithm(data)
        times.append(time.perf_counter() - start)
    fig = Figure()
    ax = fig.subplots()
    ax.plot(sizes, times, "o-")
    ax.set(xlabel="Input size", ylabel="Running time (seconds)", title=f"{algorithm.__name__} time complexity")
    return sizes, times, fig

@app.get("/analyze")
def analyze():
    name = request.args.get("algo", "").strip("[]'\" ")
    try:
        step, n_max = (int(request.args[k].replace(",", "")) for k in ("step", "n_max"))
    except (KeyError, ValueError):
        return jsonify(error="step and n_max must be integers"), 400
    if name not in ALGOS or step < 1 or n_max < 1:
        return jsonify(error=f"invalid input; algo must be one of {list(ALGOS)}"), 400
    step = max(step, n_max // 25)
    sizes, times, fig = time_complexity_visualizer(ALGOS[name], 0, n_max, step)
    Path("snapshots").mkdir(exist_ok=True)
    path = Path("snapshots") / f"{name}_{n_max}.png"
    fig.savefig(path)
    return jsonify(algo=name, n_max=n_max, step=step, sizes=sizes, times=times,
                   image_path=str(path), image_base64=base64.b64encode(path.read_bytes()).decode())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)