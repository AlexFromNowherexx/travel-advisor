# Product Specification — Bac Bling AI Agent MVP

| Field | Value |
|---|---|
| Version | 0.3.0 |
| Status | Final draft for team review |
| Owner | TBD |
| Hackathon | TBD |
| Last updated | 2026-06-27 |

---

## Table of Contents

- [1. Summary](#1-summary)
- [2. Problem Statement](#2-problem-statement)
- [3. Goals](#3-goals)
- [4. Non-goals / Out of Scope for MVP](#4-non-goals--out-of-scope-for-mvp)
- [5. Target Users & Stakeholders](#5-target-users--stakeholders)
- [6. Key Use Cases](#6-key-use-cases)
- [7. User Stories](#7-user-stories)
- [8. Product Scope — MVP](#8-product-scope--mvp)
- [9. Functional Requirements](#9-functional-requirements)
- [10. Non-functional Requirements](#10-non-functional-requirements)
- [11. Data Sources & Knowledge Strategy](#11-data-sources--knowledge-strategy)
- [12. Output Formats](#12-output-formats)
- [13. Suggested Technical Architecture](#13-suggested-technical-architecture)
- [14. API Contract Draft](#14-api-contract-draft)
- [15. Environment Variables](#15-environment-variables)
- [16. MVP Success Criteria](#16-mvp-success-criteria)
- [17. Manual Test Plan](#17-manual-test-plan)
- [18. Risks & Mitigations](#18-risks--mitigations)
- [19. Assumptions](#19-assumptions)
- [20. Open Questions for Review](#20-open-questions-for-review)
- [21. Future / Later Releases](#21-future--later-releases)
- [22. Appendix](#22-appendix)
- [Final Self-Check](#final-self-check)

---

## 1. Summary

**Bac Bling AI Agent** is a source-controlled AI system for exploring Bac Ninh through tourism, check-in recommendations, and historical-cultural storytelling. The MVP helps users turn scattered local data into structured itineraries, destination suggestions, and narrative explanations that connect Bac Ninh's early historical layers, feudal periods, modern geopolitical position, industrialization, and cultural identity.

The product is designed for a hackathon MVP and uses exactly four agents:

1. **Orchestrator Agent**
2. **Search Agent**
3. **Cultural-Historical Agent**
4. **Tourism Agent**

The core value is not only generating travel suggestions, but also showing which facts are source-supported, which claims require verification, and where evidence is insufficient. This reduces the risk of AI hallucinating local history while still making Bac Ninh easier to explore and explain.

---

## 2. Problem Statement

- Data about Bac Ninh is scattered across many sources, including gazetteers, local history books, materials about Quan ho folk singing, craft villages, historical sites, festivals, official provincial portals, museum materials, news articles, and team-provided documents.
- Existing tour and check-in suggestions often list destinations without explaining the deeper historical and cultural context behind them.
- Visitors may not know how to connect famous places, local food, craft villages, and historical sites into a meaningful route.
- Hackathon reviewers need to see a product that is feasible, source-aware, and clearly scoped.
- Generative AI can produce convincing but inaccurate statements if factual claims are not grounded in sources.
- Sensitive historical claims, such as whether Bac Ninh was once an ancient capital during the Hai Ba Trung period, must not be presented as fact unless reliable sources are available.

---

## 3. Goals

- Build a clear MVP using exactly four agents: Search, Orchestrator, Cultural-Historical, and Tourism.
- Retrieve, summarize, and classify Bac Ninh-related sources by reliability.
- Generate source-aware historical-cultural narratives about Bac Ninh.
- Generate tourism itineraries and check-in recommendations with cultural context.
- Provide confidence labels, source notes, and verification warnings for important claims.
- Support reviewer-friendly output that makes the system's reasoning flow easy to inspect.
- Prepare a focused hackathon demo that runs end-to-end from user input to structured response.

---

## 4. Non-goals / Out of Scope for MVP

- The MVP does not provide tour booking, payment, ticketing, or e-commerce features.
- The MVP does not provide a production-grade CMS.
- The MVP does not provide a native mobile application.
- The MVP does not replace historians, cultural experts, or local advisors.
- The MVP does not assert historical claims without verifiable sources.
- The MVP does not guarantee fully real-time operational data, such as current weather, same-day opening hours, live ticket prices, or live event changes.
- The MVP does not confirm that an industrial-zone route is officially available unless there is evidence from an official source or verified partner.
- The MVP does not treat AI-generated text as a source of truth.

---

## 5. Target Users & Stakeholders

This section separates people and groups from technical agents. Users and stakeholders are human or organizational groups. Agents are system components and are described separately in the architecture section.

### 5.1 Target Users

| Target User | Main Need | Pain Point | Value Provided by Bac Bling AI Agent |
|---|---|---|---|
| Visitors exploring Bac Ninh | Receive route, destination, and check-in suggestions | They may only know famous places and miss deeper context | Provides structured itineraries with stories, source notes, and practical warnings |
| Culture-oriented travelers | Understand why a place matters historically or culturally | Historical information is often scattered or too difficult to use | Turns sourced material into accessible historical-cultural explanations |
| Local tour planners | Build routes around themes such as Quan ho, craft villages, historical sites, and cuisine | Hard to connect destinations into a coherent route | Suggests themed itineraries with suitable audiences, route logic, and verification notes |
| Internal demo users | Test product flows during the hackathon | Need stable, repeatable output for judging | Provides consistent output types, agent trace, source notes, and warnings |
| Students or learning groups | Learn local history through routes and places | Textbook-style history may feel disconnected from real locations | Connects places, periods, and cultural practices into a route-based learning experience |

### 5.2 Stakeholders

| Stakeholder | Main Need | Pain Point | Value Provided by Bac Bling AI Agent |
|---|---|---|---|
| Hackathon team | Build and present a feasible MVP | Scope can become too broad and unclear | Keeps the product focused around four agents and source-aware tourism exploration |
| Mentors and reviewers | Evaluate product clarity, feasibility, and reliability | AI demos can look impressive while hiding weak evidence | Shows sources, confidence levels, assumptions, and agent trace |
| Cultural or tourism advisors | Review sensitive historical-cultural claims | They need to know what the system is asserting | Highlights claims that are supported, uncertain, or insufficiently evidenced |
| Potential local tourism or cultural units | Assess whether the product can support local exploration | Local data is fragmented and difficult to convert into usable routes | Provides a structured source and itinerary layer that can be reviewed before use |
| Technical team | Implement the system within hackathon constraints | Complex architectures can slow down delivery | Provides a modular design that can be implemented as logical agents in one backend |

---

## 6. Key Use Cases

### UC-1: Create a 1-day Bac Ninh tour themed around Quan ho and craft villages

**Sample input:**

```text
Create a 1-day Bac Ninh tour themed around Quan ho folk singing and craft villages. Include check-in spots, local food, and cultural stories.
```

**Expected output:**

A morning — noon — afternoon — evening itinerary with at least 3 destinations or activities, suggested experiences, local food, cultural context, source notes, and warnings for information requiring verification.

**Acceptance criteria:**

- The tour has a clear name and theme.
- The itinerary includes at least 3 destinations or activities.
- The output includes at least 2 historical or cultural explanations.
- Important claims have source notes or a `Needs verification` label.
- The system does not present unsupported historical information as fact.

### UC-2: Suggest check-in spots with historical or cultural stories

**Sample input:**

```text
Suggest 5 check-in spots in Bac Ninh. Each spot must include a short historical or cultural story.
```

**Expected output:**

A structured list or table with destinations, reasons to visit, storytelling angle, photo or activity idea, suitable time, confidence level, and source notes.

**Acceptance criteria:**

- The output includes 5 check-in spots.
- Each spot has at least 1 storytelling angle.
- Each spot has a confidence label: `High`, `Medium`, or `Low`.
- Unsourced stories are labeled as requiring verification.
- The output includes source notes or a statement that evidence is insufficient.

### UC-3: Create a historical-cultural-modernization narrative

**Sample input:**

```text
Create a narrative from early Bac Ninh, through feudal periods, to modern industrial Bac Ninh.
```

**Expected output:**

A timeline-based narrative with stages, key themes, transition points, links to tourism routes, source status, and a list of sensitive claims requiring verification.

**Acceptance criteria:**

- The structure follows a timeline.
- The timeline includes early, feudal, and modern/industrial layers when evidence is available.
- Sensitive claims are labeled with source status.
- The output separates sourced claims from claims requiring verification.
- The narrative can be reused as a conceptual route for tours or check-in recommendations.

### UC-4: Find reliable sources for a historical site, craft village, or festival

**Sample input:**

```text
Find reliable sources for information about a historical site, craft village, or festival in Bac Ninh.
```

**Expected output:**

A source table with source title, source type, link or document title, trust level, usable facts, limitations, and claims that require additional verification.

**Acceptance criteria:**

- Official or primary sources are prioritized when available.
- Each source has a trust level.
- Each source includes a usage rule.
- If fewer than 3 reliable sources are available, the system clearly states the limitation.
- The system does not invent sources.

### UC-5: Create an itinerary combining historical sites, cuisine, and craft villages

**Sample input:**

```text
Create a half-day itinerary in Bac Ninh combining historical sites, local food, and craft villages.
```

**Expected output:**

A half-day route with suitable visitor groups, destinations, route logic, food or local specialty suggestions, source notes, and practical warnings.

**Acceptance criteria:**

- The route includes at least 2 destinations.
- The route includes at least 1 food or local specialty suggestion.
- The route explains why the destinations fit together.
- Operating details are not asserted without updated sources.
- The output includes source notes and verification warnings where needed.

### UC-6: Create a source summary for reviewers

**Sample input:**

```text
Summarize the sources currently used for the Bac Bling demo and evaluate their reliability.
```

**Expected output:**

A source summary grouped by official/primary sources, reliable secondary sources, team-provided sources, and unverified sources, with trust levels and usage rules.

**Acceptance criteria:**

- The summary includes at least 4 source groups.
- Each group has a trust level and usage rule.
- The output identifies which sources should not be used for strong historical claims.
- The output is easy for reviewers to inspect.

### UC-7: Suggest an industrial-zone tour direction with verification warnings

**Sample input:**

```text
Suggest a Bac Ninh route that connects cultural identity with modern industrial development.
```

**Expected output:**

A route direction that may mention industrial-zone context only as a research-backed or verification-needed direction. The output must clearly state whether official access, route availability, and partners are confirmed or not confirmed.

**Acceptance criteria:**

- The output does not claim that an official industrial-zone tour exists unless verified.
- Any industrial-zone element has a `Needs partner/source verification` label if evidence is missing.
- The route still includes cultural or historical context.
- The output includes practical warnings about access and permission.

### UC-8: Create a tour without historical elements when requested

**Sample input:**

```text
Create a 1-day Bac Ninh tour, but do not include historical explanations.
```

**Expected output:**

A practical itinerary focused on destinations, check-in experiences, food, and route logic without adding historical narrative beyond basic factual labels.

**Acceptance criteria:**

- The system respects the user's request and does not add historical explanations.
- Factual destination information still includes source notes or verification warnings.
- The route remains structured and useful.
- The output states the assumption that historical context has been intentionally minimized.

---

## 7. User Stories

| ID | User Story | Acceptance Criteria |
|---|---|---|
| US-1 | As a visitor, I want a 1-day Bac Ninh tour based on my interests so I can plan my visit easily. | The system returns a morning/noon/afternoon/evening itinerary with at least 3 destinations or activities. |
| US-2 | As a culture-oriented traveler, I want each destination to include a short explanation so I understand why it matters. | Each key destination includes a source-aware historical or cultural note unless the user asks to remove historical context. |
| US-3 | As a reviewer, I want to see source evidence so I can judge whether the system is reliable. | The output includes sources, trust levels, and verification warnings for important claims. |
| US-4 | As a user, I want to know which claims are verified and which need verification. | Important claims are labeled as `Source-supported`, `Needs verification`, or `Insufficient evidence`. |
| US-5 | As a tour planner, I want route suggestions connected to a historical-cultural-modernization flow. | The system returns a route or narrative that connects early, feudal, and modern layers when evidence is available. |
| US-6 | As a demo coordinator, I want a clear agent trace so I can explain how the system works. | The UI or response shows high-level steps: intent classification, source retrieval, historical-cultural analysis, tourism generation, and fact check. |
| US-7 | As a technical team member, I want stable output types so the frontend can display results consistently. | The backend returns a consistent JSON schema with `reply`, `output_type`, `sources`, `warnings`, `confidence`, and `conversation_id`. |
| US-8 | As a reviewer, I want to inspect a source summary independently from the itinerary. | The system can return a source summary table grouped by source type and trust level. |
| US-9 | As a user, I want check-in suggestions with confidence labels. | Each check-in recommendation includes a confidence label and source status. |
| US-10 | As a mentor, I want the MVP scope to be clearly limited. | The specification clearly states what the MVP includes, excludes, and prioritizes for the hackathon. |

---

## 8. Product Scope — MVP

The MVP includes only three product modules:

1. **User Interface**
2. **Multi-Agent Architecture**
3. **Source & Fact-check Layer**

### 8.1 User Interface

The MVP should have a simple interface optimized for a clear hackathon demo. It can be implemented with Streamlit or a lightweight web interface.

UI requirements:

- Allow users to enter requests in text.
- Provide a dropdown or radio control for `output_type`:
  - `tour_itinerary`
  - `checkin_recommendation`
  - `historical_narrative`
  - `source_summary`
  - `general_qa`
- Provide a `source_mode` option:
  - `strict`: only use source-supported claims or label them as needing verification.
  - `balanced`: allow reliable secondary sources but display trust level.
  - `exploratory`: allow broader suggestions, while factual claims remain source-controlled.
- Display structured answers by output type.
- Display sources and evidence separately from the main answer.
- Display warnings and fact-check notes clearly.
- Provide a short-output mode for live demos.

### 8.2 Multi-Agent Architecture

The MVP includes exactly four agents. Agents can be implemented as separate services, modules, functions, or prompt chains. For hackathon speed, a single backend process with logical agent modules is acceptable.

#### 8.2.1 Orchestrator Agent

**Role:**

- Receive the user request.
- Classify the intent.
- Decide which agents need to be called.
- Break the task into source retrieval, cultural-historical analysis, tourism generation, and final fact check.
- Merge results into a structured final response.
- Add warnings when sources are missing or claims are sensitive.
- Ensure the output matches the selected `output_type`.

**Main input:**

```json
{
  "message": "Create a 1-day Bac Ninh tour themed around Quan ho and craft villages",
  "output_type": "tour_itinerary",
  "source_mode": "strict"
}
```

**Main output:**

```json
{
  "intent": "tour_itinerary",
  "tasks": [
    "intent_classification",
    "source_retrieval",
    "cultural_historical_analysis",
    "tourism_generation",
    "fact_check"
  ],
  "warnings": []
}
```

#### 8.2.2 Search Agent

**Role:**

- Retrieve information from priority sources.
- Read curated files such as Markdown, JSON, PDF summaries, or team-provided documents.
- Search the web only if the hackathon setup allows it.
- Extract key facts about destinations, historical sites, craft villages, festivals, food, route context, and practical details.
- Attach metadata to each fact:
  - source title,
  - source type,
  - URL or file name,
  - trust level,
  - access date when available,
  - fact or excerpt used.
- Return structured source data to the Orchestrator Agent and other agents.

**Rule:** The Search Agent must never invent sources or factual claims. If evidence is missing, it must return `not_found` or `needs_verification`.

#### 8.2.3 Cultural-Historical Agent

**Role:**

- Analyze historical and cultural context using information returned by the Search Agent.
- Organize Bac Ninh information into a timeline when relevant:
  - early or ancient layer,
  - feudal period,
  - modern and industrial layer.
- Label claims as:
  - `Source-supported`,
  - `Needs verification`,
  - `Insufficient evidence`.
- Convert sourced facts into accessible historical-cultural explanations.
- Detect sensitive claims, including:
  - ancient capital claims,
  - first/only/largest claims,
  - origin claims,
  - claims tied to historical figures,
  - claims about recognition status.

**Rule:** If a sensitive claim lacks strong sources, the agent must not present it as fact. It must label the claim as requiring verification.

#### 8.2.4 Tourism Agent

**Role:**

- Generate itineraries and check-in recommendations.
- Support route durations:
  - half day,
  - 1 day,
  - 2 days.
- Combine tourism layers when evidence is available:
  - historical sites,
  - festivals,
  - cuisine and local specialties,
  - craft villages,
  - Quan ho folk singing,
  - check-in spots,
  - modern industrial context when verified or clearly labeled as needing verification.
- Suggest suitable visitor groups:
  - students,
  - families,
  - culture-oriented travelers,
  - business visitors,
  - local explorers.
- Add practical notes:
  - route logic,
  - estimated travel effort,
  - best-fit visitor group,
  - information that requires updated checks.

**Rule:** The Tourism Agent must not assert opening hours, official access, event schedules, or industrial-zone availability unless sources support them.

### 8.3 Source & Fact-check Layer

This layer is mandatory in the MVP because the main product risk is AI inventing or overstating local history.

Processing rules:

- Every important factual claim must have one of these statuses:
  - `supported`: the claim has source evidence.
  - `needs_verification`: the claim may be useful but does not yet have enough evidence.
  - `unsupported`: the claim lacks enough evidence and must not be used as fact.
- Historical, cultural, site, festival, craft-village, and Quan ho claims must not be asserted without source support.
- The output must include `Sources/evidence`, `Fact-check notes`, or `Warnings`.
- Confidence levels:
  - `High`: official or primary source, or multiple reliable sources agree.
  - `Medium`: reliable secondary source, but stronger confirmation is needed.
  - `Low`: weak source or research direction only.
  - `Not enough evidence`: insufficient evidence to present as fact.
- If sources conflict, the system must state the conflict instead of choosing one side without basis.

---

## 9. Functional Requirements

### 9.1 Input Handling

| ID | Requirement |
|---|---|
| FR-1 | The system allows users to enter free-form text requests. |
| FR-2 | The system allows users to choose `output_type` before generation. |
| FR-3 | The system allows users to choose `source_mode`: `strict`, `balanced`, or `exploratory`. |
| FR-4 | The system handles short requests such as “1-day Quan ho tour” and infers the closest intent. |
| FR-5 | The system returns warnings if the user asks for an unsupported historical assertion. |

### 9.2 Intent Classification

| ID | Requirement |
|---|---|
| FR-6 | The system supports exactly these MVP intents: `tour_itinerary`, `checkin_recommendation`, `historical_narrative`, `source_summary`, and `general_qa`. |
| FR-7 | If intent is unclear, the system chooses the closest supported intent and records the assumption. |
| FR-8 | The Orchestrator Agent determines which of the four agents should be used for each request. |
| FR-9 | The system rejects or redirects requests that require unsupported output types. |

### 9.3 Source Retrieval

| ID | Requirement |
|---|---|
| FR-10 | The Search Agent retrieves sources from curated datasets and optionally web search if enabled. |
| FR-11 | Each source item includes `title`, `source_type`, `trust_level`, `url` or `file_name`, and `used_for`. |
| FR-12 | Official and primary sources are prioritized over secondary and unverified sources. |
| FR-13 | If no sufficiently strong source is found, the system must not assert the claim. |
| FR-14 | The system limits returned sources using `MAX_SOURCES_PER_QUERY`. |

### 9.4 Historical-Cultural Narrative Generation

| ID | Requirement |
|---|---|
| FR-15 | The Cultural-Historical Agent creates a timeline narrative when `output_type` is `historical_narrative`. |
| FR-16 | A timeline should include early, feudal, and modern/industrial layers when evidence is available. |
| FR-17 | Sensitive claims such as “Bac Ninh was once an ancient capital during the Hai Ba Trung period” must be labeled as requiring verification if no strong source is available. |
| FR-18 | The narrative must be understandable and not exaggerated. |
| FR-19 | The system separates sourced claims from claims requiring verification. |

### 9.5 Tourism and Check-in Recommendations

| ID | Requirement |
|---|---|
| FR-20 | The Tourism Agent can create half-day, 1-day, and 2-day itineraries. |
| FR-21 | A 1-day itinerary includes morning, noon, afternoon, and evening sections. |
| FR-22 | Each itinerary includes theme, suitable audience, destinations, experiences, route logic, and practical notes. |
| FR-23 | The system can generate at least 3 check-in spot suggestions with context and confidence labels. |
| FR-24 | If industrial-zone context is included, it must be labeled as verified or requiring source/partner verification. |
| FR-25 | The system must respect a user request to exclude historical explanations. |

### 9.6 Output Formatting

| ID | Requirement |
|---|---|
| FR-26 | The output must be structured by `output_type`. |
| FR-27 | The output must not be returned as one long hard-to-read paragraph. |
| FR-28 | The output must include `Sources/evidence`, `Fact-check notes`, or `Warnings`. |
| FR-29 | The output must include confidence labels when recommending check-in spots or evaluating claims. |
| FR-30 | The system provides a short-output mode for hackathon demos. |

### 9.7 Source Display

| ID | Requirement |
|---|---|
| FR-31 | The UI displays source notes at the end of the answer. |
| FR-32 | Each displayed source includes trust level and usage purpose. |
| FR-33 | Internal or curated documents are displayed by file name or document title. |
| FR-34 | If no source is available, the UI displays: “No sufficiently strong source is available to assert this.” |

### 9.8 Error Handling

| ID | Requirement |
|---|---|
| FR-35 | If the LLM or search process fails, the system returns a friendly error and does not create fake facts. |
| FR-36 | If the request is too broad, the system returns a scoped response and states assumptions. |
| FR-37 | If sources conflict, the system states the conflict and recommends further verification. |
| FR-38 | If the request asks for distorted or culturally offensive output, the system refuses or redirects safely. |

### 9.9 Review Mode

| ID | Requirement |
|---|---|
| FR-39 | Review mode displays key claims and their source status. |
| FR-40 | Review mode allows copying the answer as Markdown. |
| FR-41 | Review mode displays a high-level agent trace: Orchestrator → Search → Cultural-Historical → Tourism → Fact-check. |
| FR-42 | Review mode highlights claims with `Needs verification` or `Insufficient evidence`. |

---

## 10. Non-functional Requirements

| Area | Requirement |
|---|---|
| Accuracy | Do not assert historical, cultural, site, festival, or craft-village claims if sufficiently strong sources are missing. |
| Source transparency | Output must show source status, trust level, or verification-needed labels. |
| Simplicity | The MVP prioritizes a clear demo flow, simple UI, and limited output types. |
| Maintainability | Agent prompts and logic should be separated so the team can revise them quickly. |
| Latency | Normal demo responses should be fast when curated sources are used; web search may take longer. |
| Safety | Avoid historical distortion, cultural disrespect, illegal recommendations, and unsupported overclaims. |
| Localization | The product may accept local-language input, but the reviewed specification is written in English. |
| Demo readiness | Prepare sample sources, sample prompts, fallback responses, and consistent output formats. |
| Observability | Log intent, agents called, source count, warnings, and confidence levels. |
| Cost control | Limit number of sources, tokens, and model calls per request. |

---

## 11. Data Sources & Knowledge Strategy

### 11.1 Priority Source List

Sources that should be prioritized in the MVP:

1. Bac Ninh provincial gazetteer.
2. Bac Ninh local gazetteer.
3. History of the Bac Ninh Provincial Party Committee.
4. Chronology of historical events of the Bac Ninh Provincial Party Committee.
5. Books and research materials about Quan ho, craft villages, historical sites, and festivals.
6. Official Bac Ninh provincial websites.
7. Official websites of local cultural, tourism, or heritage management units.
8. Museum websites and local information portals.
9. Reliable secondary references from reputable publishers or research institutions.
10. Team-provided curated sources, clearly labeled as team-provided.

### 11.2 Source Classification

| Source Type | Examples | Trust Level | Usage Rule |
|---|---|---|---|
| Primary or official source | Gazetteers, official portals, official documents, museum materials | High | Can support factual claims when cited clearly. |
| Reliable secondary source | Books, research articles, reputable articles, publisher-backed materials | Medium–High | Can add context; major claims should be cross-checked. |
| Team-provided source | Uploaded files, mentor notes, curated datasets | Medium | Usable for demo, but must be labeled if not independently verified. |
| Unverified web source | Personal blogs, informal posts, unverified pages | Low | Use only as a research lead, not as proof. |
| AI-generated text | Output generated by the model | Not a source | Must never be treated as verification. |

### 11.3 Handling Conflicting Sources

If sources disagree:

- Prioritize official or primary sources.
- Do not silently choose one source if the evidence is unclear.
- Display the conflict in the output.
- Mark the claim as requiring further verification if needed.
- Provide a comparison table for reviewer-facing outputs.

### 11.4 Confidence Labeling

| Confidence | Condition |
|---|---|
| High | Official or primary source exists, or multiple reliable sources agree. |
| Medium | A reliable secondary source exists, but stronger confirmation is needed. |
| Low | Source is weak or only useful as a research direction. |
| Not enough evidence | There is insufficient evidence to present the claim as fact. |

### 11.5 Avoiding Hallucination

- Do not allow the LLM to invent sources.
- Do not allow factual claims unless the Search Agent returns supporting evidence or a clear uncertainty status.
- The Cultural-Historical Agent must label uncertain claims as requiring source verification.
- The fact-check layer should scan for risky wording such as `first`, `only`, `largest`, `ancient capital`, `originated in`, `recognized as`, and `directly associated with`.
- Unsourced facts should appear only in a verification-needed section, not as confirmed facts.

---

## 12. Output Formats

### 12.1 Tour Itinerary Output

Required structure:

```markdown
# [Tour Name]

**Theme:** ...
**Suitable audience:** ...
**Duration:** Half day / 1 day / 2 days
**Route spirit:** ...

## Itinerary

### Morning
- Destination/activity:
- Context:
- Experience/check-in:
- Source/evidence:

### Noon
- Food/local specialty suggestion:
- Notes:

### Afternoon
- Destination/activity:
- Context:
- Experience/check-in:
- Source/evidence:

### Evening
- Light activity or ending suggestion:
- Practical note:

## Sources/evidence
- ...

## Notes requiring verification
- ...
```

### 12.2 Check-in Recommendation Output

Required structure:

```markdown
# Check-in Suggestions: [Theme]

| Destination | Why Visit | Storytelling Angle | Activity / Photo Idea | Suitable Time | Confidence |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | High/Medium/Low |

## Sources/evidence
- ...

## Needs verification
- ...
```

### 12.3 Historical-Cultural Narrative Output

Required structure:

```markdown
# Bac Bling Historical-Cultural Narrative

## Big Idea
...

## Timeline Narrative

### 1. Early Layer / Ancient Context
- Usable claim:
- Source status:
- Needs verification:

### 2. Feudal Period
- Usable claim:
- Connection to sites, craft villages, or festivals:
- Sources/evidence:

### 3. Modern and Industrial Layer
- Usable claim:
- Connection to tourism routes:
- Sources/evidence:

## Route Applications
- ...

## Points Requiring Further Verification
- ...
```

### 12.4 Source Summary Output

Required structure:

```markdown
# Source Summary: [Topic]

| Source Title | Source Type | Trust Level | Usable Facts | Limitations | Usage Rule |
|---|---|---|---|---|---|
| ... | Primary/official | High | ... | ... | ... |

## Strongly Supported Claims
- ...

## Claims Requiring Verification
- ...

## Insufficient Evidence
- ...
```

---

## 13. Suggested Technical Architecture

### 13.1 Recommended Stack for MVP

- **Frontend:** Streamlit or lightweight web UI.
- **Backend:** FastAPI.
- **LLM provider:** Azure OpenAI, OpenAI, or another hackathon-approved provider.
- **Retrieval:** curated source files first; optional web search if allowed.
- **Agent orchestration:** Python backend coordinating logical agent modules.
- **MVP storage:** in-memory data, JSON files, or Markdown files.
- **Optional:** Chroma, FAISS, or another simple vector database if time allows.

### 13.2 System Flow

```text
[User]
  |
  v
[UI: Text input + output_type + source_mode]
  |
  v
[Backend]
  |
  v
[Orchestrator Agent]
  |---------------> [Search Agent]
  |                       |
  |                       v
  |              [Curated Sources / Optional Web Search]
  |
  |---------------> [Cultural-Historical Agent]
  |
  |---------------> [Tourism Agent]
  |
  v
[Source & Fact-check Layer]
  |
  v
[Structured Response: reply + sources + warnings + confidence]
  |
  v
[UI Display]
```

### 13.3 MVP Implementation Notes

- If there is not enough time for separate services, implement the four agents as logical modules in one backend.
- Keep source and fact-check handling even if all other features are simplified.
- Prepare 10–20 curated sources about Bac Ninh for stable demo behavior.
- Prepare fixed demo prompts for tour itinerary, check-in recommendation, historical narrative, and source summary.
- Store source metadata consistently so the frontend can display trust level and usage rule.

---

## 14. API Contract Draft

### 14.1 POST `/api/v1/generate`

**Request:**

```json
{
  "message": "Create a 1-day Bac Ninh tour themed around Quan ho and craft villages",
  "output_type": "tour_itinerary",
  "source_mode": "strict",
  "conversation_id": "optional-uuid"
}
```

**Response:**

```json
{
  "reply": "# 1-day Bac Ninh tour...",
  "output_type": "tour_itinerary",
  "intent": "tour_itinerary",
  "confidence": "medium",
  "sources": [
    {
      "title": "Source title",
      "url": "Link if available",
      "file_name": "Document title if curated",
      "source_type": "primary_official",
      "trust_level": "high",
      "used_for": "Information about a site, festival, craft village, or route context",
      "accessed_at": "2026-06-27"
    }
  ],
  "warnings": [
    "Some details require additional verification from official sources before use."
  ],
  "agent_trace": [
    "intent_classification",
    "source_retrieval",
    "cultural_historical_analysis",
    "tourism_generation",
    "fact_check"
  ],
  "conversation_id": "generated-or-echoed-uuid"
}
```

### 14.2 GET `/health`

**Response:**

```json
{
  "status": "ok",
  "version": "0.3.0",
  "service": "bac-bling-agent"
}
```

### 14.3 POST `/api/v1/source-summary`

**Request:**

```json
{
  "topic": "Quan ho folk singing in Bac Ninh",
  "source_mode": "strict"
}
```

**Response:**

```json
{
  "topic": "Quan ho folk singing in Bac Ninh",
  "sources": [
    {
      "title": "Source title",
      "source_type": "primary_official",
      "trust_level": "high",
      "summary": "Usable facts...",
      "limitations": "Needs further cross-checking...",
      "usage_rule": "Can support factual claims when cited clearly."
    }
  ],
  "not_enough_evidence": []
}
```

### 14.4 POST `/api/v1/tour`

**Request:**

```json
{
  "theme": "Quan ho and craft villages",
  "duration": "1_day",
  "audience": "young travelers",
  "source_mode": "strict"
}
```

**Response:**

```json
{
  "tour_name": "...",
  "duration": "1_day",
  "schedule": {
    "morning": [],
    "noon": [],
    "afternoon": [],
    "evening": []
  },
  "sources": [],
  "warnings": []
}
```

### 14.5 Supported Output Types

```json
[
  "tour_itinerary",
  "checkin_recommendation",
  "historical_narrative",
  "source_summary",
  "general_qa"
]
```

---

## 15. Environment Variables

| Variable | Required | Example | Purpose |
|---|---:|---|---|
| `OPENAI_API_KEY` | Optional | `sk-...` | API key if using OpenAI. |
| `AZURE_OPENAI_API_KEY` | Optional | `...` | API key if using Azure OpenAI. |
| `AZURE_OPENAI_ENDPOINT` | Optional | `https://example.openai.azure.com` | Azure OpenAI endpoint. |
| `AZURE_OPENAI_DEPLOYMENT` | Optional | `gpt-4.1` | Deployment or model name. |
| `SEARCH_API_KEY` | Optional | `...` | API key for web search if used. |
| `SOURCE_MODE` | Yes | `strict` | Default source mode. |
| `API_BASE_URL` | Yes | `http://localhost:8000` | Backend API base URL. |
| `MAX_SOURCES_PER_QUERY` | Yes | `5` | Maximum number of sources per query. |
| `ENABLE_WEB_SEARCH` | Yes | `false` | Enable or disable web search. |
| `CURATED_SOURCE_DIR` | Yes | `./data/sources` | Directory containing curated sources. |
| `LOG_LEVEL` | Optional | `INFO` | Logging level. |
| `DEMO_SHORT_MODE` | Optional | `true` | Enable shortened output for demos. |

---

## 16. MVP Success Criteria

- [ ] Users can enter a text request and receive a structured output.
- [ ] Users can generate a 1-day tour with at least 3 destinations or activities.
- [ ] A 1-day tour includes morning, noon, afternoon, and evening sections.
- [ ] Users can generate check-in recommendations with confidence labels.
- [ ] Users can generate a historical-cultural-modernization narrative when requested.
- [ ] Users can generate a source summary for reviewer inspection.
- [ ] The output includes at least 3 sources or clear verification warnings when sources are missing.
- [ ] The system does not assert historical claims without sources.
- [ ] Reviewers can understand the exact four-agent architecture.
- [ ] The demo runs end-to-end from UI to backend to structured response.
- [ ] The system displays a high-level agent trace.
- [ ] The test plan covers source summary, sensitive historical claims, and industrial-zone route warnings.

### Suggested Cuts if Time Is Limited

If the MVP is too broad, reduce scope in this order:

1. Temporarily remove live web search and use curated sources only.
2. Temporarily remove 2-day routes and keep only half-day and 1-day routes.
3. Temporarily reduce check-in recommendations from 5 spots to 3 spots.
4. Temporarily simplify review mode to a source table and warning list.
5. Implement the agents as logical modules in a single backend instead of separate services.

Do not cut the Source & Fact-check Layer, because it is the core reliability mechanism.

---

## 17. Manual Test Plan

| ID | Input | Expected Output | Pass/Fail Criteria |
|---|---|---|---|
| TC-1 | “Create a 1-day Bac Ninh tour themed around Quan ho and craft villages.” | A 1-day itinerary with morning/noon/afternoon/evening, destinations, experiences, sources, and warnings. | Pass if there are at least 3 destinations, at least 1 Quan ho or craft-village element, and clear source notes. |
| TC-2 | “Suggest 5 check-in spots with cultural stories.” | A table of 5 destinations, storytelling angles, activities, confidence levels, and source notes. | Pass if each spot has confidence and source status. |
| TC-3 | “Create a narrative from early Bac Ninh to modern industrial Bac Ninh.” | A timeline narrative by stage with fact-check notes. | Pass if sensitive claims are labeled as requiring verification when sources are missing. |
| TC-4 | “Find reliable sources for a historical site in Bac Ninh.” | A source table with trust level, usable facts, limitations, and usage rules. | Pass if official or primary sources are prioritized when available. |
| TC-5 | “Assert that Bac Ninh was once an ancient capital during the Hai Ba Trung period.” | The system does not assert the claim unless strong sources are available. | Pass if the output says source verification is required or evidence is insufficient. |
| TC-6 | “Summarize sources about Quan ho, craft villages, and historical sites in Bac Ninh.” | A grouped source summary with trust levels and usage rules. | Pass if weak sources are clearly labeled and not used for strong claims. |
| TC-7 | “Suggest an industrial-zone route connected with Bac Ninh culture.” | A route direction with verification warnings for access, partners, and official availability. | Pass if the system does not claim that an official route exists without evidence. |
| TC-8 | “Create a 1-day tour but do not include historical explanations.” | A practical route focused on destinations, food, route logic, and check-in activities. | Pass if the system respects the request and still includes source notes for factual information. |
| TC-9 | “Give me the oldest and most important heritage site in Bac Ninh.” | A cautious answer with source status and warning about superlative claims. | Pass if `oldest` and `most important` are not asserted without strong evidence. |
| TC-10 | “Create a route for families with children visiting Bac Ninh for half a day.” | A half-day itinerary with suitable pacing, destinations, food suggestions, and notes. | Pass if the route is realistic, structured, and source-aware. |

---

## 18. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---:|---|
| AI invents history or sources | Very high | High | Require Source & Fact-check Layer; never treat LLM output as a source; label uncertain claims. |
| Stakeholders are confused with agents | High | Medium | Keep Target Users & Stakeholders separate from Multi-Agent Architecture. |
| Scope creep reduces MVP feasibility | High | High | Keep only five output types and exactly four agents. |
| Sensitive historical claims lack strong evidence | High | High | Flag risky claims and require source verification before use. |
| Industrial-zone route suggestions lack official access information | High | Medium | Label access, partners, and route availability as requiring verification unless confirmed. |
| Sources are insufficient or conflicting | High | High | Prioritize official sources, show conflicts, and avoid unsupported conclusions. |
| Users misunderstand narrative output as official history | High | Medium | Display confidence labels, source notes, and verification warnings. |
| Real routes may be impractical due to opening hours or event changes | Medium | Medium | Label operational details as requiring updated checks. |
| Web search causes slow responses | Medium | Medium | Use curated sources first and limit source count. |
| Team lacks time to build separate agent services | Medium | High | Implement the agents as logical modules inside one backend. |

---

## 19. Assumptions

1. The hackathon requires an MVP demo, not a production-ready product.
2. Bac Ninh data can be collected from public sources or team-provided curated sources.
3. A logical multi-agent implementation is acceptable for the MVP.
4. It is acceptable to label uncertain information as requiring verification.
5. Reviewers value source transparency and hallucination prevention.
6. A simple UI with strong structured output is enough for the demo.
7. Sources such as gazetteers and specialized books can be manually added to a curated dataset.
8. Industrial-zone route ideas require official evidence or partner confirmation before being treated as available routes.
9. The product should prioritize reliability over the number of features.
10. Human review is required before using outputs in high-stakes cultural or historical contexts.

---

## 20. Open Questions for Review

1. Should the main demo flow prioritize tour itinerary, check-in recommendation, or historical-cultural narrative?
2. Is live web search required, or is a curated dataset enough for the hackathon demo?
3. Which source types are considered strong enough for sensitive historical claims?
4. Is there an official source for the claim that Bac Ninh was once an ancient capital during the Hai Ba Trung period?
5. Should industrial-zone routes be included in the MVP demo or kept as an optional scenario?
6. How many curated sources should be prepared before demo day?
7. Should the UI show agent trace by default or only in review mode?
8. What should be the minimum source requirement for each output type?
9. Should source summaries include direct excerpts, paraphrases, or only metadata and usable facts?
10. Should the MVP support English output, local-language output, or both?
11. How should the system handle a user request that asks for an unsupported superlative claim?
12. What is the fallback behavior when no source is available for a requested destination?

---

## 21. Future / Later Releases

Potential development directions after the hackathon:

1. Integrate maps, routing, and travel-time estimation.
2. Add real-time festival and event data when reliable feeds are available.
3. Personalize itineraries by age, budget, time, interests, and visitor group.
4. Build a source management system with upload, review, tagging, and versioning.
5. Add expert review workflow for historical and cultural claims.
6. Build a voice Q&A mode for Bac Ninh travel exploration.
7. Add multilingual support for international visitors.
8. Integrate booking or partner links if verified partners are available.
9. Create a recommendation engine based on season, visitor profile, and route constraints.
10. Build a knowledge graph connecting sites, figures, craft villages, festivals, and place names.
11. Add a school-trip mode for students learning local history through place-based routes.
12. Add accessibility-aware route suggestions for elderly visitors, children, and visitors with mobility needs.

---

## 22. Appendix

### 22.1 Glossary

| Term | Meaning |
|---|---|
| Bac Bling | The product concept for an AI-assisted Bac Ninh tourism and cultural exploration system. |
| Agent | A technical AI component responsible for a specific group of tasks. |
| Orchestrator Agent | The agent that classifies intent, coordinates other agents, and assembles the final response. |
| Search Agent | The agent that retrieves and structures source evidence. |
| Cultural-Historical Agent | The agent that interprets sourced cultural and historical information. |
| Tourism Agent | The agent that generates routes, itineraries, and check-in recommendations. |
| Source mode | A control setting that determines how strict the system should be with source requirements. |
| Curated sources | A selected set of sources prepared by the team for stable demo behavior. |
| Fact-check notes | Notes showing whether claims are supported, uncertain, or insufficiently evidenced. |
| Confidence level | The reliability level of a claim or recommendation based on source quality. |

### 22.2 Intent List

| Intent | Description |
|---|---|
| `tour_itinerary` | Create a travel itinerary. |
| `checkin_recommendation` | Suggest check-in spots with context and confidence labels. |
| `historical_narrative` | Create a historical-cultural-modernization narrative. |
| `source_summary` | Summarize and evaluate sources. |
| `general_qa` | Answer general Bac Ninh questions with source control. |

### 22.3 Output Type List

```json
[
  "tour_itinerary",
  "checkin_recommendation",
  "historical_narrative",
  "source_summary",
  "general_qa"
]
```

### 22.4 Sample System Prompts for the Four Agents

#### Orchestrator Agent — System Prompt Draft

```text
You are the Orchestrator Agent of Bac Bling AI Agent. Your task is to read the user's request, classify intent, decide which agents should be called, coordinate source retrieval, historical-cultural analysis, tourism generation, and final fact-checking. You must not invent facts about history, sites, festivals, craft villages, or Quan ho folk singing. If information lacks a reliable source, label it as requiring source verification. The final output must be structured and include source notes and warnings when needed.
```

#### Search Agent — System Prompt Draft

```text
You are the Search Agent. Your task is to find and extract information from priority sources about Bac Ninh. Return only sourced facts or a clear not-found / needs-verification status. Do not infer historical facts by yourself. For each fact, return metadata including title, source_type, trust_level, url or file_name, used_for, and confidence.
```

#### Cultural-Historical Agent — System Prompt Draft

```text
You are the Cultural-Historical Agent. Your task is to turn sourced Bac Ninh data into an accessible historical-cultural narrative. Clearly distinguish source-supported information, information needing verification, and insufficient evidence. Do not exaggerate. Do not use risky claims such as first, only, largest, ancient capital, or originated in period X unless strong sources support them. For uncertain claims, write source verification needed.
```

#### Tourism Agent — System Prompt Draft

```text
You are the Tourism Agent. Your task is to create Bac Ninh travel itineraries and check-in recommendations by duration, theme, and visitor group. Combine historical sites, festivals, cuisine, craft villages, Quan ho folk singing, check-in spots, and modern context only when the data supports it. Each itinerary must include route logic, suitable audience, practical notes, source notes, and warnings for uncertain information. Do not assert opening hours, event schedules, or access rules without updated sources.
```
