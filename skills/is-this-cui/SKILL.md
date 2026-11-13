---
name: is-this-cui
description: 'Decide whether a document, a data field, or a whole data type is CUI, by walking a fixed state table: public, then whose it is, then re-used content, then how it is designated, then whether a Registry authority reaches it, ending in CUI with its category, FCI, Proprietary, Public, or "potentially CUI, notice sent". Covers a subcontractor that only sees its prime. Use whenever the operator or another skill asks "is this CUI?".'
---

# Is this CUI?

This skill answers one question: is this item CUI, for this company, right now? It is the only skill in this repo that answers it (ADR-0005). Other skills send their items here and record what comes back.

It does not mark a document already found to be CUI (call the Skill tool with `cui-marking-check`), classify an item under the ITAR or EAR (call the Skill tool with `export-classification`), decide who may access export-controlled data (call the Skill tool with `export-control-overlay`), or walk every document a company makes from a customer's CUI (call the Skill tool with `cui-re-use-triage`, which sends each one back here).

## Inputs

- The item: a document, a data field, a spreadsheet column, or a whole data type. An email or package is several items: the message, and each attachment on its own. A physical part, print, or prototype is not information and is never CUI; classify it with `export-classification` and protect it under the export program, and run the files it was made from through this skill.
- Who created it and who holds it now.
- The contract or purchase order it came under, with its clause list, read firsthand.
- Every marking on it: banner, designation indicator, distribution statement, export warning, proprietary legend.
- `CONTEXT.md` and `scope/cui-determinations.md`, for determinations already recorded.

## Method

The method is a state machine, like a firewall rule set: the order is the rule. Start at `public`. At each state, choose one event from its row and move on. Stop at an outcome. Never jump ahead to what the content says before the earlier states are answered; content-first reasoning is the mistake this order exists to stop.

Run it once per item. A drawing, a spreadsheet column, and a whole data type ("our inspection reports") are each one item. Volume does not change an answer: a list of ten thousand uncontrolled part numbers is still uncontrolled, because each item needs its own authority (32 CFR 2002.12(a)). Aggregation is a classification question, settled by the program's security classification guidance, which the contract asks the contractor to watch for and report (DoDI 5200.48 para 5.3.c); it is not a way an uncontrolled item becomes CUI.

**Choose the events; let the script move.** `transitions.json`, next to this file, is the table. Run the events you chose through it, from this skill's folder:

```bash
python3 is_this_cui.py nonpublic gov clue propose_fci
```

It prints each step with its reason and citation, the status to record, and the events the next state accepts. It refuses an event that does not answer the current state, so an item cannot reach CUI without passing `designated` and `authority`. Choosing the event is the judgment, and the rules below are how to choose it. The script keeps the order and writes the path.

### The state table

| State | Question | Event → next |
|---|---|---|
| `public` | Has it been released to the public without restriction? | `public` → **Public**. `nonpublic` → `owner` |
| `owner` | Whose information is it? | `ours` → **Proprietary (own)**. `theirs` → **Proprietary (third-party)**. `reuse` → `items`. `gov` → `designated` |
| `items` | Does it re-use a controlled item? | `clean` → **Proprietary (own)**. `unsure` → `notify`. `reuses` → `designated` |
| `designated` | How is it designated? | `marked` → `authority`. `clue` → `notify`. `unmarked` → **FCI** |
| `authority` | Does a Registry category's authority reach this content? | `yes` → **CUI**. `no` → `notify` |
| `notify` | What status do you propose, and on what evidence? | `propose_cui` → `notice_open`. `propose_fci` → `notice_open`. `propose_own` → `notice_open`. `propose_theirs` → `notice_open` |
| `notice_open` | Has the window passed, or did the source reply? | `silence` → **the proposed status**. `reply_cui` → **CUI**. `reply_fci` → **FCI**. `reply_own` → **Proprietary (own)**. `reply_theirs` → **Proprietary (third-party)** |

Outcomes: **Public**, **Proprietary (own)**, **Proprietary (third-party)**, **FCI**, and **CUI**. An item that stops at `notify` is recorded as **Potentially CUI, notice drafted**, and at `notice_open` as **Potentially CUI, notice sent**, until `silence` or a reply resolves it.

