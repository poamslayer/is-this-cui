---
name: export-classification
description: Classify an item and its data under the ITAR or the EAR, and say whether the data is technical data at all. Use when a drawing, model, NC program, test report, or part needs a jurisdiction, or when a CTI or Export Controlled answer depends on one.
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

For each item, answer: which regime controls it, at which entry, and is its data technical data at all? CTI and Export Controlled exist only where an ITAR or EAR entry controls the data (10 U.S.C. 130), so `is-this-cui` waits on this answer. Who may access the data belongs to `export-control-overlay`.

**Why:** The usual mistake reasons backward from the customer: "it's for a defense program, so it's ITAR." The rules reason forward from the item, and most of a job's data drops out before any list is read.

**Pattern:**
- **Classify the data, not the job.** Data takes its status from the article it describes, and each data item in a document can land differently. Hardware is a commodity and never CUI; protect it under the export program, and classify the files it was made from.
- **Ask "is it technical data?" before "which list?"** Only what is *required* to design, make, operate, repair, or test the article at its controlled level counts (22 CFR 120.33; 15 CFR 772.1). Part numbers, prices, schedules, performance specs, routine test screens, general system descriptions, and public information usually fail. An item that fails cannot be CTI or Export Controlled; stop there for it.
- **Read the lists forward, at the right level.** USML first (22 CFR 120.11), enumerated entries before catch-alls. If nothing catches it, ask whether it is subject to the EAR at all (734.3(b)), then the CCL in the Supplement No. 4 to Part 774 order, 600 series first, then EAR99. An entry controls a named level (120.40): one that names components does not catch a part. CCL entries turn on thresholds. Read the current eCFR each time and record the date; the lists change.
- **Treat "specially designed" as a test, not a phrase.** Caught under 22 CFR 120.41(a), then released if any (b) paragraph applies: fasteners and the like, a commercial equivalent in production, or dual-use or general-purpose development. A release is only as good as the development records made at the time.
- **Unfinished is not yet the article.** A forging or machined body is a defense article only once it is identifiable as one (120.31(a)(2)). Name the operation that makes it so.
- **Only the delta is controlled.** When a commercial item was adapted to reach a controlled level, only the data that made the difference is controlled; the rest keeps its answer. One item, one regime. End by saying how much of the data is controlled, not just the item.
- **Know who decides.** The design authority classifies, because "specially designed" turns on an end use a build-to-print supplier cannot see. The supplier asks in writing (the request is in `export-control-overlay`). A 7048 clause or an export warning names both regimes and settles neither. A commodity jurisdiction request (120.12) or a BIS classification is for the OEM when the stakes justify it. IT, a program manager, or a consultant writes the memo and never signs it.

**Stop:** Do not write a regime until each data item has passed the technical data test and the entry was read in the current text. While the design authority's answer is pending, handle as ITAR only the data that passed the test, and record "pending", never "ITAR either way".

Practitioners split on whether an NC program carrying only nominal geometry is technical data. The part's compositional level and 120.31(a)(2) usually settle more of it than either side admits.

## Output

Append one entry per item to `scope/export-classifications.md`:

```markdown
## <item>

- Date: <date>. Classified by: <design authority in writing (attach) / export counsel / trade compliance / pending, asked ... on ...>
- Item: <what it is and its level, 22 CFR 120.40>; goes into: <end-item, or "not known to this company">
- Data items: <each one: technical data or not, and why>
- Entry: <USML category and paragraph / ECCN / EAR99 / not subject to the EAR (734.3(b) basis)>, read <date>; specially designed: <caught (a)(n), released (b)(n) with records / not used>
- Result: <ITAR, Category ... / EAR, ECCN ... / EAR99 / not subject to the EAR / not technical data / pending>
- For CUI: <cannot be CTI or Export Controlled / can be>; send to `is-this-cui` either way, since another category can still reach the data
- Open items: <requests and documents still missing>
```

The rules are linked in `public_sources` above.
