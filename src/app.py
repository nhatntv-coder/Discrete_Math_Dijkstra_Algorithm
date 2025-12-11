from flask import Flask, render_template, request, jsonify

from algorithms.dijkstra import dijkstra_segment
from algorithms.bfs import bfs_segment
from algorithms.dfs import dfs_segment
from algorithms.multipoint import run_multi_point_path

from utils.parsing import prepare_grid, get_points_list

app = Flask(__name__)

ALGORITHMS = {
    "dijkstra": dijkstra_segment,
    "bfs": bfs_segment,
    "dfs": dfs_segment
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run_algorithm", methods=["POST"])
def run_algorithm():
    data = request.json
    grid = prepare_grid(data)
    points = get_points_list(data)

    algo = data["algorithm"]
    if algo not in ALGORITHMS:
        return jsonify({"error": "Invalid algorithm"}), 400
    
    path, explored, cost = run_multi_point_path(ALGORITHMS[algo], grid, points)

    return jsonify({
        "path": path,
        "explored": explored,
        "cost": cost,
        "nodes_explored": len(explored)
    })

@app.route("/run_all_simultaneous", methods=["POST"])
def run_all_simultaneous():
    data = request.json
    grid = prepare_grid(data)
    points = get_points_list(data)

    results = {}
    for name, func in ALGORITHMS.items():
        path, explored, cost = run_multi_point_path(func, grid, points)
        results[name] = {
            "path": path,
            "explored": explored,
            "cost": cost,
            "nodes_explored": len(explored),
            "path_length": len(path)
        }

    return jsonify(results)

@app.route("/compare_all", methods=["POST"])
def compare_all():
    return run_all_simultaneous()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
