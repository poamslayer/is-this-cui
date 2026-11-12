> **Provenance.** This repo's own work, MIT. It lists public sources and quotes short passages from United States Government works, which are public domain. The rules for this file are in `docs/adr/0004-authority-tiers.md`.

# Authorities register

Every URL cited anywhere in `skills/` is listed here, once. `python3 scripts/check_authorities.py` (run by `verify.sh`) fails when a skill cites a URL that is not here, and when a mirror path below does not exist. `python3 scripts/check_links.py` checks that every URL here and in `skills/` still resolves.

## How to use it

- **Before citing a source in a skill**, find it here. If it is not here, add it first, in the right tier, then cite it.
- **Before stating a CUI status rule** (whether something is CUI, which category, whether a marking or a flowdown makes it CUI), cite a Tier 1 or Tier 2 entry. A Tier 3 entry can support how practitioners handle the question, never the answer. See ADR-0004 point 3.
- **To see which skills cite a source**, run `grep -rl '<url>' skills`. The register does not keep that list, because a hand-kept list goes stale.
- **When a host blocks scripted fetches**, read the mirror. When the source is reissued, refresh the mirror and its hash.

The **Checked** column gives the date a URL was last confirmed and how: `script` (it answered `check_links.py`), `browser` (the host refuses scripts, so it was opened in a browser), or `mirror` (it was fetched into `skills/is-this-cui/reference/` on that date).

Where two URLs reach the same source, both are listed, because the check matches the text of the URL.

## Tier 1: regulation and statute

Can establish a rule or a status.

