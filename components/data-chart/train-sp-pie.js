(function() {
  function renderTrainSpPie() {
    const ctx = document.getElementById("train-sp-pie");
    if (!ctx) return;

    const labels = [
      "Pad Work",
      "Sparring",
      "Defense Drills",
      "Technique Drills",
      "Bag Work"
    ];

    const values = [3, 2, 2, 1, 1];

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
  }

  // Run immediately if DOM is ready, otherwise wait
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderTrainSpPie);
  } else {
    renderTrainSpPie();
  }
})();
