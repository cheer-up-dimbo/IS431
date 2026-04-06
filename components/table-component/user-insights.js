// customer-profile-table.js
// Customer Profile & User Insights Table

new gridjs.Grid({
  columns: [
    "Customer Profile",
    {
      name: "User Insights",
      formatter: cell => gridjs.html(cell)
    }
  ],
  data: [
    [
      "Boxing-Gym Boxers",
      `<ul style="margin:0; padding-left:18px;">
<li>Motivated by competitiveness, discipline, and mastery</li>
<li>Schedule conflicts interfere with training regularity</li>
<li>Limited coaching feedback in packed group classes</li>
<li>Difficulty finding regular sparring partners of matched skill</li>
<li>Disconnect between data-driven knowledge and physical training; boxers want quantifiable progress monitoring</li>
<li>Prefer technology that enhances gym experience rather than replacing instructors</li>
</ul>`
    ],
    [
      "Training Support Stakeholders",
      `<ul style="margin:0; padding-left:18px;">
<li>Coaches struggle to provide individualised attention across mixed skill levels</li>
<li>Gym owners face high operational costs, scheduling conflicts, and space limitations</li>
<li>Parents prioritise child safety during sparring and training</li>
<li>Universal desire for tools that improve learning, safety, and scalability with reliable feedback and injury prevention</li>
</ul>`
    ]
  ]
}).render(document.getElementById("user-insights"));
