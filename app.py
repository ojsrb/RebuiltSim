"""
Flask web server for FRC 2026 Strategy Simulator.
Provides a web UI with sliders to adjust robot parameters.
"""

from flask import Flask, render_template, request, jsonify
from simulator import run_simulation, STRATEGY_INFO

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template('index.html')


@app.route('/simulate', methods=['POST'])
def simulate():
    """
    Run simulation with provided robot configurations.

    Expected JSON payload:
    {
        "robots": [
            {
                "alliance": "RED" or "BLUE",
                "shootSpeed": float,
                "intakeSpeed": float,
                "driveSpeed": float,
                "capacity": int,
                "preload": bool,
                "strategy": str
            },
            ... (6 robots total)
        ]
    }
    """
    try:
        data = request.get_json()
        robot_configs = data.get('robots', [])

        # Allow 0-6 robots for flexible testing (1v0, 2v1, etc.)
        if len(robot_configs) > 6:
            return jsonify({'error': 'Maximum 6 robots allowed'}), 400

        result = run_simulation(robot_configs)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/strategies')
def strategies():
    """Return list of available strategies with descriptions."""
    return jsonify({'strategies': STRATEGY_INFO})


if __name__ == '__main__':
    print("Starting FRC 2026 Strategy Simulator...")
    print("Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001)