An outcome is not final for ever. When new evidence arrives (a new marking, a contract modification, a reply that corrects a recorded status), send `reopen` and run the item again from `public`. The record keeps both runs.

`scripts/check_is_this_cui.py` (run on every push by `.github/workflows/check.yml`) walks every path through `transitions.json`. It fails on a path with an open end, on a path that breaks a guard (CUI reached from anywhere but `authority` or `notice_open`; `authority` reached from anywhere but `designated`), on a worked trace in `scripts/is_this_cui_traces.json` that ends wrong, and when the table above differs from the JSON. To change the method, edit the JSON, paste `is_this_cui.py --table` here, and add a trace.

### The rules behind each state

#### `public`

Released without restriction means a catalog sheet, a public specification, or a Distribution Statement A document. Public cannot be combined with CUI or either Proprietary label. A public specification cited on a customer's drawing is still public; the drawing around it is not.

#### `owner`

Who the information belongs to comes before what it says.

- **`ours`: the company created it and holds it.** CUI is information the Government creates or possesses, or that an entity creates or possesses for or on behalf of the Government; a non-executive branch entity's own information is outside that definition (32 CFR 2002.4(h)). So the company's own designs, methods, and staff records are not CUI to it, even where ITAR or EAR still reaches them. Run `export-control-overlay` on them anyway.
- **Copy A and Copy B.** The same information can have two statuses. The company's retained copy (Copy A) stays its own. The copy delivered to the Government (Copy B) can be CUI in the Government's hands, for example as Proprietary Business Information (PROPIN). Ask "to whom, and which copy" before answering.
- **Our own data that comes back marked.** The company's own information is not CUI to it even when the Government returns it marked as CUI, because the Government safeguards it as CUI only while it holds it (32 CFR 2002.4(h)). Work from the company's original unmarked copy, not the returned one. Never tell staff to ignore or strip a CUI marking, which teaches them to ignore real ones.
- **A deliverable we owe the Government.** Read the clause in the contract, never a verbal assurance. Data-rights clauses (DFARS 252.227-7013, 252.227-7014) license the Government to use delivered data and leave ownership with the company: its copy goes `ours`. Special-works and become-property clauses (DFARS 252.227-7020, 252.227-7023, FAR 52.227-17) transfer ownership of a deliverable first created and required under the contract: it goes `gov`. Work merely incidental to performing a contract, which the company would track anyway, is not created for the Government.
- **Software and "all code is CUI" clauses.** Ask two questions apart: is the code technical data under the test below, and was it created for the Government? If either answer is no, it is not CTI. A blanket clause is true only for the Government's copy. The remedy is to assert data rights on software deliverables and deliver them under restrictive legends (DFARS 252.227-7013, 252.227-7014), so everyone agrees the delivered copy may be CUI to the Government and the company's own copy is not. A contract term to safeguard the code is a contract duty, recorded as an open item, not a CUI status.
- **`theirs`: a commercial third party's, not for the Government.** A prime's own privately funded design, sent to a sub, is the prime's proprietary data. It may be export-controlled; it is not CUI because the Government never owned or held it.
- **`reuse`: the company made it while using CUI it received.** Go to `items`.
- **`gov`: provided by or generated for the Government under a contract, directly or through a prime.** That includes a deliverable that becomes the Government's, and the paperwork the company writes to win or perform a government contract: its quote, its purchase orders to suppliers, its schedules. That paperwork usually ends at FCI, and the pricing in it stays the company's own as a data category. A sub that works through a prime lands here for anything that flowed down from the Government, even though the Government never sent it anything. Go to `designated`.
- **Prime's data, `gov` or `theirs`?** Under a purchase order that carries DFARS 252.204-7012 or names a DoD prime contract, technical data the prime sends for the work goes `gov`, and `designated` sorts out its markings. It goes `theirs` only when nothing ties it to a government contract, or the prime says in writing that it is its own privately funded design.

#### `items`

The regulation's word is **re-use**: "incorporating, restating, or paraphrasing information from its originally designated form into a newly created document" (32 CFR 2002.4(pp)). It is a form of handling (2002.4(aa)). The test is content, never lineage: a new document is CUI because of the controlled information it carries, not because of where it came from, and one built only from a source's non-CUI portions is not CUI on that account (81 FR 63324, preamble at 63334).

