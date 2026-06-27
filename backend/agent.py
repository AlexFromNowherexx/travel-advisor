from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .config import settings
from .schemas import (
    Confidence,
    GenerateResponse,
    OutputType,
    SourceMetadata,
    SourceMode,
    SourceSummaryItem,
    SourceSummaryResponse,
    TourResponse,
)
from .skill_loader import load_skill


SKILL_PROMPT = load_skill(settings.skill_file_path)

AGENT_TRACE = [
    "intent_classification",
    "source_retrieval",
    "cultural_historical_analysis",
    "tourism_generation",
    "fact_check",
]

RISKY_TERMS = (
    "first",
    "only",
    "largest",
    "oldest",
    "ancient capital",
    "hai ba trung",
    "originated in",
    "recognized as",
    "directly associated with",
    "official industrial",
)


@dataclass(frozen=True, slots=True)
class SourceRecord:
    title: str
    source_type: str
    trust_level: str
    used_for: str
    summary: str
    limitations: str
    usage_rule: str
    keywords: tuple[str, ...]
    url: str | None = None
    file_name: str | None = None


SOURCE_CATALOG: tuple[SourceRecord, ...] = (
    SourceRecord(
        title="UNESCO - Quan ho Bac Ninh folk songs",
        source_type="primary_official",
        trust_level="high",
        used_for="Source-supported facts about Quan ho recognition and cultural practice.",
        summary="UNESCO listing metadata supports cautious statements about Quan ho Bac Ninh folk songs as recognized intangible cultural heritage.",
        limitations="Does not verify event schedules, current performance availability, or specific village access.",
        usage_rule="Use for high-confidence cultural context about Quan ho; verify live programs separately.",
        keywords=("quan ho", "folk", "singing", "unesco", "culture", "festival"),
        url="https://ich.unesco.org/en/RL/quan-ho-bac-ninh-folk-songs-00113",
    ),
    SourceRecord(
        title="Bac Ninh Provincial Portal",
        source_type="primary_official",
        trust_level="high",
        used_for="Official province-level context, public notices, and tourism/culture references.",
        summary="Official provincial material is preferred for current administrative, tourism, and cultural claims.",
        limitations="Individual pages should be checked for the exact claim and latest publication date.",
        usage_rule="Use for official claims when a matching page is available; otherwise mark details as needing verification.",
        keywords=("bac ninh", "official", "province", "tourism", "culture", "heritage", "industrial"),
        url="https://bacninh.gov.vn",
    ),
    SourceRecord(
        title="Vietnam National Authority of Tourism - Bac Ninh references",
        source_type="primary_official",
        trust_level="high",
        used_for="Tourism-oriented descriptions of destinations, festivals, and visitor context.",
        summary="National tourism references can support destination-level descriptions and route inspiration.",
        limitations="Opening hours, ticketing, transport, and live event details require updated local checks.",
        usage_rule="Use for destination context; do not use alone for sensitive historical superlatives.",
        keywords=("tour", "itinerary", "destination", "pagoda", "temple", "festival", "food", "check-in"),
        url="https://vietnamtourism.gov.vn",
    ),
    SourceRecord(
        title="Team-curated Bac Ninh craft village notes",
        source_type="team_provided",
        trust_level="medium",
        used_for="Demo metadata about Dong Ho folk painting, Phu Lang pottery, and craft-village route ideas.",
        summary="Curated notes identify craft villages that can be used as route candidates for the MVP demo.",
        limitations="Needs stronger official or expert sources before supporting detailed origin, age, or superlative claims.",
        usage_rule="Use for route suggestions and check-in ideas; label historical detail as needing verification.",
        keywords=("craft", "village", "dong ho", "painting", "phu lang", "pottery", "check-in"),
        file_name="built-in-demo-catalog",
    ),
    SourceRecord(
        title="Team-curated Bac Ninh historical site notes",
        source_type="team_provided",
        trust_level="medium",
        used_for="Demo metadata about major historical-cultural places such as Do Temple and But Thap Pagoda.",
        summary="Curated notes provide route candidates and high-level context for historical-cultural itineraries.",
        limitations="Specific dates, figure associations, and ranking claims require official or scholarly confirmation.",
        usage_rule="Use for cautious storytelling; mark sensitive history as source verification needed.",
        keywords=("history", "historical", "temple", "pagoda", "do temple", "but thap", "early", "feudal"),
        file_name="built-in-demo-catalog",
    ),
    SourceRecord(
        title="Team-curated Bac Ninh cuisine notes",
        source_type="team_provided",
        trust_level="medium",
        used_for="Demo ideas for local food and specialty stops in a Bac Ninh route.",
        summary="Curated notes support food suggestions as itinerary ideas rather than verified restaurant recommendations.",
        limitations="Restaurant names, prices, hours, and availability are not live-verified.",
        usage_rule="Use for food categories and local-specialty prompts; verify venues before travel.",
        keywords=("food", "cuisine", "specialty", "noon", "restaurant", "dining", "local"),
        file_name="built-in-demo-catalog",
    ),
)


