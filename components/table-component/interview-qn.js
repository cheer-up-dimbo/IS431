// Guiding Questions Table
new gridjs.Grid({
  columns: ["Segment", "Category", "Guiding Questions"],
  data: [
    // Recreational Boxers
    ["Recreational Boxers", "Motivation", "Why did you decide to train boxing, and why not sign-up for a boxing gym-membership?"],
    ["", "Pain Points", "What are the challenges you face when training without a boxing gym?"],
    ["", "Opportunities", "What kind of support or tools would make your training more effective?"],

    // Recreational Boxers at Boxing Gyms
    ["Recreational Boxers at Boxing Gyms", "Motivation", "What aspects of boxing do you enjoy the most?"],
    ["", "Pain Points", "What are some challenges you face during boxing?"],
    ["", "Training Frequency & Consistency", "How often do you train each week, and what would make you train more consistently?"],

    // Competing Boxers
    ["Competing Boxers", "Motivation", "What do you enjoy most about boxing at a competitive level?"],
    ["", "Pain Points", "Are there any challenges you face from your current training routines?"],
    ["", "Future Prospect", "What kind of change/innovation would you want to see in boxing training/boxing equipment?"],
    ["", "Competitive Edge", "What special training does competitive boxers do that casual boxers don't do?"],

    // Coaches
    ["Coaches", "Pain Points", "Are there current bottlenecks in training or your training environment (equipment availability, gym space, scheduling)?"],
    ["", "Training Engagement & Essentials", "What drills or training methods do your boxers find most engaging?"],

    // Boxing Gym Owners
    ["Boxing Gym Owners", "Business Drivers", "What's the most popular class or training format in your gym?"],
    ["", "Pain Points", "What are the biggest challenges in running your gym (cost, staffing, retention)?"],
    ["", "Equipment Decisions", "What is the most you would invest into a boxing equipment?"],

    // Parents of Young Boxers
    ["Parents of Young Boxers", "Motivation", "What made you decide to enroll your child in boxing?"],
    ["", "Concerns & Pain Points", "Do you ever worry about your child's safety when sparring or training?"],
    ["", "Future Outlook", "If your child wanted to pursue boxing more seriously, would you support it? Why?"],
  ],

  pagination: {
    // set higher than total rows so groups don't split across pages
    limit: 20
  },

  style: {
    table: {
      border: "1px solid #ccc"
    },
    th: {
      background: "#fafafa",
      borderBottom: "1px solid #ccc",
      fontWeight: "bold"
    },
    td: {
      borderBottom: "1px solid #eee"
    }
  }
}).render(document.getElementById("interview-qn"));