So break the document into data items (a part number, a dimension, a tolerance, a restated requirement, a paraphrased paragraph) and check each one. The answer can differ item by item. Having had the CUI drawing open while you worked is not a test. For technical data, the check is the technical data test below.

- **`clean`**: it re-uses no controlled item. Every item it carries fails the technical data test below: a part number, a quantity, or a material call-out from a public specification. The document is the company's own. If it carries contract information, such as a customer part number or a purchase order quantity, record FCI among its data categories.
- **`unsure`**: the only match is disputed ground, most often a toolpath or program whose coordinates equal the drawing's nominal dimensions, with no tolerance, note, or requirement carried over. Practitioners split on it. Choose `clean` when the program is the company's own method of cutting the part, or `unsure` to go to `notify` and propose a status with that reasoning. Nominal geometry alone is never `reuses`. The proposal follows the technical data test: propose CTI only when the part itself is caught (below) and the program carries what makes it so. Export status and CUI status are separate answers: a program `export-classification` finds to be ITAR technical data is recorded Export-controlled (ITAR) whatever its CUI status, and the company's own program that carries no controlled item is Proprietary (own) and Export-controlled, not CUI.
- **`reuses`**: it carries at least one controlled item over: a tolerance, a note, a requirement, a restated paragraph, or the drawing's image. Take those items to `designated` and judge them on the source's designation: a dimension copied from a drawing marked CTI is still CTI, its designating agency is unchanged, and the document carrying it is CUI.
- **A marked source can hold uncontrolled items.** The marking covers the source; each item carried over still has to be one the category's authority reaches (81 FR 63334). Run the technical data test below on the item itself. A customer's performance specification (what the part must do, verified after production) is usually not detailed enough to be CTI even inside a CTI-marked PDF, so a design the company builds to meet it re-uses no controlled item and stays the company's own, delivered or not. A dimension copied from an unmarked drawing is no more controlled in the copy than in the source. What the company added (its method, its toolpaths, its routing) stays its own.

#### The technical data test

CTI and Export Controlled are the categories most technical data falls into, and both control it through the export rules. The CTI category's authorities are 10 U.S.C. 130, 15 CFR 772.1, the CCL, and 22 CFR 120 (`reference/cui-registry/Defense--Controlled-Technical-Information.md`). 10 U.S.C. 130 reaches only technical data with military or space application that cannot be exported without a license, and not data the export rules release under a general, unrestricted license or exemption (10 U.S.C. 130(a), (c)). So before a data item can be CTI or Export Controlled, it has to be technical data at all. Read the definitions in the current eCFR, linked under Sources.

- **ITAR technical data** is information "required for the design, development, production, manufacture, assembly, operation, repair, testing, maintenance, or modification of defense articles" (22 CFR 120.33(a)(1)). It excludes general scientific and engineering principles, information in the public domain (22 CFR 120.34), and "basic marketing information on function or purpose or general system descriptions" (22 CFR 120.33(b)).
- **EAR technology** is information necessary for the development, production, or use of an item, and only the "required" part is controlled: the portion "peculiarly responsible for achieving or exceeding the controlled performance levels, characteristics or functions" (15 CFR 772.1). Information that is not technology, or is published, or comes from fundamental research, or is a non-proprietary system description, is not subject to the EAR at all (15 CFR 734.3(b)(3) and its note).

The question for each data item: **would this item help someone make, use, or repair the item at its controlled performance?** "Controlled" means a performance level, characteristic, or function that a USML paragraph or an ECCN names. A limit is not controlled because the customer wrote it into a drawing or work instruction; the question is whether the export rules name that parameter. If nobody can name the paragraph or ECCN, the item has not been shown to be required, so get the classification through `export-classification` before calling it CTI.

