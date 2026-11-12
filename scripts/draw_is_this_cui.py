#!/usr/bin/env python3
"""Draw docs/diagrams/is-this-cui.drawio from the skill's transitions.json.

Usage: python3 scripts/draw_is_this_cui.py, then export the PNG with
  drawio -x -f png -e -b 10 -o docs/diagrams/is-this-cui.drawio.png docs/diagrams/is-this-cui.drawio
Positions are fixed below; a new state or outcome needs a position and its edges."""
import html, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.argv[1:] = [str(ROOT / "skills/is-this-cui/transitions.json"), str(ROOT / "docs/diagrams/is-this-cui.drawio")]
T=json.load(open(sys.argv[1]))
S=1.6
W,H=200*S,50*S
POS={"public":[285,10],"owner":[285,100],"items":[20,215],"designated":[285,215],"authority":[285,330],"notify":[285,445],"notice_open":[285,560],
 "Public":[550,10],"Proprietary (own)":[20,100],"Proprietary (third-party)":[550,100],"FCI":[550,270],"CUI":[550,445]}
EDGES=[("public","public",[[485,35],[550,35]]),("public","nonpublic",[[385,60],[385,100]]),("owner","ours",[[285,125],[220,125]]),
 ("owner","theirs",[[485,125],[550,125]]),("owner","reuse",[[320,150],[320,182],[120,182],[120,215]]),("owner","gov",[[440,150],[440,215]]),
 ("items","clean",[[60,215],[60,150]]),("items","reuses",[[220,235],[285,235]]),("items","unsure",[[120,265],[120,480],[285,480]]),
 ("designated","marked",[[440,265],[440,330]]),("designated","unmarked",[[485,240],[515,240],[515,295],[550,295]]),
 ("designated","clue",[[300,265],[300,300],[250,300],[250,462],[285,462]]),("authority","yes",[[485,350],[520,350],[520,460],[550,460]]),
 ("authority","no",[[440,380],[440,445]]),("notify","propose_cui / propose_fci / propose_own / propose_theirs",[[385,495],[385,560]]),
 ("notice_open","reply_cui",[[485,575],[650,575],[650,495]]),("notice_open","reply_fci",[[485,592],[700,592],[700,320]]),
 ("notice_open","reply_own",[[285,585],[8,585],[8,130],[20,130]]),("notice_open","reply_theirs",[[385,610],[385,635],[766,635],[766,120],[750,120]])]
OFF=40
def p(v): return v*S+OFF
cells=[]
def esc(s): return html.escape(s,quote=True)
for i,(k,(x,y)) in enumerate(POS.items()):
    if k in T["states"]:
        hold=T["holding"].get(k)
        fill="#E8B923" if hold else "#555555"
        lab=f"<font style='font-size:11px'>{k}</font><br><b>{esc(T['states'][k]['question'])}</b>"
        if hold: lab+=f"<br><i style='font-size:11px'>records: {esc(hold)}</i>"
        st=f"rounded=1;arcSize=12;fillColor={fill};strokeColor=none;fontColor=#FFFFFF;fontSize=14;whiteSpace=wrap;html=1;"
    else:
        color={"CUI":"#9B6FB5","FCI":"#777777","Public":"#2E8B57","Proprietary (own)":"#2E8B57","Proprietary (third-party)":"#5B7FA6"}[k]
        lab=f"<b>{esc(k)}</b>"
        st=f"rounded=1;arcSize=50;fillColor={color};strokeColor=none;fontColor=#FFFFFF;fontSize=16;whiteSpace=wrap;html=1;"
    cells.append(f'<mxCell id="n{i}" value="{esc(lab)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{p(x)}" y="{p(y)}" width="{W}" height="{H}" as="geometry"/></mxCell>')
for j,(f,ev,pts) in enumerate(EDGES):
    a,b=pts[0],pts[-1]
    mids="".join(f'<mxPoint x="{p(x)}" y="{p(y)}"/>' for x,y in pts[1:-1])
    st="edgeStyle=none;rounded=0;strokeColor=#555555;strokeWidth=2;endArrow=block;endFill=1;fontSize=12;fontStyle=1;fontColor=#555555;labelBackgroundColor=#FFFFFF;html=1;fontFamily=Courier New;"
    cells.append(f'<mxCell id="e{j}" value="{esc(ev)}" style="{st}" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p(a[0])}" y="{p(a[1])}" as="sourcePoint"/><mxPoint x="{p(b[0])}" y="{p(b[1])}" as="targetPoint"/><Array as="points">{mids}</Array></mxGeometry></mxCell>')
notes=[("silence → the proposed status",140,598,140),
 ("Guards: CUI only from authority or notice_open · authority only from designated · notice_open only from notify. Any outcome + reopen → public.",20,662,760),
 ("Generated from skills/is-this-cui/transitions.json",20,684,760)]
for k,(t,x,y,w) in enumerate(notes):
    cells.append(f'<mxCell id="t{k}" value="{esc(t)}" style="text;html=1;align=left;fontSize=13;fontColor=#555555;whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="{p(x)}" y="{p(y)}" width="{w*S}" height="30" as="geometry"/></mxCell>')
cells.insert(0,f'<mxCell id="title" value="&lt;b&gt;Is this CUI?&lt;/b&gt; The is-this-cui state table" style="text;html=1;align=left;fontSize=24;fontColor=#333333;" vertex="1" parent="1"><mxGeometry x="{OFF}" y="0" width="900" height="40" as="geometry"/></mxCell>')
out=f'<mxfile host="drawio"><diagram name="Is this CUI" id="is-this-cui"><mxGraphModel dx="1400" dy="1250" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="1250" background="#FFFFFF" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>'
open(sys.argv[2],'w').write(out)
