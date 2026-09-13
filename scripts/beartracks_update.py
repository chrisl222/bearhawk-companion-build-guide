"""Reviewed Beartracks supplements. Never promote legacy numbers to Companion specs.

Applied to the baseline catalog on every rebuild; repeat runs are deterministic.
Original article text and scans remain in the user's reference library.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
REVISED=['CTRL002','CTRL004','EMP002','EMP005','GEAR001','GEAR002','GEAR004','WING006','WING007']
FACTORY='https://www.bearhawkaircraft.com/s/'

def apply_updates(items):
    byid={m['id']:m for m in items}
    data=json.loads((ROOT/'specs/beartracks_index.json').read_text(encoding='utf-8'))
    for entry in data['references']:
        for id in entry.get('manuals',[]):
            m=byid[id]
            m.setdefault('supplements',[]).append(entry['id'])
            m['sources'].append(entry['source'])
    def issue(id,key,steps,problem,source,check):
        byid[id]['issues'].append(dict(key=f'BH-REV-{key:03d}',steps=steps,issue=problem,source=source,check=check))
    def flag(id,step,text):byid[id]['steps'][step-1]['flags'].append(text)
    def note(id,step,text):byid[id]['steps'][step-1]['note']=text
    def check(id,text):byid[id].setdefault('before_build',[]).append(text)

    check('CTRL002','Before fitting brake pedals, identify the master cylinders and check factory AD-002. Replacement Matco cylinders require travel restrictors on the Companion. See GEAR004.')
    note('CTRL002',2,'CHECK CYLINDER TYPE / TRAVEL RESTRICTORS')
    flag('CTRL002',2,'READ FACTORY AD-002 FIRST')
    byid['CTRL002']['issues'][0]['check']+=' Keep hoses and return springs clear of the complete pedal sweep; check required Matco restrictors (AD-002 / GEAR004).'

    check('GEAR004','Factory AD-002 (4/1/2025) requires removal of affected Avipro/Barrows master cylinders and contact with Bearhawk for replacement. Gerdes cylinders are excluded by that alert. Identify parts from records and the factory guide; appearance alone is not sufficient.')
    check('GEAR004','For the supplied Matco replacement on a Companion, install the factory travel restrictors using AD-002 pages 3-4. Existing QB mounting inventories below do not establish the replacement-cylinder washer stack or restrictor hardware.')
    for s in byid['GEAR004']['steps']:
        s['flags']=['AVIPRO/BARROWS: REPLACE PER AD-002','? VERIFY REPLACEMENT HARDWARE']
        s['hardware_label']='QB INVENTORY - VERIFY VARIANT'
        s['source_tag']='FACTORY AD-002 pp1-4'
        s['note']='MATCO: TRAVEL RESTRICTORS REQUIRED'
    issue('GEAR004',47,'BEFORE 01-02','Affected Avipro/Barrows brake cylinders require replacement; Matco travel restrictors and replacement mounting stack require verification.','2022 Q1 p9 introduced the cylinders; 2023 Q3 p8 warned about dual brakes. Factory AD-002, 4/1/2025, now directs removal and replacement; pp3-4 show restrictors.','Identify all installed/supplied cylinders. Follow factory replacement instructions and verify Companion restrictors before using the depicted mounting relationships. Do not reuse the old washer variant note as Matco installation data.')

    check('CTRL004','Factory AD-004 identifies the aft-most flap-system pulley for recurring inspection and replacement. Keep access to this pulley when fitting the baggage floor; use the factory illustration to identify it on your kit.')
    note('CTRL004',3,'REPLACE PULLEY: 500 h / AS NEEDED')
    flag('CTRL004',3,'AD-004: INSPECT ANNUAL / 250 h')
    byid['CTRL004']['steps'][2]['detail']='AFT PULLEY · INSPECTION ACCESS'
    flag('CTRL004',1,'FLAP SPEED / DEFLECTION: SEE REVIEW')
    issue('CTRL004',48,'03','Aft-most flap pulley inspection and service-life tracking are absent from the earlier guide.','Factory AD-004, 12/11/25: MS20220-1 (AN202A-1); inspection annual / 250 h; replacement 500 h or as needed.','Identify the aft-most pulley on the actual Companion, check condition, preserve access, and record installed hours/inspection and replacement due points per AD-004. Full cable routing remains an open item.')
    issue('CTRL004',49,'01 / final rigging','First flap-speed setting conflicts between newsletter and current factory alert; in-flight deflections are not ground rigging targets.','2022 Q4 p9 and 2023 Q1 p9: 100 mph at 10 degrees; current factory OA-002: 95 mph at 10 degrees. Both associate limits with in-flight air-loaded deflection.','Obtain current applicable Companion limits from the designer/factory before placarding. Do not tighten/preload cables to force ground angles to the in-flight values. See FINAL003 for the remaining rigging requirements.')
    byid['FINAL003']['issues'][0]['source']+=' Beartracks 2018 Q3 pp3-5 is original 4-Place rigging experience, not Companion numerical rigging data; see BH-REV-049 for the flap-speed conflict.'
    byid['FINAL003']['issues'][0]['check']+=' Include independent verification of control direction, full travel, friction and attachment security; record actual Companion datum measurements.'

    note('EMP002',1,'CHECK EACH HALF FOR FREE MOVEMENT')
    note('EMP002',2,'RECHECK AFTER HORNS / WIRES / CABLES')
    byid['EMP002']['issues'][0]['check']+=' Check each elevator independently, then repeat after joining horns, tensioning brace wires and connecting cables. Isolate any stage that introduces binding; do not copy the article\'s shim fabrication, balance additions or -4 degree tail setting.'

    # New check view identifies the outboard arm joint, not an invented assembly stack.
    byid['EMP005']['steps'].append(dict(title='CHECK OUTBOARD TRIM ARM JOINTS',view='arm_check',hardware=[],note='BOTH STABILIZERS · KEEP INSPECTION ACCESS',detail='ARM COLLAR / TORQUE TUBE',flags=['? VERIFY JOINT TREATMENT'],check_lines=['CHECK ARM-TO-TUBE PLAY','RECHECK THROUGH FULL TRAVEL','RETAIN ACCESS AFTER COVERING'],source_tag='BEARTRACKS 2022 Q2 p4 · PLAN 22'))
    issue('EMP005',50,'03','Factory-kit bolted outboard trim arms may develop play; the newsletter recommendation does not identify an exact compound grade or establish this kit\'s joint.','2022 Q2 p4, Mark Goldberg: outboard arm-to-tube joint, surface cleaning and red Loctite recommendation before bolt installation.','Confirm the delivered bolted-versus-welded joint, current factory treatment/compound and fastener stack. Check both arms for play and preserve inspection access. Do not apply compound to rotating supports or rod ends.')
    byid['EMP005']['issues'][1]['source']+=' The 2019 Q1 p2 trim-tension notice predates and does not name the Companion; its numerical tension is not adopted.'

    byid['GEAR001']['steps'].append(dict(title='CHECK LOADED GEAR SPREAD',view='spread',hardware=[],note='OA-001 · MEASURE AT FRONT OF TIRES',detail='TIRE CENTERLINE / FRONT MEASUREMENT',flags=['RECORD LOAD AND MEASUREMENT'],check_lines=['ROLL STRAIGHT AT LEAST 25 ft','72 in AT FLYING WEIGHT','74 in MAXIMUM STATIC SPREAD'],source_tag='FACTORY OA-001 · 2023 Q1 p9'))
    byid['GEAR001']['issues'][0]['source']='HK-LG4 gives two washers per upper joint; Companion plan25 and factory OA-001 now supply spread criteria. Aircraft-specific stack and measured alignment still need verification.'
    byid['GEAR001']['issues'][0]['check']='Verify bolt grip, washer allocation and support setup. With completed gear/wheels and appropriate static load, roll straight at least 25 ft before measuring tire centers at their fronts; record load and spread under OA-001. Do not measure immediately after a pivot turn.'
    byid['GEAR001']['issues'][0]['steps']='01-03'
    check('GEAR001','The May 29, 2025 Barrows heavy-duty gear material note is optional and names the Companion. It is indexed as a configuration choice; this guide does not direct modification or replacement of the supplied gear.')
    note('GEAR002',1,'VERIFY ROD-END ENGAGEMENT · OA-001')
    note('GEAR002',2,'CHECK LOADED SPREAD · GEAR001 STEP 03')
    byid['GEAR002']['issues'][0]['source']+=' OA-001 specifies a recommended 5/8 in minimum rod-end thread engagement and describes configuration-dependent adjustment points.'
    byid['GEAR002']['issues'][0]['check']+=' Verify minimum engagement using the applicable factory method; exposed thread length alone is not an engagement measurement. Use GEAR001 step03 for loaded spread.'

    note('WING006',1,'MATCH PARTS · CHECK 2021 HINGE UPDATE')
    flag('WING006',1,'? VERIFY INBOARD HINGE REVISION')
    issue('WING006',51,'BEFORE FINAL HINGE FIT','April 2021 inboard flap hinge drafting correction explicitly includes the Companion.','2021 Q2 PDF p9 (issue p1), Updates from Bob Barrows; corrected hinge sketch.','Compare the applicable Companion hinge drawing and supplied hinges with the corrected sketch before drilling. Obtain a legible current drawing if dimensions cannot be confirmed. The illustration is not a drilling template.')
    byid['WING006']['issues'][0]['check']+=' For hinge fitting, use the applicable airfoil templates to hold the surface flush while checking hinge alignment and bolt access; use current plans for offsets and hole dimensions, not the builder\'s 2022 jig dimensions.'
    note('WING007',3,'BALANCE AFTER FINAL FABRIC / PAINT')
    byid['WING007']['issues'][0]['check']+=' Use current airfoil templates to check position, align hinge pivot axes, retain bolt access and check freedom of movement before final fastening. Beartracks 2022 Q1 pp6-7 supplies technique/photos only; no jig dimensions or hardware substitutions are adopted.'

    for id in REVISED:
        m=byid[id];m['revision']=3
        for n,s in enumerate(m['steps'],1):
            s['number']=n
            # Existing URLs remain stable; revision is authoritative metadata.
            s.setdefault('image',f'{id}_step_{n:02d}_v2.png')
