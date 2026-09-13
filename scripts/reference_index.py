"""Compact record of actually reviewed photographs and indexed candidates."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
rows=[]
def add(id,ref,model,subsystem,detail,basis):
    rows.append(dict(id=id,reference=ref,model=model,subsystem=subsystem,detail=detail,applicability=basis))
G='https://drive.google.com/drive/folders/'
add('G2-CONTROL101',G+'1vfpLsJLY3iOhNEbOt9k9aPnhKhofFXyL'+' | photo #101.jpg','Unknown','CONTROL_STICKS','Full view: torque-tube saddle on metal mounting tab.','Localized saddle relationship compared with Companion plan28; no model-wide equivalence claimed.')
add('G1-PEDALS',G+'1x7cV4SXHpnLQkiMElW0uLASLUAeldCsg'+' | Rudder Pedals side view.HEIC; Rudder pedals upper view.HEIC','Five','RUDDER_PEDALS','Full side + upper views: paired shafts, four pedals, cylinders forward of toe pedals.','Use only shared pedal/cylinder relationship that agrees with Companion plan29; no Five frame dimensions adopted.')
add('G2-FLAP158',G+'1rfsZ0aSDObBgWhoKHNnYVGT8rrNB6DGO'+' | photo #158.jpg','Unknown','FLAP_CONTROLS','Full oblique close-up: handle, quadrant, detent engagement and support.','Localized handle/quadrant relationship compared with Companion plan30; routing not established.')
add('G2-BELLCRANK',G+'1kvRGRbWYW6XQBfMvm5CYn8V3RMzb37jS'+' | photo #46.jpg; photo #73.jpg','Unknown','ELEVATOR_CONTROLS','Grid thumbnails: two rod-end pushrod; two-plate bellcrank and pivot spacers.','Candidates for detailed follow-up; thumbnail review alone does not release spacer allocation.')
add('G2-TAIL',G+'1VvJ7_bwjeg0k0vut4JDZ4kkSMxRp7T1Y'+' | photos #211–220.jpg','Unknown','EMPENNAGE','Grid thumbnails: hinge line, upper/lower brace tabs and rear control connections.','Localized connections consistent with Companion plans22/24; full-view factory-manual photos also used below.')
add('G2-TAIL219',G+'1VvJ7_bwjeg0k0vut4JDZ4kkSMxRp7T1Y'+' | photos #219.jpg; #220.jpg','Unknown','EMPENNAGE','Grid thumbnails: upper rudder/brace terminal and lower brace terminal.','Orientation aid only; no terminal lengths, tension or fastener identity derived.')
add('G2-FUEL35','https://drive.google.com/file/d/1nskz5nUUq13BUy_y7x3VJDuH7Oo8qWSj/view','Unknown','FUEL_SYSTEM','Full oblique view: selector mounted to triangular floor-frame bracket.','Bracket relationship only, supported by factory manual; valve ports/configuration unconfirmed.')
add('G1-GEAR','https://drive.google.com/file/d/10qsyBWlpV291c6wcx8sdO7eky3v35gxf/view','Five','LANDING_GEAR','Main Gear.HEIC, full front view: paired legs and diagonal shock-strut endpoints.','Only generic leg/strut relationship matching Companion plans25/26 used; no Five alignment, dimensions or internal strut design adopted.')
add('G3-FLAP-ROD','https://drive.google.com/file/d/1qUskTP6uEV9Hz5Of9FnCk0lWLVEVqIM6/view','Unknown','WING_FLAPS','Rh Wing Flap Control Rod.JPG, full spanwise view: tube, crossmember and actuator arm relationship.','Local relationship compared with Companion plan15 and current wing manual pp19–21.')
add('G3-LIFT-STRUT',G+'1kF0mZW0g2eYksAfbHnH15K-rl5mJ_31q'+' | Rh Strut Initial Fit Check.JPG','Unknown / legacy','FINAL_ASSEMBLY','Full oblique wing-to-fuselage view: single lift strut under main spar during supported fit.','Compared with Companion plan16 and HK-WA4 counts. Removed an incorrect second strut from the simplified scene; no photo dimensions or rigging settings adopted.')
add('G3-AILERON-CRANK',G+'1QaOs97Q0JW7ldl0M_zi3jpxNZLQLytPX'+' | Rh Wing Aileron Bell Crank.JPG','Unknown / legacy','WING_AILERONS','Full installed view: bearing axis through wing thickness and output arm through rear-spar factory opening.','Agrees with current wing manual p16; corrected the simplified pivot axis. Folder search did not establish an installed balance-tube photograph.')
def wm(p,tag,detail,photo=''):
    add(f'WM{p:02}',f'Wing+Build+Manual+Rev+2-compressed.pdf, p{p}'+photo,'Factory manual: multiple Bearhawk models',tag,detail,'Use applicable Companion instructions/plan constraints; photograph supplies installed appearance only.')
wm(3,'WING_CLOSING','CAD diagram only: packed wing and removable matched parts. No installation photograph reviewed on this page.')
wm(7,'WING_FUEL','Real photos: tank feed fittings and inboard bay; lines pass root and tank-bay ribs.')
wm(9,'WING_FUEL','Real main-tank cover/bay photos. Auxiliary-tank examples excluded.')
wm(13,'WING_AILERONS','Real interior/carry-through view and lift-strut pulley bracket close-up.')
wm(16,'WING_AILERONS','Bench bearing/bellcrank photo plus installed bellcrank close-ups; also exploded CAD.')
wm(20,'WING_FLAPS','Real tube/support setup and paired actuator arms with pushrod cross-tube and bumper.')
wm(27,'PITOT','Real pitot/fitting/line examples; SA06BL/GAP26 example is equipment-conditional.')
wm(34,'WING_CLOSING','Real nested rectangular inspection ring installed inside wing skin.')
wm(35,'WING_FLAPS','Real trailing-edge sheet overlap close-up; CAD provides whole-surface context.')
wm(37,'WING_AILERONS','CAD balance-tube relationship only on reviewed figure; no installed balance photo established.')
wm(38,'WING_CLOSING','Real conduit passing ribs; rib bracket and control clearance context.')
wm(39,'WING_CLOSING','Real lower-skin closure and riveting/access views.')
wm(42,'WING_CLOSING','Real curved aileron-pocket skin fitting with clecos; also CAD three-piece overview.')
wm(43,'WING_CLOSING','Real composite wing-tip overlap and trailing-edge termination details.')
FM='BHManual-Fuselage1-25Rev1.pdf'
add('FM13-TAIL',FM+' p13','Legacy / model not identified','EMPENNAGE','Full installation photo: stabilizer/elevator outline and brace relationship.','Companion plans20/22 constrain use; legacy incidence value not adopted.')
add('FM15-HINGES',FM+' p15','Legacy / model not identified','EMPENNAGE','Rear-fin hinge/tab view and horizontal hinge head/nut orientation.','Localized hardware axis/hinge appearance; current Companion sheet controls identity.')
add('FM16-RUDDER',FM+' p16; G2-TAIL photos #217–218','Legacy / gallery model unknown','RUDDER_PEDALS','Rear control-horn and cable connection context; gallery thumbnails show rudder horn.','Rudder-specific shape constrained by Companion plan24; full route remains unresolved.')
add('FM16-ELEVATOR',FM+' p16','Legacy / model not identified','ELEVATOR_CONTROLS','Real aft view: elevator horns, rear cables and trim tube.','Local plan22 relationships used; cable cut lengths not inferred.')
add('FM16-TRIM',FM+' p16','Legacy / model not identified','ELEVATOR_CONTROLS','Real overhead trim wheel and rear trim linkage views.','Plans21/22 control geometry; friction-stack conflict retained.')
add('FM23-FLOOR',FM+' p23','Legacy / model not identified','CONTROL_STICKS','Real overall floor and close-up around control torque tube.','Panel/access relationship only; shapes fit actual Companion frame.')
add('FM26-SEAT','BHManual-fuselage26-45Rev2.pdf, printed p26','Legacy / model not identified','SEATS','Seat-base/back frame hinge photograph.','Localized relationship checked against supplied Companion seat drawing; latch/stop detail unresolved.')
add('FM28-STRINGERS','BHManual-fuselage26-45Rev2.pdf, printed pp28–29','Legacy / model not identified','FINAL_ASSEMBLY','Real overall stringer arrangement, underside saddle and U-saddle end trim.','Plan-defined shape/current kit standoffs constrain use; no photo dimensions adopted.')
add('PLAN21','Bob Barrows Official Companion Plans - Sep 12 2026 - 19-03.pdf, plan21','Companion','FINAL_ASSEMBLY','Drawing only: cabin carry-through and wing-root fittings.','Controlling design drawing, not a photograph; no real Companion full wing-lifting sequence established.')
add('G1-TAILWHEEL-CANDIDATE',G+'1HQ8DMsCrgTQ0mHv-YTcuNDh1QpalqXv9'+' | Tailwheel.HEIC; Tailwheel2.HEIC','Five','TAILWHEEL','Filenames indexed; images not opened.','Not used: equivalence to current Companion stinger installation unestablished.')

candidates=[
('G1','Ailerons','1iKdS5D0ebfhH90e_TbdiISNT_5gZ2Wct','WING_AILERONS'),('G1','Brakes','1bivR4VRCtDGkuV4v1E1feADx9gSDd8zv','RUDDER_PEDALS'),('G1','Flaps','1_awXLzKIII0cw4-GwhFk96AojRcfkYbu','WING_FLAPS'),('G1','Wing Inspection Panels','1qIRJiwNNovR3q7qoAQJaH6oEmDma57Vj','WING_CLOSING'),
('G2','Formers 1–5','1CFPC_7aUmswA6IGGn2diJ00Qs4WyxmmV','FINAL_ASSEMBLY'),('G2','Stringers 6–11','13HMWtHE-rUnRnQHOjY2ZJDB8Uy0Cv4n3','FINAL_ASSEMBLY'),('G2','Fuel lines 36–38','1vzwoFV_uq8De42S2ShU91ysQfg0a_Ypz','FUEL_SYSTEM'),('G2','Floorboards 39–43','1XwMw02YHBxkib__88o-f3WBAfZlmn_a3','CONTROL_STICKS'),('G2','Fuel valve 70–72','17FKJaE0AkyVy1VVN7UJ0NhiHUrVyJYpw','FUEL_SYSTEM'),('G2','Shock struts 89–100','1cFiSJCVaKt8c9aDjkEp5sWpATTcebr2d','LANDING_GEAR'),('G2','Trim 103,150–162','19fjLUwr8JobXulyUvfDRtq1maBWF2-zC','ELEVATOR_CONTROLS'),('G2','Gear and belly 106–119','1EquwWyM9SZDjiWrn-BVp_ZvYxTjJZnYV','LANDING_GEAR'),('G2','Tunnel 115–118','1hQN6z7xCsh9qHGl7p53_wD1F01vS6PAv','CONTROL_STICKS'),('G2','Rudder cables 134–138','1YNjutAviZX0KIWxl82SWkJR7gmomKF8M','RUDDER_PEDALS'),('G2','Elevator cables 139–149','19016NP7AAq0PAtwwAWP8rMzBl_tDWZYJ','ELEVATOR_CONTROLS'),('G2','Brake lines 164','1O2maffERYZQivMve8DA4P7NSsDd2cLDF','RUDDER_PEDALS'),('G2','Tank covers 165–168','1wf9f09ULPIugpOh-re2QRKO-kDLaTVL8','WING_FUEL'),('G2','Flap cable pulleys 169–171','1FJV15t7SsB4P3bPrFMZSUudCtOW1FEJh','FLAP_CONTROLS'),('G2','Aileron pulley 172','1yilGSloufybd9YGIo5qqsLgjree5NXrZ','WING_AILERONS'),('G2','Inspection plates 173–178','1EOoH64Nu12MUV2nyu_8mGmfcB5Tx9-Wh','WING_CLOSING'),('G2','Flap tube 188–191','1fd7eXgSbLb6s_rdA2rFzRw9reAipmy3O','WING_FLAPS'),('G2','Flap tube drilling 192–196','1_2et5H7Ahg5w8yY-uo53g6PFOqaPOAmG','WING_FLAPS'),('G2','Fuel line holes 197–201','1ELVHAXwMvZzq4wz9h1QCbChy8a6_XS0t','WING_FUEL'),('G2','Aileron holes 204–205','134TtKrU0jeIxpCnW3NH9zgKomLFieLiF','WING_AILERONS'),
('G3','Ailerons','1QaOs97Q0JW7ldl0M_zi3jpxNZLQLytPX','WING_AILERONS'),('G3','Fuel tanks','1yioOW4rH5OmehkC00mFHhxBgB6jm-Nnb','WING_FUEL'),('G3','Lift struts','1kF0mZW0g2eYksAfbHnH15K-rl5mJ_31q','FINAL_ASSEMBLY'),('G3','Wing inspection covers','1EpKOwqIvkAoSli4QMlOXGhagxRsXlwrL','WING_CLOSING'),('G3','Wings general','1MX9xI0dfX33R1tNQ_T3NOcCQUtlioBHA','FINAL_ASSEMBLY'),('G3','Fuselage additional','1I93EMAOxYi2FUzscuGkfxW9MlSPIvfWa','FINAL_ASSEMBLY')]
data=dict(reviewed=rows,candidates=[dict(gallery=g,name=n,reference=G+i,subsystem=t,model='Five' if g=='G1' else 'Unknown',review='Folder indexed; contents not visually reviewed') for g,n,i,t in candidates])
data['candidates']=[r for r in data['candidates'] if not (r['gallery']=='G3' and r['name'] in ['Lift struts','Ailerons'])]
(ROOT/'specs/photo_index.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
text=['# Photo index','', 'First pass: 2026-09-13. This is a selective subsystem index, not an exhaustive review of every gallery image. Consult it before reopening galleries. No gallery photograph has been verified as Companion-specific from its label. Factory photos and Companion plans constrain localized use.','', 'Photos establish appearance, side, orientation and connections only. They never establish dimensions, hole locations, materials, bolt designations, grip or washer order. Plans control design; the current Companion count sheet controls explicit QB hardware.','', '## Reviewed views and drawing references','']
for r in rows:
    text += [f'### {r["id"]}',f'- Reference: {r["reference"]}',f'- Model / subsystem: {r["model"]} / {r["subsystem"]}',f'- View: {r["detail"]}',f'- Use: {r["applicability"]}','']
text += ['## Indexed candidates — open only when relevant','', '| Gallery | Folder | Subsystem | Review |','|---|---|---|---|']
for r in data['candidates']:text.append(f'| {r["gallery"]} | [{r["name"]}]({r["reference"]}) | {r["subsystem"]} | Not opened |')
(ROOT/'PHOTO_INDEX.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
print(len(rows),'reference records;',len(data['candidates']),'candidate folders')