def classify_intent(message: str, requested: OutputType) -> OutputType:
    if requested != "general_qa":
        return requested

    text = message.lower()
    if "source" in text or "reliable" in text:
        return "source_summary"
    if "check-in" in text or "check in" in text or "spots" in text:
        return "checkin_recommendation"
    if "narrative" in text or "timeline" in text or "industrial" in text:
        return "historical_narrative"
    if "tour" in text or "itinerary" in text or "route" in text or "half-day" in text or "1-day" in text:
        return "tour_itinerary"
    return "general_qa"


def select_sources(message: str, source_mode: SourceMode) -> list[SourceRecord]:
    text = message.lower()
    matched = [
        source
        for source in SOURCE_CATALOG
        if any(keyword in text for keyword in source.keywords)
    ]
    if not matched:
        matched = list(SOURCE_CATALOG[:3])

    if source_mode == "strict":
        preferred = [source for source in matched if source.trust_level == "high"]
        matched = preferred or matched
    elif source_mode == "exploratory":
        matched = list(dict.fromkeys([*matched, *SOURCE_CATALOG]))

    limit = max(settings.max_sources_per_query, 1)
    return matched[:limit]


def to_metadata(source: SourceRecord) -> SourceMetadata:
    return SourceMetadata(
        title=source.title,
        url=source.url,
        file_name=source.file_name,
        source_type=source.source_type,
        trust_level=source.trust_level,
        used_for=source.used_for,
        accessed_at=date.today().isoformat(),
    )


def confidence_for(sources: list[SourceRecord], warnings: list[str]) -> Confidence:
    if not sources:
        return "not_enough_evidence"
    if any(source.trust_level == "high" for source in sources) and not warnings:
        return "high"
    if any(source.trust_level == "high" for source in sources):
        return "medium"
    return "low"


def fact_check_warnings(message: str, sources: list[SourceRecord]) -> list[str]:
    text = message.lower()
    warnings: list[str] = []

    if any(term in text for term in RISKY_TERMS):
        warnings.append(
            "Sensitive or superlative historical claims require strong official or scholarly sources; unsupported claims are labeled as needing verification."
        )
    if "industrial" in text or "industrial-zone" in text or "industrial zone" in text:
        warnings.append(
            "Industrial-zone access, official route availability, and partner permissions are not confirmed and need partner/source verification."
        )
    if not sources:
        warnings.append("No matching curated source was found; factual claims should be treated as insufficiently evidenced.")
    warnings.append("Opening hours, event schedules, prices, weather, and live access details must be checked with current official sources before travel.")
    return list(dict.fromkeys(warnings))


def render_tour(message: str, sources: list[SourceRecord]) -> str:
    minimized_history = "do not include historical" in message.lower() or "without historical" in message.lower()
    context_label = "Historical context intentionally minimized by user request." if minimized_history else "Cultural context is included only where source notes or verification labels are shown."

    return f"""# Quan ho and Craft Villages Bac Ninh Route

**Theme:** Quan ho culture, craft villages, food, and source-aware check-in stops
**Suitable audience:** Culture-oriented travelers, students, families, and local explorers
**Duration:** 1 day
**Route spirit:** Move from cultural identity to hands-on craft and easy photo moments. {context_label}

## Itinerary

### Morning
- Destination/activity: Start with a Quan ho-focused cultural stop or village-area experience.
- Context: Source-supported at a high level by UNESCO for Quan ho Bac Ninh folk songs. Live performances and village access need updated checks.
- Experience/check-in: Listen if a verified program is available, take respectful photos around public cultural spaces, and note call-and-response singing as the storytelling frame.
- Source/evidence: UNESCO - Quan ho Bac Ninh folk songs.

### Noon
- Food/local specialty suggestion: Choose a local Bac Ninh meal or specialty stop near the route rather than a fixed restaurant.
- Notes: Venue names, opening hours, prices, and dietary details require same-day verification.

### Afternoon
- Destination/activity: Visit a craft-village direction such as Dong Ho folk painting or Phu Lang pottery if access is confirmed.
- Context: Craft-village details in this MVP are demo-curated and should be verified before strong historical claims.
- Experience/check-in: Photograph tools, materials, finished work, or workshop streets only where permitted.
- Source/evidence: Team-curated Bac Ninh craft village notes; official confirmation recommended.

### Evening
- Light activity or ending suggestion: End with a gentle city-center walk, cafe stop, or source-supported cultural recap.
- Practical note: Keep the evening flexible because event schedules and site access are not guaranteed by the MVP.

## Sources/evidence
{format_source_bullets(sources)}

## Notes requiring verification
- Exact opening hours, tickets, event schedules, and restaurant availability.
- Detailed origin stories, "first/oldest/only/largest" claims, and figure associations.
- Any official industrial-zone route or partner access, if included.
"""


