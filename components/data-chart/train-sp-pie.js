(function() {
  function renderTrainSpPie() {
    const ctx = document.getElementById("train-sp-pie");
    if (!ctx) return;

    const labels = [
      "Pad Work",
      "Defense Drills",
      "Technique Drills",
      "Sparring",
      "Bag Work"
    ];

    // Values scaled by priority (lower average rank = higher priority)
    // All 10 support stakeholders answered drill rankings
    const values = [10, 6, 6, 4, 2];
    const totalRespondents = 12;  // Total support stakeholders surveyed

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
                const value = context.raw;
                return `${context.label}: priority score ${value}/5`;
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