- **Nomenclature is not technical data.** A part number, a description that names the part, a filename, a customer or program name, a quantity, a price, a date, or a schedule gives none of the information needed to make anything. The one CUI category that can reach names and part numbers is Operations Security, and only when they are on the program's Critical Information List.
- **What, not how.** A photograph or a general description shows what an item is, not how to make it. A performance requirement that is verified after production and is not carried in the design is usually not "required"; the design geometry with its tolerances is.
- **Public domain.** A published specification, a fuel grade, or a patent's functional description is excluded, and the exclusion is the easiest one to prove, because the evidence is public.
- **Test data** is technical data only when it tests what is peculiarly responsible for a controlled performance level. Checking connector pins for defects is not; testing a specially designed material against a pressure the USML entry names is. Tests to a published industry standard, with results in normal commercial ranges, usually are not.
- **"Operation"** in the ITAR definition means operating a system or end item (a startup sequence, a procedure), not how an inert part behaves at a temperature over time.
- **Joining does not change it.** Saving test data with the contract number, part number, or program name does not make it CTI, and stripping them out does not make it not CTI. Content decides, so separating or obfuscating identifiers is not a fix.
- **Is the part itself caught?** Technical data takes its status from the article it describes. A USML paragraph or ECCN controls items at a level: an end-item, a component, or a part (22 CFR 120.40). A part is "any single unassembled element" of a component (120.40(e)); an entry that names only end-items, components, or systems does not catch it, so data about that part cannot be ITAR technical data, and the EAR is checked next. If no USML or CCL entry catches the part, its drawing, model, and program cannot be CTI or Export Controlled. That holds however much of the drawing a program or model carries, and it makes a CTI marking on the drawing itself one no authority reaches, so `authority` answers `no` and the item goes to a notice. Get the paragraph or ECCN, and whether it says "specially designed" (a defined term, 22 CFR 120.41), through `export-classification` before settling a program or model. The phrase "specially designed for military use" in a part description is a claim, not a classification.
- **A practical check.** Practitioner consensus: if trade compliance would clear an item for a trade show or marketing, it is not CTI.

This test screens whether an item is technical data. Which regime controls it, its entry, and whether the part is caught are decided by the classification memo: call the Skill tool with `export-classification`. Who may access it and how it is handled stay with `export-control-overlay`.

The holder checks a new document when it creates it (DoDI 5200.48 para 3.6.a). Marking it CUI because of its source, with no controlled item in it, is misuse (32 CFR 2002.4(ee)), and it pulls every asset that stores it into scope.

#### `designated`

Only a contract or a marking that names a CUI category designates CUI (32 CFR 2002.20). Everything else is a clue.

- **`marked`**: a CUI banner or designation indicator naming the category, or a Distribution Statement B to E whose defense category reads Controlled Technical Information. DoDI 5230.24 requires a statement B to E to name a category (para 4.1.c(2)) and says "CTI is a category of CUI" (para 4.3.a), so that statement is the controlling DoD office saying CTI even when the banner is missing. Go to `authority`.
- **`clue`**: something says CUI may be present but does not name a category.
  - A distribution statement with any other defense category. "The application of a distribution statement does not automatically mean the document is CUI" (DoD CUI Program FAQ, Use of Distribution Statements). Look the category up in `reference/dodi-5230-24-defense-categories.md`, which gives its Registry category, its authority, and the test for whether that authority reaches the content.
  - Check who the statement allows and who it names. Distribution E allows DoD Components only, so one sent to a subcontractor is itself a defect, and a referral to a company is not a controlling DoD office. Name each defect in the notice.
  - An export warning with no statement and no banner.
  - A marking that is incomplete or ambiguous, or an unmarked document formatted like a controlled one.
  Go to `notify`.
- **Clauses and blanket lines are not clues about the page that carries them.** DFARS 252.204-7012 or 252.204-7021 in the contract, a CMMC Level 2 requirement in a purchase order, or a buyer's "treat everything as CUI" say CUI may flow under the contract. They designate nothing and make no document CUI, the purchase order and its clause page included. Answer `unmarked` for the paperwork, and list the clue in the notice index for the documents that come under it.
- **`unmarked`**: no marking and no clue about this item, from a source that marks correctly, or the company's own contract paperwork. Not CTI and not Export Controlled, because both need a Distribution Statement B to F. Lack of a marking does not exempt information that qualifies (32 CFR 2002.20(a)(7)), so turn the assumption into evidence: check that nothing in the package or the contract designates this item, and get the source's "not CUI" in writing when it matters. The outcome is **FCI**.
- **Re-used items** are judged here on the source's marking, not the new document's. A missing or wrong marking on the new document is a finding for `cui-marking-check`, not a reason to change the answer.

