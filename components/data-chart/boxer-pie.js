(function() {
  function renderBoxerPie() {
    const ctx = document.getElementById("boxer-pie");
    if (!ctx) return;

    const labels = [
      "Limited Coaching Attention",
      "Lack of Training Partners",
      "Slow Progress",
      "Time Commitment",
      "Injury-Prone",
      "Unmotivated",
      "Tracking Progress"
    ];

    const values = [40, 38, 36, 22, 18, 14, 14];
    const totalRespondents = 50;

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
                const percent = ((value / totalRespondents) * 100).toFixed(1);
                return `${context.label}: ${percent}% (${value} of ${totalRespondents} boxers)`;
              }
            }
          }
        }
      }
    });
  }

  // Run immediately if DOM is ready, otherwise wait
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderBoxerPie);
  } else {
    renderBoxerPie();
  }
})();
