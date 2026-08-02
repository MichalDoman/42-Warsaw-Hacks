const dashboardData = window.dashboardData ?? {
    hourLabels: [],
    hourlyLoginActivity: [],
    peakLoginHour: null,
};

const peakOrbitCanvas =
    document.getElementById("peakOrbitChart");

if (
    peakOrbitCanvas
    && typeof Chart !== "undefined"
) {
    const peakHour =
        dashboardData.peakLoginHour?.hour ?? null;

    const pointColors =
        dashboardData.hourlyLoginActivity.map(
            (_, index) => (
                index === peakHour
                    ? "#ffd84d"
                    : "#5cd6ff"
            ),
        );

    const pointRadii =
        dashboardData.hourlyLoginActivity.map(
            (_, index) => (
                index === peakHour
                    ? 7
                    : 3
            ),
        );

    new Chart(peakOrbitCanvas, {
        type: "line",

        data: {
            labels: dashboardData.hourLabels,

            datasets: [
                {
                    label: "Unique logins",
                    data:
                        dashboardData
                            .hourlyLoginActivity,
                    borderColor: "#5cd6ff",
                    backgroundColor:
                        "rgba(92, 214, 255, 0.09)",
                    borderWidth: 3,
                    tension: 0.38,
                    fill: true,
                    pointRadius: pointRadii,
                    pointHoverRadius: 7,
                    pointBackgroundColor:
                        pointColors,
                    pointBorderColor: "#0b1025",
                    pointBorderWidth: 2,
                },
            ],
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            interaction: {
                intersect: false,
                mode: "index",
            },

            plugins: {
                legend: {
                    display: false,
                },

                tooltip: {
                    backgroundColor:
                        "rgba(11, 16, 37, 0.96)",
                    borderColor:
                        "rgba(92, 214, 255, 0.3)",
                    borderWidth: 1,
                    titleColor: "#ffffff",
                    bodyColor: "#c7d3f5",

                    callbacks: {
                        label(context) {
                            const value = context.raw;

                            return (
                                `${value} unique `
                                + (
                                    value === 1
                                        ? "student"
                                        : "students"
                                )
                            );
                        },
                    },
                },
            },

            scales: {
                x: {
                    grid: {
                        display: false,
                    },

                    ticks: {
                        color: "#7f8db7",
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 12,
                    },

                    border: {
                        color:
                            "rgba(255, 255, 255, 0.07)",
                    },
                },

                y: {
                    beginAtZero: true,

                    suggestedMax: 5,

                    grid: {
                        color:
                            "rgba(255, 255, 255, 0.055)",
                    },

                    ticks: {
                        color: "#7f8db7",
                        precision: 0,
                        stepSize: 1,
                    },

                    border: {
                        display: false,
                    },
                },
            },
        },
    });
}

const refreshButton =
    document.getElementById("refreshButton");

if (refreshButton) {
    refreshButton.addEventListener(
        "click",
        () => window.location.reload(),
    );
}

const oneHour = 60 * 60 * 1000;

window.setTimeout(
    () => window.location.reload(),
    oneHour,
);