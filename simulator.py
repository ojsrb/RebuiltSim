"""
Simulation runner module - extracts simulation logic for reuse by CLI and web UI.
"""

from models.field import Field, fieldState
from models.robot import Robot, alliance, Instruction, action
import models.display as display


# Strategy name to object mapping
def get_strategy(name: str) -> Instruction:
    """Get an Instruction object by strategy name."""
    strategies = {
        'cycle': create_cycle_strategy(),
        'shuttle': create_shuttle_strategy(),
        'shoot': create_shoot_strategy(),
        'test': create_test_strategy(),
    }
    return strategies.get(name, create_cycle_strategy())


def create_cycle_strategy() -> Instruction:
    """Cycle between alliance area and neutral zone."""
    inst = Instruction()
    inst.activeHub([
        action.MOVE_HOME,
        action.INTAKE,
        action.SCORE,
        action.MOVE_NEUTRAL,
        action.INTAKE,
        action.MOVE_HOME,
        action.SCORE
    ])
    inst.inactiveHub([
        action.MOVE_NEUTRAL,
        action.PASS
    ])
    return inst


def create_shuttle_strategy() -> Instruction:
    """Camp in neutral zone and send fuel to alliance area."""
    inst = Instruction()
    inst.activeHub([
        action.MOVE_NEUTRAL,
        action.PASS
    ])
    inst.inactiveHub([
        action.MOVE_NEUTRAL,
        action.PASS
    ])
    return inst


def create_shoot_strategy() -> Instruction:
    """Camp in alliance zone and score delivered fuel."""
    inst = Instruction()
    inst.activeHub([
        action.MOVE_HOME,
        action.INTAKE,
        action.SCORE,
    ])
    inst.inactiveHub([
        action.MOVE_NEUTRAL,
        action.PASS
    ])
    return inst


def create_test_strategy() -> Instruction:
    """Test strategy - minimal shuttle behavior."""
    inst = Instruction()
    inst.activeHub([
        action.MOVE_NEUTRAL,
        action.PASS
    ])
    inst.inactiveHub([
        action.MOVE_NEUTRAL,
        action.PASS
    ])
    return inst


def run_simulation(robot_configs: list) -> dict:
    """
    Run simulation with given robot configurations.

    Args:
        robot_configs: List of 6 dicts with keys:
            - alliance: "RED" or "BLUE"
            - shootSpeed: float (fuel/second)
            - intakeSpeed: float (fuel/second)
            - driveSpeed: float (inches/second)
            - capacity: int
            - preload: bool
            - strategy: str ("cycle", "shuttle", "shoot", "test")

    Returns:
        dict with keys:
            - graph_base64: str (PNG image as base64)
            - redScore: int
            - blueScore: int
            - autoWinner: str
            - winner: str
    """
    # Reset graph data for fresh simulation
    display.reset_graph_data()

    # Initialize field (contains match variables and field stats)
    # Initial fuel: 0 red, 0 blue, 400 neutral, 0-0 score
    field = Field(0, 0, 400, 0, 0)

    # Create robots from configurations
    robots = []
    for config in robot_configs:
        color = alliance.RED if config['alliance'] == 'RED' else alliance.BLUE
        strategy = get_strategy(config['strategy'])

        robot = Robot(
            field=field,
            color=color,
            shootSpeed=config['shootSpeed'],
            intakeSpeed=config['intakeSpeed'],
            driveSpeed=config['driveSpeed'],
            capacity=config['capacity'],
            preload=config['preload'],
            instruction=strategy
        )
        robots.append(robot)

    # Run simulation loop
    frame = 0
    while True:
        # Update field state
        field.update(frame)

        # Update each robot
        for robot in robots:
            robot.tick()

        # Increment frame
        frame += 1

        # Update graph data
        display.update(field)

        # End simulation when match is over
        if field.state == fieldState.OVER:
            break

    # Generate results
    graph_base64 = display.generate_graph_base64(field)

    auto_winner = "Red" if field.redWonAuto else "Blue"
    if field.redScore > field.blueScore:
        winner = "Red"
    elif field.blueScore > field.redScore:
        winner = "Blue"
    else:
        winner = "Tie"

    return {
        'graph_base64': graph_base64,
        'redScore': field.redScore,
        'blueScore': field.blueScore,
        'autoWinner': auto_winner,
        'winner': winner
    }


# Strategy descriptions for UI
STRATEGY_INFO = [
    {
        'name': 'cycle',
        'description': 'Cycle between home and neutral zones. Score when active, shuttle when inactive.'
    },
    {
        'name': 'shuttle',
        'description': 'Stay in neutral zone and pass fuel to alliance zone.'
    },
    {
        'name': 'shoot',
        'description': 'Stay home and score delivered fuel when active, shuttle when inactive.'
    },
    {
        'name': 'test',
        'description': 'Test strategy - minimal shuttle behavior only.'
    }
]
