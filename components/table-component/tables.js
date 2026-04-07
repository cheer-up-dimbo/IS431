// Strike Types Table
new gridjs.Grid({
  columns: [{name: "Strike Type",width: "140px"},{name: "Motion",width: "499px"}],
  data: [
    [
      "Jab / Cross", 
      "A rapid, linear strike. The arm must simulate a coach swinging the noodle from a high, upright guard position downwards in a fast, direct path toward the user."
    ],
    [
      "Hook", 
      "A horizontal, arcing strike. The arm must lower the noodle to a horizontal (parallel to the floor) level and swing it inwards toward the side of the user's head."
    ],
    [
      "Uppercut", 
      "A rising strike. The arm must drop the noodle tip below the user's chin and swing it diagonally upwards, simulating an uppercut motion."
    ]
  ],
}).render(document.getElementById("table-strike-types"));
 
 // Robot Arm Specifications Table
new gridjs.Grid({
  columns: [
    { name: "Parameter",width: "152px"},{name: "Specification",width: "104px"},
    {name: "Rationale",width: "362px"}
  ],
  data: [
    [
      "Striking Speed", 
      "≤ 6.04 rad/s", 
      "Matches a high tempo striking rate"
    ],
    [
      "Training Stick Length", 
      "90 cm", 
      "Provides a substantial and realistic reach"
    ]
  ]
}).render(document.getElementById("table-robot-arm-specs"));

// Fidelity Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "16%",
      // This 'attributes' style overrides the global 'td' style
      // to center-align the cells in this column only.
      attributes: {
        'style': 'text-align: center; vertical-align: top;'
      }
    },
    { 
      name: "Requirement",
      width: "45%"
    },
    { 
      name: "Rationale",
      width: "37%"
    }
  ],
  
  // The 'rowspan' is flattened by repeating "Fidelity"
  data: [
    [
      "Fidelity", 
      "No obstruction of striking zones", 
      "Ensures training is realistic and effective"
    ],
    [
      "Fidelity", 
      "accurately simulate the arc, trajectory, and angle of all human punches (jabs, hooks, uppercuts).", 
      "Accurately simulate the arc, trajectory, and angle of all human punches (jabs, hooks, uppercuts)."
    ]
  ]
}).render(document.getElementById("table-fidelity-specs"));

// Padding Specifications Table
new gridjs.Grid({
  columns: [
    { name: "Parameter",
      width: "152px"},
    { name: "Specification",
      width: "104px"},
    { name: "Rationale",
      width: "362px"}
  ],
  data: [
    [
      "Padding Offset", 
      "40cm", 
      "Ensure safe boxing proximity to prevent tripping over the base"
    ]
  ]
}).render(document.getElementById("table-padding-specs"));

// Opponent Body Specifications Table
new gridjs.Grid({
  columns: [
    { name: "Parameter",
      width: "152px"},
    { name: "Requirements",
      width: "232px"},
    {name: "Rationale",
      width: "234px"}
  ],
  data: [
    [
      "Fidelity", 
      "Anatomically correct for key strike points (head, liver, celiac plexus)", 
      "Simulates a realistic opponent"
    ],
    [
      "Accuracy", 
      "Small, delimited target zones", 
      "Fosters proper technique and precision"
    ],
    [
      "Safety", 
      "Soft contact surface, high energy absorption", 
      "Prevents injury to the user and damage to the robot"
    ]
  ]
}).render(document.getElementById("table-opponent-body-specs"));

// Reliability Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "152px"
    },
    { 
      name: "Requirements",
      width: "232px"
    },
    { 
      name: "Rationale",
      width: "234px"
    }
  ],
  data: [
    [
      "Reliability", 
      "Anatomically correct for key strike points (head, liver, celiac plexus)", 
      "Simulates a realistic opponent"
    ]
  ]
}).render(document.getElementById("table-reliability-specs"));

