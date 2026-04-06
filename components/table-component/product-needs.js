new gridjs.Grid({
  columns: ["Design Improvement", "Product Needs"],
  data: [
    // 1 — BLUE ROW
    [
      `Performance Analytics
1. Refined into a performance quantification system that records punch power, accuracy, and timing.
2. Integrated into a full performance measurement system syncing impact data with CV tracking.
3. Performance dashboards that promote motivation.`,
      `1. The product needs to record punch power, accuracy, and timing using sensors with visual analytics.
2. The product needs to synchronize sensor data with computer vision for real-time insights.
3. The product must display dashboards that visualize stats and motivate user progress.`
    ],

    // 2 — GREEN ROW
    [
      `Realistic Training Partner
1. Active arm actuation, rotational motion, and haptic feedback simulate real strikes safely.
2. CV-based opponent behaviour for human-like reactive movements.`,
      `1. The product needs active arm actuation, rotational motion, and haptic feedback for realistic sparring.
2. The product needs computer vision to trigger reactions that mimic human opponents.`
    ],

    // 3 — RED ROW
    [
      `Skill Progression Studio
1. Modular training programs and guided drills with AI assistance.
2. Progressive modules blending offensive, defensive, and reactive exercises.`,
      `1. The product requires modular programs with AI-guided drills for structured development.
2. The product needs progressive modules that combine offensive, defensive, and reactive techniques.`
    ],

    // 4 — PURPLE ROW
    [
      `Adaptive Fight Intelligence
1. Responsive counterpunching system reacting dynamically.
2. Auditory + visual cues reinforcing rhythm and form.`,
      `1. The product must detect and counter user attacks using CV and arm actuation in real time.
2. The product needs auditory and visual cues that reinforce proper rhythm, timing, and technique.`
    ],

    // 5 — GREY ROW
    [
      `Modular Boxing Platform
1. Adjustable, safe, durable platform for all heights.
2. Supports gym + home use without losing durability.
3. Cost-efficient design.`,
      `1. The product must be height-adjustable, safe, and durable for real punching interaction.
2. The product must remain portable and suitable for gym and home environments.
3. The product must be cost-effective for accessibility.`
    ]
  ],
  style: {
    table: { "white-space": "pre-wrap" },
    td: { "vertical-align": "top", "padding": "10px" }
  }
}).render(document.getElementById("product-needs"));
