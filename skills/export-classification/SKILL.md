---
name: export-classification
description: Classify an item and its technical data under the ITAR and EAR the way trade compliance does: whether it is technical data at all, the USML order of review, whether "specially designed" catches or releases it at its compositional level, unfinished products, not subject to the EAR versus EAR99, the CCL order of review, and when to ask the design authority or file a jurisdiction request. Use when a drawing, model, NC program, test report, or part needs a jurisdiction, or when a CTI or Export Controlled answer depends on one.
vault_sources:
  - "Export Controls and CUI"
  - "Controlled Technical Information"
  - "Practitioner insights A"
  - "Practitioner insights B"
public_sources:
  - "22 CFR 121.1 (the U.S. Munitions List): https://www.ecfr.gov/current/title-22/section-121.1"
  - "22 CFR 120.11 (ITAR order of review): https://www.ecfr.gov/current/title-22/section-120.11"
  - "22 CFR 120.12 (commodity jurisdiction requests): https://www.ecfr.gov/current/title-22/section-120.12"
  - "22 CFR 120.31 (defense article; unfinished products at (a)(2)): https://www.ecfr.gov/current/title-22/section-120.31"
  - "22 CFR 120.33 (ITAR technical data): https://www.ecfr.gov/current/title-22/section-120.33"
  - "22 CFR 120.34 (public domain): https://www.ecfr.gov/current/title-22/section-120.34"
  - "22 CFR 120.40 (compositional terms): https://www.ecfr.gov/current/title-22/section-120.40"
  - "22 CFR 120.41 (specially designed): https://www.ecfr.gov/current/title-22/section-120.41"
  - "22 CFR 120.42 (enumerated and catch-all control): https://www.ecfr.gov/current/title-22/section-120.42"
  - "15 CFR 734.3 (subject and not subject to the EAR, EAR99): https://www.ecfr.gov/current/title-15/section-734.3"
  - "15 CFR 772.1 (technology, required, specially designed): https://www.ecfr.gov/current/title-15/section-772.1"
  - "15 CFR Part 774, Supplement No. 4 (CCL order of review): https://www.ecfr.gov/current/title-15/part-774/appendix-Supplement%20No.%204%20to%20Part%20774"
  - "10 U.S.C. 130 (technical data with military or space application): https://www.law.cornell.edu/uscode/text/10/130"
---

# Export classification

This skill answers one question per item: **is it controlled by the ITAR or the EAR, at which entry, and is its data technical data?** It writes the memo trade compliance writes. It does not decide CUI status (call the Skill tool with `is-this-cui`, which rests its CTI and Export Controlled answers on this one), and it does not cover who may access the data, travel, encryption, or providers (call the Skill tool with `export-control-overlay`).

The answer matters for CUI because CTI and Export Controlled are bound by these rules: 10 U.S.C. 130 reaches only technical data that cannot be exported without a license, and not data released under a general, unrestricted license or exemption. Information no ITAR or EAR entry controls cannot be CTI or Export Controlled.

## Inputs

- The item: a part, component, assembly, end-item, material, software, or process, and what it goes into, as far as anyone knows.
- The data about it: drawings, models, specifications, NC programs, test reports, work instructions. Each is classified by the article it describes.
- Who designed it, when, and with what knowledge of its use, with the documents made at the time: concept designs, marketing plans, patent filings, contracts.
- Every export warning, distribution statement, and DFARS 252.225-7048 clause on the item or its order.
- Any jurisdiction or classification already given in writing: a commodity jurisdiction determination, a classification from BIS, or the design authority's answer.

## Method

Work the steps in order and stop where the item is placed. The regulations set the order; skipping ahead to "it's for a defense program, so it's ITAR" is the mistake this order exists to stop. Read every rule cited here in the current eCFR at the links under Sources, not from memory or a saved copy, because the rules change; the memo records the date they were read.

1. **Split what you are classifying.** A commodity and its data are classified separately, and data takes its status from the article it describes. Break a mixed document into data items, as `is-this-cui` does, because each can land differently.
   - **Hardware is never CUI.** CUI is information. A printed, machined, or molded piece is a commodity: it is a defense article only once it has reached the stage where it is recognizable as the finished article (22 CFR 120.31(a)(2)), or when it is a model or mockup that reveals technical data about a USML item (120.31(a)(1)). A controlled piece is protected under the export program (who may see, handle, or photograph it), not as CUI under the 800-171 media or physical controls; those protect the files it was made from.

