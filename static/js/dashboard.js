const dashboardData = window.dashboardData ?? { xpValues: [], coalitionCounts: {} };

const coalitionColors = {
    orionis: "#9068d8",
    lunaria: "#74c9ec",
    unitterax: "#f1cf4f",
};

const xpCanvas = document.getElementById("xpChart");
if (xpCanvas && typeof Chart !== "undefined") {
    new Chart(xpCanvas, {
        type: "line",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            datasets: [{
                label: "XP activity",
                data: dashboardData.xpValues,
                borderColor: "#27344a",
                backgroundColor: "rgba(39, 52, 74, 0.08)",
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { x: { grid: { display: false } }, y: { beginAtZero: true } },
        },
    });
}

const coalitionCanvas = document.getElementById("coalitionChart");
if (coalitionCanvas && typeof Chart !== "undefined") {
    const filteredEntries = Object.entries(dashboardData.coalitionCounts)
        .filter(([coalition]) => coalition !== "unknown");
    const labels = filteredEntries.map(([coalition]) => coalition);
    const values = filteredEntries.map(([, count]) => count);

    new Chart(coalitionCanvas, {
        type: "doughnut",
        data: {
            labels: labels.map((coalition) => coalition.charAt(0).toUpperCase() + coalition.slice(1)),
            datasets: [{
                data: values,
                backgroundColor: labels.map((coalition) => coalitionColors[coalition]),
                borderColor: "#ffffff",
                borderWidth: 5,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "62%",
            plugins: { legend: { position: "bottom", labels: { usePointStyle: true, padding: 18 } } },
        },
    });
}

const refreshButton = document.getElementById("refreshButton");
if (refreshButton) {
    refreshButton.addEventListener("click", () => window.location.reload());
}

window.setTimeout(() => window.location.reload(), 60 * 60 * 1000);
