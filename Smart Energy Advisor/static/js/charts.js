// Chart.js Configurations for Smart Energy Advisor

document.addEventListener("DOMContentLoaded", () => {
    // Check if graph data is injected
    if (!window.energyGraphData) return;
    
    const data = window.energyGraphData;
    
    // ----------------------------------------------------
    // Chart 1: Monthly Consumption (Line Chart)
    // ----------------------------------------------------
    const ctxConsumption = document.getElementById("consumptionChart");
    if (ctxConsumption) {
        new Chart(ctxConsumption.getContext("2d"), {
            type: "line",
            data: {
                labels: data.months,
                datasets: [{
                    label: "Electricity Consumption (kWh)",
                    data: data.consumption,
                    borderColor: "#10b981", // Emerald Green
                    backgroundColor: "rgba(16, 185, 129, 0.08)",
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: "#047857"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: { color: "rgba(226, 232, 240, 0.8)" } }
                }
            }
        });
    }
    
    // ----------------------------------------------------
    // Chart 2: Monthly Bills (Bar Chart)
    // ----------------------------------------------------
    const ctxBill = document.getElementById("billChart");
    if (ctxBill) {
        new Chart(ctxBill.getContext("2d"), {
            type: "bar",
            data: {
                labels: data.months,
                datasets: [{
                    label: "Monthly Bill (₹)",
                    data: data.bills,
                    backgroundColor: "#3b82f6", // Accent Blue
                    borderRadius: 8,
                    maxBarThickness: 35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: { color: "rgba(226, 232, 240, 0.8)" } }
                }
            }
        });
    }
    
    // ----------------------------------------------------
    // Chart 3: Appliance Allocation (Doughnut Chart)
    // ----------------------------------------------------
    const ctxAppliance = document.getElementById("applianceChart");
    if (ctxAppliance) {
        new Chart(ctxAppliance.getContext("2d"), {
            type: "doughnut",
            data: {
                labels: data.appliances,
                datasets: [{
                    data: data.appliance_values,
                    backgroundColor: [
                        "#047857", // Dark Emerald
                        "#10b981", // Emerald
                        "#3b82f6", // Blue
                        "#f59e0b", // Amber
                        "#64748b"  // Slate
                    ],
                    borderWidth: 2,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            boxWidth: 12,
                            padding: 15,
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }
    
    // ----------------------------------------------------
    // Chart 4: Prediction Trend (Double Line Bounds)
    // ----------------------------------------------------
    const ctxPredictionTrend = document.getElementById("predictionTrendChart");
    if (ctxPredictionTrend) {
        // Calculate mock future trend bounds based on latest consumption
        const latestVal = data.consumption[data.consumption.length - 1];
        const monthsFuture = ["Current Month", "Month +1", "Month +2", "Month +3"];
        
        // Dynamic simulated projection ranges
        const expected = [latestVal, latestVal * 0.96, latestVal * 0.94, latestVal * 0.93];
        const upperBound = [latestVal, latestVal * 1.05, latestVal * 1.10, latestVal * 1.12];
        const lowerBound = [latestVal, latestVal * 0.90, latestVal * 0.85, latestVal * 0.82];
        
        new Chart(ctxPredictionTrend.getContext("2d"), {
            type: "line",
            data: {
                labels: monthsFuture,
                datasets: [
                    {
                        label: "Expected Forecast",
                        data: expected,
                        borderColor: "#10b981",
                        borderWidth: 2.5,
                        fill: false,
                        tension: 0.3
                    },
                    {
                        label: "Upper Bound (High Load)",
                        data: upperBound,
                        borderColor: "rgba(244, 63, 94, 0.4)",
                        borderDash: [5, 5],
                        borderWidth: 1.5,
                        fill: false
                    },
                    {
                        label: "Lower Bound (Efficient)",
                        data: lowerBound,
                        borderColor: "rgba(59, 130, 246, 0.4)",
                        borderDash: [5, 5],
                        borderWidth: 1.5,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top",
                        labels: { boxWidth: 12, font: { size: 10 } }
                    }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: { color: "rgba(226, 232, 240, 0.8)" } }
                }
            }
        });
    }
    
    // ----------------------------------------------------
    // Chart 5: Weekly Energy Load (Bar Graph)
    // ----------------------------------------------------
    const ctxWeekly = document.getElementById("weeklyLoadChart");
    if (ctxWeekly) {
        const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        // Simulated load shifts peaking on weekends
        const weekdayLoad = [18.5, 17.2, 19.0, 18.0, 21.5, 27.2, 29.5];
        
        new Chart(ctxWeekly.getContext("2d"), {
            type: "bar",
            data: {
                labels: weekdays,
                datasets: [{
                    label: "Daily Consumption (kWh)",
                    data: weekdayLoad,
                    backgroundColor: "rgba(16, 185, 129, 0.85)",
                    hoverBackgroundColor: "#059669",
                    borderRadius: 6,
                    maxBarThickness: 50
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: {
                        grid: { color: "rgba(226, 232, 240, 0.8)" },
                        ticks: { callback: value => value + " kWh" }
                    }
                }
            }
        });
    }
});