// Motion Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "74px"
      
    },
    { 
      name: "Sub-Parameter", // The 2nd column under the 'Parameter' group
      width: "104px"
      
    },
    { 
      name: "Specification",
      width: "98px"
    },
    {
      name: "Rationale",
      width: "345px"
    }
  ],
  
  // Data is flattened. "Linear Motion" and "Rotation Motion" are repeated.
  data: [
    [
      "Linear Motion",
      "Peak Speed",
      "≤ 1 m/s",
      "Comparable to human walking / jab-step speed; responsive yet controllable"
    ],
    [
      "Linear Motion",
      "Stroke Length",
      "300 mm",
      "Provides meaningful range change without sweeping into bystanders"
    ],
    [
      "Rotation Motion",
      "Peak Speed",
      // Use gridjs.html() to render the line break
      gridjs.html("150°/s<br>(25 rpm)"),
      "Upper bound from self padwork experiments; adequate for pivot drills"
    ],
    [
      "Rotation Motion",
      "Yaw Angle",
      "± 90°",
      "Sufficient to re-present new attack/defence lines around the user"
    ]
  ]
}).render(document.getElementById("table-motion-specs"));

// Control & Durability Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "16%"
    },
    { 
      name: "Requirement",
      width: "45%"
    },
    { 
      name: "Rationale",
      width: "37%"
    }
  ],
  
  data: [
    [
      "Controllability", 
      "Smooth starts/stops and repeatable positioning", 
      "Preserves timing windows; avoids unpleasant jerks or overshoot"
    ],
    [
      "Pose stiffness under impact", 
      "High mechanical stiffness with minimal deflection", 
      "Maintains angle/position hold during punches for safety and realism"
    ],
    [
      "Shock tolerance", 
      "Survive repeated impacts without excessive backlash", 
      "Ensures durability and consistent behaviour over many training sessions"
    ]
  ]
}).render(document.getElementById("table-control-specs"));

// Base & Stability Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "16%"
    },
    { 
      name: "Requirement",
      width: "41%"
    },
    { 
      name: "Rationale",
      width: "42%"
    }
  ],
  
  data: [
    [
      "Base plan dimensions", 
      "Minimal footprint with safe front clearance", 
      "Preserves training area; reduces risk of stepping on or into the base"
    ],
    [
      "Stability margin", 
      "Overturning moment capacity > peak punch loads", 
      "Ensures robot will not tip under worst-case hits"
    ],
    [
      "Pivot / stance clearance", 
      "Free space at front corners", 
      "Allows realistic pivots and angle work without contacting the base"
    ]
  ]
}).render(document.getElementById("table-base-specs"));

// Vertical Lift (Stroke Length) Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "28%"
    },
    { 
      name: "Specification",
      width: "15%"
    },
    { 
      name: "Rationale",
      width: "56%"
    }
  ],
  
  data: [
    [
      "Stroke Length", 
      "400 mm", 
      "Matches average user height spread with ±20% range; aligns targets to head/torso zones"
    ]
  ]
}).render(document.getElementById("table-stroke-length-specs"));

// Vertical Lift (General) Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "16%"
    },
    { 
      name: "Requirement",
      width: "41%"
    },
    { 
      name: "Rationale",
      width: "42%"
    }
  ],
  
  data: [
    [
      "Axial load capacity", 
      "> total upper-body mass with safety margin", 
      "Prevents structural failure or excessive creep"
    ],
    [
      "Fail-safe behaviour", 
      "Self-locking / non-backdrivable under load", 
      "Avoids sudden collapses or uncontrolled descent even in the event of power loss or user error"
    ],
    [
      "Vertical stiffness", 
      "Minimal deflection and bounce under impacts", 
      "Preserves realistic strike feel and user confidence"
    ],
    [
      "Ease of adjustment", 
      "Intuitive manual adjustment for occasional use", 
      "Allows quick set-up between users without complex controls"
    ]
  ]
}).render(document.getElementById("table-vertical-lift-specs"));