def render_checkins(sources: list[SourceRecord]) -> str:
    return f"""# Check-in Suggestions: Bac Ninh Culture and Craft

| Destination | Why Visit | Storytelling Angle | Activity / Photo Idea | Suitable Time | Confidence |
|---|---|---|---|---|---|
| Quan ho cultural stop | Connects the route to Bac Ninh's best-known singing heritage | Source-supported cultural identity; live programs need verification | Respectful photos around public cultural spaces | Morning or evening | High |
| Dong Ho folk painting direction | Strong craft-village check-in idea | Craft practice and visual folk-art identity need stronger source notes for details | Workshop textures, prints, tools where permitted | Morning or afternoon | Medium |
| Phu Lang pottery direction | Hands-on craft and village atmosphere | Pottery route works as a craft layer; detailed history needs verification | Clay, kiln, ceramics, street scenes | Afternoon | Medium |
| Do Temple direction | Useful historical-cultural anchor | Sensitive figure/date claims should be source-checked before use | Gates, courtyards, respectful architecture shots | Morning | Medium |
| But Thap Pagoda direction | Calm heritage-style stop | Cultural and architectural claims require official or scholarly support | Pagoda landscape and quiet details | Morning or late afternoon | Medium |

## Sources/evidence
{format_source_bullets(sources)}

## Needs verification
- Whether each site is open on the travel date.
- Whether photography, workshops, performances, or guided access are allowed.
- Detailed historical claims beyond the high-level source notes.
"""


def render_narrative(message: str, sources: list[SourceRecord]) -> str:
    industrial_note = "Industrial context is included as a verification-needed route direction, not as a confirmed official tour." if "industrial" in message.lower() else "Modern context can be connected to current provincial identity when supported by official sources."
    return f"""# Bac Bling Historical-Cultural Narrative

## Big Idea
Bac Ninh can be presented as a layered place: early settlement and regional identity, feudal-era cultural and religious sites, craft and Quan ho traditions, and a modern province shaped by urban and industrial development. The MVP separates source-supported claims from claims needing verification.

## Timeline Narrative

### 1. Early Layer / Ancient Context
- Usable claim: Bac Ninh can be discussed as part of northern Vietnam's long historical-cultural landscape when supported by sources.
- Source status: Needs verification for specific ancient-capital, origin, first, or oldest claims.
- Needs verification: Any claim that Bac Ninh was an ancient capital during the Hai Ba Trung period must not be asserted without strong evidence.

### 2. Feudal Period
- Usable claim: Historical-cultural route anchors can include temple and pagoda directions where source notes support them.
- Connection to sites, craft villages, or festivals: Do Temple and But Thap Pagoda can be used as route candidates, but exact dates and figure associations require stronger source confirmation.
- Sources/evidence: Team-curated historical site notes; official or scholarly references recommended before demo narration.

### 3. Modern and Industrial Layer
- Usable claim: Bac Ninh's modern identity may be discussed alongside culture when official sources support the framing.
- Connection to tourism routes: {industrial_note}
- Sources/evidence: Bac Ninh Provincial Portal for official context; route access remains unconfirmed unless separately sourced.

## Route Applications
- Build a Quan ho plus craft-village route for culture-oriented visitors.
- Build a half-day heritage route for students or families.
- Build a culture-to-modernization concept route only with clear warnings about industrial-zone access.

## Points Requiring Further Verification
- Ancient capital claims.
- Superlative claims such as first, oldest, largest, or only.
- Origin stories and claims tied to specific historical figures.
- Official recognition status when not backed by primary sources.
"""


def render_source_summary(topic: str, sources: list[SourceRecord]) -> str:
    rows = "\n".join(
        f"| {source.title} | {source.source_type} | {source.trust_level.title()} | {source.summary} | {source.limitations} | {source.usage_rule} |"
        for source in sources
    )
    return f"""# Source Summary: {topic}

| Source Title | Source Type | Trust Level | Usable Facts | Limitations | Usage Rule |
|---|---|---|---|---|---|
{rows}

## Strongly Supported Claims
- Quan ho high-level recognition and cultural framing can be supported when citing UNESCO.
- Official province-level claims should be tied to the Bac Ninh Provincial Portal or another official page.

## Claims Requiring Verification
- Specific historical dates, origin stories, and claims tied to named figures.
- Site access, schedules, tickets, and live event availability.

## Insufficient Evidence
- Any ancient-capital claim unless a strong source is added.
- Any official industrial-zone tourism route unless partner or official evidence is added.
"""


