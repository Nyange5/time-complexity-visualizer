# Time Complexity Visualizer (Flask)

A Flask endpoint that times an algorithm for growing input sizes, plots the running time,
saves a PNG snapshot locally and returns the image as a base64 string in the JSON response.

## Run
```
pip install -r requirements.txt
python time_complexity_visualizer.py
```

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
`selection_sort`, `merge_sort`, `quick_sort`

## Response (JSON)
`algo`, `n_max`, `step` (step actually used), `sizes`, `times` (seconds),
`image_path` (saved in `snapshots/`) and `image_base64` (PNG encoded as base64).