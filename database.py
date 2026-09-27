from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

COMPLEXITY_LABELS = {
    "linear_search": "O(n)",
    "binary_search": "O(log n)",
    "bubble_sort": "O(n^2)",
    "nested_loops": "O(n^2)",
    "selection_sort": "O(n^2)",
    "merge_sort": "O(n log n)",
    "quick_sort": "O(n log n)",
    "stack_push_pop": "O(n)",
    "queue_enqueue_dequeue": "O(n)",
    "queue_naive_dequeue": "O(n^2)",
}


class AnalysisRecord(db.Model):
    __tablename__ = "analysis_records"

    id = db.Column(db.Integer, primary_key=True)
    algorithm_name = db.Column(db.String(50), nullable=False)
    input_size = db.Column(db.Integer, nullable=False)
    step_size = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.Float, nullable=False)
    finished_at = db.Column(db.Float, nullable=False)
    duration_seconds = db.Column(db.Float, nullable=False)
    big_o = db.Column(db.String(20), nullable=False)
    plot_path = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "algorithm_name": self.algorithm_name,
            "input_size": self.input_size,
            "step_size": self.step_size,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "big_o": self.big_o,
            "plot_path": self.plot_path,
        }