// Subsystem Validation Table
new gridjs.Grid({
  columns: [
    { 
      name: "Subsystem",
      width: "140px"
    },
    { 
      name: "Purpose",
      width: "180px"
    },
    { 
      name: "Scope",
      width: "160px"
    },
    {
      name: "Approach",
      width: "180px"
    }
  ],
  
  data: [
    [
      gridjs.html("2DOF Arm<br>(Pitch + Yaw Motors)"),
      "Ensure smooth arm motion and correct striking behaviour.",
      "Motor speed/torque, positional accuracy, collision detection, repeatability.",
      "Encoder validation, repeated strike cycles, induced collision tests to detect torque/encoder spikes."
    ],
    [
      gridjs.html("Rotation Motor<br>(Torso Tracking)"),
      "Ensure torso rotates accurately to face user.",
      "Rotation angle accuracy, response speed, stability under load.",
      "Step-response testing, load-bearing trials, integrated CV-driven rotation tests."
    ],
    [
      gridjs.html("Translation Motor<br>(Pivoting System)"),
      "Validate forward/backward movement and safety.",
      "Linear travel accuracy, collision avoidance, load capacity.",
      "Rail motion tests, limit-switch verification, CV-guided safety tests against user proximity."
    ],
    [
      gridjs.html("Height Adjustment<br>(Jack System)"),
      "Confirm smooth and safe height adjustment for users of different heights.",
      "Vertical motion stability, load support, repeatability.",
      "Static/dynamic load tests, repeated adjustment cycles."
    ],
    [
      gridjs.html("Impact Sensors<br>(Head + Body)"),
      "Detect punch force and direction reliably.",
      "Sensitivity across placements/orientations, false positives, latency.",
      "Multi-angle punch tests, padding variation tests, calibration sweeps."
    ],
    [
      "User Input / GUI",
      "Validate user controls and interface interactions.",
      "Input reliability, response speed, mapping to robot behaviour.",
      "Button/menu testing, command-response tests, integration with motors."
    ],
    [
      "Full System Integration",
      "Ensure all subsystems operate correctly together.",
      "Timing synchronisation, safety behaviour, real-time performance.",
      "End-to-end tests, latency logging, full sparring simulations."
    ],
    [
      "User Testing & Fine-Tuning",
      "Evaluate real-world usability and safety; refine system.",
      "Responsiveness, comfort, clarity of feedback, failure cases.",
      "Guided user trials, structured feedback, iterative tuning of thresholds and model parameters."
    ]
  ]
}).render(document.getElementById("table-subsystem-validation"));

 // Robot Intelligence Table — replaced by inline HTML table in robot-intelligence.html
  // (Old Grid.js definition removed to prevent console errors)

  // Foam Specifications Table 1 (Measured)
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "119px"
    },
    { 
      name: "Symbol",
      width: "110px"
    },
    { 
      name: "Value",
      width: "247px"
    },
    {
      name: "Units",
      width: "159px"
    }
  ],
  
  data: [
    [
      "Length",
      "L",
      "580",
      "mm"
    ],
    [
      "Diameter",
      "D",
      "60",
      "mm"
    ],
    [
      "Mass",
      "M",
      "49.25",
      "g"
    ],
    [
      "Calculated Density",
      gridjs.html("Ρ <sub>mat</sub>"),
      "30",
      gridjs.html("kg/m <sup>3</sup>")
    ]
  ]
}).render(document.getElementById("table-foam-specs-1"));

// Foam Specifications Table 2 (Target)
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "120px"
    },
    { 
      name: "Symbol",
      width: "110px"
    },
    { 
      name: "Value",
      width: "247px"
    },
    {
      name: "Units",
      width: "159px"
    }
  ],
  
  data: [
    [
      "Length",
      "L",
      "900",
      "mm"
    ],
    [
      "Diameter",
      "D",
      "60",
      "mm"
    ],
    [
      "Density",
      gridjs.html("Ρ <sub>mat</sub>"),
      "30",
      gridjs.html("kg/m <sup>3</sup>")
    ],
    [
      "Calculated Mass",
      "M",
      "76.3",
      gridjs.html("g <sup></sup>")
    ]
  ]
}).render(document.getElementById("table-foam-specs-2"));

