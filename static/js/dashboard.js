const dashboardData = window.dashboardData ?? { xpValues: [], coalitionCounts: {} };

const coalitionColors = {
    orionis: "#a970ff",
    lunaria: "#5cd6ff",
    unitterax: "#ffd84d",
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
                borderColor: "#5cd6ff",
                backgroundColor: "rgba(92, 214, 255, 0.09)",
                borderWidth: 3,
                tension: 0.42,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: "#0b1025",
                pointBorderColor: "#a970ff",
                pointBorderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { intersect: false, mode: "index" },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "rgba(11, 16, 37, 0.96)",
                    borderColor: "rgba(92, 214, 255, 0.3)",
                    borderWidth: 1,
                    titleColor: "#ffffff",
                    bodyColor: "#c7d3f5",
                },
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: "#7f8db7" },
                    border: { color: "rgba(255,255,255,0.07)" },
                },
                y: {
                    beginAtZero: true,
                    grid: { color: "rgba(255,255,255,0.055)" },
                    ticks: { color: "#7f8db7" },
                    border: { display: false },
                },
            },
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
                borderColor: "#0b1025",
                borderWidth: 7,
                hoverOffset: 8,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "66%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: "#aeb9db",
                        usePointStyle: true,
                        pointStyle: "circle",
                        padding: 18,
                    },
                },
                tooltip: {
                    backgroundColor: "rgba(11, 16, 37, 0.96)",
                    borderColor: "rgba(157, 184, 255, 0.25)",
                    borderWidth: 1,
                    titleColor: "#ffffff",
                    bodyColor: "#c7d3f5",
                },
            },
        },
    });
}

const refreshButton = document.getElementById("refreshButton");
if (refreshButton) {
    refreshButton.addEventListener("click", () => window.location.reload());
}

window.setTimeout(() => window.location.reload(), 60 * 60 * 1000);
