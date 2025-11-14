// customer-profile-table.js
// Customer Profile & User Insights Table

new gridjs.Grid({
  columns: ["Customer Profile", "User Insights"],
  data: [
    [
      "Boxing-Gym Boxers",
      `Boxers that train in gyms are motivated by competitiveness, discipline, and mastery, 
but they also complain about the restrictions of their training spaces. Many complain about 
schedule conflicts that interfere with training regularity, limited coaching feedback in packed 
classes, and trouble finding regular training partners of appropriate competence.

Additionally, there is a disconnect between data-driven knowledge and physical training, which 
makes boxers uncertain of their rate of improvement. Secure sparring training experiences and 
quantifiable performance monitoring are important to these users. They choose technology that 
enhances their gym experience, improving accuracy, accountability, and accessibility outside of 
regular gym hours rather than taking the place of instructors.`
    ],
    [
      "Training Support Stakeholders",
      `In group lessons, coaches find it difficult to provide individualized attention and to 
maintain engagement across a range of skill levels. Owners of gyms deal with high operational 
expenses, schedule conflicts, and space limitations. Parents seek out surroundings that place a 
high value on their children's safety.

The desire for training tools that can improve learning, safety, and scalability—systems that 
offer reliable feedback, lower the chance of injuries, and boost trainer productivity—is universal.`
    ]
  ]
}).render(document.getElementById("user-insights"));
