# Threat Intelligence and OSINT: A Professional Course Book

- Language: English (`en`); professional course, six months.
- Editorial state: **published**. Chapters 1–12 of 12 have hand-written teaching text; exercises EX001–EX060 have matching worked results with 0–3 rubrics; two offline labs use only the Python 3 standard library on synthetic data, with outputs embedded from real runs. Independent review and the 300-page A4 verification remain open.
- Audience: working practitioners adding cyber threat intelligence (CTI) and OSINT skills to an IT or security role.
- Author: [hiagokinlevi](https://github.com/hiagokinlevi). Original text [CC0 1.0](../../../../../LICENSE); cited works keep their rights.
- Ethical boundary: no collection on real private individuals, no terms-of-service evasion, no deanonymisation, no contact with adversary infrastructure. Organisations, people and indicators are **synthetic** unless a sentence cites a public source; addresses use RFC 5737 ranges and domains use `.example`.

[Course home](../../README.md) · [Chapter index](../SUBJECTS.md) · [Book plan](PLAN.md) · [Course skill](../../skill/SKILL.md) · [Worked results](#worked-results)

## How to use this draft

Chapters 1–4 cover foundations, stakeholders, authorised practice and core methods. Chapters 5–8 cover tools and interpretation (with a triage-scoring lab), workflow, controls and verification, and a supervised case. Chapters 9–12 cover communication and ethics, quality and troubleshooting, a supervised laboratory (with a brief-release check lab) and the practice portfolio. Each chapter has outcomes, teaching, a worked example, a labelled synthetic case, errors and limits, five exercises scored 0–3, a synthesis and a **Continue studying** block.

### Synthetic running case

| Element | Role | Boundary |
|---|---|---|
| **Bramwell Insurance Brokers (BIB)** — 300 staff, a client portal, a CRM and broker email | Organisation served by CTI | Invented |
| **Priya Nair** | IT support lead taking on CTI duties part-time | Invented |
| **Financial Services Sharing Group (FSSG)** | Sector community sharing intelligence under TLP 2.0 | Invented |

### Core sources

MITRE [ATT&CK](https://attack.mitre.org/); OASIS [STIX 2.1](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html) and [TAXII 2.1](https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html); [Diamond Model](https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf); Hutchins et al. [kill chain](https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Intel-Driven-Defense.pdf); NIST [SP 800-150](https://doi.org/10.6028/NIST.SP.800-150); FIRST [TLP 2.0](https://www.first.org/tlp/); [ICD 203](https://www.odni.gov/files/documents/ICD/ICD-203.pdf). Full list in [References](#references).

## Contents

| Chapters |
|---|
| [1](#ch-01) · [2](#ch-02) · [3](#ch-03) · [4](#ch-04) · [5](#ch-05) · [6](#ch-06) |
| [7](#ch-07) · [8](#ch-08) · [9](#ch-09) · [10](#ch-10) · [11](#ch-11) · [12](#ch-12) |

[Worked results](#worked-results) · [References](#references)

<a id="ch-01"></a>

## Chapter 1 — Security foundations for practitioners

### Learning outcomes

You will (1) restate core security concepts in a CTI context; (2) describe the intelligence cycle as a working routine; (3) name the main models and standards; (4) set realistic goals for a part-time CTI role.

### 1.1 Starting point

Priya has run IT support at Bramwell Insurance Brokers for eight years. She knows the systems, the users and the help desk. Her manager adds CTI to her role: one day a week to turn outside information about threats into better defences. Those eight years matter for CTI work, because Priya already knows which systems hold client data and who owns the CRM, the portal and broker email. What she lacks is a habit of reading outside reports and asking what they mean for BIB. The single weekly day is a hard limit, so every routine in the following chapters is sized to fit it.

### 1.2 Core terms

Threat: an actor or event that could cause harm. Vulnerability: a weakness. Risk: likelihood combined with impact. Control: a measure that reduces risk. Intelligence informs the threat side so controls are chosen well. At BIB each of these four terms maps onto something Priya can point to. A fraudster sending fake insurer bank details is a threat, and finance staff paying without a check is the vulnerability. The risk is a lost client premium, and call-back verification is the control. Priya's FSSG reading changes the likelihood side of that risk by showing how often brokers are being targeted this quarter.

### 1.3 The cycle as a routine

Direction (what does BIB need to know?), collection (FSSG, advisories, internal reports), processing (cleaning indicators), analysis (what it means for BIB), dissemination (to whoever acts) and feedback. For Priya it becomes a weekly checklist. Each stage of the cycle has a day or a recurring date attached to it. Direction is the requirements list her manager approves; collection is Monday's FSSG reading; processing and log matching happen on Tuesday; dissemination is the Wednesday help-desk update and the monthly summary. Feedback comes from the quarterly consumer forms and the monthly note to FSSG, and it changes the requirements for the next quarter.

### 1.4 Models

MITRE ATT&CK names adversary techniques — Phishing is T1566. The Hutchins et al. kill chain shows phases where defenders can act. The Diamond Model describes events by adversary, capability, infrastructure and victim. Priya uses each of the three models to answer a different question about an event. ATT&CK gives her the technique names she tags on FSSG items and later in the fraud case. The kill chain shows where BIB could have stopped an intrusion, which matters when there was no exploitation at all. The Diamond Model lets her describe the lookalike-domain fraud without needing to know who the adversary is.

### 1.5 Standards

STIX 2.1 for data, TAXII 2.1 for exchange, FIRST TLP 2.0 for sharing limits, NIST SP 800-150 for sharing practice. For Priya the four standards are practical tools she meets every week, not theory. FSSG may deliver items as STIX objects over TAXII, but she mostly reads their summaries and copies indicators into tickets. The TLP label on each item decides whether she may forward it to the help desk, to clients or nobody at all. NIST SP 800-150 shapes how BIB shares sanitised items back to the community.

### 1.6 Realistic goals

In one day a week Priya can triage FSSG items, match indicators against email and DNS logs, brief the help desk and report monthly. Deep malware analysis and attribution are out of scope. These limits are written down because a part-time role can easily drift into work that cannot be finished well. If FSSG reports a malware family, Priya takes the indicators and the advice and leaves reverse-engineering to the vendor or an external responder. Attribution to a named group would not change any BIB decision, so it stays outside her scope.

### 1.7 What brokers face

Insurance brokers hold personal and financial client data and move money. Business email compromise, credential phishing against the client portal and ransomware are the main concerns reported in the sector. Those three concerns set the shape of the year that follows. Business email compromise leads to the call-back control and the fraud case in Chapter 8. Credential phishing against the portal leads to the MFA pilot and the failed-login analysis. Ransomware remains a concern Priya tracks through advisories, but no BIB incident of that kind appears in the case.

### 1.8 Learning plan

Each chapter adds one routine to her week, so the role grows steadily. Chapter 2 adds the requirements list, Chapter 5 the Monday scoring, Chapter 6 the ticket for every item, and Chapter 7 the control register. By Chapter 11 she runs a pre-release check on every brief. The order matters, because each routine depends on the one before it: scoring needs requirements, and tickets need the scores to record. By the portfolio review in Chapter 12, the routines together have produced twelve control changes traced to intelligence, which is the measure of whether this gradual approach worked.

### Worked example

Priya's first weekly checklist: Monday, read FSSG items and triage; Tuesday morning, search logs for this week's indicators; Wednesday, send the help desk a short scam update; last Friday of the month, write a one-page summary for her manager.

> **Synthetic case.** BIB and Priya are invented.

### Errors and limits

A part-time role cannot cover everything; agree priorities in writing.

### Exercises

- **EX001 — Define risk.** Define risk and explain how CTI contributes to it. *Rubric:* 3 = likelihood × impact; CTI informs threat/likelihood; 2 = definition; 1 = vague; 0 = none.
- **EX002 — Weekly routine.** Turn the intelligence cycle into a weekly routine for a part-time role. *Rubric:* 3 = all stages mapped to days/tasks; 2 = most; 1 = list; 0 = none.
- **EX003 — Out of scope.** Name two tasks outside Priya's realistic scope. *Rubric:* 3 = malware analysis, attribution; 2 = one; 1 = log search; 0 = none.
- **EX004 — Broker threats.** List three threats brokers commonly face. *Rubric:* 3 = BEC, portal credential phishing, ransomware; 2 = two; 1 = one; 0 = none.
- **EX005 — Model purpose.** Match ATT&CK, the kill chain and the Diamond Model to what each describes. *Rubric:* 3 = techniques; phases; event vertices; 2 = two; 1 = one; 0 = none.

### Synthesis

CTI informs risk decisions through a steady cycle, shaped by models and standards and sized to the time available.

### Continue studying — chapter 01 of 12

[← Course home](../../README.md) · [Course chapter index](../SUBJECTS.md) · [Chapter 02 (draft) →](#ch-02)

<a id="ch-02"></a>

## Chapter 2 — Threat intelligence and OSINT: service and stakeholder context

### Learning outcomes

You will (1) identify BIB's intelligence consumers and their decisions; (2) write priority intelligence requirements; (3) match products to consumers; (4) manage expectations.

### 2.1 Consumers

The managing director decides budgets. The operations manager decides on process changes such as payment verification. The IT team configures email and network controls. The help desk talks to staff. The compliance officer handles regulators and data protection. Each consumer needs different evidence for the decision they own. The managing director will fund a control only if she sees its cost against the risk; the operations manager needs to know which fraud method is active before changing payment steps. IT needs domains, software versions and dates it can turn into blocks and patches. The help desk needs one example of each current scam, written in plain words.

### 2.2 Requirements

Priya interviews each and writes requirements: "Which fraud methods target brokers' payment processes this quarter?" (operations); "Which vulnerabilities in our CRM and portal are being exploited?" (IT); "Are BIB credentials or client data exposed publicly?" (compliance). Each requirement is written as a question that one consumer can act on within a set period. That wording lets Priya test every FSSG item against the list on Monday morning. An item about manufacturing ransomware answers none of the three questions, which is why Q2 in the scoring lab is logged only. The list is reviewed every quarter with the consumers who own each question.

### 2.3 Products

Managing director: quarterly half-page. Operations: alerts when a fraud method appears. IT: indicator lists and vulnerability notes. Help desk: weekly scam update. Compliance: notices of data exposure. Products differ in length and timing as much as content. The managing director's half-page arrives each quarter, while an operations alert goes out the same day a new fraud method appears. IT's indicator lists carry domains and dates ready to block, and the help desk's update carries one example per scam, not indicators. Compliance hears from Priya only when BIB credentials or client data are found exposed publicly.

### 2.4 Expectations

Priya explains that CTI reduces surprise but cannot predict every attack. She agrees what "urgent" means: active exploitation of a system BIB runs, or a fraud method targeting BIB by name. Writing the definition down protects both Priya and her consumers. Without it, every alarming FSSG headline could become a phone call, and real urgent items would lose their force. With it, the CRM exploitation report in Chapter 6 clearly qualifies, because BIB runs that version. A ransomware wave against manufacturers, however serious elsewhere, waits for the normal Monday routine.

### 2.5 Business email compromise

Fraudsters impersonate clients or insurers to redirect payments. The operations manager's decision — whether to require call-back verification for changed bank details — depends on intelligence about how common this is in the sector. For the operations manager, the decision weighs a cost to every payment change against a risk. Call-back verification adds work to every bank-detail change, so the operations manager wants evidence that the fraud is common enough to justify it. FSSG's report of three brokers losing client premiums supplies that evidence, and the manager introduces the call-back step the same week. Chapter 8 later shows what happens when it is skipped.

### 2.6 Feedback

Each consumer gets a two-question form quarterly. The two questions are short on purpose: 'What helped you decide something this quarter?' and 'What could we stop sending?'. Short forms get answered, while long surveys sit in inboxes. The answers feed the quarterly requirements review, and later they lead to the help desk's request that moved scam updates from Wednesday to Monday, recorded in the improvement log in Chapter 10. Priya keeps the completed forms with the requirements list, so each review can see which consumer asked for which change and why.

### 2.7 Saying no

Requests outside requirements, such as researching a difficult client's personal life, are declined politely. Priya declines by pointing to the approved requirements list, which avoids a personal argument with the requester. Researching a client's private life serves no BIB decision, intrudes on that person's privacy and would expose BIB if it became known. If a consumer believes a new need is genuine, Priya invites them to raise it at the quarterly requirements review instead. The refusal and its reason go into her log, which protects her if the request is repeated later by someone more senior.

### 2.8 Writing it down

A one-page requirements list, approved by the manager, guides what Priya collects. The single page lists each requirement, its consumer, the product that answers it and how often. Because her manager approved it, Priya can point to it when she declines a request or drops a low-scored item. The list also tells the IT manager what to collect when he covers her routine, so absence does not change the role's direction. Without the written list, collection would follow whatever looked interesting each Monday rather than what BIB's consumers decide.

### Regulatory context

Financial regulators expect firms to manage operational and cyber risk. Showing that intelligence informed controls — such as call-back verification — helps the compliance officer evidence good practice during reviews.

### Worked example

FSSG reports that three brokers lost client premiums through fake insurer bank-detail changes. Priya alerts the operations manager with the method and two sender domains. The manager introduces call-back verification for any bank-detail change the same week.

> **Synthetic case.** The losses and change are invented.

### Errors and limits

Requirements change; review them every quarter.

### Exercises

- **EX006 — Consumer map.** Map three BIB consumers to the decisions they make. *Rubric:* 3 = three correct pairs; 2 = two; 1 = one; 0 = none.
- **EX007 — Write a requirement.** Write one priority intelligence requirement for the compliance officer. *Rubric:* 3 = specific question, consumer, timeframe; 2 = two; 1 = topic; 0 = none.
- **EX008 — BEC decision.** Which decision did the FSSG fraud report support? *Rubric:* 3 = call-back verification for bank-detail changes; 2 = partial; 1 = vague; 0 = none.
- **EX009 — Urgent definition.** How did Priya define "urgent"? *Rubric:* 3 = active exploitation of BIB system or fraud naming BIB; 2 = one; 1 = everything; 0 = none.
- **EX010 — Decline politely.** Why decline researching a client's personal life? *Rubric:* 3 = outside requirements; privacy/law; 2 = partial; 1 = do it; 0 = none.

### Synthesis

Know your consumers, write requirements with them, match products to decisions and manage expectations.

### Continue studying — chapter 02 of 12

[← Chapter 01 (draft)](#ch-01) · [Course chapter index](../SUBJECTS.md) · [Chapter 03 (draft) →](#ch-03)

<a id="ch-03"></a>

## Chapter 3 — Authorized practice and evidence handling

### Learning outcomes

You will (1) work within written authorisation; (2) apply TLP 2.0 and data-protection rules; (3) handle evidence with provenance; (4) recognise actions that need legal or management approval.

### 3.1 Authorisation

Priya's role description and the IT security policy list what she may do: read intelligence sources, search BIB logs, draft requests, share sanitised items with FSSG. Anything else needs approval. The written list protects Priya as much as it limits her. Searching BIB's email logs for an FSSG indicator is covered, so she does not need to ask each time. Requesting a takedown, buying a feed or contacting police is not covered, so those go to her manager. When a task falls between the two, she asks first and records the answer.

### 3.2 TLP 2.0

CLEAR: public. GREEN: community. AMBER: BIB and its clients on need-to-know. AMBER+STRICT: BIB only. RED: named people. Priya stores items with labels and checks before forwarding. The TLP labels decide where each item can travel once it reaches BIB. An FSSG item marked AMBER can reach a client only when that client needs it to protect itself, while AMBER+STRICT items stay inside BIB. A RED item stays with the people named on it, even if her manager asks for a copy. Priya checks the label before every forward, not after the item has already gone out.

### 3.3 Data protection

Logs and emails contain personal data of staff and clients. Under the GDPR-style rules BIB follows, she uses only what is needed, keeps extracts briefly and removes personal details before sharing. In practice this means a log search for an FSSG sender domain returns only matching rows, not whole mailboxes. Extracts she keeps for a ticket are deleted when the ticket closes. Before a sender domain goes back to FSSG, she removes client names, staff addresses and anything else that would identify a person. The compliance officer can inspect these practices at any time, for example during a regulator's review.

### 3.4 Evidence

When a phishing email is reported, she saves the original message file, records who reported it and when, and computes a hash of the file. Analysis uses a copy. Each of the four evidence steps has its own reason in this routine. The original file keeps headers that a forwarded copy may lose, and the reporter and time show where the item came from. The hash lets anyone later confirm that the file has not changed. Working on a copy means a mistake during analysis cannot damage the only original, which matters if the case reaches police.

### 3.5 Approval needed

Contacting police, requesting takedowns, notifying regulators, buying intelligence services, or engaging with suspected criminals. Each goes through management and, where needed, legal advice. These actions can bind BIB legally, cost money or alert criminals, so Priya cannot take them alone. For the lookalike domain in Chapter 5 she asks IT to block it but asks management to approve the takedown request. In the fraud case, management reports to the bank and police while Priya supplies the timeline that supports both reports.

### 3.6 OSINT boundaries

Public sources only, within terms of service, no fake accounts, no closed forums, no attempts to identify private individuals. Each of the five OSINT rules closes a specific risk for BIB and for Priya. Fake accounts breach platform terms and are deceptive, and closed forums expose BIB to criminals and possible legal trouble. Identifying private individuals is outside every requirement and would intrude on their privacy. That is why the forum claim about broker data in Chapter 5 is checked through FSSG rather than by Priya visiting the forum herself.

### 3.7 Records

A simple log: item, source, label, action, date. One row per item lets Priya answer simple but important questions later, such as where a domain came from and who received it. For the forwarded client email, the row would read: the sender domain, the client report, GREEN, shared with FSSG, and the date. The ticket system in Chapter 6 later replaces this log with richer fields. Later reviews and FSSG questions about an item can then be answered from the log rather than from Priya's memory of it.

### 3.8 Mistakes

If something is shared wrongly, report it at once and ask recipients to delete it. Speed matters more than embarrassment when something has been shared too widely. If an AMBER+STRICT item reached a client by mistake, Priya would tell her manager the same day, ask the client to delete it and inform the source. The cause goes into her records, so the same slip does not happen again. Hiding a mistake would damage FSSG's trust in BIB far more than the slip itself would.

### Chain of custody

If an incident may lead to legal action, evidence handling must show who held each item and when. Priya records every transfer of the saved email file — to the IT manager, to an external responder — with date, recipient and purpose.

### Worked example

A client forwards a suspicious email claiming to come from BIB. Priya saves the original, hashes it, removes the client's details from her working notes and shares the sender domain with FSSG at GREEN. The compliance officer decides whether the client must be told anything further.

> **Synthetic case.** The email is invented.

### Errors and limits

Policies need updating as the role grows.

### Exercises

- **EX011 — Approval list.** Name four actions requiring management or legal approval. *Rubric:* 3 = four of police, takedown, regulator, purchase, engaging criminals; 2 = three; 1 = one; 0 = none.
- **EX012 — Evidence steps.** List the evidence steps for a reported phishing email. *Rubric:* 3 = save original, record reporter/time, hash, work on copy; 2 = three; 1 = one; 0 = none.
- **EX013 — AMBER+STRICT reach.** Who may receive TLP:AMBER+STRICT material? *Rubric:* 3 = BIB only, need-to-know; 2 = partial; 1 = clients; 0 = none.
- **EX014 — Client email decision.** Who decides on informing the client further, and why? *Rubric:* 3 = compliance officer; regulatory/data duties; 2 = partial; 1 = Priya; 0 = none.
- **EX015 — Fake accounts.** Why are fake accounts forbidden for OSINT? *Rubric:* 3 = breaches terms/law/ethics; risk to BIB; 2 = partial; 1 = allowed; 0 = none.

### Synthesis

Work inside written authority, apply TLP and data protection, preserve evidence and escalate actions that need approval.

### Continue studying — chapter 03 of 12

[← Chapter 02 (draft)](#ch-02) · [Course chapter index](../SUBJECTS.md) · [Chapter 04 (draft) →](#ch-04)

<a id="ch-04"></a>

## Chapter 4 — Threat intelligence and OSINT: core methods

### Learning outcomes

You will (1) triage, grade and tag intelligence; (2) write calibrated judgments; (3) consider alternative explanations; (4) produce short, actionable notes.

### 4.1 Triage

Relevant? Timely? Actionable? Source known? Most items fail relevance and are logged only. Each of the four triage questions removes a different kind of noise from the forty weekly items. An item about a system BIB does not run fails relevance; a forty-day-old address list fails timeliness; an item with nothing to block or change fails actionability. An unknown source does not fail outright but lowers the grade. Items that fail are logged with their reason, so a later review can check the decision.

### 4.2 Grading

Admiralty scale: source A–F, information 1–6. FSSG with a good record: B. A vendor blog: C until its record is known. Anonymous posts: F. Source and information are graded separately, because a reliable source can pass on doubtful information and an unknown source can be right. FSSG earns B through a record of accurate items, and a new vendor blog starts at C until its claims can be checked. In the scoring lab, the A source behind Q3 adds three points, while the F forum adds none.

### 4.3 Tagging

Tag ATT&CK techniques supported by the text: invoice fraud by email (T1566 if links or attachments are used; otherwise a social-engineering pretext), credential use (T1078), encryption for impact (T1486). The rule is to tag only what the text supports. A bank-detail email without a link or attachment is a pretext, so it should not be tagged T1566 by habit. Accurate tags let Priya later count which techniques FSSG reports most often against brokers, and they point her to the ATT&CK mitigation pages when she drafts control requests.

### 4.4 Calibrated words

Use a fixed scale: unlikely (20–45%), roughly even (45–55%), likely (55–80%), very likely (80–95%). ICD 203 asks analysts to express uncertainty clearly and explain confidence. A fixed scale stops two readers from hearing the same word differently. When Priya writes 'likely' in the failed-login note, the operations manager knows she means roughly 55 to 80 per cent, not certainty. The scale also feeds her accuracy tracking in Chapter 10, where she later checks whether her 'likely' judgments happened more often than her 'unlikely' ones. Words outside the scale, such as 'probable', are later caught by the brief check Priya extends in Chapter 11.

### 4.5 Alternatives

Before concluding, ask: what else could explain this? A spike in failed logins may be an attack — or a password-policy change forcing resets. Asking the question early, before writing anything, prevents a confident report that later proves wrong. In the worked example, the portal update and the rise in support calls fit a lockout explanation better than an attack. Yet a small share of attempts from addresses FSSG flagged keeps credential stuffing open. Writing both into the note lets IT and support act on each, instead of betting on one.

### 4.6 Notes

Three lines: what happened; what it means for BIB with likelihood and confidence; what to do and who does it. The failed-login note from the worked example shows the three-line format in practice. Line one states that failed logins tripled overnight; line two gives the likely cause, the portal update, with moderate confidence and the minority stuffing signal. Line three names the actions: IT reviews the flagged addresses and support sends clients reset guidance. A reader who stops after line one still knows something happened.

### 4.7 Consistency

Priya and the IT manager grade the same five items monthly and compare. Comparing grades shows where the scale is being read differently. If Priya grades an item B and the IT manager grades it D, they discuss the evidence and agree a rule for similar items. The exercise also prepares him to cover her routine, because he will be grading items when she is away and needs to apply the same standard. Disagreements and the rules agreed to settle them go into a short note kept with the scoring records.

### 4.8 Time

Triage in minutes; analysis only for items that pass. With about forty items a week and one working day, Priya cannot analyse everything. Triage takes a few minutes per item and filters out most of them. Only items that pass relevance and timeliness get analysis time, which is why scoring in Chapter 5 matters. Logged-only items are still read in summary each week, so nothing unusual is missed entirely. Priya times her Monday triage for a few weeks to confirm that forty items really fit inside the morning.

### Business email compromise signs

Requests to change bank details, urgency, a slightly altered sender domain and replies directed elsewhere are common signs. Intelligence about current pretexts — fake insurer mergers, new payment portals — helps staff recognise them quickly, and gives the operations manager concrete examples for training sessions.

### Worked example

Failed logins on the client portal triple overnight. Alternative explanations: credential stuffing, or clients locked out after a portal update. Priya checks: the update changed the login page and support calls rose. She writes: "Spike likely caused by the update (moderate confidence); a small share of attempts came from addresses FSSG flagged, so stuffing may also be occurring. Action: IT to review those addresses; support to send clients reset guidance."

> **Synthetic case.** The spike is invented.

### Errors and limits

Scales reduce ambiguity, not error; track outcomes.

### Exercises

- **EX016 — Grade a blog.** What grade would a new vendor blog's source receive and why? *Rubric:* 3 = C (or similar) until record known; 2 = grade; 1 = A; 0 = none.
- **EX017 — Alternative.** Give an alternative explanation for a failed-login spike. *Rubric:* 3 = policy change/update lockouts; 2 = vague; 1 = minimal attempt; 0 = none.
- **EX018 — Likely band.** What range does "likely" cover on the scale? *Rubric:* 3 = 55–80%; 2 = close; 1 = wrong; 0 = none.
- **EX019 — Two causes.** Why did Priya's note mention both causes? *Rubric:* 3 = evidence for both; avoid ignoring minority attack; 2 = partial; 1 = indecision; 0 = none.
- **EX020 — Note lines.** What are the three lines of a note? *Rubric:* 3 = what, meaning with likelihood/confidence, action/owner; 2 = two; 1 = one; 0 = none.

### Synthesis

Triage fast, grade and tag with reasons, write calibrated judgments, consider alternatives and keep notes actionable.

### Continue studying — chapter 04 of 12

[← Chapter 03 (draft)](#ch-03) · [Course chapter index](../SUBJECTS.md) · [Chapter 05 (draft) →](#ch-05)

<a id="ch-05"></a>

## Chapter 5 — Threat intelligence and OSINT: tools and interpretation

### Learning outcomes

You will (1) use a simple scoring tool for triage; (2) interpret its output critically; (3) use passive OSINT tools within their terms; (4) know when tool output needs human judgment.

### 5.1 Why score

Priya receives about forty items a week. A transparent score — relevance, freshness, source grade — puts the most useful first. Ordering by hand worked when items were few, but forty a week makes inconsistency likely. A score written as a simple rule can be checked by anyone: three points for relevance, two for freshness within seven days, and up to three for source grade. The lab that follows applies that rule to five synthetic items and prints a decision for each.

### Lab — triage scoring

```python
"""Lab (ch 05): score incoming items on relevance, timeliness and source grade, then sort (synthetic)."""
GRADE = {"A": 3, "B": 2, "C": 1, "D": 0, "E": 0, "F": 0}
items = [("Q1", "broker portal phishing wave", True, 2, "B"),
         ("Q2", "ransomware in manufacturing", False, 1, "B"),
         ("Q3", "flaw in our CRM version", True, 5, "A"),
         ("Q4", "forum claim of broker data sale", True, 1, "F"),
         ("Q5", "old address list", True, 40, "C")]
for qid, title, relevant, age_days, grade in items:
    score = (3 if relevant else 0) + (2 if age_days <= 7 else 0) + GRADE[grade]
    items[items.index((qid, title, relevant, age_days, grade))] = (score, qid, title)
for score, qid, title in sorted(items, reverse=True):
    print(qid, score, title, "-> analyse" if score >= 6 else "-> log only" if score < 5 else "-> check")
```

Run with `python3 lab_triage.py`. Verified output:

```text
Q3 8 flaw in our CRM version -> analyse
Q1 7 broker portal phishing wave -> analyse
Q4 5 forum claim of broker data sale -> check
Q5 4 old address list -> log only
Q2 4 ransomware in manufacturing -> log only
```

### 5.2 Reading the result

Q3, a flaw in BIB's CRM version from an A-grade source within five days, scores 8 and goes to analysis. Q1, the broker-portal phishing wave from FSSG, scores 7 — analysis. Q4, a forum claim that broker data is for sale, scores 5 — check, because it is relevant and fresh but from an F source. Q5 (relevant but 40 days old) and Q2 (fresh but about manufacturing) score 4 and are logged only. The two items tied at 4 are a reminder that one rule can fail different items for different reasons. Q5 fails freshness, while Q2 fails relevance, and the sorted output alone does not show which was which.

### 5.3 Interpreting

Scores order work; they do not decide. Q4 is low-grade but could matter if true; Priya checks whether BIB data appears in the claim's sample through FSSG rather than visiting the forum. The lab's thresholds of 6 and 5 are a starting point for Priya's attention, not a verdict. A score of 5 sends Q4 to 'check', which means a cheap verification step rather than full analysis. If FSSG confirms that a sample contains BIB data, the item moves straight onto the urgent path. If FSSG finds nothing, Priya records that answer and closes the ticket with the reason.

### 5.4 OSINT tools

Certificate-transparency search for lookalikes of bramwell.example; national advisories; vendor vulnerability pages. Used within terms. Each of these passive tools answers one of the requirements written with BIB's consumers. Certificate-transparency logs answer the compliance question about exposure by showing new certificates for names like bramwell-claims.example. National advisories and vendor vulnerability pages answer IT's question about exploited flaws in the CRM and portal. All three are public, used passively and within their terms, so none needs special approval under BIB's policy.

### 5.5 Tool limits

A score ignores context the tool does not know — such as a planned CRM upgrade making Q3 moot next week. The scoring script sees relevance, age and source grade, and nothing else at all. It does not know that IT plans a CRM upgrade, that marketing launched a new site, or that a partner insurer uses a similar domain. Priya adds that missing context by hand, from colleagues and plans, before acting on a score. For Q3, a planned upgrade next week might change the action from urgent patching to confirming the upgrade date.

### 5.6 Adjusting weights

If too many irrelevant items reach analysis, adjust weights and document the change. A change might be lowering the relevance weight or raising the threshold for analysis from 6 to 7. Each change is written down with the date, the reason and the items that prompted it. After a month, Priya checks whether the change reduced wasted analysis without dropping items that later proved useful. Undocumented changes would make the monthly review meaningless, because scores from different weeks could no longer be compared.

### 5.7 Spreadsheet versions

The same scoring works in a spreadsheet; the script is easier to audit. A spreadsheet suits the IT manager when he covers for Priya, because he can see each column. The script is easier to audit, because the rule sits in one line rather than spread across cells that someone might overwrite. Either way, both must produce the same five scores on the lab items before anyone relies on them. Priya keeps the script as the reference version and checks the spreadsheet against it whenever either one changes.

### 5.8 Review

Monthly, compare scores with what actually proved useful. The review compares each week's scored list with what actually happened to the items. If an item logged only at 4 later turned out to matter, the rule missed something and the weights may need adjusting. If analysed items rarely led to any action, the threshold may be too low. The saved weekly lists, dated and kept with the tickets, make this comparison possible months later. The findings feed weight changes, which are then documented with their date and reason as described earlier in this chapter.

### Recording tool runs

Save each week's scored list with the date. Later comparison of scores against what proved useful needs those records.

### Worked example

A certificate-transparency search shows "bramwell-claims.example" registered yesterday. Not a BIB domain. Priya scores it high (relevant, fresh, reliable log), checks with marketing that it is not a new campaign site, and asks IT to block it and management to approve a takedown request.

> **Synthetic case.** The domain is invented.

### Errors and limits

Scores encode assumptions; review them.

### Exercises

- **EX021 — Lab order.** Give the lab's ranking with actions. *Rubric:* 3 = Q3 8, Q1 7 analyse; Q4 5 check; Q5, Q2 4 log; 2 = order; 1 = partial; 0 = none.
- **EX022 — Q4 handling.** How should Priya check the forum claim safely? *Rubric:* 3 = via FSSG/contracted provider, not visiting forum; 2 = partial; 1 = visit forum; 0 = none.
- **EX023 — Missing context.** Give an example of context a score cannot know. *Rubric:* 3 = planned upgrade or similar; 2 = vague; 1 = minimal attempt; 0 = none.
- **EX024 — Lookalike check.** Why ask marketing before blocking the new domain? *Rubric:* 3 = may be legitimate campaign site; 2 = partial; 1 = no need; 0 = none.
- **EX025 — Weight change.** What should accompany any change to scoring weights? *Rubric:* 3 = documentation with reason, review; 2 = partial; 1 = vague; 0 = none.

### Synthesis

Use transparent scoring to order work, interpret it with context, keep OSINT passive and review the tool against outcomes.

### Continue studying — chapter 05 of 12

[← Chapter 04 (draft)](#ch-04) · [Course chapter index](../SUBJECTS.md) · [Chapter 06 (draft) →](#ch-06)

<a id="ch-06"></a>

## Chapter 6 — Threat intelligence and OSINT: operational workflow

### Learning outcomes

You will (1) run a repeatable weekly CTI workflow; (2) track items from arrival to closure; (3) coordinate with IT and the help desk; (4) handle urgent items outside the routine.

### 6.1 The week

Monday: FSSG items scored and triaged. Tuesday: indicator matching in email and DNS logs; requests drafted. Wednesday: help-desk scam update. Thursday: follow-ups. Last Friday: monthly summary. The fixed days make Priya's part-time work predictable for the colleagues who depend on it. IT knows requests arrive on Tuesday, the help desk knows when its update comes, and her manager knows when the summary lands. Thursday is kept for follow-ups because requests sent on Tuesday need chasing. The urgent path sits outside this week and can interrupt any day when its triggers are met.

### 6.2 Tracking

Each item gets a ticket: arrival, source, label, grade, score, decision, actions, closure date. Open tickets show what is pending. The ticket turns each item into something with a visible state. When the IT manager covers her routine, he opens the list of open tickets instead of reading her notes. The fields also feed the monthly metrics: arrival and closure dates give the time to action, and the decision field shows how many items were logged only. A ticket left open past its deadline shows up in Thursday's follow-ups, so stalled requests are chased rather than forgotten.

### 6.3 Coordination

IT applies blocks and patches; the help desk briefs staff; operations changes processes. Priya's requests name the owner and deadline. Naming one owner per request avoids the common failure where everyone assumes someone else will act. For the CRM exploitation report, the owner was the IT manager and the deadline was that evening. Priya's job is to make the request clear and follow it up, not to apply the change herself, since her role description does not cover system changes.

### 6.4 Urgent path

Active exploitation of BIB's CRM or portal, or a fraud method naming BIB, skips the routine: phone the owner, open a priority ticket, inform the manager. The CRM case in the worked example used exactly this path. The FSSG report arrived on Wednesday, outside Monday's triage, and named the CRM version BIB runs. A phone call reached the IT manager within the hour, rather than an email that might wait. The priority ticket recorded the decision and later held the evidence of the version check.

### 6.5 Closure

Items close when action is done and verified, or when a decision not to act is recorded with reason. Verification is a required part of closing a ticket, not an optional extra after it. For the CRM patch, Priya checked the version the next morning before closing the ticket. For an item where the decision is not to act, such as Q2 about manufacturing ransomware, the reason is recorded instead. A ticket closed without either cannot be defended at the monthly review.

### 6.6 Cover

When Priya is away, the IT manager follows the same checklist, using her handover note. The handover note makes cover possible without anyone phoning Priya while she is on leave. It lists open tickets with next steps, scheduled reports and anything urgent in progress. The IT manager already grades five items a month with Priya, so he applies the same scale. Training him as a trained backup becomes part of her plan for the next six months. After each period of cover, Priya reads what he did and updates the note where it was unclear to him.

### 6.7 Metrics

Items received, analysed, actioned; time from arrival to action; blocks that stopped connections. These counts are cheap to collect from the tickets and show whether the routine produces action. If forty items arrive and only one leads to action, Priya questions her sources or her scoring. The time from arrival to action shows whether urgent items really moved faster. Blocked connections give IT and the managing director a concrete sign of value. Priya reports these numbers in the monthly summary for her manager, with the source of each figure stated beside it.

### 6.8 Workload

If the week overflows, Priya drops lowest-scored items first and tells her manager. Dropping items by score keeps the decision consistent from week to week and defensible at review. Items at 4 go first, then items in the 'check' band; analysis items stay. Telling her manager matters because a full week every week is a staffing problem, not a personal one. The record of dropped items also helps the monthly review spot something important that was skipped. Over a quarter, the pattern of overflows shows whether the single weekly day is still enough for BIB's needs.

### 6.9 FSSG feedback

Every month she tells FSSG which items helped BIB; communities improve when members respond. The feedback is specific: which FSSG items led to a block, a process change or a help-desk update, and which were noise for a broker. FSSG can then adjust what it sends to its members. The feedback is shared at GREEN or lower and contains no client details, following the same sanitising rules as any other item. FSSG's sharing agreement covers this feedback, so Priya does not need separate approval each month to send it.

### Handover note

A short handover note lists open tickets with next steps, scheduled reports and any urgent items in progress. The IT manager can continue the routine from it without calling Priya on leave.

### Worked example

On Wednesday FSSG reports active exploitation of the CRM version BIB runs. Priya uses the urgent path: she phones the IT manager, opens a priority ticket and informs her manager. The vendor fix is applied that evening; she verifies the version the next morning and closes the ticket with evidence.

> **Synthetic case.** The exploitation report is invented.

### Errors and limits

Routines can make people miss unusual items; read summaries of logged-only items weekly.

### Exercises

- **EX026 — Ticket fields.** List six ticket fields Priya uses. *Rubric:* 3 = six of arrival, source, label, grade, score, decision, actions, closure; 2 = four; 1 = two; 0 = none.
- **EX027 — Urgent triggers.** What triggers the urgent path? *Rubric:* 3 = active exploitation of BIB system; fraud naming BIB; 2 = one; 1 = any item; 0 = none.
- **EX028 — Closure rule.** When may an item be closed? *Rubric:* 3 = action verified, or decision not to act recorded; 2 = one; 1 = anytime; 0 = none.
- **EX029 — Overflow.** What should Priya do when the week overflows? *Rubric:* 3 = drop lowest-scored first; tell manager; 2 = one; 1 = work weekends silently; 0 = none.
- **EX030 — CRM case.** Describe the steps taken for the CRM exploitation report. *Rubric:* 3 = phone, priority ticket, manager, patch, verify, close; 2 = most; 1 = some; 0 = none.

### Synthesis

Run a weekly routine, track every item, coordinate owners, keep an urgent path and close with evidence.

### Continue studying — chapter 06 of 12

[← Chapter 05 (draft)](#ch-05) · [Course chapter index](../SUBJECTS.md) · [Chapter 07 (draft) →](#ch-07)

<a id="ch-07"></a>

## Chapter 7 — Threat intelligence and OSINT: controls and verification

### Learning outcomes

You will (1) turn intelligence into control requests; (2) choose controls by indicator and technique; (3) verify controls after change; (4) avoid collateral damage.

### 7.1 Requests

Each request states intelligence and source, label, the control change, expected benefit, side effects, verification and review date. A complete request lets the owner decide without asking questions. For the MFA pilot, the intelligence was FSSG reports of credential phishing against three brokers, labelled GREEN. The change was MFA on brokers' remote email for a pilot group; the benefit was blocking stolen passwords; the side effect was extra login steps. Verification through sign-in logs and a review date completed the request before IT acted.

### 7.2 Choosing controls

Sender domains to the email gateway; malicious domains to DNS filtering; hashes to endpoint protection; technique intelligence to configuration — for example, multi-factor authentication on the client portal against Valid Accounts (T1078), and call-back verification against payment fraud. Matching the indicator to the control that can use it saves effort. A sender domain is useless in endpoint protection, and a file hash is useless in the email gateway. Technique intelligence often matters more than indicators, because indicators change quickly. The call-back step against payment fraud works whatever domain the fraudster uses next, which no indicator list can promise.

### 7.3 Process controls

Not all controls are technical. Business email compromise is best countered by verification procedures, dual approval for payments and staff awareness. The fraud case in Chapter 8 shows clearly why technical controls alone fall short. The lookalike email contained no malware and no link, so the gateway, DNS filtering and endpoint tools saw nothing unusual. Only the call-back on the second request stopped the payment. Dual approval would add a second person who checks the bank details, and awareness helps finance staff recognise the pretext before anyone pays.

### 7.4 Verification

Technical: test lookups, harmless test messages, configuration checks. Process: ask operations to confirm call-backs happened for the month's bank-detail changes. Each test produces a record that can go into the ticket. A test lookup of a blocked domain shows the DNS filter answering as expected, and a harmless test message shows the gateway quarantining a blocked sender. For the call-back control, operations shows the call log for each bank-detail change that month, which proves the step actually happened. Every verification record names who performed the test and when, so the result can be repeated by someone else later.

### 7.5 Collateral damage

Blocking a domain used by an insurer partner would disrupt business; check with operations first. A lookalike domain and a partner's real new domain can look alike in certificate-transparency results. Blocking an insurer's domain would stop policy documents and premium notices reaching brokers. That is why Priya checks with operations, and with marketing for domains that resemble BIB's own, before asking IT to block. The check costs minutes; a wrong block costs a working day. Any domain that turns out to belong to a partner is noted, so the same question does not need asking next month.

### 7.6 Review

Blocks expire; process controls are reviewed annually. Expiry stops the block lists growing forever with stale indicators that cause false positives later. Each block in the register carries a review date, after which IT removes it unless Priya renews it with fresh evidence. Process controls such as call-back verification last longer, so an annual review with operations is enough to confirm they still fit the work. When a block expires without renewal, IT records its removal in the register so the history of each indicator stays complete.

### 7.7 Recording

The control register lists every change made because of intelligence. Each row records the change, the intelligence behind it, the owner, the verification and the review date. The register is what lets Priya show, in her portfolio, twelve control changes traced to intelligence over six months. It also supports expiry, since IT can see which blocks are due for removal without searching old tickets. Without the register, nobody could tell which settings came from intelligence and which came from ordinary IT administration, so reviews would stall.

### 7.8 Measuring effect

Count blocked connections, quarantined messages and prevented fraudulent payments reported by operations. These counts need care if they are to give an honest picture of the controls' effect. A blocked connection might be a staff member mistyping a domain, not an attack. A prevented fraudulent payment is the strongest measure, but it depends on operations reporting it, as with the two prevented attempts in her portfolio review. Priya reports each figure with its source so readers can judge its weight.

### 7.9 ATT&CK mitigations

Technique pages list mitigations that can inspire requests, adapted to BIB's tools. For Valid Accounts (T1078), the mitigation pages point to multi-factor authentication, which became the MFA request for brokers' remote email. Priya adapts each idea to what BIB actually runs and can afford. A mitigation that needs tools BIB lacks becomes a note for the managing director's quarterly half-page rather than a request to IT. Each request that came from a mitigation page cites that page, so reviewers can check the original guidance against what BIB changed.

### Staff awareness as a control

Awareness sessions using current, real-looking but synthetic examples help staff spot pretexts. Short monthly reminders beat a long annual course. Priya supplies the examples from intelligence; the help desk delivers them in team meetings. Reports of suspicious messages from staff are counted as a sign that awareness is working, and each report receives a thank-you reply.

### Worked example

Priya requests multi-factor authentication for brokers' remote email access, citing FSSG reports of credential phishing against three brokers. IT enables it for a pilot group. Verification: sign-in logs show the second factor requested for each pilot login. A month later, failed sign-ins from flagged addresses no longer succeed.

> **Synthetic case.** The pilot is invented.

### Errors and limits

A control's absence of alerts does not prove it works; test it.

### Exercises

- **EX031 — BEC controls.** Which controls best counter business email compromise? *Rubric:* 3 = verification call-backs, dual approval, awareness; 2 = two; 1 = firewall; 0 = none.
- **EX032 — Process verification.** How can a process control be verified? *Rubric:* 3 = confirm call-backs happened for actual changes; 2 = partial; 1 = assume; 0 = none.
- **EX033 — Partner domain.** Why check with operations before blocking a domain? *Rubric:* 3 = may be partner insurer; business disruption; 2 = partial; 1 = no need; 0 = none.
- **EX034 — MFA verification.** How was the MFA pilot verified? *Rubric:* 3 = sign-in logs show second factor per login; 2 = partial; 1 = vague; 0 = none.
- **EX035 — Register.** Why keep a register of intelligence-driven changes? *Rubric:* 3 = traceability, review, evidence of value; 2 = partial; 1 = no reason; 0 = none.

### Synthesis

Request controls with evidence, include process controls, verify technically and procedurally, avoid collateral damage and record changes.

### Continue studying — chapter 07 of 12

[← Chapter 06 (draft)](#ch-06) · [Course chapter index](../SUBJECTS.md) · [Chapter 08 (draft) →](#ch-08)

<a id="ch-08"></a>

## Chapter 8 — Threat intelligence and OSINT: supervised case analysis

### Learning outcomes

You will (1) analyse a realistic incident under supervision; (2) build a timeline; (3) map events to ATT&CK and kill-chain phases; (4) present findings with confidence and gaps.

### 8.1 The case

A broker receives an email apparently from an insurer announcing new bank details. Finance pays one premium to the new account before call-back verification catches a second request. Priya analyses the case with an external responder as supervisor. The case tests every routine from earlier chapters at once. One premium was paid before the fraud was noticed, so a client's money was at stake. The external responder supervises because Priya has not led a fraud analysis before, and because the findings may support reports to the bank and police. Her job in the case is the UTC timeline and the intelligence view, not the legal steps.

### 8.2 Timeline

Collect times from the email gateway, finance system and call-back log. Convert all to UTC. Order events: lookalike domain registered; email received; first payment; second request; call-back; fraud confirmed. Converting to UTC matters because systems record time differently, and one wrong offset could reverse the order of the payment and the call-back. Each event keeps a note of its source: the domain registration date from public records, the email from the gateway, the payment from finance and the call-back from its log. The sequence later shows registration four days before the email.

### 8.3 Mapping

Domain registration: Acquire Infrastructure (T1583) — preparation. Email: Phishing (T1566) as delivery of a pretext. No malware or account compromise is evident. Mapping only what the evidence shows keeps the report honest. There was no link or attachment to exploit, and no BIB account was used by the fraudster, so tagging T1078 or malware techniques would be wrong. The lack of technical techniques is itself a finding, because it explains why process controls, not technical tools, matter most for this threat.

### 8.4 Diamond view

Adversary: unknown fraud group. Capability: social-engineering pretext. Infrastructure: lookalike domain and a bank account. Victim: BIB finance team. The Diamond view still works when the adversary vertex can only say 'unknown fraud group'. Infrastructure is the most useful vertex for BIB, because the lookalike domain can be shared with FSSG and the receiving bank account can be reported. The victim vertex names a team, not a person, which keeps the analysis focused on the process that failed rather than the staff member involved.

### 8.5 Confidence and gaps

High confidence in the sequence; low confidence about whether the insurer's own mailbox was compromised. Ask the insurer through proper channels. Separating confidence by question, rather than giving one overall level, keeps the report precise. The sequence rests on BIB's own records, so confidence is high. Whether the insurer's mailbox was compromised depends on records BIB cannot see. Priya does not guess; the open question goes into the report as a gap and the request goes to the insurer through BIB's formal contacts.

### 8.6 Lessons

Call-back verification worked on the second request; it was not yet mandatory on the first. The call-back step introduced after the FSSG alert in Chapter 2 was still guidance rather than a rule, and the first request was paid without it. The second request was checked by a call-back to the insurer and stopped before payment. That contrast is the strongest evidence for Priya's recommendation to make call-back verification mandatory for every bank-detail change, which the operations manager can act on immediately.

### 8.7 Sharing

A GREEN item to FSSG with the lookalike domain and pretext, without client details. The FSSG item carries what other brokers can use: the lookalike insurer domain, the bank-detail pretext and the four days between registration and the email. It leaves out the client, the premium amount and the staff involved. Sharing at GREEN lets FSSG members check their own logs and warn their finance teams within the community. Priya's sharing item also passes the responder's review before release, since the same wording standards apply to community products.

### 8.8 Supervisor review

The responder checks Priya's timeline and wording before release. The responder reads the timeline against the source records and checks that each judgment matches its evidence. Wording gets particular attention: 'no evidence of BIB system compromise' is accurate, while 'BIB was not compromised' would claim more than the logs show. Priya records the responder's comments and the changes made before the report is released. Review by someone outside the case is especially valuable here, because the report may support reports to the bank and police.

### 8.9 Legal steps

Management reports the fraud to the bank and police; Priya provides the timeline. Priya supplies facts, not legal conclusions: the UTC timeline, the lookalike domain and the payment record from finance. Management decides what to report and when, with legal advice where needed. Her role description does not include contacting police, which is one of the actions listed as needing approval, so the reports go through management. Keeping the timeline in UTC with each source named makes it usable by the bank and police without further explanation from Priya.

### Kill chain view

On the kill chain, the case covers weaponization of a pretext, delivery by email and actions on objectives as payment. There is no exploitation or installation, which explains why technical tools saw nothing unusual.

### Worked example

Priya's timeline shows the lookalike domain was registered four days before the email. Her report: "Payment fraud using a lookalike insurer domain (high confidence on sequence). No evidence of BIB system compromise. Insurer mailbox compromise not excluded. Recommend mandatory call-back for all bank-detail changes and lookalike monitoring for insurer partners."

> **Synthetic case.** The fraud is invented.

### Errors and limits

Missing logs at partners limit conclusions; state them.

### Exercises

- **EX036 — Timeline order.** Order the case's events. *Rubric:* 3 = registration, email, payment, second request, call-back, confirmation; 2 = mostly; 1 = muddled; 0 = none.
- **EX037 — Technique map.** Map the registration and email to ATT&CK. *Rubric:* 3 = T1583; T1566; 2 = one; 1 = wrong; 0 = none.
- **EX038 — Diamond vertices.** Fill the Diamond vertices for the case. *Rubric:* 3 = all four correct; 2 = three; 1 = one; 0 = none.
- **EX039 — Open question.** What remained uncertain, and how should it be resolved? *Rubric:* 3 = insurer mailbox compromise; ask insurer through channels; 2 = one; 1 = vague; 0 = none.
- **EX040 — Recommendation.** What two recommendations followed? *Rubric:* 3 = mandatory call-back; lookalike monitoring for partners; 2 = one; 1 = vague; 0 = none.

### Synthesis

Build a UTC timeline, map to models, state confidence and gaps, share sanitised lessons and accept review.

### Continue studying — chapter 08 of 12

[← Chapter 07 (draft)](#ch-07) · [Course chapter index](../SUBJECTS.md) · [Chapter 09 (draft) →](#ch-09)

<a id="ch-09"></a>

## Chapter 9 — Communication, ethics and reporting

### Learning outcomes

You will (1) write reports for different audiences; (2) express uncertainty honestly; (3) handle ethical dilemmas in reporting; (4) apply handling labels to every product.

### 9.1 Bottom line first

Start with the judgment and the action. Detail follows for those who need it. Busy readers often stop after the first sentence, so it must carry the judgment and the action. Priya's fraud report opens with 'Payment fraud using a lookalike insurer domain' and the confidence, then the recommendation. The timeline and Diamond view follow for the responder and IT. A director who reads one line still knows what happened and what to fund. Priya checks every report against this rule before release by reading only its first sentence and asking whether it stands alone.

### 9.2 Audiences

Managing director: risk and decisions. Operations: process changes. IT: technical details. Staff: what to look for and how to report. The same fraud case produces four separate products, one for each audience at BIB. The managing director gets the risk and the call-back decision; operations gets the process change; IT gets the lookalike domain and the monitoring request; staff get a short note on spotting bank-detail pretexts and reporting them. Each product leaves out what its reader does not need, which keeps it short.

### 9.3 Uncertainty

Use the agreed probability words and a confidence level, and say what would change the judgment. ICD 203 standards — sourcing, uncertainty, alternatives, logic — make a good self-check. Saying what new evidence would change the judgment makes that judgment testable by its readers. For the insurer mailbox question, Priya writes that confidence would rise if the insurer confirmed a compromise or confirmed clean logs. The failed-login note does the same, naming the flagged addresses as what could shift the cause. Readers can then see the judgment's limits rather than guessing at them.

### 9.4 Labels

Every product carries a TLP label in the header. Staff awareness notes are usually CLEAR internally; FSSG-derived detail may be AMBER. A missing label is treated as a fault, because readers cannot tell whether they may forward the product. Staff notes are CLEAR inside BIB so the help desk can reuse them freely. Detail taken from FSSG keeps the label FSSG gave it; if FSSG marked an item AMBER, Priya's product carries AMBER too, even when most of its content is CLEAR.

### 9.5 Ethical dilemmas

Pressure to make a threat sound bigger to win budget; pressure to downplay an incident to avoid embarrassment. Both damage trust. Report what the evidence supports. The director's request to call the fraud 'a sophisticated cyber attack' is the first kind of pressure. Accepting it would steer the board toward technical tools when the evidence points to payment verification. Downplaying the incident would hide the premium already paid to the fraudsters from the board. Priya's answer in both cases is the same: describe what happened, with confidence and gaps, and let decisions follow.

### 9.6 Naming people

Reports name roles, not staff who clicked a link. Blame discourages reporting. The fraud report says 'the BIB finance team', not the name of the person who paid. Staff who fear being named in reports stop reporting suspicious messages, and those reports are one of the signals Priya counts to judge whether awareness is working. Roles also keep the focus on the process that needs fixing, such as the call-back step. The help desk's thank-you replies to people who report suspicious messages reinforce the same message from the other direction.

### 9.7 Clients

Client details stay out of intelligence products; the compliance officer manages client communications. Intelligence products travel to FSSG, the help desk and management, so client details there would spread personal data well beyond need. When a client forwards a suspicious email, the client's name stays in the restricted ticket and leaves the product. Whether the client should be told anything further is a compliance decision, because it involves regulatory and data-protection duties. Priya's brief-release check later catches staff email addresses automatically, but client details still rely on her own careful reading before release.

### 9.8 Length

One page for most products; appendices for detail. One page forces Priya to choose what matters and keeps the bottom line visible. The managing director can read it in under two minutes. Detail is not lost: the fraud timeline, the Diamond view and the source list sit in appendices, so the responder or IT can check the evidence without making the main page longer. Products that keep growing beyond one page are a signal that the audience or the question needs to be narrowed.

### 9.9 Review

A colleague reads each management report before release. A second reader catches what the writer no longer sees, such as an inflated adjective or a missing confidence level. For the fraud report, the external responder was that reader. For routine monthly summaries, the IT manager reads before release. The automated check introduced in Chapter 11 adds to this review but never replaces it. The reviewer's comments and the changes made are kept with the ticket, so the next review can see what was corrected.

### Report structure

A standard structure helps readers find things: label and date; bottom line; key judgments with likelihood and confidence; evidence summary; recommended actions with owners; gaps and next steps. Priya keeps a template so every report looks the same, which saves her time and lets the managing director read each one in under two minutes. When a report needs more detail, she adds an appendix rather than lengthening the main page, so the bottom line stays visible at the top.

### Worked example

After the fraud case, a director asks Priya to describe it as "a sophisticated cyber attack" in the board report. Priya explains the evidence shows a simple lookalike-domain pretext, and that accurate wording helps the board fund the right control — payment verification — rather than expensive technical tools.

> **Synthetic case.** The exchange is invented.

### Errors and limits

Plain words can oversimplify; keep detail available.

### Exercises

- **EX041 — Board wording.** Why did Priya resist "sophisticated cyber attack"? *Rubric:* 3 = inaccurate; misdirects investment; 2 = partial; 1 = agreed; 0 = none.
- **EX042 — Naming staff.** Why name roles rather than staff who clicked? *Rubric:* 3 = blame discourages reporting; 2 = partial; 1 = name them; 0 = none.
- **EX043 — Self-check standards.** Name three ICD 203-style checks for a report. *Rubric:* 3 = three valid; 2 = two; 1 = one; 0 = none.
- **EX044 — Audience fit.** What does the operations manager need from a report? *Rubric:* 3 = process change implications/actions; 2 = partial; 1 = indicators; 0 = none.
- **EX045 — Label placement.** Where must the TLP label appear in a product? *Rubric:* 3 = header (and email subject); every product; 2 = partial; 1 = optional; 0 = none.

### Synthesis

Lead with the bottom line, fit the audience, state uncertainty, label every product and resist pressure to distort.

### Continue studying — chapter 09 of 12

[← Chapter 08 (draft)](#ch-08) · [Course chapter index](../SUBJECTS.md) · [Chapter 10 (draft) →](#ch-10)

<a id="ch-10"></a>

## Chapter 10 — Threat intelligence and OSINT: quality and troubleshooting

### Learning outcomes

You will (1) measure the quality of CTI products; (2) detect and fix common faults; (3) collect consumer feedback; (4) improve continuously.

### 10.1 Quality dimensions

Relevance, timeliness, accuracy, clarity and actionability. Each can be checked: was the item about BIB systems? delivered before it mattered? confirmed or withdrawn later? understood? acted on? Each dimension gets a simple test from records Priya already keeps. Relevance comes from the ticket's requirement field; timeliness from arrival and action dates; accuracy from whether a judgment was later confirmed or withdrawn. Clarity shows in follow-up questions from readers, and actionability in whether a request was carried out. Together the five tests show at which point a particular product failed its reader.

### 10.2 Common faults

Stale indicators causing false blocks; missed items because email alerts went to spam; wrong labels; notes without clear actions. Each of these four faults has a typical cause in the way BIB works. Stale indicators come from blocks that were never expired; alerts in spam come from a mail filter treating FSSG's bulk messages as marketing. Wrong labels slip in when items are copied quickly, and notes without actions usually mean the analysis stopped at describing the threat rather than deciding what BIB should do.

### 10.3 Troubleshooting

Trace the item's path: received, triaged, analysed, sent, acted. Find where it stopped. The ticket fields recorded for every item make tracing a lost item possible. If an expected FSSG alert never reached triage, Priya checks whether it arrived and then looks in mail filter quarantine and spam folders. If it reached analysis but nobody acted, the request may have lacked an owner or deadline. Fixing the stage where it stopped prevents the same loss next time. The trace is recorded in the ticket, so the same break in the path can be checked first if it recurs.

### 10.4 Feedback

Quarterly two-question forms; quick chats with the help desk. "What helped? What was noise?" The help-desk chats are often more useful than the forms because they are quick and specific. Those conversations revealed that the Wednesday scam update arrived after Monday's peak of suspicious calls. 'What was noise?' matters as much as 'What helped?', because removing a useless product frees part of Priya's single day for work that someone actually uses. The answers go into the quarterly requirements review alongside the forms, together with the dates of the chats they came from.

### 10.5 Improvements

One change per month: shorter notes, earlier scam updates, new lookalike monitoring. Changing one thing at a time lets Priya see what each change did. Moving the scam update to Monday was one such change; calls needing escalation fell slightly over the next month. Had she also shortened notes in the same month, she could not tell which change helped. Each change and its result goes into the improvement log. Waiting a month between changes is slow, but with one working day a week it is the only way to see effects.

### 10.6 Accuracy tracking

Record judgments with probability words; later note what happened. Over time, see if "likely" events happened more often than "unlikely" ones. The record needs only the date, the judgment, the probability word and the later outcome. With a small team, the sample stays small, so Priya treats the comparison as a rough indicator. If events she called 'likely' happened no more often than 'unlikely' ones, she would revisit how she chooses words rather than abandon the scale. The scale itself is never adjusted quietly, because older judgments must stay comparable with the newer ones being tracked.

### 10.7 Source review

Each quarter, review sources: items received, used, withdrawn. The quarterly review compares each source's items received with those used and those later withdrawn or corrected. A source that sends many items but few useful ones costs reading time. A vendor blog graded C may move to B if its claims keep proving accurate. Changes to source grades are recorded so later scores can be understood. A source that is withdrawn often is downgraded, and the reason is noted for anyone reading older tickets that relied on it.

### 10.8 False positives

When a block is wrong, remove it quickly, apologise, find the cause, adjust rules. Speed limits the harm a wrong block does to brokers, partners and BIB's reputation. The false-positive block in her portfolio review was fixed within an hour. Apologising to affected users keeps their trust in future requests, and finding the cause, such as a stale indicator or a missing check with operations, leads to a change in rules rather than simply removing the block. The wrong block and its fix are also recorded in the control register beside the original request that caused it.

### 10.9 Documentation

Keep a short improvement log. Each entry records the date, the change, the reason and what happened afterwards. The move of the scam update from Wednesday to Monday is a typical entry in the log. The log goes into the portfolio in Chapter 12 and shows assessors that improvements came from evidence rather than habit. It also helps the IT manager understand why the routine looks the way it does. Entries are kept short, often two or three lines, so that writing them never competes with the weekly routine itself.

### Peer comparison

Twice a year Priya swaps an anonymised product with a peer at another FSSG member and each reviews the other's work against the same quality dimensions. The outside view catches habits she no longer notices, such as long sentences or vague actions, and gives her ideas from a team facing similar threats with different tools. The peer review is covered by FSSG's sharing agreement, and only TLP:GREEN or CLEAR material is exchanged.

### Worked example

The help desk says scam updates arrive on Wednesday, after Monday's peak of suspicious calls. Priya moves the update to Monday morning using the previous week's data. Calls needing escalation fall slightly over the next month; she records the change and result in her improvement log.

> **Synthetic case.** The change is invented.

### Errors and limits

Small teams have small samples; treat measures as indicators.

### Exercises

- **EX046 — Quality list.** Name five quality dimensions. *Rubric:* 3 = relevance, timeliness, accuracy, clarity, actionability; 2 = three; 1 = one; 0 = none.
- **EX047 — Spam fault.** How would Priya find that FSSG alerts were going to spam? *Rubric:* 3 = trace path; item received? check mail filters; 2 = partial; 1 = guess; 0 = none.
- **EX048 — Timing change.** Why move the scam update to Monday? *Rubric:* 3 = match call peak; 2 = partial; 1 = random; 0 = none.
- **EX049 — Calibration over time.** How can Priya check her probability words? *Rubric:* 3 = record judgments and outcomes; compare frequencies; 2 = partial; 1 = ask manager; 0 = none.
- **EX050 — Wrong block.** List the steps after a wrong block. *Rubric:* 3 = remove quickly, apologise, find cause, adjust; 2 = three; 1 = one; 0 = none.

### Synthesis

Measure quality, trace faults, gather feedback, make one improvement at a time and track accuracy.

### Continue studying — chapter 10 of 12

[← Chapter 09 (draft)](#ch-09) · [Course chapter index](../SUBJECTS.md) · [Chapter 11 (draft) →](#ch-11)

<a id="ch-11"></a>

## Chapter 11 — Supervised laboratory

### Learning outcomes

You will (1) run an automated pre-release check on a brief; (2) fix failures before release; (3) explain each check's purpose; (4) extend checks responsibly.

### 11.1 Lab rules

Offline, synthetic, standard library. The supervisor reviews outputs and the corrected brief. Offline and synthetic means the lab cannot leak anything real: the brief, the staff address and the domains are invented for teaching. Using only the standard library keeps the script runnable on a locked-down work machine. The supervisor's review covers both the first failing output and the corrected brief, so learners show the fix rather than just describing it. The same rules apply to any extension a learner adds, including new test cases, which must also use invented content only.

### Lab — brief release check

```python
"""Lab (ch 11): assemble a one-page brief and refuse to release it if checks fail (synthetic)."""
brief = {"tlp": "TLP:GREEN", "bluf": "Phishing against broker portals is likely to continue this month.",
         "confidence": "moderate", "actions": ["Block 3 sender domains", "Remind staff about portal logins"],
         "text": "Sample sent to j.smith@bramwell.example was reported."}
checks = [("label valid", brief["tlp"] in {"TLP:CLEAR", "TLP:GREEN", "TLP:AMBER", "TLP:AMBER+STRICT", "TLP:RED"}),
          ("bottom line first", bool(brief["bluf"])),
          ("confidence stated", brief["confidence"] in {"low", "moderate", "high"}),
          ("actions listed", len(brief["actions"]) > 0),
          ("no staff email", "@bramwell.example" not in brief["text"])]
for name, ok in checks:
    print(f"{name}: {'pass' if ok else 'FAIL'}")
print("release" if all(ok for _, ok in checks) else "HOLD: fix failures before release")
```

Run with `python3 lab_brief.py`. Verified output:

```text
label valid: pass
bottom line first: pass
confidence stated: pass
actions listed: pass
no staff email: FAIL
HOLD: fix failures before release
```

### 11.2 Reading the result

The brief has a valid TLP:GREEN label, a bottom line first, a confidence level and listed actions. It fails one check: the text contains a staff email address at bramwell.example. The script holds the release until the failure is fixed. The output shows four passes before the failure, so the problem is specific and easy to find. The failing line names the check, not the address, which keeps the output itself safe to paste into a ticket. Because the final line reads 'HOLD: fix failures before release', nobody can mistake a partly passing brief for one ready to send.

### 11.3 Fixing

Replace "j.smith@bramwell.example" with "a staff member". Rerun: all checks pass and the script prints "release". Rerunning the script after the fix matters as much as the edit itself. A replacement could introduce a new problem or miss a second address, and only a second run shows that all five checks pass. Priya saves both outputs, the failing run and the passing run, in the ticket. That record is what the supervisor reads before signing off the corrected brief.

### 11.4 Why each check

Label: wrong or missing labels cause leaks. Bottom line: busy readers act on the first sentence. Confidence: readers need to know how sure we are. Actions: intelligence without action is news. Staff email: personal data does not belong in a GREEN community product. Each check guards against a failure that already appears in the book. A wrong label could send FSSG detail beyond its audience. A missing bottom line wastes the reader's first sentence; a missing confidence hides uncertainty; an empty action list produces news rather than intelligence. The staff address would breach the sanitising rule for anything shared at GREEN.

### 11.5 Limits of checks

The script finds email addresses only for BIB's domain; it misses names and client addresses. A human read remains mandatory. The staff-email check tests only for '@bramwell.example' in the text. A name such as 'Jo Smith' written without an address, a client's postal address or a staff member's personal email at another domain would all pass. That is why the supervisor and Priya still read every brief, and the script output is evidence of a check, not proof of safety.

### 11.6 Extending

Students may add a check for phone numbers, or for probability words outside the agreed scale. Each new check gets a test case. A test case is two short pieces of text: one that should fail and one that should pass. For phone numbers, 'call 01632 960123' should fail and 'call the help desk' should pass. Priya's own extension flags any probability word outside BIB's scale, tested with 'probable' failing and 'likely' passing, as shown in the worked example. Without a failing test, a broken check could pass every brief and nobody would notice the gap in the release process.

### 11.7 Holding is safe

The script holds rather than releases when anything fails — a fail-closed design. Failing closed means a mistake in the brief or the script leads to a delay, not a leak. If the TLP field were missing, the brief would be held rather than sent unlabelled. The cost is that a correct brief may occasionally wait for a fix, which is acceptable for products going to FSSG or management. Priya treats a HOLD as a normal outcome of the check, not as a failure of her work.

### 11.8 Lab report

Record the first run, the fix, the second run and one proposed extension with its test case. The report shows the whole cycle in order: what failed first, what was changed, what passed second, and how the check could grow. Including a test case for the extension proves it works rather than only describing it. Learners also note any limit they found, such as names without email addresses passing the staff-email check. Dates and times of both runs are recorded, so the order of failure, fix and success can be shown to the supervisor.

### 11.9 Supervisor sign-off

The supervisor signs only after reading the corrected brief. Signing only after reading means the supervisor's signature confirms the brief, not just the script's output. A passing run does not prove the text is safe, as the limits of the checks show. The signature goes into the lab record alongside both runs, so an assessor can see who approved the brief and when. If the supervisor finds a problem the script missed, Priya fixes it, reruns the check and asks for a fresh signature.

### Running in practice

After the lab, Priya runs the check on every real brief before release, on her work machine, with the output saved to the ticket.

### Worked example

Priya extends the check to flag any probability word not on BIB's scale. Her test brief uses "probable" and the check fails as intended; she rewrites it as "likely" and the brief passes.

> **Synthetic case.** The brief and extension are invented teaching material.

### Errors and limits

Automated checks catch patterns, not meaning.

### Exercises

- **EX051 — Lab failure.** Which check failed and why? *Rubric:* 3 = no staff email; address in text; 2 = check only; 1 = label; 0 = none.
- **EX052 — Fix and rerun.** How is the failure fixed and confirmed? *Rubric:* 3 = replace with role; rerun shows release; 2 = one; 1 = ignore; 0 = none.
- **EX053 — Check purposes.** Explain why the confidence check exists. *Rubric:* 3 = readers need to know certainty; 2 = partial; 1 = decoration; 0 = none.
- **EX054 — Missed by script.** Name something the script would miss. *Rubric:* 3 = names, client addresses, other domains; 2 = one correct item without the other two; 1 = vague; 0 = none.
- **EX055 — New check.** Propose a new check with a test case. *Rubric:* 3 = check + failing test + passing test; 2 = check + one test; 1 = check only; 0 = none.

### Synthesis

Automate simple pre-release checks, hold on failure, fix and rerun, and keep a human read for what scripts miss.

### Continue studying — chapter 11 of 12

[← Chapter 10 (draft)](#ch-10) · [Course chapter index](../SUBJECTS.md) · [Chapter 12 (draft) →](#ch-12)

<a id="ch-12"></a>

## Chapter 12 — Practice portfolio and final review

### Learning outcomes

You will (1) assemble a CTI practice portfolio; (2) reflect on growth and gaps; (3) plan the next six months of the role; (4) hand over or sustain the routine.

### 12.1 Portfolio contents

Requirements list; weekly routine and ticket samples (sanitised); triage scoring with a review; the fraud case report; a control request with verification; a management report; the improvement log; the lab outputs. Each portfolio item shows one routine that Priya built during the six months. The requirements list shows direction; ticket samples show tracking; the scoring review shows triage judged against outcomes. The fraud case report, the MFA request with its sign-in log verification and a management report show analysis and communication. The improvement log and lab outputs show how she checked and refined her own work.

### 12.2 Sanitising

All portfolio items use synthetic or sanitised content. FSSG material appears only as GREEN summaries or not at all. Staff and clients are never named. Sanitising the portfolio follows the same rules Priya applies to live intelligence work. Ticket samples keep fields and decisions but replace client and staff details with roles. The fraud case keeps the lookalike pattern and timeline shape but not the client or premium. Anything FSSG marked above GREEN is either summarised at GREEN or left out, since the portfolio goes to assessors outside BIB.

### 12.3 Reflection

What changed at BIB because of CTI? Call-back verification, MFA for remote email, lookalike monitoring. What remains weak? Partner mailbox compromise, limited log retention. Each of these three changes has a dated record behind it at BIB. Call-back verification appears in the operations process and the register, MFA in the pilot's sign-in logs, and lookalike monitoring in the certificate-transparency checks. The two remaining weaknesses are just as concrete and just as well documented. Partner mailbox compromise remained an open question in the fraud case, and limited log retention restricts how far back any investigation can look.

### 12.4 Next six months

Extend lookalike monitoring to insurer partners; formalise FSSG feedback; train the IT manager as backup; review requirements with the new operations manager. Each item answers a weakness or risk named during the six months. Monitoring partner domains answers the open question from the fraud case. Formal FSSG feedback builds on the monthly notes she already sends to the community. Training the IT manager reduces dependence on one person, and a new operations manager means the requirements written in Chapter 2 need checking against new priorities.

### 12.5 Sustaining

Document the routine, keep templates, schedule reviews and keep the manager's support by showing outcomes. Documentation is what lets the routine survive Priya's absence or departure. The checklist, ticket fields, scoring rule and report template are kept where the IT manager can find them. Scheduled reviews keep the requirements list and the scoring weights current as BIB changes. Showing outcomes, such as the two prevented fraud attempts, is how she keeps her one day a week allocated. Templates for the ticket, the control request and the report carry the agreed fields, so nobody has to remember them from scratch.

### 12.6 Assessment

The portfolio is assessed on safety, accuracy, usefulness and reflection, using the course rubric. Safety means nothing in the portfolio breaks TLP, data-protection or OSINT boundaries. Accuracy means the figures and judgments match their evidence, including lab outputs. Usefulness means each item led to a decision or action at BIB, and reflection means Priya names what did not work, such as the false-positive block, alongside what did. Assessors may ask to see routine ticket samples as well as the selected highlights, so both must be ready.

### 12.7 Continuing learning

Follow ATT&CK and TLP updates, attend FSSG meetings, read sector advisories and consider the technical or postgraduate courses. ATT&CK technique pages and the TLP definitions change over time, so tags and labels need checking against current versions. FSSG meetings keep Priya in contact with peers facing the same fraud methods. The technical course deepens log analysis and detection, while the postgraduate course suits someone moving toward running a CTI programme rather than one part-time role. Each new source or course is still tested against BIB's requirements before it takes any of Priya's limited weekly time.

### 12.8 Mentoring

Explaining the routine to a colleague confirms that it is documented well enough to survive absence. Teaching the IT manager tests the documentation as a real reader would. If he cannot follow the handover note or the scoring rule without asking, the gap is in the document, not in him. Each question he asks becomes an edit to the checklist, so the routine is clearer before Priya next takes leave. The IT manager's own monthly grading with Priya gives him practice before he covers the full routine alone.

### 12.9 Celebrate

Note concrete wins: a prevented payment, a blocked lookalike, an avoided outage. Concrete wins are what management remembers when budgets are set. The two prevented fraud attempts reported by operations and the blocked lookalike domain are examples Priya can point to in her portfolio. Recording them at the time, with dates and sources, keeps the claims accurate. It also stops the year's successes being forgotten in favour of recent problems. The one false-positive block, fixed within an hour, belongs in the same record, because honest reporting makes the wins credible.

### Feedback from consumers

Before the final review, Priya asks each consumer for one sentence on what CTI changed for them. The operations manager cites call-back verification; the help desk cites Monday scam updates. These quotes, kept anonymous, strengthen the portfolio's evidence.

### Worked example

Priya's portfolio review shows twelve control changes traced to intelligence in six months, two prevented fraud attempts reported by operations and one false-positive block, fixed within an hour. Her plan names the IT manager as trained backup and schedules a requirements review in January.

> **Synthetic case.** The figures are invented.

### Errors and limits

Portfolios show selected work; assessors may ask to see routine samples.

### Exercises

- **EX056 — Portfolio list.** List six portfolio items. *Rubric:* 3 = six valid; 2 = four; 1 = two; 0 = none.
- **EX057 — Sanitising rule.** How should FSSG material appear in the portfolio? *Rubric:* 3 = only GREEN summaries or not at all; no names; 2 = partial; 1 = full; 0 = none.
- **EX058 — Remaining weakness.** Name two remaining weaknesses at BIB. *Rubric:* 3 = partner mailbox compromise; log retention; 2 = one; 1 = vague; 0 = none.
- **EX059 — Six-month plan.** Give three items for the next six months. *Rubric:* 3 = three valid; 2 = two; 1 = one; 0 = none.
- **EX060 — Concrete wins.** Why record concrete wins? *Rubric:* 3 = show value, keep support/budget; 2 = partial; 1 = vanity; 0 = none.

### Synthesis

Assemble a sanitised portfolio, reflect honestly, plan ahead, build backup and show concrete value.

### Continue studying — chapter 12 of 12

[← Chapter 11 (draft)](#ch-11) · [Course chapter index](../SUBJECTS.md) · [Worked results ↓](#worked-results) · [Next course via chapter index →](../SUBJECTS.md)

<a id="worked-results"></a>

## Worked results

Model answers for EX001–EX060. Bramwell Insurance Brokers, Priya Nair, the Financial Services Sharing Group and every figure are synthetic. Lab answers quote verified outputs. Any answer meeting the rubric scores equally.

**EX001.** Risk is the likelihood of harm combined with its impact; CTI improves the likelihood estimate by showing which threats are active and relevant.

**EX002.** Monday direction and collection from FSSG; Tuesday processing and log matching; Wednesday analysis and dissemination to the help desk; monthly feedback and summary to the manager.

**EX003.** Reverse-engineering malware and attributing attacks to named groups.

**EX004.** Business email compromise, credential phishing against the client portal and ransomware.

**EX005.** ATT&CK catalogues techniques; the kill chain orders intrusion phases; the Diamond Model describes an event by adversary, capability, infrastructure and victim.

**EX006.** The managing director sets budgets; the operations manager sets payment processes; the IT team configures controls.

**EX007.** "Each month, for the compliance officer, are any BIB staff credentials or client records being offered or published on public sites?"

**EX008.** Introducing call-back verification before acting on any change to bank details.

**EX009.** Active exploitation of a system BIB runs, or a fraud method that targets BIB by name.

**EX010.** It is outside CTI's requirements and would intrude on the client's privacy without lawful purpose.

**EX011.** Contacting police, requesting takedowns, notifying regulators and engaging with suspected criminals (also buying intelligence services).

**EX012.** Save the original message file, record who reported it and when, compute its hash, and analyse only a copy.

**EX013.** Only people inside BIB who need to know.

**EX014.** The compliance officer, because notification duties to clients involve regulation and data-protection law.

**EX015.** They breach platform terms and possibly law, are deceptive, and expose BIB to legal and reputational harm.

**EX016.** C — fairly reliable — until its track record can be checked; it can move up or down later.

**EX017.** A portal update or password-policy change that locked many legitimate clients out.

**EX018.** 55–80%.

**EX019.** The evidence supported the update as the main cause, but some attempts came from flagged addresses, so ignoring the attack possibility would be unsafe.

**EX020.** What happened; what it means for BIB with likelihood and confidence; and what action is needed by whom.

**EX021.** Q3 (8) and Q1 (7) go to analysis; Q4 (5) is checked; Q5 and Q2 (4 each) are logged only.

**EX022.** Ask FSSG or a contracted provider whether any sample contains BIB data, rather than visiting the forum herself.

**EX023.** A planned CRM upgrade next week that would remove the vulnerable version anyway.

**EX024.** The domain might be a legitimate new marketing site registered by BIB staff or an agency.

**EX025.** A written record of the change, the reason and a later check that it improved results.

**EX026.** Arrival date, source, TLP label, grade, score and decision (also actions and closure date).

**EX027.** Active exploitation of a system BIB runs, or a fraud method that names BIB.

**EX028.** When the action is complete and verified, or when a reasoned decision not to act is recorded.

**EX029.** Drop the lowest-scored items first and tell her manager about the overflow.

**EX030.** She phoned the IT manager, opened a priority ticket, informed her manager; the fix was applied that evening, she verified the version next morning and closed the ticket with evidence.

**EX031.** Call-back verification for bank-detail changes, dual approval for payments and staff awareness of pretexts.

**EX032.** Ask operations to show that call-backs were made for each bank-detail change during the period.

**EX033.** The domain could belong to an insurer partner, and blocking it would disrupt business.

**EX034.** Sign-in logs showed the second factor being requested for every pilot user's login.

**EX035.** It shows which changes came from intelligence, supports reviews and expiry, and evidences the programme's value.

**EX036.** Lookalike domain registered; email received; first payment made; second request received; call-back performed; fraud confirmed.

**EX037.** Registering the lookalike domain is Acquire Infrastructure (T1583); the email is Phishing (T1566) delivering the pretext.

**EX038.** Adversary: unknown fraud group. Capability: bank-detail-change pretext. Infrastructure: lookalike domain and receiving bank account. Victim: BIB finance team.

**EX039.** Whether the insurer's own mailbox was compromised; BIB should ask the insurer through its formal contacts.

**EX040.** Make call-back verification mandatory for every bank-detail change, and monitor for lookalike domains of insurer partners.

**EX041.** It was inaccurate — a simple lookalike pretext — and would push the board toward technical spending instead of payment verification.

**EX042.** Blaming individuals makes staff hide mistakes and stop reporting suspicious messages.

**EX043.** Describe source quality, express uncertainty with confidence, and consider alternative explanations.

**EX044.** What process change is recommended, why, and what it costs the team in effort.

**EX045.** In the header of every product, and in the subject line when sent by email.

**EX046.** Relevance, timeliness, accuracy, clarity and actionability.

**EX047.** By tracing an expected item: if it never reached triage, check whether it arrived and inspect mail filter quarantine and spam folders.

**EX048.** Suspicious calls peak on Monday, so an update on Wednesday arrived after it was most needed.

**EX049.** Log each judgment's probability word and later outcome, then compare how often each word's events actually happened.

**EX050.** Remove the block quickly, apologise to affected users, find why it happened and adjust the rule or source.

**EX051.** "No staff email" failed because the text contained j.smith@bramwell.example.

**EX052.** Replace the address with a role such as "a staff member", then rerun; all checks pass and the script prints "release".

**EX053.** Readers must know how certain the judgment is to decide how strongly to act on it.

**EX054.** Personal names without email addresses, client addresses or email addresses at other domains.

**EX055.** Check: phone numbers absent. Failing test: "call 01632 960123". Passing test: "call the help desk".

**EX056.** Requirements list, sanitised ticket samples, triage scoring review, fraud case report, control request with verification and management report.

**EX057.** Only as TLP:GREEN summaries, or left out, with no staff or client names.

**EX058.** Possible compromise of partner insurers' mailboxes, and short log retention limiting investigations.

**EX059.** Extend lookalike monitoring to insurer partners, train the IT manager as backup and review requirements with the new operations manager.

**EX060.** Concrete outcomes show leadership the role's value and keep support and time allocated to it.

<a id="references"></a>

## References

Links checked 12 October 2026; re-verify editions before citing.

- Bianco, D. (2013). The Pyramid of Pain. <https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html>
- Caltagirone, S., Pendergast, A. and Betz, C. (2013). The Diamond Model of Intrusion Analysis. Technical Report ADA586960, Center for Cyber Intelligence Analysis and Threat Research. <https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf>
- European Union. Regulation (EU) 2016/679 (General Data Protection Regulation). <https://eur-lex.europa.eu/eli/reg/2016/679/oj>
- FIRST. Traffic Light Protocol (TLP) version 2.0. <https://www.first.org/tlp/>
- Heuer, R. J. (1999). Psychology of Intelligence Analysis. CIA Center for the Study of Intelligence. <https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/>
- Hutchins, E. M., Cloppert, M. J. and Amin, R. M. (2011). Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains. Lockheed Martin. <https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Intel-Driven-Defense.pdf>
- Kent, S. (1964). Words of Estimative Probability. CIA Studies in Intelligence. <https://www.cia.gov/resources/csi/static/Words-of-Estimative-Probability.pdf>
- MITRE ATT&CK Enterprise matrix, groups, software and technique pages. <https://attack.mitre.org/>
- NIST SP 800-150 (2016). Guide to Cyber Threat Information Sharing. <https://doi.org/10.6028/NIST.SP.800-150>
- NIST SP 800-61 Rev. 3 (2025). Incident Response Recommendations and Considerations for Cybersecurity Risk Management. <https://doi.org/10.6028/NIST.SP.800-61r3>
- OASIS. STIX Version 2.1 (Committee Specification / OASIS Standard). <https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html>
- OASIS. TAXII Version 2.1. <https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html>
- ODNI. Intelligence Community Directive 203: Analytic Standards (2015, amended 2022). <https://www.odni.gov/files/documents/ICD/ICD-203.pdf>
