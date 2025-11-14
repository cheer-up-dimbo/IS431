console.log("boxer-pie.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOMContentLoaded fired in boxer-pie.js");

  const ctx = document.getElementById("boxer-pie");
  console.log("ctx in boxer-pie.js:", ctx);
  if (!ctx) return;

  const labels = [
    "Lack of Training Partners",
    "Slow Progress",
    "Injury-Prone",
    "Limited Coaching Attention",
    "Time Commitment",
    "Unmotivated",
    "Tracking Progress"
  ];

  const values = [12, 11, 8, 8, 7, 5, 2];

  console.log("Chart type:", typeof Chart);

  new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [{ data: values }]
    },
    options: {
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const value = context.raw;
              const percent = ((value / total) * 100).toFixed(1);
              return `${context.label}: ${percent}% (${value})`;
            }
          }
        }
      }
    }
  });
});
