const mdToHtml = (text) => 
  text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

new gridjs.Grid({
  columns: [
    "Competitor",
    "Product Features",
    { 
      name: "Reviews",
      formatter: cell => gridjs.html(mdToHtml(cell))
    }
  ],

  data: [
    [
      "Nexersys",
      `
On-Screen Live & 3D animated coaching
- To coach users
Bilateral Head Pad Movement
- Reduces force translation
Multiple Strike Zones
- Supports different punches
Variety of Training Modes
- Cardio, Strike, Mitts, Sparring, Core
Skills Assessment
- Tracks performance
Height-adjustable frame
- Fits all users
Strike pads with impact sensors
- Measures punch output
Commercial-grade frame
- Durability
Glide wheels
- Portability
      `,
      mdToHtml(`
**Positive**
Multi-user leaderboard  
- Boosts motivation

**Negative**
Unstable when punched  
- Not suitable for gyms  
No haptic feedback  
- Lacks sparring realism  
Strike pads unrealistic angles
- Poor simulation
      `)
    ],

    [
      "STRYK RXT-1",
      `
Practice / Spar / Combo modes  
- Variety  
Adjustable intensity / speed  
- Fits all skill levels  
Stance selection  
- Southpaw / orthodox  
4 foam arms, head, torso  
- Many strike targets  
Wall-mounted 12" height adjust  
- Fits all heights
      `,
      mdToHtml(`
**Positive**
Great for conditioning  
- Improves reaction time  
Accessible anytime  
- Home-friendly  
Builds defensive habits  
- Slipping / weaving / ducking

**Negative**
Cannot replace real partner  
Stationary  
- No footwork
      `)
    ],

    [
      "BotBoxer",
      `
AI punch tracking  
- Predicts punches  
Evading target  
- Dodges / ducks  
Punch force & velocity  
- Analytics  
Voice coaching  
- Real-time cues  
75 microsecond reaction  
- Extreme realism  
Cloud progress app  
- Tracks improvement
      `,
      mdToHtml(`
**Positive**
True interactive sparring

**Negative**
~$25,000  
- Too expensive  
Large base  
- Limits footwork  
No robotic arms  
- Low sparring realism  
No punchable surface  
- Reduces stress-relief
      `)
    ]
  ],

  style: {
    table: { "white-space": "pre-wrap" }
  }
}).render(document.getElementById("competitor-table"));