2. **Ask whether each data item is technical data or technology at all.** ITAR technical data is information "required for" the design, production, operation, repair, testing, or modification of defense articles (22 CFR 120.33(a)(1)), and software directly related to them (120.33(a)(4)). It excludes general principles taught in schools, public domain information (120.34), and "basic marketing information on function or purpose or general system descriptions" (120.33(b)). Under the EAR only the "required" portion of technology is controlled: the part "peculiarly responsible for achieving or exceeding the controlled performance levels, characteristics or functions" (15 CFR 772.1). Information that is not technology, is published, comes from fundamental research, or is a non-proprietary system description is not subject to the EAR at all (15 CFR 734.3(b)(3)).
   - Part numbers, names, filenames, quantities, prices, and schedules are nomenclature, not technical data.
   - A performance specification says what an item must do, not how to make it, and is usually not "required".
   - Test data is technical data only when it tests what is peculiarly responsible for a controlled level; routine screens are not.
   - "Operation" means operating a system or end-item, not how an inert part behaves at a temperature.
   - Software is classified by its parts. Code that does not perform the controlled function and carries none of the controlled data can be set apart from the controlled portion; touching ITAR code does not make the rest ITAR.

   A data item that fails here is **not technical data**. Record that, with the exclusion, and stop for that item: it is not ITAR or EAR controlled as technical data, so it cannot be CTI or Export Controlled.

3. **Decide who classifies.** The commodity the item goes into usually decides the jurisdiction: parts of an EAR assembly often drop to EAR99, while parts of a USML commodity rarely leave it. The design authority, the company that designed the item and knows its end use, classifies it. A build-to-print supplier usually cannot see the end-item, and "specially designed" turns on it, so it asks the design authority in writing for the USML category or ECCN of the part and its technical data, using the request in `export-control-overlay`, and files the answer. A customer's export warning or a 7048 clause names both regimes and settles neither. While the answer is pending, handle as ITAR only the data that passed step 2; nomenclature and routine records stay as they are. Pending is pending: do not write "ITAR either way" before the answer arrives.

4. **The US Munitions List, under 22 CFR 120.11.** Find the USML category from the item's general characteristics, then the entry. Read the category in the current text at https://www.ecfr.gov/current/title-22/section-121.1, never from memory or a saved copy: DDTC revises the list often, and the memo records the date it was read. An enumerated entry wins over a catch-all (120.11(b)(2); 120.42).
   - **Check the compositional level.** An entry controls a named level: an end-item, a component, an accessory or attachment, or a part (22 CFR 120.40). A part is "any single unassembled element" of a component (120.40(e)). An entry, or a catch-all, that names components but not parts does not catch a part; the part goes to the EAR.
   - A USML item stays on the USML after it is built into something that is not (120.11(c)).

5. **Test "specially designed" when a catch-all uses it (22 CFR 120.41).** It is caught if, as a result of development, it has properties peculiarly responsible for the controlled performance in the USML paragraph (120.41(a)(1)), or it is a part, component, accessory, attachment, or software for use in or with a defense article (120.41(a)(2)). It is then released if any paragraph (b) applies:
   - (b)(1) a commodity jurisdiction determination made it subject to the EAR;
   - (b)(2) it is a fastener, washer, spacer, insulator, grommet, bushing, spring, wire, or solder, regardless of form or fit;
   - (b)(3) it has the same function, performance, and form and fit as a commodity that is or was in production and is not enumerated on the USML; when that commercial commodity entered production is evidence worth keeping;
   - (b)(4) it was developed knowing it would be used with both USML and non-USML commodities;
   - (b)(5) it was developed as general purpose, with no knowledge of a particular commodity or type.

   A (b)(4) or (b)(5) release needs documents made at the time of development that, in their totality, establish it (Note 2 to paragraph (b)). "Knowledge" includes awareness of a high probability and willful avoidance (Note 3). "Specially designed for military use" in a description is a claim, not this analysis.

6. **Unfinished products.** Forgings, castings, and machined bodies are defense articles only once they have "reached a stage in manufacturing where they are clearly identifiable by mechanical properties, material composition, geometry, or function as defense articles" (22 CFR 120.31(a)(2)). Practitioner consensus: a program that only takes a part to a stage that is not yet identifiable probably is not regulated, while one that produces the recognizable part takes the part's answer. Record which operation produces the identifiable form.

