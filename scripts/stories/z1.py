from scripts.unit1_story_common import zone,cast
META={
'palace_id':'Z1','palace_name':'Scientific Inquiry Lab Annex','story_title':'The Evidence Lockdown',
'tagline':'One glowing result has triggered a lab lockdown. Follow the evidence until you can decide what the experiment actually supports.',
'guide':{'name':'Dr. Rowan Lee','role':'night research director','visual':'white lab coat, copper-rimmed glasses, orange evidence folder','story_job':'keeps one reporter-cell experiment intact from first observation to final interpretation'},
'premise':'At 11:47 p.m., an automated cell experiment reports an unexpectedly bright signal and seals the research annex. The doors will reopen only after the result has been traced from observation through experimental design and statistical interpretation.',
'mission':'Stay with Dr. Rowan Lee and audit one reporter-cell experiment. Decide what changed, what was measured, which comparisons make the result interpretable, how variable the data are, and how much confidence the sample mean deserves.',
'finale':'On the Sampling Balcony, the last uncertainty bars settle around the treatment and control means. Rowan closes the orange folder: the annex opens because you can now say exactly what the experiment supports, what it does not prove, and how the data justify that conclusion.',
'estimated_minutes':16,'checkpoint_indices':[1,4,8],
'route_orientation':'The annex is a straight glass corridor that bends around a central data chamber. You begin at the south Observation Window, move clockwise through experiment design, then climb one level to the statistics rooms and finish on the north Sampling Balcony.',
'route':[
{'scene_index':0,'locus':'Observation Window','short':'Observe','floor':'South wing','symbol':'◉'},
{'scene_index':1,'locus':'Hypothesis Doors','short':'Hypotheses','floor':'South wing','symbol':'⇄'},
{'scene_index':2,'locus':'Control Benches','short':'Controls','floor':'West lab','symbol':'⚖'},
{'scene_index':3,'locus':'Variable Control Panel','short':'Variables','floor':'West lab','symbol':'↔'},
{'scene_index':4,'locus':'Bias Goggles Cabinet','short':'Bias','floor':'North turn','symbol':'⌁'},
{'scene_index':5,'locus':'Statistics Reporter Desk','short':'Statistics','floor':'Upper level','symbol':'▤'},
{'scene_index':6,'locus':'Center-of-Data Roundabout','short':'Center','floor':'Upper level','symbol':'◎'},
{'scene_index':7,'locus':'Variability Floor','short':'Spread','floor':'Upper level','symbol':'↔'},
{'scene_index':8,'locus':'Sampling Balcony','short':'Sampling','floor':'North balcony','symbol':'±'}]
}
SCENES=[
{
'locus':'Observation Window','title':'The Light That Should Not Be There','kicker':'A single observation starts the investigation, but it cannot finish it.',
'location_description':'You stand at the south end of the annex behind a thick observation window. Beyond the glass are two trays of identical reporter cells. One tray glows faint green. The other burns bright enough to color the room.',
'orientation':'The corridor is behind you. The two cell trays sit directly ahead. Rowan’s orange evidence board is fixed to the right wall, and the sealed door to the hypothesis chamber is on the far left.',
'zones':[zone('left','Sealed hypothesis door','⇄','Two dark doors wait for possible explanations.'),zone('center','Reporter-cell chamber','🧫','Two trays of cells show the unexpected difference that triggered the lockdown.'),zone('right','Evidence board','📋','Rowan pins observations, questions, predictions, methods, data, and conclusions here as the investigation develops.')],
'cast':[cast('Reporter cells','experimental subjects','two clear trays of cultured cells, one dim and one bright','provide the observable response that needs an explanation'),cast('Orange evidence board','investigation map','six connected slots with arrows that can point forward or backward','keeps observation, question, hypothesis, experiment, data, and conclusion connected without pretending science always moves in one rigid line')],
'paragraphs':[
'The annex locks with a metallic thud. Beyond the Observation Window, one tray of reporter cells gives off the faint green glow Rowan expected. The second tray shines like a row of tiny emergency lamps. Rowan does not celebrate. He opens his orange folder and says, “First we describe what we can actually see.”',
'That first careful noticing is an **observation**. It raises a question: why are these cells brighter? Rowan slides the observation into the first slot of the evidence board, but the arrows on the board do not form a one-way staircase. They loop backward as well as forward. Scientific inquiry can move from observations to questions, hypotheses or predictions, experiments or other methods, data, and evidence-based conclusions, then circle back when the evidence creates a new question. That whole evidence-seeking process is the **scientific method**, while observation → question → hypothesis → experiment → data → conclusion is a useful organizing sequence, not a law that scientists must follow mechanically.',
'Rowan writes a tentative explanation: perhaps the new nutrient solution increases production of the glowing reporter protein. A scientific **hypothesis** is a tentative explanation that leads to testable predictions. Beneath it he writes, “If cells receive the new solution, then reporter brightness will increase because…” The **if–then–because** form is a useful way to make the manipulated condition, predicted response, and reasoning visible, but the grammar itself is optional.',
'He underlines one final warning in red. Evidence can **support** a hypothesis or fail to support it; even a strong result does not prove the explanation eternally true. The bright tray is an invitation to test, not permission to skip the experiment.',
'A green light appears above the two doors on the left. The annex will let you move on only after the explanation is turned into competing predictions.'
]},
{
'locus':'Hypothesis Doors','title':'Two Doors, Two Possible Worlds','kicker':'The same experiment must be able to separate “no effect” from an effect.',
'location_description':'You enter a narrow chamber with two identical steel doors facing you. A white zero is painted on the left door. A glowing upward arrow is painted on the right. The cell experiment can unlock only one path at a time.',
'orientation':'You entered from the south. The NULL door is on your left, the ALTERNATIVE door on your right, and a small decision console sits between them.',
'zones':[zone('left','Null door','0','Represents the possibility that the treatment produces no effect or difference of the type being tested.'),zone('center','Decision console','?','Holds the research question and forces both predictions to refer to the same measured outcome.'),zone('right','Alternative door','↑','Represents an effect, association, or difference inconsistent with the null.')],
'cast':[cast('Null door','hypothesis','flat white door marked NO DIFFERENCE','represents the formal null hypothesis when null-hypothesis testing is appropriate'),cast('Alternative door','hypothesis','dark door with a bright arrow climbing upward','represents a treatment effect that conflicts with the null')],
'paragraphs':[
'The left door flashes **NULL HYPOTHESIS**. Rowan reads the plate aloud: if formal null-hypothesis testing is appropriate, the null predicts no treatment effect, association, or difference of the type being tested. For this experiment, that means the new solution does not change mean reporter brightness beyond the variation expected in the experiment.',
'The right door flashes **ALTERNATIVE HYPOTHESIS**. It predicts an effect inconsistent with the null: cells receiving the new solution will differ in reporter brightness from the comparison condition. Rowan keeps both doors tied to the same response so the test can actually distinguish them.',
'“Notice what we are not doing,” Rowan says. “We are not declaring the null false because we dislike it, and we are not pretending every investigation in science must begin with this formal pair.” When the statistics are appropriate, the language later will be **reject** or **fail to reject** the null, not “prove the null” or “prove the alternative.”',
'The console accepts both predictions. A floor panel opens beneath the doors and reveals two long experimental benches waiting in the next room.'
],
'checkpoint_object_id':'MO-APBIO-U1-P006','checkpoint_prompt':'In formal hypothesis testing, which hypothesis predicts no effect, association, or difference of the type being tested?'
},
{
'locus':'Control Benches','title':'The Comparisons That Make the Result Mean Something','kicker':'A treatment result is interpretable only when the comparison conditions tell you what “normal” looks like.',
'location_description':'You step into a wide wet-lab room containing four parallel benches. Each bench holds identical reporter cells, but the labels above them differ: CONTROL, EXPERIMENTAL, NEGATIVE CONTROL, and POSITIVE CONTROL.',
'orientation':'The benches run west to east like lanes. The ordinary control is nearest the entrance, the experimental bench is beside it, and the negative and positive controls occupy the two far lanes.',
'zones':[zone('left','Comparison lanes','⚖','The ordinary control and experimental group sit side by side so one focal difference can be judged.'),zone('center','Replication rack','▦','Multiple independent wells repeat each condition so variability can be estimated.'),zone('right','Validation lanes','−/+','Negative and positive controls test whether false signals or a broken detection system could explain the result.')],
'cast':[cast('Control group','comparison condition','cells handled like the experimental group but without the focal treatment','provides the baseline needed to isolate the treatment effect'),cast('Experimental group','treatment condition','cells receiving the new nutrient solution','receives the independent-variable condition whose effect is being evaluated'),cast('Negative control','validation comparison','cells arranged so the target glow should not appear','reveals unwanted signal or contamination if the assay lights up anyway'),cast('Positive control','validation comparison','cells given a condition already expected to produce glow','shows whether the system is capable of detecting the response at all')],
'paragraphs':[
'Rowan walks first to the **control group**. These cells provide the comparison condition. Beside them sits the **experimental group**, which receives the new nutrient solution. If the two groups differ while other relevant conditions remain comparable, the treatment becomes a plausible explanation for the difference.',
'Two more benches protect the interpretation. The **negative control** is set up so the target response should not appear; if it glows anyway, something besides the intended biological effect may be producing signal. The **positive control** receives a condition already known or strongly expected to produce glow; if that bench stays dark, the assay may be unable to detect the effect even when it is present.',
'At the center rack, Rowan loads several independent wells for each condition. Replication helps estimate variability and improves reliability, but he tears down a sign that says THREE TRIALS = SCIENCE. There is no universal rule that every group must contain exactly three trials; the needed replication depends on the design and question.',
'He then points to the thermostat, light timer, cell density, and incubation time. Those will be held constant, but they are not “the control.” **Controlled variables or constants** are conditions kept comparable. A **control group** is a comparison condition. Their jobs are different.',
'All four benches slide forward on rails and lock into a single illuminated control panel in the next room.'
]},
{
'locus':'Variable Control Panel','title':'Change One Lever, Watch One Gauge','kicker':'The experiment becomes interpretable when the manipulated factor and measured response are unmistakable.',
'location_description':'A wall-sized control panel fills the next room. One large blue lever controls treatment concentration. A green gauge displays reporter brightness. Smaller locked dials control temperature, light, time, and cell number.',
'orientation':'The blue treatment lever is on the left, the measured brightness gauge is centered at eye level, and the bank of locked constant-condition dials is on the right. A graph screen hangs above the center gauge.',
'zones':[zone('left','Manipulation lever','X','The treatment condition is deliberately changed here.'),zone('center','Response gauge','Y','Reporter brightness is measured here as the experiment responds.'),zone('right','Locked condition dials','🔒','Other relevant conditions stay comparable across groups.')],
'cast':[cast('Independent variable','manipulated factor','a blue lever labeled nutrient treatment','is deliberately changed or used to define comparison groups'),cast('Dependent variable','measured response','a bright green gauge labeled reporter fluorescence','records the response used to evaluate the manipulation'),cast('Controlled variables','held conditions','locked dials for temperature, light, time, and cell number','prevent other changing conditions from becoming competing explanations')],
'paragraphs':[
'Rowan places your hand on the blue lever. This is the **independent variable**: the factor deliberately manipulated or used to define the comparison groups. Here it is the nutrient treatment. On the central gauge, **reporter brightness** is the **dependent variable**, the measured response used to evaluate what the treatment does.',
'The smaller dials are the **controlled variables**, or constants. Temperature, exposure time, light, starting cell density, and other relevant conditions are held comparable. A well-controlled experiment changes the focal independent variable while keeping those competing influences from drifting apart.',
'Above the panel, a graph appears. Rowan drags treatment condition to the horizontal axis and brightness to the vertical axis. When that graphing convention fits the data, the **independent variable goes on the x-axis** and the **dependent variable goes on the y-axis**. The graph type still has to match the kind of data being displayed; x and y labels do not rescue a bad graph.',
'The blue lever moves. The treatment wells brighten. Before Rowan lets you call it an effect, however, he opens a cabinet containing two pairs of mirrored goggles.'
]},
{
'locus':'Bias Goggles Cabinet','title':'The Goggles That Change What You Think You Saw','kicker':'Expectations can bend a study even when nobody intends to cheat.',
'location_description':'At the north turn of the corridor stands a tall black cabinet filled with mirrored safety goggles. Through one pair, every treatment well looks brighter before the measurement even begins.',
'orientation':'The cabinet is on the left wall, a blinded sample rack is centered under neutral white light, and a two-key double-blind lock is mounted on the right.',
'zones':[zone('left','Bias goggles','👓','These distorted lenses make expectations visibly warp what an observer thinks they see.'),zone('center','Coded sample rack','A/B','Treatment identities are replaced with neutral codes.'),zone('right','Double-key lock','🔐','One key hides group identity from participants or handlers; another can hide it from the observer or assessor.')],
'cast':[cast('Bias','systematic distortion','mirrored goggles that make favored samples look brighter','represents systematic influences that can distort design, measurement, analysis, or interpretation'),cast('Blinding','bias-control method','sample labels replaced by neutral codes','withholds treatment or group information from people whose expectations could affect the result')],
'paragraphs':[
'Rowan hands you the first pair of goggles. The treatment wells seem brighter before the detector has measured anything. That systematic pull on design, measurement, analysis, or interpretation is **bias**. It need not be deliberate; expectations can distort a study precisely because they feel reasonable to the person holding them.',
'He replaces the treatment labels with neutral codes. In a **blind** design, relevant treatment information is withheld from participants, observers, or another group whose knowledge could influence behavior or measurement. When the design allows both participants and the people assessing outcomes to remain unaware of group assignment, a **double-blind** design can reduce additional forms of expectation bias.',
'The point is not that every biology experiment can be blinded in the same way. The point is to ask who knows what, whether that knowledge could alter the study, and whether masking it would reduce a systematic distortion.',
'When the goggles come off, the detector exports a clean table of numbers. Rowan carries it upstairs to the Statistics Reporter Desk.'
],
'checkpoint_object_id':'MO-APBIO-U1-P016','checkpoint_prompt':'What term describes a systematic influence that can distort study design, measurement, analysis, or interpretation?'
},
{
'locus':'Statistics Reporter Desk','title':'The Numbers Become a Report','kicker':'First describe the sample you actually measured; only then ask what it suggests beyond itself.',
'location_description':'On the upper level, an old newsroom desk faces two wall screens. The left screen rearranges the measured values into tables and graphs. The right screen projects a much larger population of cell cultures beyond the experiment.',
'orientation':'The observed sample fills the left screen, the reporter desk is in the center, and the larger target population appears on the right screen.',
'zones':[zone('left','Observed-data screen','▤','Shows only the values actually measured in this experiment.'),zone('center','Reporter desk','✎','Turns raw values into interpretable summaries.'),zone('right','Population screen','◌','Represents the broader population the sample may be used to understand.')],
'cast':[cast('Descriptive statistics','sample summarizer','a reporter arranging the measured values into tables, graphs, centers, and spreads','summarizes and displays the data that were actually observed'),cast('Inferential statistics','population reasoner','a reporter projecting from the sample toward a much larger field of cells','uses sample data, together with uncertainty and sampling assumptions, to draw conclusions about a broader population')],
'paragraphs':[
'The left screen is crowded with raw fluorescence values. Rowan asks the desk to summarize only what was actually observed. **Descriptive statistics** organize, display, and summarize the sample: tables, graphs, measures of center, and measures of spread help you see the important features of the measured data.',
'The right screen is more ambitious. It asks whether this sample tells us something about a broader population of cells that were never placed on these benches. **Inferential statistics** use sample data to draw conclusions or generalize beyond that sample, but the quality of the inference depends on how the sample was obtained and how uncertainty is handled.',
'“Description tells us what happened in our data,” Rowan says. “Inference asks how far we can responsibly carry that information.” The desk prints three candidate summaries of the center and sends them spinning into a circular chamber ahead.'
]},
{
'locus':'Center-of-Data Roundabout','title':'Three Ways to Find the Middle','kicker':'The center of a data set depends on what you mean by “typical.”',
'location_description':'A circular room contains a rotating platform of numbered fluorescence values. Three stations surround it: an adding machine, an ordered staircase, and a frequency bell.',
'orientation':'The mean station is left of the entrance, the median staircase occupies the center, and the mode bell is on the right. The data values circle all three stations.',
'zones':[zone('left','Mean station','Σ/n','Adds every value and divides by the number of observations.'),zone('center','Median staircase','↕','Orders values and selects the middle position.'),zone('right','Mode bell','🔔','Rings beside the value that appears most often.')],
'cast':[cast('Central tendency','family of measures','a circular target drawn over the middle of the rotating data set','describes the center or typical value of a distribution'),cast('Mean','measure of center','adding machine marked Σ ÷ n','adds all observations and divides by their number'),cast('Median','measure of center','middle stair in an ordered line','identifies the middle value after the observations are ordered'),cast('Mode','measure of center','bell attached to the most repeated value','identifies the value occurring most frequently')],
'paragraphs':[
'Rowan calls the room the **central tendency** roundabout because every station tries to describe the center or typical value of the same data set in a different way.',
'At the left station, every fluorescence value falls into an adding machine. Their sum is divided by the number of observations. The number that emerges is the **mean**.',
'At the center staircase, the observations line themselves up from least to greatest. The **median** is the middle value, the point that separates the lower half from the upper half.',
'At the right bell, no arithmetic is required. It rings beside the value that appears most frequently. That most common value is the **mode**.',
'Rowan takes the mean for the next analysis, but the floor begins stretching under the same center point. “A mean without spread can hide a lot,” he says, stepping into the Variability Floor.'
]},
{
'locus':'Variability Floor','title':'The Floor That Stretches Around the Same Mean','kicker':'Two data sets can share a center and still tell very different stories.',
'location_description':'The floor is printed with a number line. One set of glowing data points clusters tightly around the mean. A second set stretches far toward both walls even though its mean marker sits in the same place.',
'orientation':'The narrow cluster occupies the left half, the shared mean marker stands at center, and the widely scattered cluster spans the right half.',
'zones':[zone('left','Tight distribution','••••','Observations sit close to the mean.'),zone('center','Shared mean','│','Both example distributions balance around the same center.'),zone('right','Wide distribution','•   •','Observations spread much farther from the mean.')],
'cast':[cast('Variability','spread of observations','a floor that can contract or stretch around the same center','describes how dispersed the observed values are'),cast('Range','simple spread measure','a tape stretched from the smallest value to the largest','equals the greatest observation minus the smallest'),cast('Standard deviation','spread around the mean','a glowing band expanding or contracting around the mean','describes how widely observations are distributed around their mean')],
'paragraphs':[
'The room makes **variability** impossible to ignore. On the left, measurements hug the mean. On the right, they are scattered across the floor. The center alone cannot tell you which pattern you have.',
'Rowan stretches a tape from the smallest observation to the largest. The distance, calculated as greatest minus smallest, is the **range**. It is easy to compute, but it depends only on the two extreme values.',
'Then a glowing band appears around the mean. Its width represents the **standard deviation**, a measure of how observations spread around that mean. A smaller standard deviation means the observations are more tightly clustered. Rowan refuses a sign that says SMALL SD = RELIABLE. “Tight spread describes this data distribution,” he says. “Reliability is a broader judgment about measurement and study design.”',
'The floor retracts and a glass door opens onto the balcony, where identical experiments seem to be repeating far below.'
]},
{
'locus':'Sampling Balcony','title':'How Much Would the Mean Move If We Repeated This?','kicker':'The final question is not how scattered individual observations are, but how precise the estimated mean is.',
'location_description':'You step onto a north-facing balcony overlooking dozens of miniature copies of the same experiment. Each copy produces a slightly different sample mean. Their mean markers float like lanterns over the courtyard.',
'orientation':'Repeated experiments fill the courtyard below, a formula rail marked s/√n runs along the balcony center, and the final graph with error bars glows on the right wall.',
'zones':[zone('left','Repeated samples','◌◌◌','Each miniature experiment produces its own sample mean.'),zone('center','SEM rail','s/√n','Connects sample standard deviation and sample size to the expected variation of the sample mean.'),zone('right','Error-bar display','±','Shows the two group means with clearly labeled uncertainty bars.')],
'cast':[cast('Standard error of the mean','precision measure','a cloud of sample means narrowing as sample size grows','describes how much a sample mean would be expected to vary across repeated samples; SEM = s/√n'),cast('Error bars','uncertainty display','vertical bars extending above and below each plotted mean','visualize a specified measure of uncertainty or variation, which must be identified before interpretation')],
'paragraphs':[
'The balcony reveals a different kind of variation. Individual cells varied downstairs; now whole **sample means** vary from one repeated sample to another. The **standard error of the mean**, or **SEM**, describes how much the sample mean would be expected to vary across repeated sampling. Rowan taps the rail: SEM = s/√n. For the same underlying spread, larger samples generally give a smaller SEM and a more precise estimate of the mean.',
'On the final graph, each group mean carries a vertical bar. Rowan makes you read the legend before the graph. **Error bars** can represent different quantities, so their meaning must be stated. In one common classroom convention, mean ± 2 SEM gives a rough range for where repeated-sample means would often fall, but the bars are not magic significance detectors.',
'He drags two error bars until they overlap, then separates them again. “Overlap or non-overlap of SEM bars by itself is not a formal statistical-significance test.” A proper inferential conclusion depends on the chosen statistical procedure and its assumptions, not a visual shortcut.',
'Rowan lays the experiment beside the original observation. The bright cells are no longer a mysterious green flash. You can trace the result through hypotheses, comparisons, variables, bias controls, descriptive summaries, variability, and sampling uncertainty. The annex doors unlock with a soft click.'
],
'checkpoint_object_id':'MO-APBIO-U1-P028','checkpoint_prompt':'What statistic, calculated as s/√n, describes how much a sample mean would be expected to vary across repeated samples?'
}
]