#### `authority`

CUI categories are the exclusive designations (32 CFR 2002.12(a)). An item is CUI only when a law, regulation, or Government-wide policy named in a Registry category reaches its content.

- For CTI and Export Controlled, the authority reaches only an item that passes the technical data test above.
- Read the authorities cited at the bottom of the Registry category page (https://www.dodcui.mil/CUI-Categories-and-Abbreviations/), not the summary at the top. A keyword match ("vulnerability", "export") is not a match. CTI covers technical information with military or space application under access and dissemination controls; it does not cover a schedule, a quote, or a part list because they sit in the same file.
- DFARS 252.204-7012 covered defense information is CTI or any other Registry category, provided by or for DoD or developed in support of the contract. The second prong is a link to the contract, not a net: the DoD FAQ says it "does NOT mean that all information used by the contractor to support contract performance ... is considered to be covered defense information" (DoD Cybersecurity FAQs, A32).
- The clause is DoD's alone. Space work under a DoD contract can be CTI, since 10 U.S.C. 130 covers "military or space application". Data under a NASA or civilian agency contract is not CTI and brings no CMMC requirement; it can still be that agency's CUI, protected under NIST SP 800-171 through its contract terms (32 CFR 2002.14(h)(2)). Which contract the work runs under decides it, not which agency the data came from.
- **`yes`**: the outcome is **CUI**, with its Registry category.
- **`no`**: a marking that no authority reaches (a schedule marked CTI, for example) is a designation you believe is improper. Go to `notify` and propose the correction.

#### `notify`

`notify` is for items still in doubt. An item that already reached an outcome is recorded, safeguarded by that outcome, and listed in the index with its status; it is not held as CUI while a notice is open. The company decides on the evidence, writes the reasoning down, and tells the source. It does not send an open question. A holder who believes a designation is improper, or that it has received unmarked CUI, "should notify the disseminating agency", and keeps safeguarding the item while it does (32 CFR 2002.50(a), (d)). Practitioner consensus is that an open question to a prime or program office gets no answer, or "treat it all as CUI" with no category or authority behind it.

The notice is an index, not a letter about one file. List everything received and generated under the contract, and give every item a definite proposed status, with a category and dissemination control where it is CUI and the reason where it is not (How To Know If You Have CUI, from 40:40). Where a clean file with the markings removed, a performance specification, or only the sheets the work needs would settle the doubt, ask for that too: what the company never receives never has to be decided.

Until the notice has gone, the item stays at `notify`, recorded as **Potentially CUI, notice drafted** and safeguarded as CUI. Send the event once it has gone: **`propose_cui`** (with its category), or **`propose_fci`**, **`propose_own`**, or **`propose_theirs`** (with the reason it is not CUI and whose it is). Each moves the item to `notice_open`, recorded as **Potentially CUI, notice sent**. Write the reply-by date into the notice, so silence is judged against a date the source saw. Then:

- **`silence`** past the reply-by date accepts the notice. That is this repo's recording rule (ADR-0005), not a rule in 32 CFR 2002.50: say in the notice that silence will be recorded as acceptance, and never tell anyone the regulation makes silence binding. The proposed status becomes the record.
- **`reply_cui`**, a reply that gives a category and authority, records CUI. **`reply_fci`**, **`reply_own`**, or **`reply_theirs`**, a reply that says it is not CUI, records the status it gives.

Write each notice index into `scope/cui-determinations.md` under `## Notice to <source>`, and keep the reasoning and the reply or the silence beside it. That is the record of a good-faith determination.

**A subcontractor that only sees its prime.** It usually cannot read the prime contract, its funding, or its data-rights clauses, so `owner` and `designated` have gaps it cannot fill alone. The regulation expects that: DFARS 252.204-7012(m)(1) makes the prime "determine if the information required for subcontractor performance retains its identity as covered defense information". Work from what the prime actually sent and wrote: the markings on each document, the clauses in the purchase order (7012, 7021, 252.225-7048), and what the prime says in writing. Nothing is CUI by default, on either side: not because the purchase order asks for Level 2, and not "not CUI" because nobody marked it. Send the prime the index. Where the evidence still does not settle it, `enclave-or-enterprise-decision` gives the design that removes the need to decide at the inbox.

#### The outcomes

- **CUI**: name the Registry category, and run `cui-marking-check` for how it is marked.
- **FCI**: the named "not CUI" for information not intended for public release, provided by or generated for the Government under a contract (FAR 52.204-21). Quotes, purchase orders, schedules, and delivery paperwork. The clause flows down to subcontracts except those for commercially available off-the-shelf items (FAR 52.204-21(c)), so buying a COTS item, such as fuel to a published grade, carries no FCI flowdown. It is a different category with its own floor, the fifteen basic safeguarding requirements, not a lesser kind of CUI. Recording it stops the item being re-argued every quarter.
- **Proprietary (own)** and **Proprietary (third-party)**: not CUI. A proprietary legend says who owns the data; it does not decide CUI status, and it survives a CUI decontrol because the NDA or license behind it is separate.
- **Public**.
- **Potentially CUI, notice drafted** and **Potentially CUI, notice sent**: the statuses of `notify` and `notice_open`, safeguarded as CUI until `silence`, `reply_cui`, or `reply_fci`.

## Who decides

This is a business decision. Sales, contracts, program management, engineering, and trade compliance own it as a deal moves from quote to delivery, and IT acts on it last. An assessor does not decide CUI status either; it is outside a C3PAO's role.

## Output

Append one entry per item to `scope/cui-determinations.md`, creating it if it does not exist:

```markdown
## <item>

- Date: <date>
- Contract or agreement: <id, or "none">
- Events: <the events in order, as passed to is_this_cui.py>
- Path: <is_this_cui.py's output, one step per line>
- Copy: <Copy A, retained / Copy B, delivered / both / not applicable>
- Re-used items: <each controlled item carried over and its source, or "none">
- Authority: <Registry category and citation, or "none found">
- Determination: <CUI (<category>) / FCI / Proprietary (own) / Proprietary (third-party, owner) / Public / Potentially CUI, notice drafted / Potentially CUI, notice sent>
- Data categories: <every one that applies, from CONTEXT.md>
- Notice: <date sent or "drafted", to whom, reply-by date, reply or silence, or "none">
- Open items: <anything unresolved>
```

Record every data category that applies, not only the determination: CUI, FCI, Export-controlled (ITAR or EAR), Proprietary (own), Proprietary (third-party), PII, Security Protection Data (32 CFR 170.4), and Public. Use `CONTEXT.md`'s definitions where it has them. Only CUI and FCI set the assessment scope; the others record where the company's own IP, its customers' IP, and its people's data sit.

A determination that sets a precedent the engagement will rely on again goes into `CONTEXT.md` through the `domain-modeling` skill. An open determination goes on the open items list, never into a conformity statement as though it were settled.

## Where practitioners disagree

- **Ask the source, or notify it.** One position asks the customer for the category, the authority, and the distribution statement, and treats no answer as no CUI. This skill notifies with a proposed status (ADR-0005), because an open question usually gets no answer or a blanket one, and a notice puts the reasoning on record either way. The outcome depends on the customer more than the assessor.
- **Who reads the Registry.** One position holds that a contractor cannot compare information against the Registry itself and must take the category from the source. This skill reads the authority in `authority`, and sends what it finds to the source in `notify`, so the source still has the last word.
- **Paper only, no clause.** Whether a document received with a CUI marking but under no contract clause about CUI is handled as marked until the customer confirms, or is not CUI until the customer says so in writing. The outcome depends on the assessor.
- **Our own documents that carry the customer's content.** One position tests each data item a company document carries over: a traveler or model with snippets of the customer's drawing holds customer content the company does not own, and calling it proprietary is no way out where the ITAR reaches that content. The other position puts ownership first: what the company creates is its own and not CUI to it, and there is no "derivative" CUI unless the contract says the company is creating CUI. This skill follows the first, because 32 CFR 2002.4(pp) and the final rule's preamble test content. Both agree that a model built only to meet the customer's performance specifications carries nothing controlled and is the company's own.
- **Pre-contract quotes.** Whether sensitive end-use context shared to support a quote, before any contract exists, is already inside the determination. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run it with the client's contracts and program staff in the room; `owner` needs someone who can read the actual clauses. **OSC seat**: if nobody has read the data-rights and special-works clauses yet, start there; they settle most of the easy items at `owner`.

## Sources

- 32 CFR 2002.4: https://www.ecfr.gov/current/title-32/section-2002.4 ((h) the definition and its exclusion, `owner`; (aa) and (pp) re-use, `items`; (ee) misuse).
- 81 FR 63324, the CUI final rule, preamble at 63334: https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information (content, not lineage, `items`; quoted in `reference/authorities.md`).
- DoDI 5200.48, para 3.6.a: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/520048p.PDF (mirrored at `reference/dod-issuances/dodi-5200-48.md`; the holder checks a new document at creation, `items`).
- 32 CFR 2002.20 (marking): https://www.ecfr.gov/current/title-32/section-2002.20 (`designated`).
- DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf (mirrored at `reference/dod-issuances/dodi-5230-24.md`; `designated`).
- DoD CUI Program FAQ, Use of Distribution Statements: https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/ (mirrored at `reference/cui-registry/Frequently-Asked-Questions--Use-of-Distribution-Statements.md`; `designated`).
- `reference/dodi-5230-24-defense-categories.md`: the fourteen defense categories, the authority behind each, and the test for each (`designated`).
- 32 CFR 2002.12: https://www.ecfr.gov/current/title-32/section-2002.12 (categories are the exclusive designations, `authority`).
- CUI Registry, National Archives, mirrored at dodcui.mil: https://www.dodcui.mil/CUI-Categories-and-Abbreviations/ (`authority`).
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012 (covered defense information, `authority`; (m)(1) the prime determines, `notify`).
- DoD Cybersecurity FAQs on DFARS Subpart 204.73, A32: https://dodprocurementtoolbox.com/uploads/Cybersecurity_FAQ_update_12_19_22_ba047be683.pdf (mirrored at `reference/dod-issuances/dod-cybersecurity-faq-covered-defense-information.md`; `authority`).
- 32 CFR 2002.14 (safeguarding; (h)(2) NIST SP 800-171 for non-Federal systems): https://www.ecfr.gov/current/title-32/section-2002.14 (civilian agency CUI, `authority`).
- 32 CFR 2002.50: https://www.ecfr.gov/current/title-32/section-2002.50 (notify and keep safeguarding, `notify`).
- DFARS 252.227-7013, Rights in Technical Data: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013 (the data-rights clause family, `owner`).
- FAR 52.204-21: https://www.ecfr.gov/current/title-48/section-52.204-21 (FCI).
- 22 CFR 120.31, 120.33, 120.34, 120.40; 15 CFR 772.1, 734.3; 10 U.S.C. 130, read live, not mirrored (the technical data test): https://www.ecfr.gov/current/title-22/section-120.31, https://www.ecfr.gov/current/title-22/section-120.40, https://www.ecfr.gov/current/title-22/section-120.33, https://www.ecfr.gov/current/title-22/section-120.34, https://www.ecfr.gov/current/title-15/section-772.1, https://www.ecfr.gov/current/title-15/section-734.3, https://www.law.cornell.edu/uscode/text/10/130.
- DoDI 5200.48, para 5.3.c: aggregation and compilation (volume does not change an answer).
- 32 CFR 170.4 (Security Protection Data definition): https://www.ecfr.gov/current/title-32/section-170.4 (data categories).
- How To Know If You Have CUI, a talk by Ryan Bonner at CS2, hosted by Summit 7: https://www.youtube.com/watch?v=IEy-TkmKMt8 (read the contract first, and the index sent as a notice, `notify`).
- Practitioner consensus, unattributed, backs the state order, Copy A and Copy B, reading the Registry's authorities rather than its summary, the clue list in `designated`, the trade-show check in the technical data test, the open-question failure in `notify`, and the rule that IT and assessors do not decide. None of it sets a CUI status on its own.
