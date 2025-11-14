console.log("train-sp-pie.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOMContentLoaded fired in train-sp-pie.js");

  const ctx = document.getElementById("train-sp-pie");
  console.log("ctx in boxer-pie.js:", ctx);
  if (!ctx) return;

  const labels = [
    "Pad Work",
    "Sparring",
    "Defense Drills",
    "Technique Drills",
    "Bag Work"
  ];

  const values = [3, 2, 2, 1,1];

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