| Source | Relied on for | URL | Mirror | Checked |
|---|---|---|---|---|
| 32 CFR 170.4 | Definitions: ESP, CSP, Security Protection Data, Operational Plan of Action, Test Equipment | https://www.ecfr.gov/current/title-32/section-170.4 | | 2026-09-26 script |
| 32 CFR Part 2002 | The CUI Program | https://www.ecfr.gov/current/title-32/part-2002 and https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002 | | 2026-09-26 script |
| 32 CFR 2002.4(h) | CUI definition, and the exclusion for a non-executive branch entity's own information. Quoted below | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.4(aa), (pp) | "Handling" includes re-using; "re-use" defined | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.4(ee) | Misuse includes marking information as CUI when it does not qualify | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.4(nn) | "Required or permitted" basis; general agency discretion excluded | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.12(a) | CUI categories are the exclusive designations | https://www.ecfr.gov/current/title-32/section-2002.12 | | 2026-09-26 script |
| 32 CFR 2002.14(h)(2) | Agencies must use NIST SP 800-171 for CUI on non-Federal information systems; how a civilian agency's CUI reaches a contractor without DFARS | https://www.ecfr.gov/current/title-32/section-2002.14 | | 2026-09-26 script |
| 32 CFR 2002.20 | Marking. (a)(1), (a)(2), (a)(4), (a)(7), (d), (f): only Registry markings designate; legacy markings are void; the designating agency determines; lack of a marking does not exempt; designation indicator; portion marking | https://www.ecfr.gov/current/title-32/section-2002.20 | | 2026-09-26 script |
| 32 CFR 2002.50 | Challenges to a CUI designation | https://www.ecfr.gov/current/title-32/section-2002.50 | | 2026-09-26 script |
| 81 FR 63324 (2016-09-14), the CUI final rule and its preamble | The preamble at 81 FR 63334: a document derived from CUI is CUI "because it contains controlled information, not simply because it is derived from a document that contains CUI". Published by NARA with the rule it explains. Quoted below | https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information and https://www.govinfo.gov/content/pkg/FR-2016-09-14/html/2016-21665.htm | | 2026-09-26 script |
| DFARS 252.204-7012 | Covered defense information (both prongs), CTI, technical information, safeguarding, incident reporting | https://www.ecfr.gov/current/title-48/section-252.204-7012 and https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012 | | 2026-09-26 script |
| DFARS 252.227-7013 | Rights in technical data: technical data definition, data rights, private expense | https://www.ecfr.gov/current/title-48/section-252.227-7013 and https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013 | | 2026-09-26 script |
| DFARS 252.225-7048 | Export-controlled items clause; (a) defines the term to cover both EAR and ITAR items, so the clause alone does not say which regime applies | https://www.ecfr.gov/current/title-48/section-252.225-7048 | | 2026-09-26 script |
| FAR 52.204-21 | FCI and basic safeguarding | https://www.ecfr.gov/current/title-48/section-52.204-21 and https://www.acquisition.gov/far/52.204-21 | | 2026-09-26 script |
| 22 CFR Part 120 | ITAR definitions | https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120 | | 2026-09-26 script |
| 22 CFR 120.31 | Defense article, including unfinished products that have reached a stage in manufacturing where they are identifiable as defense articles | https://www.ecfr.gov/current/title-22/section-120.31 and https://www.ecfr.gov/current/title-22/part-120/section-120.31 | | 2026-09-26 script |
| 22 CFR 120.33 | ITAR technical data ("required for"); (b) excludes public domain, general principles, basic marketing information and general system descriptions | https://www.ecfr.gov/current/title-22/section-120.33 | | 2026-11-12 script |
| 22 CFR 120.34 | Public domain, excluded from ITAR technical data | https://www.ecfr.gov/current/title-22/section-120.34 | | 2026-11-12 script |
| 22 CFR 120.50 | Export; (a)(2) defines the deemed export: releasing technical data to a foreign person in the United States | https://www.ecfr.gov/current/title-22/section-120.50 | | 2026-09-26 script |
| 22 CFR 120.56 | Release, including release to a foreign person (deemed export) | https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/section-120.56 | | 2026-09-26 script |
| 22 CFR 120.40 | Compositional terms: end-item, component, part; a USML entry that names only components or end-items does not catch a part | https://www.ecfr.gov/current/title-22/section-120.40 | | 2026-11-12 script |
| 22 CFR 120.41 | "Specially designed"; (b)(2) releases fasteners, washers, spacers, and similar hardware "regardless of form or fit"; the release does not reach an item a USML entry names directly | https://www.ecfr.gov/current/title-22/section-120.41 | | 2026-11-12 script |
| 22 CFR 121.1 | The U.S. Munitions List, every category and entry; linked, not mirrored, because DDTC revises it often | https://www.ecfr.gov/current/title-22/section-121.1 | | 2026-11-12 script |
| 22 CFR 120.11 | ITAR order of review: USML first, enumerated entry over "specially designed" catch-all, integration rule, pointer to the CCL order of review | https://www.ecfr.gov/current/title-22/section-120.11 | | 2026-11-12 script |
| 22 CFR 120.12 | Commodity jurisdiction determination requests to DDTC | https://www.ecfr.gov/current/title-22/section-120.12 | | 2026-11-12 script |
| 22 CFR 120.42 | Form, fit, function, performance capability, equivalent; enumerated vs catch-all control | https://www.ecfr.gov/current/title-22/section-120.42 | | 2026-11-12 script |
| 15 CFR 734.3 | Items subject to the EAR; ITAR items excluded at (b)(1)(i); published, fundamental research and other information excluded at (b)(3); EAR99 designation at (c) | https://www.ecfr.gov/current/title-15/section-734.3 | | 2026-09-26 script |
| 15 CFR 772.1 | EAR definitions: "technology", "required", "specially designed" (fasteners released at (b)(2), "regardless of form or fit") | https://www.ecfr.gov/current/title-15/section-772.1 | | 2026-09-26 script |
| 15 CFR Part 774, Supplement No. 4 | Commerce Control List order of review: no CCL review for a USML item, "600 series" and 9x515 first, EAR99 may still need a license by end user, end use, or destination | https://www.ecfr.gov/current/title-15/part-774/appendix-Supplement%20No.%204%20to%20Part%20774 | | 2026-11-12 script |
| 22 CFR 120.54 | Activities that are not exports; (a)(5) sending, taking, or storing technical data that is unclassified, end-to-end encrypted with FIPS 140-2 or successor modules (or at least AES-128 strength), and not sent to or stored in a 126.1 country; (b) end-to-end encryption means the means of decryption are not provided to any third party; (c) access to data encrypted that way is not a release | https://www.ecfr.gov/current/title-22/section-120.54 | | 2026-09-26 script |
| 22 CFR 122.1 | Registration; (a) a manufacturer of defense articles must register even if it does not export | https://www.ecfr.gov/current/title-22/section-122.1 | | 2026-09-26 script |
| 22 CFR 122.5 | Records a registrant keeps, how they are kept, and the five-year retention period | https://www.ecfr.gov/current/title-22/section-122.5 | | 2026-09-26 script |
| 22 CFR 125.4 | Exemptions of general applicability; (a) none apply to 126.1 destinations; (b)(9) technical data taken abroad by a U.S. person, or a foreign person employee of a U.S. person, travelling or on temporary assignment, with its conditions | https://www.ecfr.gov/current/title-22/section-125.4 | | 2026-09-26 script |
| 22 CFR 126.1 | Prohibited exports and proscribed countries | https://www.ecfr.gov/current/title-22/section-126.1 | | 2026-09-26 script |
| 22 CFR 127.12 | Voluntary disclosures to DDTC; (b)(2) timing, before the government learns of it from another source; (b)(3)(v) senior management knowledge and authorization | https://www.ecfr.gov/current/title-22/section-127.12 | | 2026-09-26 script |
| 15 CFR 734.18 | Activities that are not exports under the EAR; (a)(5) the encrypted sending, taking, or storing rule, with Country Group D:5; (c) access to data encrypted that way is not a release | https://www.ecfr.gov/current/title-15/section-734.18 | | 2026-09-26 script |
| 15 CFR 740.9 | License Exception TMP; (a)(1) tools of trade; (a)(3) "technology" taken abroad by a U.S. person or a foreign person employee travelling, with its conditions | https://www.ecfr.gov/current/title-15/section-740.9 | | 2026-09-26 script |
| 15 CFR 762.6 | EAR records are kept five years | https://www.ecfr.gov/current/title-15/section-762.6 | | 2026-09-26 script |
| 15 CFR 764.5 | Voluntary self-disclosures to BIS | https://www.ecfr.gov/current/title-15/section-764.5 | | 2026-09-26 script |
| 10 U.S.C. 130 | DoD authority to withhold technical data; "can be used, or be adapted for use" | https://www.law.cornell.edu/uscode/text/10/130 | | 2026-09-26 script |

