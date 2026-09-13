"""Source-distilled Phase 3 catalog. Dimensions are never inferred from photographs."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
QB='Companion Hardware Callout Rev2, supplied Companion+Hardware+Customer+-+Sheet1-2.pdf'
WM='Wing+Build+Manual+Rev+2-compressed.pdf, 11/5/24'
FM='BHManual-Fuselage1-25Rev1.pdf'
FM2='BHManual-fuselage26-45Rev2.pdf'
catalog=[]
def hardware(b,n,w,nut,cotter=None,wm=1):
    r=[['bolt',n,b],['washer',n*wm,w],['castle' if cotter else 'locknut',n,nut]]
    if cotter:r.append(['cotter',n,cotter])
    return r
def step(title,view,rows=(),note='',detail='CONNECTION DETAIL',flags=()):
    return dict(title=title,view=view,hardware=list(rows),note=note,detail=detail,flags=list(flags))
def manual(n,id,title,section,model,sources,steps,issues=(),status=None,photo=None):
    slug=title.lower().replace(' / ','-').replace(' ','-').replace('&','and')
    m=dict(number=n,id=id,title=title,section=section,slug=f'{section}/{slug}',model=model,revision=2,
           pdf=f'{n:02d}_'+title.replace(' / ','_').replace(' ','_').replace('&','and')+'.pdf',
           sources=sources,steps=steps,issues=list(issues),photo=photo,
           status=status or ('REVIEW REQUIRED' if issues else 'RELEASED'))
    for i,s in enumerate(steps,1):s.update(number=i,image=f'{id}_step_{i:02d}_v2.png')
    catalog.append(m)
def issue(steps,text,source,check):return dict(steps=steps,issue=text,source=source,check=check)

manual(2,'CTRL002','Rudder Pedals','controls','pedals',[ 'Companion plan 29',FM+' pp19–20',QB+' p1 HK-RS4'],[
 step('MOUNT RUDDER PEDAL ASSEMBLY','mount',hardware('AN3-4A',4,'AN960-10L','AN365-1032A'), 'METAL-TO-METAL · SEE PLAN 29'),
 step('INSTALL TOE BRAKE PEDALS','toe',hardware('AN4-21',4,'AN960-416','AN310-4','MS24665-208'),'FOUR PEDALS · SEE PLAN 29')],
 [issue('01–02','Final pedal position and firewall clearance depend on fitted cylinders.','Plan 29 / legacy pp19–20; no aircraft-specific fit check.','Dry-fit all four cylinders and check full travel before final positioning.')],photo='G1-PEDALS')
manual(3,'CTRL003','Rudder Cable Connections','controls','rudder_cable',['Companion plans 29, 24',FM+' p20',QB+' p1 HK-RS4'],[
 step('CONNECT CABLE TO PEDAL TAB','pedal',hardware('AN3-5',2,'AN960-10L','AN310-3','MS24665-132',3),'2× AN115-21 · BOTH SIDES',flags=['? VERIFY WASHER POSITION']),
 step('CONNECT CABLE TO RUDDER HORN','horn',hardware('AN4-6',2,'AN960-416L','AN310-4','MS24665-208'),'2× AN115-32 · SEE PLAN 24',flags=['? VERIFY SHACKLE PREPARATION'])],
 [issue('01','Three thin washers are called out, but exact allocation across the tab joint is not established.','HK-RS4 cable-to-tab row.','Confirm stack against current factory installation; washers remain in parts tray.'),
 issue('02','Shackle preparation and full fuselage routing are not released by these endpoint illustrations.','HK-RS4 says AN115-32: drill to AN4; route not fully constrained by supplied Companion drawings.','Confirm factory drilling detail, route through installed fairleads, spring connection and cable termination inspection.')],photo='FM16-RUDDER')
manual(4,'CTRL004','Flap Cockpit Controls','controls','flap_handle',['Companion plan 30',FM+' pp21–22',QB+' p3 HK-FCC'],[
 step('FIT HANDLE AND QUADRANT','handle',hardware('AN3-5A',2,'AN960-10','AN365-1032A'),'SEE PLAN 30',flags=['? VERIFY DETENT ENGAGEMENT']),
 step('CONNECT HANDLE CABLE','cable',hardware('AN3-5',1,'AN960-10L','AN310-3','MS24665-132',3),'1× AN115-21 · HANDLE END',flags=['? VERIFY WASHER POSITION']),
 step('FIT FLAP CABLE SPLITTER','splitter',[['bushing',1,'AN115-21'],['rodend',2,'AN130-22S']],'SEE PLAN 30 · REAR BAGGAGE',flags=['? VERIFY ROUTING'])],
 [issue('01','Pin engagement, spring fit and travel-stop setting need kit fit verification.','HK-FCC lists R-FHS and AN3-4A travel limit; plan30.','Check all detents, spring return and supplied stop before use.'),issue('02–03','Full Companion pulley route and washer allocation remain unresolved.','Plan30 shows splitter relationship; legacy full routing is not a complete Companion installation map.','Trace cable through current kit pulleys and guards; confirm all stacks. Do not fabricate cable lengths from scene.')],photo='G2-FLAP158')
manual(5,'CTRL005','Elevator Horn Connections','controls','elevator_horn',['Companion plan22',FM+' pp15–18',QB+' p2 HK-ES4'],[
 step('JOIN ELEVATOR HORNS','union',hardware('AN3-6A',2,'AN960-10L','AN365-1032A'),'ALUMINUM BUSHING BETWEEN HORNS'),
 step('CONNECT ELEVATOR CABLES','cables',hardware('AN3-6',2,'AN960-10L','AN310-3','MS24665-132'),'STEEL BUSHING · OUTER HOLES')],
 [issue('01–02','Bushing lengths and full forward-to-tail routing are not established here.','HK-ES4 distinguishes aluminum union and steel cable bushings; no bushing lengths in count sheet.','Confirm bushings from plan22/current kit. Verify lower cable fairlead and full route before termination.')],photo='FM16-ELEVATOR')
manual(6,'FUS001','Floorboard Relationships','fuselage','floors',[FM+' pp18–24',QB+' p4 Skins Floors Stringers'],[
 step('FIT PANELS BETWEEN CONTROLS','fit',[],'PANELS CLEAR CONTROL MOUNTS','REMOVABLE PANEL EDGE'),
 step('ATTACH REMOVABLE FLOOR PANELS','attach',[['bolt',46,'AN526C-632-6'],['locknut',46,'K1000-06']],'46 LOCATIONS · AIRCRAFT TOTAL','SCREW / PANEL / TAB / NUTPLATE',flags=['? VERIFY PANEL FIT'])],
 [issue('01–02','Panel boundaries and access openings are fitted to the individual airframe.','Legacy preferred removable arrangement; QB 46 attachment locations is aircraft total.','Check pedal/stick sweep, cable access and each supplied tab. Scene is not a cutting pattern.')],photo='FM23-FLOOR')
manual(7,'EMP001','Horizontal Stabilizer','empennage','stabilizer',['Companion plans20,22',FM+' pp13–15',QB+' p2 HK-EA4'],[
 step('FIT FORWARD CARRY-THROUGH','carry',hardware('AN4-22A',2,'AN960-416','AN365-428A'),'MATCH FACTORY ORIENTATION',flags=['SOURCE CONFLICT — VERIFY']),
 step('SLIDE ON STABILIZER HALVES','halves',hardware('AN3-12A',4,'AN960-10L','AN365-1032A',wm=2),'FRONT + REAR SPAR · BOTH HALVES',flags=['? VERIFY WASHER POSITION']),
 step('FIT LOWER BRACE STRUTS','brace',hardware('AN3-14A',2,'AN960-10L / -10','AN365-1032A'),'OUTBOARD ENDS · SEE PLAN 22',flags=['? VERIFY CLEVIS STACK'])],
 [issue('01','Legacy incidence guidance differs from current Companion count sheet.','Legacy p13 says four degrees down; HK-EA4 says -2 degrees. Plans control design.','Confirm Companion incidence and reference datum from current factory/plans before fixing spacers.'),issue('02–03','Carry-through orientation and brace washer allocation need kit confirmation.','HK-EA4 calls mixed outboard washers and thin washer at lower clevis.','Match factory holes without forcing; verify all washers and lower AN3-5A / AN960-10L / AN365-1032A set.')],photo='G2-TAIL')
manual(8,'EMP002','Elevators','empennage','elevators',['Companion plans22,24',FM+' p15',QB+' p2 HK-EA4'],[
 step('FIT INBOARD ELEVATOR HINGES','inboard',hardware('AN4-14A',2,'AN960-416','AN365-428A'),'HINGE STRAPS CLEAR SUPPORTS'),
 step('FIT OUTBOARD HINGES AND TABS','outboard',hardware('AN4-18A',2,'AN960-416','AN365-428A'),'FLYING-WIRE TABS: HEAD + NUT',flags=['? VERIFY TAB ORIENTATION'])],
 [issue('01–02','Hinge support fit and flying-wire tab orientation depend on supplied kit.','Plan24 hinge detail / HK-EA4 / legacy p15.','Check hinge fit, free travel and brace tab orientation. Final balance/rigging remains outside this manual.')],photo='G2-TAIL')
manual(9,'EMP003','Rudder','empennage','rudder',['Companion plan24',FM+' pp15–16',QB+' pp1–2 HK-RS4 / HK-EA4'],[
 step('FIT RUDDER TO HINGE LINE','fit',[],'SEE PLAN 24 · ALIGN BOTH HINGES','HINGE RELATIONSHIP',flags=['? VERIFY LOWER HINGE HARDWARE']),
 step('ATTACH UPPER RUDDER HINGE','upper',hardware('AN4-17A',1,'AN960-416L','AN365-428A'),'FLYING-WIRE TABS: HEAD + NUT',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('01–02','Lower rudder bolt conflicts within current hardware sheet.','HK-RS4 p1: AN4-15A; HK-EA4 p2: AN4-13A.','Obtain corrected factory lower hinge callout. Lower hinge remains unfastened in illustration; upper set is consistent.')],photo='G2-TAIL219')
manual(10,'EMP004','Tail Brace Wires','empennage','tail_wires',['Companion plans20,22,24',QB+' p2 HK-EA4'],[
 step('IDENTIFY BRACE WIRE TERMINALS','parts',[['rodend',4,'AN665-34R'],['rodend',4,'AN665-34L'],['checknut',4,'AN315-4'],['checknut',4,'AN315-4L']],'KEEP RIGHT / LEFT THREADS PAIRED','TERMINAL RELATIONSHIP'),
 step('CONNECT WIRES TO TABS','fit',[['bolt',8,'AN394-17'],['washer',8,'AN960-416L'],['cotter',8,'MS24665-132']],'BOTH SIDES · SEE PLANS 22 / 24',flags=['? VERIFY WIRE ROUTING'])],
 [issue('01–02','Wire lengths, individual terminal allocation and final tension need current-kit confirmation.','HK-EA4 lists totals; supplied photos do not establish lengths or tension.','Match each wire and thread to supplied assembly; confirm routing and tension from controlling documentation.')],photo='G2-TAIL219')
manual(11,'EMP005','Trim Wheel and Linkages','empennage','trim',['Companion plans21–22',FM+' p16',QB+' p4 HK-TS4'],[
 step('INSTALL TRIM WHEEL','wheel',hardware('AN4-22',1,'AN960-416','AN310-4','MS24665-208',3),'#25 CHAIN · SEE PLAN 21',flags=['SOURCE CONFLICT — VERIFY']),
 step('CONNECT TRIM TAB PUSHRODS','rods',hardware('AN3-6A',4,'AN960-10','AN365-1032A'),'4× JM-3 · 4× AN345-10',flags=['? VERIFY ROD LENGTH'])],
 [issue('01','Trim-wheel friction stack differs between drawing and count sheet.','Plan21 shows bronze/split-lock washers; HK-TS4 calls three AN960-416.','Confirm current factory friction stack; inventory is shown separately.'),issue('02','Complete trim cable route, length and adjustment not released.','Plan22 linkage; HK-TS4 supplies rod ends but no completed adjustment.','Verify both tab directions, stops, cable route and rod adjustment with current kit.')],photo='FM16-TRIM')
manual(12,'GEAR001','Main Landing Gear','landing-gear','gear',['Companion plans25–26',FM+' pp9–11',QB+' p1 HK-LG4'],[
 step('FIT FORWARD GEAR ATTACHMENTS','front',hardware('AN6-26',2,'AN960-616','AN310-6','MS24665-283',2),'AIRFRAME SUPPORTED · BOTH LEGS'),
 step('FIT REAR GEAR ATTACHMENTS','rear',hardware('AN6-25',2,'AN960-616','AN310-6','MS24665-283',2),'KEEP AIRFRAME SUPPORTED',flags=['? VERIFY WASHER POSITION'])],
 [issue('01–02','Exact washer allocation, gear alignment and support setup need current-kit verification.','HK-LG4 gives two washers per upper joint; legacy tread values are not adopted.','Verify bolt grip and washer placement without substituting parts. Fit shock struts before loading gear; use current alignment instructions.')],photo='G1-GEAR')
manual(13,'GEAR002','Shock Strut Mounting','landing-gear','shock',['Companion plans25–27',QB+' p1 HK-LG4'],[
 step('FIT UPPER SHOCK STRUT ENDS','upper',hardware('AN6-14A',2,'AN960-616','AN365-624A'),'ASSEMBLED STRUTS · BOTH SIDES'),
 step('FIT LOWER SHOCK STRUT ENDS','lower',hardware('AN6-14A',2,'AN960-616','AN365-624A'),'4× AN316-8R CHECK NUTS',flags=['? VERIFY STRUT CONFIGURATION'])],
 [issue('01–02','Internal shock assembly, service fluid and rod-end adjustment are withheld.','Legacy XAM-7M system differs from current check-nut callout; actual shipped strut configuration not established.','Confirm strut model, bearings, bushings and current assembly/service instructions before loading aircraft.')],photo='G1-GEAR')
manual(14,'GEAR003','Tailwheel','landing-gear',None,[QB+' p2 HK-TW4',FM+' p12'],[],[
 issue('BLOCKED','Current stinger installation cannot be reconstructed from legacy leaf-spring instructions.','HK-TW4 specifies stinger; legacy p12 illustrates leaf springs.','Provide current Companion stinger/tailwheel installation drawing and identify fitted tailwheel.')],status='BLOCKED',photo='G1-TAILWHEEL-CANDIDATE')
manual(15,'GEAR004','Brake Master Cylinders','landing-gear','brakes',['Companion plan29',FM+' pp19–20',QB+' p1 HK-RS4'],[
 step('CONNECT CYLINDERS TO FRAME','lower',hardware('AN3-6',4,'AN960-10L','AN310-3','MS24665-132'),'FOUR CYLINDERS · SEE PLAN 29'),
 step('CONNECT CYLINDERS TO TOE PEDALS','upper',hardware('AN3-7',4,'AN960-10','AN310-3','MS24665-132',4),'CHECK FIREWALL CLEARANCE',flags=['SOURCE VARIANT — VERIFY'])],
 [issue('02','Upper-joint washers depend on master-cylinder variant.','HK-RS4: four AN960-10 per joint; note says two thin washers for Bearhawk cylinders.','Identify shipped cylinder and confirm washer set. No hydraulic routing or brake bleeding instructions are released.')],photo='G1-PEDALS')
manual(16,'FUS002','Front Seats','fuselage','seats',['Companion seat drawing (PDF p1)',FM2+' printed pp26–27',QB+' p4 HK-SH4'],[
 step('JOIN SEAT BACKS TO BASES','backs',hardware('AN4-12',4,'AN960-416L','AN310-4','MS24665-208'),'BACKS OFFSET TOWARD CENTER'),
 step('FIT SEAT ROLLERS','rollers',hardware('AN4-10A',8,'AN960-416L','AN365-428A'),'ROLLERS · BOTH SEATS',flags=['? VERIFY LATCH ENGAGEMENT'])],
 [issue('01–02','Current latch detail and track-stop positions require kit fit check.','HK-SH4 gives incomplete latch line; stops AN4-12A / AN960-416 / AN365-428A, four sets.','Verify latch/stop assembly, positive engagement and full travel. Restraint installation is not released.')],photo='FM26-SEAT')
manual(17,'FUS003','Fuselage Stringers','fuselage','stringers',['Companion plans17–21',FM2+' printed pp28–29',QB+' p4 Stringer attach'],[
 step('SEAT STRINGERS IN STANDOFFS','fit',[],'SMOOTH LINE · CLEAR PULLEYS','STRINGER / SADDLE'),
 step('SECURE STRINGERS TO SADDLES','rivet',[['bolt',43,'CCP-42']],'43 RIVETS · AIRCRAFT TOTAL',flags=['? VERIFY END TRIM'])],
 [issue('01–02','Standoff and end-trim positions must match the actual fuselage.','Plans define shape; legacy photo variations are not adopted as kit geometry.','Verify stringer material, supplied saddles, fabric clearance and smooth aft transition.')],photo='G2-STRINGERS-CANDIDATE')
manual(18,'FUS004','Fuel Selector Mounting','fuselage','fuel_valve',[FM2+' printed pp31–32',QB+' p4 HK-FS4'],[
 step('FIT SELECTOR BRACKET','bracket',[['bolt',2,'AN507C632R6'],['locknut',2,'K1000-06']],'BRACKET TO FUSELAGE',flags=['? VERIFY BRACKET POSITION']),
 step('FIT SELECTOR TO BRACKET','valve',[['bolt',3,'AN507C632R6'],['locknut',3,'K1000-06']],'SELECTOR TO BRACKET',flags=['? VERIFY VALVE CONFIGURATION'])],
 [issue('01–02','Valve model, gascolator support and full port-to-port fuselage plumbing are not established.','HK-FS4 names hardware; legacy explicitly allows different valve arrangements.','Identify supplied selector/gascolator and obtain current routing diagram. Only bracket relationship is illustrated; no port assignment or plumbing is released.')],photo='G2-FUEL35')
manual(19,'WING001','Wing Preparation','wings','wing_prep',[WM+' p3'],[
 step('IDENTIFY WING AND MATCHED PARTS','labels',[],'KEEP GOLD SERIAL TAG','WING / COVER / POCKET SKIN'),
 step('OPEN AND INVENTORY WING BOX','inventory',[],'MATCH LEFT / RIGHT · RETAIN LABELS','PARTS PACKED IN WING')],photo='WM03')
manual(20,'WING002','Tank Bay Covers','wings','tank_cover',[WM+' pp4,8–9',QB+' p5 Wings'],[
 step('MATCH COVER TO TANK BAY','cover',[['bolt',182,'AN507C632R6']],'182 SCREWS · BOTH MAIN COVERS',flags=['? VERIFY DRAIN POSITION']),
 step('PREPARE NUTPLATE PERIMETER','nutplates',[['locknut',182,'K1000-06']],'RIVET FORWARD ROW ONLY',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('01','Drain holes must be transferred from installed tanks.','WM p4; no dimension inferred from scene.','Confirm matched cover and actual drain center before cutting.'),issue('02','Corner nutplates differ between sources; rivet naming is inconsistent.','QB p5: K1000-06 throughout; WM pp8–9: MS21055L06 at four main-bay corners; WM rivet text conflicts with example.','Use QB identities as inventory, obtain factory confirmation at corners and for rivet diameter/length before riveting.')],photo='WM09')
manual(21,'WING003','Aileron Bellcranks and Pulleys','wings','aileron_bellcrank',['Companion plan15',WM+' pp15–16',QB+' p3 HK-AS4'],[
 step('PRESS BELLCRANK BEARINGS','bearings',[['bushing',4,'R4FF']],'TWO BEARINGS + SPACER PER CRANK','PRESS OUTER RACES'),
 step('CAPTURE BELLCRANK BEARINGS','mount',hardware('AN4-27A',2,'AN960-416L','AN365-428A',wm=3),'4× AN970-4 · BOTH BELLCRANKS',flags=['? VERIFY THIN-WASHER STACK']),
 step('FIT AILERON CROSSMEMBER PULLEYS','pulley',hardware('AN4-24A',2,'AN960-416L','AN365-428A'),'2× AN210-4A · FIT CABLE GUARDS',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('02','Thin-washer allocation around large-area bearing retainers needs confirmation.','HK-AS4: three thin and two large-area washers per bellcrank.','Confirm full stack and free rotation; do not press bearing inner races.'),issue('03','Pulley nut designation differs.','WM p15: AN365-416A; QB HK-AS4: AN365-428A.','Keep QB set and verify factory correction; confirm cable guard and upper strut pulley installation separately.')],photo='WM16')
manual(22,'WING004','Aileron Cable Routing','wings','wing_cables',['Companion plan15',WM+' pp13–18,28',QB+' pp2–3 HK-AS4'],[
 step('TRACE ACTUATION CABLE PATH','actuation',[['bushing',2,'MS20220-1'],['bushing',2,'AN210-4A']],'STRUT → FRONT SPAR → BELLCRANK','ROUTING RELATIONSHIP',flags=['? VERIFY GUARDS / CLEARANCE']),
 step('TRACE CARRY-THROUGH PATH','carry',[['bushing',18,'04-05793'],['bushing',4,'05-05500']],'RIB GUIDES → CABIN TURNBUCKLE','ROUTING RELATIONSHIP',flags=['DRILLING TEMPLATES REQUIRED'])],
 [issue('01–02','No hole locations or cable cut lengths are released.','WM p18 requires separate model-specific drill guides 1–5, not supplied.','Obtain current Companion templates, check actual cable sweep and all guards; verify terminations under approved cable process.')],photo='WM13')
manual(23,'WING005','Flap Torque Tube','wings','flap_tube',['Companion plan15',WM+' pp19–21',QB+' p3 HK-FCC'],[
 step('FIT TORQUE TUBE AND PAIRED ARMS','tube',hardware('AN3-12A',4,'AN960-10','AN365-1032A'),'ONE ARM EACH SIDE OF SUPPORT',flags=['? VERIFY POSITION BEFORE DRILLING']),
 step('CONNECT FLAP PUSHRODS','pushrod',hardware('AN3-26',2,'AN960L-10','AN310-3','MS24665-132'),'INSERT PUSHROD BUSHING',flags=['SOURCE CONFLICT — VERIFY']),
 step('FIT RETURN SPRINGS AND BUMPER','spring',[['bushing',2,'W-FRS1'],['bushing','2 cuts','6000-12']],'SPRINGS BEFORE WING CLOSING',flags=['? VERIFY SPRING ATTACHMENTS'])],
 [issue('01–02','QB pushrod bolt differs from current wing manual; setup needs jig verification.','QB: AN3-26 and AN960L-10; WM pp20–21: AN3-16 and AN960-10L.','Keep literal QB callouts; ask factory to verify bolt/washer and jig geometry before match drilling.'),issue('03','Spring end assignment and final preload require kit check.','WM p21 spring/bumper; no preload inferred from photos.','Confirm both W-FRS1 attachments, bumper retention and unrestricted motion.')],photo='WM20')
manual(24,'WING006','Flap Preparation','wings','flap_surface',[WM+' p35',QB+' p3 HK-FCC'],[
 step('FIT MATCHED TRAILING EDGE','fit',[],'KEEP TRAILING EDGE STRAIGHT','RIB / TRAILING-EDGE OVERLAP'),
 step('RIVET TRAILING EDGE','rivet',[['bolt','per hole','CCP-42']],'ALTERNATE HOLES · THEN COMPLETE',flags=['? VERIFY FINAL MOUNT HARDWARE'])],
 [issue('02 / final mount','Final flap-to-weldment mounting is withheld due to incompatible row.','HK-FCC: AN6-6A with AN960-10L and AN365-1032A, six sets.','Obtain corrected factory row. This manual covers surface preparation only; do not install that mixed set.')],photo='WM35')
manual(25,'WING007','Aileron Preparation','wings','aileron_surface',[WM+' pp36–37'],[
 step('FIT AILERON TRAILING EDGE','fit',[],'CURVED LEADING EDGE UP','RIB / TRAILING-EDGE OVERLAP'),
 step('RIVET AILERON TRAILING EDGE','rivet',[['bolt','per hole','CCP-42']],'ALTERNATE HOLES · THEN COMPLETE'),
 step('INSTALL BALANCE TUBE','balance',[['bushing',2,'R-ABT'],['bolt',8,'CCP-42']],'INSERT FROM INBOARD END',flags=['FINAL BALANCE STILL REQUIRED'])],
 [issue('03 / final mount','Surface balance and final hinge/pushrod installation are not released.','WM p37 defers balancing until fabric/paint; complete final attachment details not established by this preparation chapter.','Confirm final hinge hardware, pushrod retention and current balance procedure before flight.')],photo='WM37')
manual(26,'WING008','Main Tanks and Fuel Lines','wings','wing_fuel',[WM+' pp5–7',QB+' pp3–4 HK-FS4'],[
 step('FIT TANK FEED CONNECTIONS','fittings',[['bushing',4,'05-17700'],['bolt',4,'AN816-6D']],'BOTH TANKS · FEED PORTS',flags=['SOURCE CONFLICT — VERIFY']),
 step('PASS LINES THROUGH PROTECTED RIBS','lines',[['bushing',8,'AN931-6-10'],['bushing',6,'AN931-4-7']],'3/8 FEED · 1/4 SIGHT GAUGE',flags=['? VERIFY HOLE LOCATIONS']),
 step('FIT SIGHT-GAUGE BULKHEADS','sight',[['bolt',4,'AN832-4D'],['locknut',4,'AN924-4D'],['bushing',8,'AN819-4D'],['locknut',8,'AN818-4D']],'LINES REST WITHOUT PRELOAD',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('01','Tank strainer identity differs from current wing manual.','QB:05-17700; WM p7:AN375/PN-520.','Verify supplied strainers and tank ports with factory; QB identities retained.'),issue('02–03','Root-hole counts and sight-gauge flare-nut prose contain inconsistencies.','WM p5 mentions five lines then four locations; p6 prose gives AN818-6D for 1/4 tube but figure/QB give AN818-4D.','Use QB fittings; transfer actual tank port geometry and confirm layout. Final tank straps, venting and leak checks require current installation instructions.')],photo='WM07')
manual(27,'WING009','Pitot Mast and Lines','wings','pitot',[WM+' pp25–27'],[
 step('FIT PITOT MAST BASE','mast',[['bolt',6,'AN526C-632R6'],['locknut',6,'K1000-06']],'LEFT WING · SA06BL EXAMPLE',flags=['MATCH ACTUAL MAST TEMPLATE']),
 step('ROUTE PITOT AND AOA LINES','lines',[['bolt',2,'AN818-3D'],['bushing',2,'AN819-3D']],'KEEP CLEAR OF AILERON CABLE',flags=['? VERIFY SELECTED PITOT'])],
 [issue('01–02','Selected mast/pitot and its drilling template are not identified.','WM describes SA06BL / GAP26 example; other equipment differs.','Confirm actual equipment and vendor template; do not transfer geometry from illustration. Wiring remains outside scope.')],photo='WM27')
manual(28,'WING010','Conduit Preparation','wings','conduit',[WM+' p38'],[
 step('PLAN ACCESS BEFORE CLOSING','plan',[],'CONFIRM REQUIRED WING SERVICES','AFT LIGHTENING-HOLE PATH'),
 step('SECURE OPTIONAL CONDUIT','fit',[['bolt','per bracket','CCP-32']],'SUPPORT AT EACH RIB',flags=['? VERIFY SYSTEM CLEARANCE'])],
 [issue('01–02','Conduit diameter, brackets and equipment are configuration-specific.','WM p38 describes optional PEX method, not a universal electrical design.','Confirm required services and clearance from every moving control; no avionics/electrical architecture is specified.')],photo='WM38')
manual(29,'WING011','Inspection Panels','wings','inspection',[WM+' pp29–34',QB+' p5 Wings'],[
 step('MATCH PANEL AND RING','match',[],'LABEL LOCATION · RETAIN ORIENTATION','RING OUTSIDE FOR MATCH-DRILLING'),
 step('INSTALL RING INSIDE SKIN','inside',[['bolt',140,'AN507C632R6'],['locknut',140,'K1000-06']],'140 SCREWS · BOTH WINGS',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('01–02','Cover screw head and ring preparation differ by source/kit revision.','QB countersunk AN507; WM p29 prefers AN526 and varies rivets for .032/.040 rings.','Verify current ring thickness, screw head and compatible dimple/countersink preparation before machining; preserve ring orientation.')],photo='WM34')
manual(30,'WING012','Wing Closing','wings','closing',[WM+' pp39–40',QB+' p5 Wings'],[
 step('CLOSE WING ROOT SKIN','root',[],'COMPLETE INTERNAL SYSTEMS FIRST',flags=['? VERIFY RIVET LENGTH']),
 step('CLOSE MAIN LOWER SKIN','main',[['bolt',316,'MS20426AD-3-3.5']],'COUNT-SHEET TOTAL · BOTH WINGS',flags=['? VERIFY EACH MATERIAL STACK']),
 step('CLOSE AFT TANK BAY SKIN','aft',[],'LEAVE AFT DOUBLER ROWS OPEN',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('01–03','Rivet callouts and local stack lengths require location-specific verification.','QB p5 stock totals; WM pp39–40 contain inconsistent rivet examples and thicker aft-bay rows.','Complete internal inspection, verify every local rivet and approved bucking method; schematic rows are not a drilling/rivet-count map.')],photo='WM39')
manual(31,'WING013','Aileron Pocket Skins','wings','pocket',[WM+' pp41–42',QB+' p5 Wings'],[
 step('FIT THREE MATCHED POCKET SKINS','fit',[],'LONG CENTER · TWO SHORT ENDS','KEEP TRAILING EDGE STRAIGHT'),
 step('ATTACH POCKET SKINS','rivet',[['bolt',108,'CCP-42'],['bolt',248,'MS20426AD-3-3.5']],'BOTH WINGS · VERIFY LOCAL LENGTH',flags=['SOURCE CONFLICT — VERIFY'])],
 [issue('01–02','Rivet length and implied hole totals differ.','QB 248 skin rivets at -3.5; WM p42 -3 and p41 7+32+8 locations per edge.','Retain QB identities, verify actual matched holes, stack lengths, dimple/countersink method and factory count before riveting.')],photo='WM42')
manual(32,'WING014','Wing Tips','wings','tip',[WM+' pp12,43',QB+' p5 Wings'],[
 step('FIT TIP TO MATCHED WING END','fit',[],'EVEN OVERLAP · KEEP TIP SQUARE','TRANSFER EXISTING NUTPLATES'),
 step('ATTACH REMOVABLE WING TIP','attach',[['bolt',84,'AN526C-632-6'],['locknut',84,'K1000-06']],'84 LOCATIONS · BOTH WINGS',flags=['? VERIFY AILERON CLEARANCE'])],
 [issue('01–02','Tip fit and trailing-edge termination depend on supplied composite tip.','WM p43 distinguishes open/closed trailing edges and different materials.','Trial-fit actual aileron before trimming; confirm clearance and screw locations. Illustration is not a cutting template.')],photo='WM43')
manual(33,'FINAL001','Wing and Lift Strut Attachments','final-assembly','wing_attach',['Companion plans16,21',QB+' p3 HK-WA4'],[
 step('ALIGN SUPPORTED WING ROOT','root',[['bolt',2,'AN6-15A'],['bolt',2,'AN5-12A']],'FRONT / REAR SPAR · BOTH WINGS',flags=['? VERIFY ATTACHMENT STACK']),
 step('FIT SUPPORTED LIFT STRUTS','strut',hardware('AN6-15A',4,'AN960-616','AN365-624A'),'UPPER + LOWER ENDS · BOTH WINGS',flags=['? VERIFY INCIDENCE / RIGGING'])],
 [issue('01–02','Full lifting procedure, strut fitting assembly and incidence setup are not released.','HK-WA4 gives root/end hardware; strut-fitting washer AN960-428 is unresolved.','Use current factory supported-wing procedure; confirm all stack/grip details and plan incidence before loading. Do not drill structural holes from scene.')],photo='PLAN21')
manual(34,'FINAL002','Wing Root Connections','final-assembly','root_connections',[WM+' pp13,28',QB+' pp3–4 HK-AS4 / HK-FS4'],[
 step('JOIN AILERON CARRY-THROUGH CABLE','cable',[['rodend',1,'AN140-22S']],'CABIN TURNBUCKLE · SEE PLAN 15',flags=['? VERIFY RIGGING']),
 step('JOIN WING ROOT FUEL FEEDS','fuel',[['bushing',2,'05-03598'],['bushing',8,'6504']],'SLEEVE STOCK / CLAMPS: KIT TOTAL',flags=['? VERIFY HOSE APPLICATION'])],
 [issue('01–02','Final cable rigging and fuel sleeve lengths/clamp allocation are not established.','QB lists turnbuckle and hose/clamp totals, not all installation details.','Obtain current final-assembly instructions. Verify cable safetying, full travel, fuel sleeve specification and leak testing before closing fairings.')],photo='WM13')
manual(35,'FINAL003','Final Rigging Checks','final-assembly',None,['Companion plans; supplied current and legacy manuals'],[],[
 issue('BLOCKED','A complete consistent Companion rigging/check set has not been established.','Surface travels, neutral references, balance, cable tensions and configuration-specific adjustments require consolidated current factory values.','Obtain current Companion final rigging checklist and resolve source conflicts before release.')],status='BLOCKED')
manual(36,'EMP006','Vertical Stabilizer','empennage',None,['Companion plan20; QB hardware sheet'],[],[
 issue('BLOCKED','No separate bolt-on vertical-fin operation is established for this QB fuselage.','Fin appears in welded fuselage structure; no distinct installation callout found.','Confirm delivered welded fin configuration and inspection requirements. Do not invent a fin attachment or copy another model.')],status='BLOCKED')

def main():
    old=json.loads((ROOT/'docs/assets/images/control-sticks/assembly.json').read_text(encoding='utf-8'))
    old.update(number=1,section='controls',status='REVIEW REQUIRED',model='preserved',sources=[old['geometry_authority'],old['hardware_authority']],photo='G2-CONTROL101')
    old['issues']=[issue('02','Generic plan pivot notation differs from specific QB callout.','Plan28 AN4 vs HK-CS4 AN174-20.','Confirm current-kit correspondence; retain QB set.'),issue('05','Legacy moving-joint retention guidance differs from QB rod-end set.','Legacy p18 vs HK-CS4 AN3-7A / AN365-1032A.','Confirm application; retain QB set.'),issue('04,06','Application of both pushrod nut types unresolved.','HK-CS4 AN316-4R and AN345-524.','Confirm each application; existing separate tray retained.'),issue('05,06','Bellcrank lateral position/spacers unverified.','Legacy p18 does not settle Companion kit fit.','Confirm support, spacers and flap-cable clearance.')]
    all_items=[old]+catalog
    # Preserve the original 46 public review identifiers across later additions.
    review_number=0
    for m in all_items:
        for r in m['issues']:
            review_number+=1
            r['key']=f'BH-REV-{review_number:03d}'
    from beartracks_update import apply_updates
    apply_updates(all_items)
    # Shape families identify parts visually; exact designations remain literal.
    for m in catalog:
        if m['id']=='FUS003':m['photo']='FM28-STRINGERS'
        for s in m['steps']:
            for row in s['hardware']:
                pn=row[2]
                if pn.startswith('K1000'):row[0]='nutplate'
                elif pn.startswith('CCP-'):row[0]='rivet'
                elif pn.startswith('MS20426'):row[0]='rivet_flush'
                elif pn.startswith('AN507'):row[0]='screw_flat'
                elif pn.startswith('AN526'):row[0]='screw_round'
                elif pn.startswith(('AN393','AN394')):row[0]='pin'
                elif pn.startswith('AN115'):row[0]='shackle'
                elif pn.startswith(('AN130','AN140')):row[0]='turnbuckle'
                elif pn in ['W-FRS1','R-FHS']:row[0]='spring'
                elif pn in ['6000-12','05-03598']:row[0]='hose'
                elif pn=='6504':row[0]='clamp'
                elif pn=='05-17700':row[0]='strainer'
                elif pn.startswith(('AN816','AN832')):row[0]='fitting'
                elif pn.startswith('AN818'):row[0]='tubenut'
                elif pn.startswith('AN924'):row[0]='hexnut'
                elif pn.startswith(('AN210','MS20220')):row[0]='pulley'
    for m in all_items:
        (ROOT/'specs'/f'{m["number"]:02d}_{m["id"]}.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
    (ROOT/'specs/catalog.json').write_text(json.dumps(all_items,indent=2,ensure_ascii=False),encoding='utf-8')
    print(len(all_items),'scope entries;',sum(bool(x['steps']) for x in all_items),'manuals;',sum(len(x['steps']) for x in all_items),'instruction pages')
if __name__=='__main__':main()