7. **The EAR, if the item is not on the USML.** An item subject to the ITAR is not subject to the EAR (15 CFR 734.3(b)(1)(i)). Otherwise:
   - **Subject to the EAR at all?** Record "not subject to the EAR" with its 734.3(b) basis when it applies. It is a different answer from EAR99.
   - **The CCL, in the order Supplement No. 4 to Part 774 sets:** category 0 to 9 by general characteristics, product group A to E, then the "600 series" and 9x515 entries first, their "specially designed" paragraphs next (15 CFR 772.1 sets the EAR's own catch and release test), then the rest of the group. Read each entry's parameters: CCL entries turn on thresholds such as size, frequency, or temperature, and an item below them is not caught.
   - **EAR99** when nothing matches. It still needs end-user, end-use, and destination screening before export.

8. **Give the technical data its answer.** Data required for an article on the USML is ITAR technical data. Data for an article with an ECCN is controlled technology only where an E-group entry controls it and only for its "required" portion. Data for an EAR99 item, or for an item not subject to the EAR, is not controlled technology. Data for a part the USML does not catch cannot be ITAR technical data however much of a drawing it carries.
   - **Only the delta is controlled.** When a commercial or EAR item was adapted to reach a USML performance level, only the data that achieved that difference is ITAR technical data; the rest keeps its earlier answer. An item is under one regime, never both, and an earlier version does not change jurisdiction because a later one did. A commercial process that meets a defense specification without being redesigned for it is not ITAR technical data because of the part it is applied to, unless the process is controlled in its own right (enumerated, or always controlled by its nature). Look for the delta where the defense article's needs exceed commercial norms, and keep the evidence that the process needs no license before relying on it.
   - Classifying the item is not the end. Say how much of its data is actually subject to the ITAR or EAR; most memos stop one step short.

9. **A company may do its own order of review** and classify items and their technical data without asking the agencies. **When it stays unclear and the stakes justify it,** the design authority can ask DDTC for a commodity jurisdiction determination (22 CFR 120.12) or BIS for a classification. That is realistically worth it to an OEM, not to a deep-tier supplier, which asks its customer.

10. **Hand the result to `is-this-cui`.** Not technical data, not subject to the EAR, or EAR99: the item cannot be CTI or Export Controlled. That is an export answer only: another CUI category, set by the contract or a marking, can still reach the same data, so `is-this-cui` still runs. ITAR or an ECCN: it can be, and `is-this-cui` decides whether a DoD nexus and the company's ownership make it so.

## Who decides

The design authority or the company's export counsel or trade compliance lead, with engineering. IT, a program manager, or a CMMC consultant gathers the facts and writes the memo; it does not sign the classification. A memo signed by the wrong person is itself a finding.

## Output

Append one entry per item to `scope/export-classifications.md`, creating it if it does not exist:

```markdown
## <item>

- Date: <date>. Classified by: <design authority in writing (attach) / export counsel / trade compliance / pending, request sent to ... on ...>
- What it is: <commodity type and compositional level (end-item, component, part, 22 CFR 120.40)>; goes into: <end-item, or "not known to this company">
- Data items and technical data test: <each data item: technical data / not technical data, with the 120.33(b) or 734.3(b)(3) basis or the "required" reason>
- USML: <category and entry, read on <date> from the current eCFR / not caught, and why (level not named, released under 120.41(b)(n), not identifiable under 120.31(a)(2)) / undetermined>
- Specially designed: <caught under (a)(1) / (a)(2); released under (b)(n), with the contemporaneous documents / not tested, enumerated entry>
- EAR: <not subject (734.3(b) basis) / ECCN ..., 600 series and 9x515 checked first / EAR99, screening done yes or no / not reached>
- Result: <ITAR, Category ... / EAR, ECCN ... / EAR99 / not subject to the EAR / not technical data / pending, handled as ITAR for the data that passed the test>
- For CUI: <cannot be CTI or Export Controlled / can be; sent to is-this-cui>
- Open items: <the request, the documents still missing>
```

## Where practitioners disagree

- **Nominal geometry in a program.** One position: toolpaths are the shop's own method and, without tolerances, tools, and setups, do not let anyone make the part. The other: a program that produces the recognizable part is software directly related to a defense article. 22 CFR 120.31(a)(2) and the compositional level usually settle more of it than either position admits.
- **How far "handle as ITAR" reaches while a jurisdiction answer is pending.** This skill limits it to data that passes the technical data test. Some programs apply it to everything on the job, which is simpler to run and costs more.

## Seat notes

**Consultant seat**: write the memo and the request; never sign the classification. **OSC seat**: if you are the design authority, keep your development records, because a (b)(4) or (b)(5) release is only as good as the documents made at the time.

## Sources

- 22 CFR 121.1, the U.S. Munitions List, read live: https://www.ecfr.gov/current/title-22/section-121.1. Not mirrored, because it changes often.
- ITAR, read live: 22 CFR 120.11 https://www.ecfr.gov/current/title-22/section-120.11, 120.12 https://www.ecfr.gov/current/title-22/section-120.12, 120.31 https://www.ecfr.gov/current/title-22/section-120.31, 120.33 https://www.ecfr.gov/current/title-22/section-120.33, 120.34 https://www.ecfr.gov/current/title-22/section-120.34, 120.40 https://www.ecfr.gov/current/title-22/section-120.40, 120.41 https://www.ecfr.gov/current/title-22/section-120.41, 120.42 https://www.ecfr.gov/current/title-22/section-120.42.
- EAR, read live: 15 CFR 734.3 https://www.ecfr.gov/current/title-15/section-734.3, 772.1 ("technology", "required", "specially designed") https://www.ecfr.gov/current/title-15/section-772.1, Supplement No. 4 to Part 774 https://www.ecfr.gov/current/title-15/part-774/appendix-Supplement%20No.%204%20to%20Part%20774.
- 10 U.S.C. 130: https://www.law.cornell.edu/uscode/text/10/130.
- Practitioner consensus, unattributed, backs the nomenclature and performance-specification points, separable software, the unfinished-products reading of programs, and the limit on "handle as ITAR". None of it sets a classification on its own.