## Tier 2: official federal guidance

Can state how the government reads a rule. Cite it next to the Tier 1 rule it explains, not in place of it.

| Source | Relied on for | URL | Mirror | Checked |
|---|---|---|---|---|
| DoD CUI Registry, category list and abbreviations | Categories as the DoD lists them | https://www.dodcui.mil/CUI-Categories-and-Abbreviations/ | `skills/is-this-cui/reference/cui-registry/CUI-Categories-and-Abbreviations.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Export Controlled | Export Controlled category | https://www.dodcui.mil/Export-Control/Export-Controlled/ | `skills/is-this-cui/reference/cui-registry/Export-Control--Export-Controlled.md` | 2026-09-26 browser; mirror 2026-05-13 |
| BIS, Export Compliance Guidelines: The Elements of an Effective Export Compliance Program | The eight elements of an export compliance program; what a Technology Control Plan should contain; the six fields of a foreign-national visitor record. PDF sha256 1f757636ba40f5860da631e1f7cbed4422305a98b771dfe681f70e598ce03bea | https://www.bis.gov/media/documents/export-compliance-guidelines | | 2026-09-26 script |
| DoD CUI Program FAQ, Use of Distribution Statements | "A distribution statement does not automatically mean the document is CUI." Quoted below | https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/ | `skills/is-this-cui/reference/cui-registry/Frequently-Asked-Questions--Use-of-Distribution-Statements.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoDI 5230.24, "Distribution Statements on DoD Technical Information," January 10, 2023 | Distribution statements B to F, the controlling DoD office, reason codes. The 2012 version was titled "on Technical Documents" | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf | `skills/is-this-cui/reference/dod-issuances/dodi-5230-24.md` | 2026-09-26 mirror |
| DoD Cybersecurity FAQs on DFARS Subpart 204.73 and 239.76, July 30, 2020 rev 3 (updated 2021-12-19), Defense Pricing and Contracting | A32: "in support of the performance of the contract" does not make all information a contractor uses to perform the contract covered defense information. Quoted below. Dated: read the current DoD CIO and DPC guidance before relying on it | https://dodprocurementtoolbox.com/uploads/Cybersecurity_FAQ_update_12_19_22_ba047be683.pdf | `skills/is-this-cui/reference/dod-issuances/dod-cybersecurity-faq-covered-defense-information.md` | 2026-09-26 mirror |
| DoDI 5200.48, "Controlled Unclassified Information (CUI)," March 6, 2020 | How the DoD implements the CUI Program; para 3.6.a, the authorized holder determines at creation whether information in a new document falls into a CUI category. Quoted below | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/520048p.PDF | `skills/is-this-cui/reference/dod-issuances/dodi-5200-48.md` | 2026-09-26 mirror |

## Tier 3: public secondary sources

Can support a method or a practice. Never settles a status question on its own. Commercial sources are marked **commercial**.

| Source | Relied on for | URL | Mirror | Checked |
|---|---|---|---|---|
| Summit 7, "How To Know If You Have CUI", CS2 talk | Method for finding CUI | https://www.youtube.com/watch?v=IEy-TkmKMt8 | | 2026-09-26 script |
| Public panel on a 2019 DDTC consent agreement (FLIR), Summit 7 | ITAR enforcement lessons | https://www.youtube.com/watch?v=qS44dOwoWUs | | 2026-09-26 script |
| Public panel on practical ITAR compliance steps, Summit 7 | ITAR practice for small and mid-size firms | https://www.youtube.com/watch?v=xhFX1eCHHSI | | 2026-09-26 script |

## Not sources

Links that attribute a licence, define a working term, or point at an image a skill embeds. They support no claim and have no tier. They are listed so the register check has no exceptions.

| Link | Why it is cited | URL |
|---|---|---|

## Quoted text for CUI status rules

These are the passages the repo relies on to state a CUI status rule, quoted exactly.

**32 CFR 2002.4(h).** "Controlled Unclassified Information (CUI) is information the Government creates or possesses, or that an entity creates or possesses for or on behalf of the Government, that a law, regulation, or Government-wide policy requires or permits an agency to handle using safeguarding or dissemination controls. However, CUI does not include classified information (see paragraph (e) of this section) or information a non-executive branch entity possesses and maintains in its own systems that did not come from, or was not created or possessed by or for, an executive branch agency or an entity acting for an agency."

**ISOO, CUI Stakeholders Update Q2 FY2020, slide 8.** Under "Is my Proprietary Information CUI?": "The government will protect it as CUI (and may even send it back to you as CUI) but the proprietary information you create internally and maintain ownership of is not CUI (though it may require protections pursuant to other laws or regs)."

The same slide says "Information should always be protected in accordance with the requirements in the contract under which it was produced or received." That sentence answers a different question on the slide, about legacy markings such as FOUO and SBU. Do not cite it as ISOO's answer on proprietary information.

**DoD CUI Program FAQ, Use of Distribution Statements.** "The application of a distribution statement does not automatically mean the document is CUI. Do not confuse the two issues."

**81 FR 63324, 63334 (preamble to the CUI final rule).** "A document containing CUI that is derived from another document that contains CUI would also be CUI--because it contains controlled information, not simply because it is derived from a document that contains CUI. It is possible the original document contains both CUI and non-CUI and the derived document could therefore contain only information derived from the non-CUI portions of the original document. In such a case, the derived document would not become CUI simply because the information was derived from a CUI document."

**32 CFR 2002.4(pp).** "Re-use means incorporating, restating, or paraphrasing information from its originally designated form into a newly created document."

**32 CFR 2002.4(ee).** Misuse of CUI "may also include designating or marking information as CUI when it does not qualify as CUI."

**DoDI 5200.48, para 3.6.a.** "The authorized holder of a document or material is responsible for determining, at the time of creation, whether information in a document or material falls into a CUI category. If so, the authorized holder is responsible for applying CUI markings and dissemination instructions accordingly."

**DoD Cybersecurity FAQs, A32.** "It is meant to include any covered defense information used in performance of the contract and exclude other information that may be developed by the contractor but not associated with contract performance. It does NOT mean that all information used by the contractor to support contract performance, e.g., information in the contractor's human resources or financial/accounting systems, is considered to be covered defense information."