def render_general_answer(message: str, sources: list[SourceRecord]) -> str:
    return f"""# Bac Bling Answer

I can help with Bac Ninh tours, check-in suggestions, historical-cultural narratives, and source summaries. For this request, the safest next step is to choose one of the structured output types so the answer can separate recommendations from evidence.

## Useful direction
- For a route, choose `tour_itinerary`.
- For photo spots, choose `checkin_recommendation`.
- For early-to-modern cultural framing, choose `historical_narrative`.
- For reviewer inspection, choose `source_summary`.

## Source posture
{format_source_bullets(sources)}

## Notes requiring verification
- I will not treat AI-generated text as a source of truth.
- Sensitive historical claims need official, primary, or scholarly support.
"""


def format_source_bullets(sources: list[SourceRecord]) -> str:
    if not sources:
        return "- No matching curated source found."
    return "\n".join(
        f"- {source.title} ({source.source_type}, trust: {source.trust_level}) - {source.used_for}"
        for source in sources
    )


def generate_response(
    message: str,
    history: list[dict[str, str]],
    output_type: OutputType,
    source_mode: SourceMode,
    conversation_id: str,
) -> GenerateResponse:
    del history
    intent = classify_intent(message, output_type)
    sources = select_sources(message, source_mode)
    warnings = fact_check_warnings(message, sources)

    if intent == "tour_itinerary":
        reply = render_tour(message, sources)
    elif intent == "checkin_recommendation":
        reply = render_checkins(sources)
    elif intent == "historical_narrative":
        reply = render_narrative(message, sources)
    elif intent == "source_summary":
        reply = render_source_summary(message, sources)
    else:
        reply = render_general_answer(message, sources)

    return GenerateResponse(
        reply=reply,
        output_type=output_type,
        intent=intent,
        confidence=confidence_for(sources, warnings),
        sources=[to_metadata(source) for source in sources],
        warnings=warnings,
        agent_trace=AGENT_TRACE,
        conversation_id=conversation_id,
    )


def summarize_sources(topic: str, source_mode: SourceMode) -> SourceSummaryResponse:
    sources = select_sources(topic, source_mode)
    not_enough_evidence = []
    if not any(source.trust_level == "high" for source in sources):
        not_enough_evidence.append("No high-trust official source matched the topic in the curated MVP catalog.")

    if any(term in topic.lower() for term in RISKY_TERMS):
        not_enough_evidence.append("Sensitive or superlative claims require stronger source verification.")

    return SourceSummaryResponse(
        topic=topic,
        sources=[
            SourceSummaryItem(
                title=source.title,
                source_type=source.source_type,
                trust_level=source.trust_level,
                summary=source.summary,
                limitations=source.limitations,
                usage_rule=source.usage_rule,
                url=source.url,
                file_name=source.file_name,
            )
            for source in sources
        ],
        not_enough_evidence=not_enough_evidence,
    )


def build_tour(theme: str, duration: str, audience: str, source_mode: SourceMode) -> TourResponse:
    message = f"{duration} Bac Ninh tour for {audience}: {theme}"
    sources = select_sources(message, source_mode)
    warnings = fact_check_warnings(message, sources)
    if duration == "half_day":
        schedule = {
            "morning": ["Quan ho or heritage anchor with source notes", "Nearby food or specialty stop"],
            "noon": ["Wrap up with practical verification notes"],
        }
    elif duration == "2_days":
        schedule = {
            "day_1": ["Quan ho cultural layer", "Craft village direction", "Local food stop"],
            "day_2": ["Historical site direction", "Modern context recap if sourced", "Flexible check-in ending"],
        }
    else:
        schedule = {
            "morning": ["Quan ho cultural stop or heritage anchor"],
            "noon": ["Local food or specialty stop"],
            "afternoon": ["Craft-village direction such as Dong Ho or Phu Lang if access is confirmed"],
            "evening": ["Light city-center ending or cultural recap"],
        }

    return TourResponse(
        tour_name=f"Bac Ninh {theme.title()} Route",
        duration=duration,  # type: ignore[arg-type]
        schedule=schedule,
        sources=[to_metadata(source) for source in sources],
        warnings=warnings,
    )


def get_reply(message: str, history: list[dict[str, str]]) -> str:
    response = generate_response(
        message=message,
        history=history,
        output_type="general_qa",
        source_mode="strict",
        conversation_id="compatibility",
    )
    return response.reply
