**5.2.X.4.1 Design Ideation**

The ideation process for height adjustment was not treated as a single
component-selection exercise. Instead, it progressed through a sequence
of design questions, where each stage of the subsystem was compared
against the most important needs of BoxBunny: sufficient stroke,
structural stiffness under punching, compact packaging,
manufacturability at prototype scale, and practical usability. To make
those trade-offs explicit, **selection matrices** were used as a
decision-support tool.

In this subsystem, the role of the selection matrix was not simply to
identify the "best" mechanism numerically. Rather, it was used to
structure the design progression from **basic adjustability concepts**,
to **guide-and-actuator separation**, to the final **integrated
telescopic column architecture**. Each matrix narrowed the solution
space and made the design trade-offs explicit.

**Concept selection matrix: high-level height-adjustment concept**

  ---------------------------------------------------------------------------------------------
  **Concept**    **User            **Structural   **Complexity**   **Packaging**   **Final
                 adjustability**   rigidity under                                  decision**
                                   punch loads**                                   
  -------------- ----------------- -------------- ---------------- --------------- ------------
  Fixed-height   None              High           Low              High            Rejected
  body                                                                             

  Manual         Moderate          Moderate       Low              Moderate        Rejected
  telescopic                                                                       
  mast                                                                             

  Commercial     High              Uncertain      Low              High            Not selected
  lift column                                                                      

  Guided lift    High              High           Moderate         High            Selected
  column + screw                                                                   direction
  jack                                                                             
  ---------------------------------------------------------------------------------------------

This first matrix was used to decide the **overall adjustment
philosophy**. A fixed-height body was rejected immediately because it
could not accommodate different users. A manually adjustable mast would
reduce electrical complexity, but it would compromise ease of use and
would not give clean, repeatable setup positioning. Commercial lift
columns were attractive because of their integrated packaging, but their
side-load capability under boxing disturbances was too uncertain.

The **guided lift column plus screw jack** direction was selected
because it was the only concept that directly addressed both the user's
need for adjustability and the robot's need for structural stability
under punch loading. This was the first point at which the subsystem
moved beyond simple height change and became a true structural design
problem.

**Concept selection matrix: guide strategy**

  ------------------------------------------------------------------------------------------
  **Concept**      **Lateral     **Part    **Tolerance     **Serviceability**   **Final
                   stiffness**   count**   sensitivity**                        decision**
  ---------------- ------------- --------- --------------- -------------------- ------------
  Dual rear linear High          Poor      Poor            Moderate             Early
  guides +                                                                      serious
  carriage                                                                      concept

  Telescopic       High          High      High            High                 Selected
  guided column                                                                 

  Actuator-only    Poor          High      High            Poor                 Rejected
  guidance                                                                      
  ------------------------------------------------------------------------------------------

This matrix was used to decide how the subsystem should react
punching-induced side loads. The early dual-linear-guide concept was
mechanically sound and played an important role in clarifying the
load-path logic. It offered good stiffness, but it relied on many
precision-mounted components and introduced alignment sensitivity and
potential failure points. An actuator-only guidance concept was rejected
because it would side-load the screw and compromise reliability.

The **telescopic guided column** was selected because it preserved the
same fundamental structural logic as the rear-linear-guide concept, but
implemented it with fewer parts, a cleaner load path, and lower
tolerance sensitivity. This was one of the most important design
refinements in the subsystem.

**Concept selection matrix: actuator strategy**

  -----------------------------------------------------------------------------------------
  **Concept**   **Axial load **Self-holding / **Integration   **Complexity**   **Final
                capacity**   fail-safe        with guide                       decision**
                             behaviour**      structure**                      
  ------------- ------------ ---------------- --------------- ---------------- ------------
  Gas spring /  Moderate     Poor             Poor            Low              Rejected
  gas lift                                                                     

  Powered       Moderate to  Moderate         Moderate        Low              Not selected
  linear        high                                                           
  actuator                                                                     
  column                                                                       

  Screw jack    High         High             High            Moderate         Selected
  with                                                                         
  travelling                                                                   
  nut                                                                          
  -----------------------------------------------------------------------------------------

This matrix focused on the actual lifting device. Gas-spring-based
concepts were rejected because they behave like spring-damper systems
and are structurally too compliant for a robot that receives impact.
Commercial powered lift columns remained attractive, but again suffered
from uncertainty in side-load behaviour and less explicit control over
load-path design.

The **travelling-nut screw jack** was selected because it provides a
strong axial support mechanism, has inherent self-holding behaviour, and
integrates naturally with a guide structure that resists lateral loads
separately. This matched the desired fail-safe and load-separation
philosophy of the subsystem.

Overall, the selection matrices made the height-adjustment design more
disciplined. They helped move the subsystem from a vague idea of
"raising the robot" toward a proper structural solution in which
lifting, guiding, and side-load resistance were treated as related but
distinct engineering functions.
