# Time Complexity Visualizer (Flask)

A Flask endpoint that times an algorithm for growing input sizes, plots the running time,
saves a PNG snapshot locally and returns the image as a base64 string in the JSON response.

## Run
```
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python time_complexity_visualizer.py
```
On Windows (PowerShell), activate with `.venv\Scripts\activate` instead of the `source` line.

Keep the terminal open: the server only runs while this command is running.
`localhost` means your own computer, so the URL below only works after you start the server.

## Endpoint
```
GET http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10,000
```
| Parameter | Meaning |
|-----------|---------|
| `algo`    | algorithm name (see below) |
| `step`    | increase in input size between measurements |
| `n_max`   | largest input size (`10,000` and `10000` both work); the minimum is always 0 |

To keep slow algorithms responsive, at most ~25 points are measured (the step is raised if needed).

## Supported algorithms
`linear_search`, `binary_search`, `bubble_sort`, `nested_loops`,
`selection_sort`, `merge_sort`, `quick_sort`,
`stack_push_pop`, `queue_enqueue_dequeue`, `queue_naive_dequeue`

## Stack and Queue
`stack.py` and `queue_ds.py` hold plain implementations, independent of Flask:
- `Stack` (list-backed): `push`, `pop`, `peek`, `is_empty`, `len()`, `in`.
- `Queue` (deque-backed): `enqueue`, `dequeue`, `peek`, `is_empty`, `len()`, `in`.
- `NaiveQueue`: same interface as `Queue`, but backed by a plain list, so
  `dequeue()` is O(n) instead of O(1). It exists only so the visualizer can
  show why a deque-backed queue is faster.

Run the test suites:
```
python -m unittest test_stack.py test_queue_ds.py -v
```

Visualize the three structure-based algorithms:
```
http://localhost:8000/analyze?algo=stack_push_pop&step=100&n_max=50000
http://localhost:8000/analyze?algo=queue_enqueue_dequeue&step=100&n_max=50000
http://localhost:8000/analyze?algo=queue_naive_dequeue&step=100&n_max=50000
```
`stack_push_pop` and `queue_enqueue_dequeue` push/enqueue n items then pop/dequeue
them all, and both come out O(n). `queue_naive_dequeue` does the same with
`NaiveQueue` and comes out O(n^2), visibly bending upward against the other two.

## Response (JSON)
`algo`, `n_max`, `step` (step actually used), `sizes`, `times` (seconds),
`image_path` (saved in `snapshots/`) and `image_base64` (PNG encoded as base64).

## Saving an analysis (database)
`models.py` defines an `AnalysisRecord` table with Flask-SQLAlchemy, backed
by SQLite (a single file, `instance/analysis.db`, created automatically the
first time the server runs). No raw SQL is written anywhere; SQLAlchemy's
ORM builds the queries. Flask-SQLAlchemy always puts a relative SQLite path
inside an `instance/` folder next to the code, which is why the file isn't
directly in the project root.

To point this at a real MySQL server instead, install `pymysql` and change
one line in `time_complexity_visualizer.py`:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://USER:PASSWORD@localhost:3306/DBNAME"
```

```
POST /save_analysis    body: {"algo": "...", "step": 10, "n_max": 10000}
GET  /analyses          list saved rows (id, algorithm_name, input_size, step_size,
                         started_at, finished_at, duration_seconds, big_o, plot_path)
GET  /analyses/<id>     one saved row
```

Example:
```
curl -X POST "http://localhost:8000/save_analysis" -H "Content-Type: application/json" -d "{\"algo\":\"linear_search\",\"step\":10,\"n_max\":10000}"
curl "http://localhost:8000/analyses"
curl "http://localhost:8000/analyses/1"
```