// Strike Speed Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "120px"
    },
    { 
      name: "Symbol",
      width: "110px"
    },
    { 
      name: "Value",
      width: "248px"
    },
    {
      name: "Units",
      width: "160px"
    }
  ],
  
  data: [
    [
      "Strike Angle",
      gridjs.html("ф <sub>strike</sub>"),
      "90",
      "degree"
    ],
    [
      "Number of Strikes",
      "n",
      "5",
      "Unitless"
    ],
    [
      "Duration",
      gridjs.html("T <sub>strikes</sub>"),
      "2.62",
      "s"
    ],
    [
      "Calculated Angular Speed",
      gridjs.html("ω"),
      "6.04",
      gridjs.html("rad/s <sup></sup>")
    ],
    [
      "Rotation Per Minute",
      "RPM",
      "57.7",
      "rotation/min"
    ]
  ]
}).render(document.getElementById("table-strike-speed-specs"));

// Angular Acceleration Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "121px"
    },
    { 
      name: "Symbol",
      width: "112px"
    },
    { 
      name: "Value",
      width: "251px"
    },
    {
      name: "Units",
      width: "161px"
    }
  ],
  
  data: [
    [
      "Time to full speed",
      "t",
      "0.25",
      "s"
    ],
    [
      "Angular Speed",
      gridjs.html("ω"),
      "6.04",
      "rad/s"
    ],
    [
      "Calculated Acceleration",
      gridjs.html("α"),
      "24.2",
      gridjs.html("rad/s <sup>2</sup>")
    ]
  ]
}).render(document.getElementById("table-acceleration-specs"));

// Drag Torque Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "122px"
    },
    { 
      name: "Symbol",
      width: "112px"
    },
    { 
      name: "Value",
      width: "251px"
    },
    {
      name: "Units",
      width: "162px"
    }
  ],
  
  data: [
    [
      "Diameter",
      "D",
      "60",
      "mm"
    ],
    [
      "Calculated Angular Speed",
      gridjs.html("ω"),
      "6.04",
      gridjs.html("rad/s <sup></sup>")
    ],
    [
      gridjs.html("Calculated<br>Tip Speed"),
      "u",
      "5.43",
      "m/s"
    ],
    [
      "Dynamic Viscosity of Air",
      gridjs.html("Ν <sub>air(15°)</sub>"),
      gridjs.html("1.81 x 10 <sup>-5</sup>"),
      gridjs.html("m<sup>2</sup>/s")
    ],
    [
      "Air Density",
      gridjs.html("Ρ <sub>air(15°)</sub>"),
      "1.225",
      gridjs.html("kg/m <sup>3</sup>")
    ],
    [
      "Reynolds Number",
      "Re",
      gridjs.html("1.8 x 10 <sup>4</sup>"),
      "unitless"
    ],
    [
      "Drag Coeff",
      gridjs.html("C <sub>d</sub>"),
      "1.2",
      "unitless"
    ],
    [
      "Drag Torque",
      gridjs.html("τ <sub>drag</sub>"),
      "0.215",
      "N∙m"
    ]
  ]
}).render(document.getElementById("table-drag-torque-specs"));

// Torque Specifications Table
new gridjs.Grid({
  columns: [
    { 
      name: "Parameter",
      width: "121px"
    },
    { 
      name: "Symbol",
      width: "112px"
    },
    { 
      name: "Value",
      width: "251px"
    },
    {
      name: "Units",
      width: "162px"
    }
  ],
  
  data: [
    [
      "Peak Torque",
      gridjs.html("Τ <sub>peak</sub>"),
      "1.26",
      gridjs.html("N∙m <sup></sup>")
    ],
    [
      "Continuous Torque",
      gridjs.html("T <sub>continuous</sub>"),
      "0.828",
      "N∙m"
    ],
    [
      "Rotation Per Minute",
      "RPM",
      "57.7",
      "rotation/minute"
    ]
  ]
}).render(document.getElementById("table-torque-specs"));
  