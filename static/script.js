// FRC 2026 Strategy Simulator - Frontend JavaScript

// Update slider value displays in real-time
document.addEventListener('DOMContentLoaded', function() {
    // Add input listeners to all range sliders
    document.querySelectorAll('input[type="range"]').forEach(slider => {
        slider.addEventListener('input', function() {
            const valueSpan = this.parentElement.querySelector('.value');
            if (valueSpan) {
                valueSpan.textContent = this.value;
            }
        });
    });

    // Add listeners to enable/disable checkboxes
    document.querySelectorAll('.enabled').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const card = this.closest('.robot-card');
            if (this.checked) {
                card.classList.remove('disabled');
            } else {
                card.classList.add('disabled');
            }
        });
    });
});

// Collect robot configurations from the form (only enabled robots)
function collectRobotConfigs() {
    const configs = [];

    // Robot indices and their alliances
    const robotAlliances = {
        0: 'RED', 1: 'RED', 2: 'RED',
        3: 'BLUE', 4: 'BLUE', 5: 'BLUE'
    };

    for (let i = 0; i < 6; i++) {
        const card = document.getElementById(`robot-${i}`);

        // Skip disabled robots
        const enabled = card.querySelector('.enabled').checked;
        if (!enabled) continue;

        const config = {
            alliance: robotAlliances[i],
            shootSpeed: parseFloat(card.querySelector('.shootSpeed').value),
            intakeSpeed: parseFloat(card.querySelector('.intakeSpeed').value),
            driveSpeed: parseFloat(card.querySelector('.driveSpeed').value),
            capacity: parseInt(card.querySelector('.capacity').value),
            preload: card.querySelector('.preload').checked,
            strategy: card.querySelector('.strategy').value
        };

        configs.push(config);
    }

    return configs;
}

// Run simulation with current parameters
async function runSimulation() {
    const button = document.getElementById('runSimulation');
    const loading = document.getElementById('loading');
    const graphImg = document.getElementById('graph');
    const placeholder = document.getElementById('placeholder');
    const scoreDiv = document.getElementById('score');

    // Disable button and show loading
    button.disabled = true;
    loading.classList.remove('hidden');
    scoreDiv.classList.add('hidden');

    try {
        const configs = collectRobotConfigs();

        const response = await fetch('/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ robots: configs })
        });

        if (!response.ok) {
            throw new Error('Simulation failed');
        }

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        // Display the graph
        graphImg.src = 'data:image/png;base64,' + result.graph_base64;
        graphImg.classList.remove('hidden');
        placeholder.classList.add('hidden');

        // Display the score
        scoreDiv.textContent = `${result.winner} wins! Red ${result.redScore} - Blue ${result.blueScore} (Auto: ${result.autoWinner})`;
        scoreDiv.classList.remove('hidden', 'red-wins', 'blue-wins', 'tie');

        if (result.winner === 'Red') {
            scoreDiv.classList.add('red-wins');
        } else if (result.winner === 'Blue') {
            scoreDiv.classList.add('blue-wins');
        } else {
            scoreDiv.classList.add('tie');
            scoreDiv.textContent = `Tie! Red ${result.redScore} - Blue ${result.blueScore} (Auto: ${result.autoWinner})`;
        }

    } catch (error) {
        console.error('Error running simulation:', error);
        alert('Error running simulation: ' + error.message);
    } finally {
        // Re-enable button and hide loading
        button.disabled = false;
        loading.classList.add('hidden');
    }
}
