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

const leaderboard =
    document.querySelector("[data-leaderboard]");

if (leaderboard) {
    const slides = Array.from(
        leaderboard.querySelectorAll(
            "[data-leaderboard-slide]",
        ),
    );

    const buttons = Array.from(
        leaderboard.querySelectorAll(
            "[data-leaderboard-button]",
        ),
    );

    const title = leaderboard.querySelector(
        "[data-leaderboard-title]",
    );

    const eyebrow = leaderboard.querySelector(
        "[data-leaderboard-eyebrow]",
    );

    const progress = leaderboard.querySelector(
        "[data-leaderboard-progress]",
    );

    const leaderboardContent = [
        {
            eyebrow: "WALLET SIGNALS",
            title: "Top 3 richest students",
        },
        {
            eyebrow: "COALITION COMMAND",
            title: "Leaders of every orbit",
        },
        {
            eyebrow: "EVALUATION RADAR",
            title: "Top 3 evaluators",
        },
    ];

    let activeSlide = 0;
    let rotationTimer = null;

    const rotationDelay = 8000;

    function restartProgressAnimation() {
        if (!progress) {
            return;
        }

        progress.style.animation = "none";

        void progress.offsetWidth;

        progress.style.animation = (
            `leaderboard-progress-fill `
            + `${rotationDelay}ms linear forwards`
        );
    }

    function showLeaderboardSlide(index) {
        activeSlide = index;

        slides.forEach((slide, slideIndex) => {
            const isActive = slideIndex === index;

            slide.hidden = !isActive;

            slide.classList.toggle(
                "leaderboard-slide-active",
                isActive,
            );
        });

        buttons.forEach((button, buttonIndex) => {
            const isActive = buttonIndex === index;

            button.classList.toggle(
                "leaderboard-dot-active",
                isActive,
            );

            button.setAttribute(
                "aria-selected",
                String(isActive),
            );
        });

        const content = leaderboardContent[index];

        if (title && content) {
            title.textContent = content.title;
        }

        if (eyebrow && content) {
            eyebrow.textContent = content.eyebrow;
        }

        restartProgressAnimation();
    }

    function startLeaderboardRotation() {
        window.clearInterval(rotationTimer);

        rotationTimer = window.setInterval(
            () => {
                const nextSlide =
                    (activeSlide + 1) % slides.length;

                showLeaderboardSlide(nextSlide);
            },
            rotationDelay,
        );
    }

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const selectedSlide = Number(
                button.dataset.leaderboardButton,
            );

            showLeaderboardSlide(selectedSlide);
            startLeaderboardRotation();
        });
    });

    leaderboard.addEventListener(
        "mouseenter",
        () => {
            window.clearInterval(rotationTimer);

            if (progress) {
                progress.style.animationPlayState =
                    "paused";
            }
        },
    );

    leaderboard.addEventListener(
        "mouseleave",
        () => {
            if (progress) {
                progress.style.animationPlayState =
                    "running";
            }

            startLeaderboardRotation();
        },
    );

    showLeaderboardSlide(0);
    startLeaderboardRotation();
}