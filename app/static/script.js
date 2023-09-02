document.addEventListener("DOMContentLoaded", function() {
    let hasRun = false; // flag to check if the simulation has been run
    const runSimulationButton = document.getElementById("run-simulation");
    
    runSimulationButton.addEventListener("click", function() {
        if (hasRun) {
            location.reload();
            return;
        }

        runSimulationButton.disabled = true;
        runSimulationButton.innerText = "Running...";

        document.getElementById("functions-plot").src = "";
        document.getElementById("distributions-plot").src = "";

        const menUsers = document.getElementById("men-users").value;
        const menSwipes = document.getElementById("men-swipes").value;
        const menFormula = document.getElementById("men-formula").value;

        const womenUsers = document.getElementById("women-users").value;
        const womenSwipes = document.getElementById("women-swipes").value;
        const womenFormula = document.getElementById("women-formula").value;

        const payload = {
            men_users: menUsers,
            men_swipes: menSwipes,
            men_formula: menFormula,
            women_users: womenUsers,
            women_swipes: womenSwipes,
            women_formula: womenFormula
        };

        fetch("/run_simulation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            const statsTableDiv = document.getElementById("stats-table");
            const stats = data.stats;

            const tableHTML = `
            <h2>Simulation Stats</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Men</th>
                        <th>Women</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Likes Mean</td>
                        <td>${stats.men_likes_mean}</td>
                        <td>${stats.women_likes_mean}</td>
                    </tr>
                    <tr>
                        <td>Likes Median</td>
                        <td>${stats.men_likes_median}</td>
                        <td>${stats.women_likes_median}</td>
                    </tr>
                    <tr>
                        <td>Matches Mean</td>
                        <td>${stats.men_matches_mean}</td>
                        <td>${stats.women_matches_mean}</td>
                    </tr>
                    <tr>
                        <td>Matches Median</td>
                        <td>${stats.men_matches_median}</td>
                        <td>${stats.women_matches_median}</td>
                    </tr>
                </tbody>
            </table>`;

            statsTableDiv.innerHTML = tableHTML;

            runSimulationButton.disabled = false;

            document.getElementById("functions-plot").src = "/plots/functions.png";
            document.getElementById("functions-plot").style.display = "block";
            document.getElementById("distributions-plot").src = "/plots/distributions.png";
            document.getElementById("distributions-plot").style.display = "block";

            runSimulationButton.innerText = "Refresh";
            hasRun = true;
        });
    });
});
