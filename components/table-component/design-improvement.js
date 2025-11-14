document.addEventListener("DOMContentLoaded", () => {
  new gridjs.Grid({
    columns: [
    { name: "Proposed Product/Service", width: "25%" },
    { name: "Existing Features & Feedback of Competitor’s Offerings", width: "35%" },
    { name: "Design Improvement", width: "40%" }
    ],

    data: [
      [
        "Performance Analytics",
        `
1. Progress tracking  
2. Strike pads with impact sensors  
3. Competitive leaderboard and multi-user modes
        `,
        `
1. Refined into a performance quantification system that records punch power, accuracy, and timing with visual analytics.  
2. Integrated into a full performance measurement system, syncing impact data with computer vision tracking.  
3. Performance dashboards that promote motivation.
        `
      ],

      [
        "Intelligent Training System",
        `
1. Complaints of “no haptic feedback” and “stationary base limits realism”  
2. Negative review: “Cannot replace a real partner”
        `,
        `
1. Addressed through active arm actuation, rotational motion, and haptic feedback to simulate real incoming strikes safely.  
2. Responded with CV-based opponent behaviour and reactive movements that replicate human-like responses.
        `
      ],

      [
        "Skill Progression Studio",
        `
1. On-screen live and 3D animated coaching  
2. Variety of training modes (Cardio, Mitts, Sparring, Core, Combo)
        `,
        `
1. Translated into modular training programs and guided training drills with real-time AI assistance for structured learning.  
2. Expanded into progressive training modules that blend offensive, defensive, and reactive exercises.
        `
      ],

      [
        "Adaptive Fight Intelligence",
        `
1. Evading target that dodges punches in real time  
2. Voice coaching & real-time cues
        `,
        `
1. Enhanced into a responsive counterpunching system that reacts dynamically to user attacks, mimicking opponents.  
2. Embedded as auditory and visual feedback mechanisms that reinforce correct form and rhythm.
        `
      ],

      [
        "Modular Boxing Platform",
        `
1. Height-adjustable frame, multiple strike zones, stance selection  
2. Commercial-grade materials and glide wheels for portability  
3. Negative review: “Extremely expensive” & “too bulky for gym use”
        `,
        `
1. Reimagined into an adjustable, safe, and durable platform that fits all user heights and allows real punching interaction during or after class.  
2. Carried forward to support gym and home usage without compromising safety or durability.  
3. Simplified into a cost-efficient design suitable for both gym and home environments.
        `
      ]
    ],
    style: {
      table: { "white-space": "pre-wrap" }
    }
  }).render(document.getElementById("design-improvement"));
});
