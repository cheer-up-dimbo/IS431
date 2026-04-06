**5.2.2.4.1 Design Ideation**

The ideation process for the rotation subsystem was not treated as a
single component-selection exercise. Instead, it progressed through a
sequence of design questions, where each stage of the yaw system was
compared against the most important needs of BoxBunny: realistic
re-angling behaviour, positional stiffness under punching, compact
packaging, manufacturability at prototype scale, and practical
integration with the wider lower mechanism. To make those trade-offs
explicit, **selection matrices** were used as a decision-support tool.

In this subsystem, the role of the selection matrix was not simply to
identify the "best" component numerically. Rather, it was used to
structure the progression from **system-level motion architecture** down
to **bearing selection**, then to **drive-transmission strategy**, and
finally to **supporting refinements for stability and deployment**. Each
matrix narrowed the solution space and informed the next stage of design
refinement.

**Concept selection matrix: lower-mechanism motion architecture**

  -------------------------------------------------------------------------------------------------------------------
  **Concept**             **Positional   **Motion   **Floor      **Integration   **Manufacturability**   **Final
                          stiffness      realism    dependence / with other                              decision**
                          under impact** for boxing slip risk**  subsystems**                            
                                         drills**                                                        
  ----------------------- -------------- ---------- ------------ --------------- ----------------------- ------------
  Omnidirectional-wheel   Moderate       High in    Poor         Moderate        Moderate                Rejected
  base                                   theory                                                          

  Differential-drive      Low to         Poor to    Poor         Moderate        High                    Rejected
  mobile base             moderate       moderate                                                        

  Decoupled yaw stage +   High           High       High         High            High                    Selected
  linear stage                                                                                           
  -------------------------------------------------------------------------------------------------------------------

This matrix was used to choose the **overall motion philosophy** of the
lower mechanism. Wheel-based solutions were rejected because they
introduce floor dependence, pose drift, and poorer stiffness under
repeated impacts. The **decoupled yaw stage plus linear stage** was
selected because it best matched the actual use case: it allows the
rotation axis to be designed specifically for combined loading while
preserving repeatable motion geometry.

**Concept selection matrix: rotary support / bearing concept**

  -----------------------------------------------------------------------------------------------------------------
  **Concept**    **Combined            **Rotational   **Availability / **Ease of       **Suitability   **Final
                 axial/radial/moment   stiffness**    cost**           integration**   for punching    decision**
                 capacity**                                                            environment**   
  -------------- --------------------- -------------- ---------------- --------------- --------------- ------------
  Lazy-Susan /   Low                   Low            High             High            Poor            Rejected
  turntable                                                                                            
  bearing                                                                                              

  Cross-roller   Excellent             Excellent      Poor             Moderate        High            Not selected
  bearing                                                                                              

  Four-point     High                  High           High             High            High            Selected
  contact                                                                                              
  slewing ring                                                                                         
  -----------------------------------------------------------------------------------------------------------------

This matrix was used to decide the **type of rotary support** for the
yaw stage. The lazy-Susan option was rejected because it is too loose
and too weak in overturning resistance. A cross-roller bearing was
attractive in stiffness but less favourable in cost and accessibility.
The **four-point contact slewing ring** was selected because it provides
the best balance of structural performance, prototype practicality, and
appropriate stiffness for the punching environment.

**Concept selection matrix: geared vs non-geared slewing-ring strategy**

  --------------------------------------------------------------------------------------------------------------
  **Concept**    **Structural   **Mass**   **Cost /     **Ease of    **Motor    **Design            **Final
                 capacity**                shipping**   handling**   power      appropriateness**   decision**
                                                                     demand**                       
  -------------- -------------- ---------- ------------ ------------ ---------- ------------------- ------------
  Geared slewing Excellent      Very poor  Very poor    Poor         Poor       Poor                Rejected
  ring                                                                                              
  (011.25.400)                                                                                      

  Non-geared     Adequate       High       High         High         High       High                Selected
  slewing ring                                                                                      
  (010.10.120)                                                                                      
  --------------------------------------------------------------------------------------------------------------

This matrix captured the most important refinement in the design
journey. The geared slewing ring was structurally excellent but far too
heavy, costly, and power-hungry relative to the robot's real needs. The
**010.10.120 non-geared slewing ring** was selected because it satisfies
realistic load requirements while greatly improving manufacturability
and design appropriateness. This marks the point where the design
shifted clearly from **maximum capability** to **fit-for-purpose
engineering**.

**Concept selection matrix: rotation drive-transmission strategy**

  ------------------------------------------------------------------------------------------------------------------
  **Concept**      **Positive       **Packaging    **Ratio         **Fabrication   **Serviceability**   **Final
                   torque           simplicity**   flexibility**   tolerance**                          decision**
                   transmission**                                                                       
  ---------------- ---------------- -------------- --------------- --------------- -------------------- ------------
  Direct pinion on High             Moderate       Moderate        Moderate        Moderate             Early
  external gear                                                                                         concept only

  Friction-drive / Low              High           Low             Poor            Moderate             Rejected
  wheel-drive                                                                                           
  concept                                                                                               

  Timing-belt      High             High           High            High            High                 Selected
  drive to inner                                                                                        
  rotating surface                                                                                      
  ------------------------------------------------------------------------------------------------------------------

Once the non-geared bearing had been selected, the drive system had to
become a separately designed subassembly. The **timing-belt drive** was
selected because it preserves positive torque transmission while
improving packaging flexibility, allowing the motor to remain on the
fixed structure and the ratio to be tuned through pulley selection. This
made it the most buildable and maintainable solution for the welded-base
architecture.

**Concept selection matrix: outboard support and deployment refinement**

  ---------------------------------------------------------------------------------------
  **Concept**    **Edge          **Added   **Packaging     **Transport       **Final
                 stability under part      cleanliness**   compatibility**   decision**
                 overturning**   count**                                     
  -------------- --------------- --------- --------------- ----------------- ------------
  Central        Moderate        High      High            Moderate          Not
  bearing only                                                               preferred
                                                                             alone

  Ring of many   High            Poor      Poor            Poor              Rejected
  support                                                                    
  rollers                                                                    

  Discrete       High            High      High            High              Selected
  cam-follower                                                               
  supports +                                                                 
  rear transport                                                             
  wheels                                                                     
  ---------------------------------------------------------------------------------------

This final matrix was used to refine the subsystem beyond its minimum
working form. The selected approach used **discrete cam-follower
supports** to improve edge stability without excessive part count,
together with **rear transport integration** to ensure the module
remained practical for workshop and demo handling. This is where the
rotation subsystem matured from a pure motion axis into a more complete
base module.

Overall, the matrices made the rotation design more disciplined. They
helped move the subsystem step-by-step from motion architecture, to
bearing concept, to transmission method, to support refinement,
producing a final yaw module that is more coherent with the way BoxBunny
is intended to be built and used.
