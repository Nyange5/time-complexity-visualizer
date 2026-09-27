import base64, random, time
from heapq import merge
from pathlib import Path
from flask import Flask, jsonify, request
from matplotlib.figure import Figure
from stack import Stack
from queue_ds import Queue, NaiveQueue
from database import db, AnalysisRecord, COMPLEXITY_LABELS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///analysis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()

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

def stack_push_pop(a):
    s = Stack()
    for x in a: s.push(x)
    while not s.is_empty(): s.pop()

def queue_enqueue_dequeue(a):
    q = Queue()
    for x in a: q.enqueue(x)
    while not q.is_empty(): q.dequeue()

def queue_naive_dequeue(a):
    q = NaiveQueue()
    for x in a: q.enqueue(x)
    while not q.is_empty(): q.dequeue()

ALGOS = {f.__name__: f for f in [linear_search, binary_search, bubble_sort, nested_loops,
                                 selection_sort, merge_sort, quick_sort,
                                 stack_push_pop, queue_enqueue_dequeue, queue_naive_dequeue]}

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

def parse_request():
    name = request.args.get("algo", "").strip("[]'\" ")
    try:
        step, n_max = (int(request.args[k].replace(",", "")) for k in ("step", "n_max"))
    except (KeyError, ValueError):
        return None, (jsonify(error="step and n_max must be integers"), 400)
    if name not in ALGOS or step < 1 or n_max < 1:
        return None, (jsonify(error=f"invalid input; algo must be one of {list(ALGOS)}"), 400)
    return (name, step, n_max), None

def run_analysis(name, step, n_max):
    step = max(step, n_max // 25)
    sizes, times, fig = time_complexity_visualizer(ALGOS[name], 0, n_max, step)
    Path("snapshots").mkdir(exist_ok=True)
    img_path = Path("snapshots") / f"{name}_{n_max}.png"
    fig.savefig(img_path)
    return dict(algo=name, n_max=n_max, step=step, sizes=sizes, times=times,
                image_path=str(img_path), image_base64=base64.b64encode(img_path.read_bytes()).decode())

@app.get("/analyze")
def analyze():
    parsed, err = parse_request()
    if err: return err
    return jsonify(run_analysis(*parsed))

def parse_body():
    data = request.get_json(silent=True) or {}
    try:
        name = str(data["algo"]).strip("[]'\" ")
        step = int(str(data["step"]).replace(",", ""))
        n_max = int(str(data["n_max"]).replace(",", ""))
    except (KeyError, ValueError, TypeError):
        return None, (jsonify(error="JSON body must include algo, step, n_max"), 400)
    if name not in ALGOS or step < 1 or n_max < 1:
        return None, (jsonify(error=f"invalid input; algo must be one of {list(ALGOS)}"), 400)
    return (name, step, n_max), None

@app.post("/save_analysis")
def save_analysis():
    parsed, err = parse_body()
    if err: return err
    name, step, n_max = parsed
    started_at = time.time()
    result = run_analysis(name, step, n_max)
    finished_at = time.time()
    record = AnalysisRecord(
        algorithm_name=name, input_size=n_max, step_size=result["step"],
        started_at=started_at, finished_at=finished_at, duration_seconds=finished_at - started_at,
        big_o=COMPLEXITY_LABELS.get(name, "unknown"), plot_path=result["image_path"],
    )
    db.session.add(record)
    db.session.commit()
    result["id"] = record.id
    result["big_o"] = record.big_o
    return jsonify(result)

@app.get("/analyses")
def list_analyses():
    rows = AnalysisRecord.query.order_by(AnalysisRecord.id.desc()).all()
    return jsonify([r.to_dict() for r in rows])

@app.get("/analyses/<int:analysis_id>")
def get_analysis(analysis_id):
    record = db.session.get(AnalysisRecord, analysis_id)
    if record is None:
        return jsonify(error=f"no analysis with id {analysis_id}"), 404
    return jsonify(record.to_dict())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
