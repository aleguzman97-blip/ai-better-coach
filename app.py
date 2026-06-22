"""
AI Better Coach — Alejandra Eugenia Guzman Moros
Senior Manager | Caracas, Venezuela
Powered by Streamlit + Supabase + Anthropic Claude
"""

import os, json, random, math
from datetime import datetime, timedelta, date
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Better Coach · Ale",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── OURA-INSPIRED DESIGN SYSTEM ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #111318 !important;
    color: #E4E6EF !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #18191F !important;
    border-right: 1px solid #2A2D3A !important;
}
[data-testid="stSidebar"] * { color: #C8CAD8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #5A5D70 !important;
}

/* Main background */
[data-testid="stMain"], .main, .block-container {
    background-color: #111318 !important;
    padding-top: 1.5rem !important;
}

/* Remove default streamlit borders/shadows */
div[data-testid="metric-container"] { display: none; }
.stTabs [data-baseweb="tab-list"] {
    background: #18191F;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #2A2D3A;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #6B6E80 !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #2A2D3A !important;
    color: #E4E6EF !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px !important;
}

/* KPI Cards — Oura style */
.oura-card {
    background: #18191F;
    border: 1px solid #2A2D3A;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 12px;
    position: relative;
}
.oura-card-accent-green  { border-top: 2px solid #4ECFA0; }
.oura-card-accent-blue   { border-top: 2px solid #5B9CF6; }
.oura-card-accent-purple { border-top: 2px solid #A78BFA; }
.oura-card-accent-orange { border-top: 2px solid #FB923C; }
.oura-card-accent-pink   { border-top: 2px solid #F472B6; }

.oura-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5A5D70;
    margin-bottom: 8px;
}
.oura-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 38px;
    font-weight: 500;
    color: #E4E6EF;
    line-height: 1;
    margin-bottom: 6px;
}
.oura-value span { font-size: 16px; color: #8B8EA0; margin-left: 3px; }
.oura-sub {
    font-size: 12px;
    color: #5A5D70;
    margin-top: 4px;
}
.oura-delta-up   { color: #4ECFA0; font-size: 12px; font-weight: 600; }
.oura-delta-down { color: #F87171; font-size: 12px; font-weight: 600; }

/* Score ring area */
.score-wrap {
    background: #18191F;
    border: 1px solid #2A2D3A;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
}

/* Recommendation card */
.rec-card {
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 12px;
}
.rec-go    { background: #0D2420; border: 1px solid #4ECFA040; }
.rec-easy  { background: #1E1A0E; border: 1px solid #FCD34D40; }
.rec-rest  { background: #1E0D18; border: 1px solid #F4728040; }
.rec-title { font-size: 22px; font-weight: 700; margin-bottom: 8px; color: #E4E6EF; }
.rec-body  { font-size: 14px; color: #8B8EA0; line-height: 1.7; }

/* Insight chips */
.insight-wrap {
    background: #18191F;
    border: 1px solid #2A2D3A;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 10px;
    height: 100%;
}
.insight-tag {
    display: inline-block;
    background: #A78BFA18;
    color: #A78BFA;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 3px 8px;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.insight-tag-green  { background: #4ECFA018; color: #4ECFA0; }
.insight-tag-blue   { background: #5B9CF618; color: #5B9CF6; }
.insight-tag-orange { background: #FB923C18; color: #FB923C; }
.insight-text { font-size: 13px; color: #9DA0B0; line-height: 1.6; }

/* Section divider */
.sec-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5A5D70;
    margin: 28px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #2A2D3A;
}

/* Sidebar section label */
.sb-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3A3D4A;
    margin: 20px 0 8px 0;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111318; }
::-webkit-scrollbar-thumb { background: #2A2D3A; border-radius: 3px; }

/* Buttons */
.stButton > button {
    background: #A78BFA !important;
    color: #111318 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 9px 22px !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

h1, h2, h3 { color: #E4E6EF !important; }
p, li { color: #9DA0B0 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def safe_num(v):
    """Convert NaN / None / non-numeric to None safely."""
    if v is None:
        return None
    try:
        f = float(v)
        return None if math.isnan(f) or math.isinf(f) else f
    except (TypeError, ValueError):
        return None

def fmt(v, decimals=1, unit="", fallback="—"):
    """Format a number for display, returning fallback if None."""
    sv = safe_num(v)
    if sv is None:
        return fallback
    if decimals == 0:
        return f"{int(sv)}{unit}"
    return f"{sv:.{decimals}f}{unit}"


# ═══════════════════════════════════════════════════════════════
# DATA LAYER
# ═══════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def load_json(path="HealthAutoExport-2026-02-14-2026-06-21.json") -> pd.DataFrame:
    try:
        with open(path) as f:
            raw = json.load(f)
    except FileNotFoundError:
        return pd.DataFrame()

    metrics = {m["name"]: m for m in raw["data"]["metrics"]}

    def daily_qty(key):
        out = {}
        for d in metrics.get(key, {}).get("data", []):
            dt = d["date"][:10]
            val = safe_num(d.get("qty"))
            if val is not None:
                out[dt] = val
        return out

    active  = daily_qty("active_energy")
    steps   = daily_qty("step_count")
    rhr     = daily_qty("resting_heart_rate")
    resp    = daily_qty("respiratory_rate")
    basal   = daily_qty("basal_energy_burned")
    walk_mi = daily_qty("walking_running_distance")
    hr_avg  = {d["date"][:10]: safe_num(d.get("Avg"))
               for d in metrics.get("heart_rate", {}).get("data", [])
               if safe_num(d.get("Avg")) is not None}

    # Sleep — keep longest inBed per date
    sleep_raw: dict = {}
    for d in metrics.get("sleep_analysis", {}).get("data", []):
        dt = d["date"][:10]
        in_bed = safe_num(d.get("inBed")) or 0
        if dt not in sleep_raw or in_bed > (safe_num(sleep_raw[dt].get("inBed")) or 0):
            sleep_raw[dt] = d

    all_dates = sorted(set(active) | set(sleep_raw) | set(rhr))
    rows = []
    for dt in all_dates:
        sl = sleep_raw.get(dt, {})
        total_sleep = safe_num(sl.get("totalSleep"))
        in_bed      = safe_num(sl.get("inBed"))
        deep        = safe_num(sl.get("deep"))   or 0.0
        rem         = safe_num(sl.get("rem"))    or 0.0
        awake       = safe_num(sl.get("awake"))  or 0.0
        sleep_eff   = (total_sleep / in_bed * 100
                       if total_sleep and in_bed and in_bed > 0 else None)
        rows.append({
            "date":        pd.to_datetime(dt),
            "active_kcal": safe_num(active.get(dt)),
            "steps":       safe_num(steps.get(dt)),
            "walk_mi":     safe_num(walk_mi.get(dt)),
            "basal_kcal":  safe_num(basal.get(dt)),
            "rhr":         safe_num(rhr.get(dt)),
            "hr_avg":      safe_num(hr_avg.get(dt)),
            "resp_rate":   safe_num(resp.get(dt)),
            "total_sleep": total_sleep,
            "deep_sleep":  deep,
            "rem_sleep":   rem,
            "awake_hrs":   awake,
            "sleep_eff":   sleep_eff,
        })

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def mock_data(n=130) -> pd.DataFrame:
    random.seed(42)
    today = date.today()
    rows = []
    for i in range(n):
        d        = today - timedelta(days=n - i)
        stress   = 0.5 + 0.3 * (i % 7 < 5)
        sleep_h  = max(4.5, min(9.5, random.gauss(7.2 - 0.8 * stress, 0.6)))
        deep     = round(sleep_h * random.uniform(0.12, 0.22), 2)
        rem      = round(sleep_h * random.uniform(0.18, 0.28), 2)
        rhr_v    = max(48, min(88, int(random.gauss(62 + 10 * stress, 4))))
        steps_v  = max(2000, int(random.gauss(8000 - 3000 * stress, 1500)))
        rows.append({
            "date":        pd.to_datetime(d),
            "active_kcal": round(steps_v * random.uniform(0.055, 0.07), 1),
            "steps":       steps_v,
            "walk_mi":     round(steps_v / 1300, 2),
            "basal_kcal":  round(random.gauss(1450, 60), 1),
            "rhr":         rhr_v,
            "hr_avg":      rhr_v + int(random.gauss(18, 5)),
            "resp_rate":   round(random.gauss(14.5, 0.8), 1),
            "total_sleep": round(sleep_h, 2),
            "deep_sleep":  deep,
            "rem_sleep":   rem,
            "awake_hrs":   round(random.uniform(0.3, 1.2), 2),
            "sleep_eff":   round(random.uniform(82, 96) - 6 * stress, 1),
        })
    return pd.DataFrame(rows)


def try_supabase():
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        return None
    try:
        from supabase import create_client
        sb = create_client(url, key)
        r  = sb.table("daily_metrics").select("*").order("date").execute()
        if r.data:
            df = pd.DataFrame(r.data)
            df["date"] = pd.to_datetime(df["date"])
            return df
    except Exception:
        pass
    return None


@st.cache_data(ttl=300)
def get_data() -> tuple:
    sb = try_supabase()
    if sb is not None and not sb.empty:
        return sb, "🟢 Supabase live"
    df = load_json()
    if not df.empty:
        return df, "📂 Health Auto Export JSON"
    return mock_data(), "🟡 Demo (datos simulados)"


# ═══════════════════════════════════════════════════════════════
# SCORING ENGINE
# ═══════════════════════════════════════════════════════════════

GOALS = {
    "🏃 30K Septiembre": {
        "aggression": 0.85,
        "recovery_weight": 0.50,
        "target_steps": 10000,
        "description": "Carrera de 30 km — requiere base aeróbica sólida, rodajes largos progresivos y recuperación activa. El volumen semanal debe escalar gradualmente hasta ~45–55 km en pico.",
    },
    "🔧 Mantenimiento": {
        "aggression": 0.55,
        "recovery_weight": 0.65,
        "target_steps": 7500,
        "description": "Mantener forma y salud cardiovascular sin picos de carga.",
    },
    "💪 Hipertrofia": {
        "aggression": 0.70,
        "recovery_weight": 0.55,
        "target_steps": 6000,
        "description": "Desarrollo muscular — prioriza pesas, proteína y sueño profundo.",
    },
    "🧘 Salud General": {
        "aggression": 0.45,
        "recovery_weight": 0.75,
        "target_steps": 8000,
        "description": "Bienestar integral. Movimiento diario, estrés bajo y sueño como pilar.",
    },
    "🏅 Media Maratón": {
        "aggression": 0.78,
        "recovery_weight": 0.55,
        "target_steps": 9500,
        "description": "21.1 km — volumen moderado-alto con trabajo de ritmo específico.",
    },
}



def compute_stress_from_data(row: pd.Series, df_all: pd.DataFrame) -> dict:
    """
    Derive stress level (1–5 scale) from biometric signals instead of user input.
    Uses: RHR vs personal baseline, respiratory rate, sleep efficiency, awake time.
    Returns dict with numeric level and explanation string.
    """
    signals = []
    reasons = []

    # ── Personal baselines from last 30 days ──────────────────
    recent = df_all.tail(30)
    baseline_rhr  = safe_num(recent["rhr"].dropna().mean())  or 62.0
    baseline_resp = safe_num(recent["resp_rate"].dropna().mean()) or 14.5
    baseline_eff  = safe_num(recent["sleep_eff"].dropna().mean()) or 88.0

    # ── Signal 1: RHR elevation above personal baseline ───────
    rhr = safe_num(row.get("rhr"))
    if rhr is not None:
        delta_rhr = rhr - baseline_rhr
        if delta_rhr >= 8:
            signals.append(5); reasons.append(f"FC reposo {rhr:.0f} bpm (+{delta_rhr:.0f} sobre tu base)")
        elif delta_rhr >= 5:
            signals.append(4); reasons.append(f"FC reposo elevada {rhr:.0f} bpm (+{delta_rhr:.0f})")
        elif delta_rhr >= 2:
            signals.append(3); reasons.append(f"FC reposo ligeramente alta ({rhr:.0f} bpm)")
        elif delta_rhr <= -2:
            signals.append(1); reasons.append(f"FC reposo baja ({rhr:.0f} bpm) — buena recuperación")
        else:
            signals.append(2)

    # ── Signal 2: Respiratory rate elevation ──────────────────
    resp = safe_num(row.get("resp_rate"))
    if resp is not None:
        delta_resp = resp - baseline_resp
        if delta_resp >= 2.0:
            signals.append(5); reasons.append(f"Frecuencia respiratoria alta ({resp:.1f} rpm)")
        elif delta_resp >= 1.0:
            signals.append(4)
        elif delta_resp >= 0.4:
            signals.append(3)
        else:
            signals.append(2)

    # ── Signal 3: Sleep efficiency drop ───────────────────────
    eff = safe_num(row.get("sleep_eff"))
    if eff is not None:
        delta_eff = baseline_eff - eff  # positive = worse than baseline
        if delta_eff >= 10:
            signals.append(5); reasons.append(f"Eficiencia sueño baja ({eff:.0f}%)")
        elif delta_eff >= 5:
            signals.append(4); reasons.append(f"Eficiencia sueño moderada ({eff:.0f}%)")
        elif delta_eff <= -3:
            signals.append(1); reasons.append(f"Sueño muy eficiente ({eff:.0f}%) ✅")
        else:
            signals.append(2)

    # ── Signal 4: Awake time during sleep ─────────────────────
    awake = safe_num(row.get("awake_hrs"))
    if awake is not None:
        if awake >= 1.5:
            signals.append(4); reasons.append(f"Mucho tiempo despierta de noche ({awake:.1f}h)")
        elif awake >= 1.0:
            signals.append(3)
        else:
            signals.append(2)

    # ── Signal 5: Weekend vs weekday (cortisol context) ────────
    if hasattr(row.get("date"), "dayofweek"):
        dow = row["date"].dayofweek
    else:
        try:
            dow = pd.to_datetime(row.get("date")).dayofweek
        except Exception:
            dow = 2  # default Wednesday
    if dow >= 5:  # weekend — lower baseline stress
        signals.append(1)
    else:
        signals.append(3)  # weekday — moderate baseline

    # ── Final score: weighted average, rounded to 1–5 ─────────
    if not signals:
        level = 3
    else:
        level = round(sum(signals) / len(signals))
        level = max(1, min(5, level))

    label_map = {
        1: "Muy baja 🟢",
        2: "Baja 🟢",
        3: "Moderada 🟡",
        4: "Alta 🟠",
        5: "Muy alta 🔴",
    }
    color_map = {1: C_GREEN, 2: C_GREEN, 3: C_YELLOW, 4: C_ORANGE, 5: C_RED}

    explanation = " · ".join(reasons) if reasons else "Calculado desde señales biométricas"

    return {
        "level":       level,
        "label":       label_map[level],
        "color":       color_map.get(level, C_YELLOW),
        "explanation": explanation,
    }

def compute_readiness(row: pd.Series, gp: dict, stress: int = 3) -> dict:
    score = 70.0

    sleep   = safe_num(row.get("total_sleep")) or 6.5
    deep    = safe_num(row.get("deep_sleep"))  or 1.0
    rem     = safe_num(row.get("rem_sleep"))   or 1.2
    s_eff   = safe_num(row.get("sleep_eff"))   or 86.0
    rhr_v   = safe_num(row.get("rhr"))
    resp_v  = safe_num(row.get("resp_rate"))

    # Sleep contribution
    score += (min(100, sleep / 8.0 * 100) - 70) * 0.35
    score += min(10, deep / 1.5 * 10)
    score += min(10, rem  / 1.8 * 10)
    score += (s_eff - 85) * 0.35 if s_eff else 0

    # RHR (baseline ~62 bpm for Ale)
    if rhr_v:
        score -= (rhr_v - 62) * 1.2

    # Respiratory rate (baseline ~14.5)
    if resp_v:
        score -= (resp_v - 14.5) * 3.0

    # Stress penalty
    score -= (stress - 3) * 6 * gp["recovery_weight"]

    # Goal aggression modifier
    score = score * (0.5 + 0.5 * gp["aggression"])
    score = max(5.0, min(100.0, score))

    if score >= 75:
        tier, color, label_es = "ÓPTIMA",   "#4ECFA0", "Óptima"
    elif score >= 55:
        tier, color, label_es = "MODERADA", "#FCD34D", "Moderada"
    else:
        tier, color, label_es = "BAJA",     "#F87171", "Baja"

    return {"score": round(score, 1), "tier": tier, "color": color, "label": label_es}


def recommend(readiness: dict, mins: int, moment: str, goal_key: str, stress: int) -> dict:
    score = readiness["score"]
    tier  = readiness["tier"]
    night = "noche" in moment.lower()

    if tier == "ÓPTIMA":
        if "30K" in goal_key or "Maratón" in goal_key:
            if mins >= 60:
                act  = "Rodaje de calidad 🏃"
                body = (f"Tu sueño y FC reposo están en verde. Corre {min(60, mins - 10)} min "
                        f"a ritmo conversacional–moderado (Z2–Z3). "
                        f"{'Evita series intensas de noche — el cortisol nocturno afecta el sueño.' if night else 'Puedes incluir 4×2 min a ritmo 10K si te sientes bien.'}")
            else:
                act  = "Trote corto Z2 🏃"
                body = f"{mins} min de trote fácil. Calidad > cantidad — mantén la FC bajo 145."
        elif "Hipertrofia" in goal_key:
            act  = "Pesas — sesión de volumen 💪"
            body = f"Tu recuperación es alta ({score:.0f}/100). Sesión de {mins} min con énfasis en compuestos: sentadilla, press, jalón. La creatina está trabajando hoy."
        else:
            act  = "Cardio o fuerza moderada ✅"
            body = f"Disposición alta — elige lo que más disfrutes. Tu cuerpo está listo."

    elif tier == "MODERADA":
        if stress >= 4 and night:
            act  = "Movilidad o yoga suave 🧘"
            body = ("El cortisol laboral + noche = riesgo de sueño fragmentado si entrenas duro. "
                    "30 min de movilidad o yoga restaurativo te descomprimirá sin sacrificar recuperación.")
        elif mins >= 45:
            act  = "Trote suave Z2 🏃"
            body = (f"{min(45, mins)} min a ritmo conversacional. "
                    "Zona 2 construye base aeróbica sin estresar el sistema nervioso simpático.")
        else:
            act  = "Caminata activa o pesas livianas 🚶"
            body = f"Muévete sin forzar. {mins} min de caminata rápida o circuito con cargas ligeras."

    else:
        act  = "Descanso activo 🛌"
        body = ("Tu cuerpo está en modo reparación — insistir hoy acumula deuda de fatiga. "
                "20–30 min de caminata suave o estiramientos. "
                "Recuerda: la creatina y beta-alanina solo dan resultado si hay recuperación real.")

    css_map = {"ÓPTIMA": "rec-go", "MODERADA": "rec-easy", "BAJA": "rec-rest"}
    return {"activity": act, "body": body, "css": css_map[tier]}


# ═══════════════════════════════════════════════════════════════
# AI INSIGHTS
# ═══════════════════════════════════════════════════════════════

def get_ai_insights(df: pd.DataFrame, goal: str, score: float) -> list:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return []
    try:
        import urllib.request
        r30 = df.tail(30)
        avg_sleep = safe_num(r30["total_sleep"].mean()) or 0
        avg_deep  = safe_num(r30["deep_sleep"].mean())  or 0
        avg_rhr   = safe_num(r30["rhr"].dropna().mean()) or 0
        avg_steps = safe_num(r30["steps"].mean()) or 0
        avg_cal   = safe_num(r30["active_kcal"].mean()) or 0

        prompt = f"""Eres el coach de rendimiento de Alejandra Eugenia Guzmán Morros, 29 años, Caracas, Venezuela.
Es Senior Manager con alto desgaste cognitivo. Su meta actual: {goal}.
Usa creatina y beta-alanina.

Promedios reales de sus últimos 30 días:
- Sueño total: {avg_sleep:.1f} h/noche
- Sueño profundo: {avg_deep:.1f} h
- FC reposo: {avg_rhr:.0f} bpm
- Pasos/día: {avg_steps:.0f}
- Calorías activas: {avg_cal:.0f} kcal
- Score de disposición hoy: {score:.0f}/100

Genera exactamente 3 insights poderosos y personalizados para este mes.
Cada uno debe: ser específico a sus números, conectar estrés laboral con recuperación, dar acción concreta.

Responde ÚNICAMENTE en JSON válido, sin texto adicional, sin bloques de código:
{{"insights":[{{"tag":"LOGRO","color":"green","text":"..."}},{{"tag":"PATRÓN","color":"blue","text":"..."}},{{"tag":"ACCIÓN","color":"orange","text":"..."}}]}}"""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
        req  = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Strip markdown code fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw).get("insights", [])
    except Exception:
        return []


def static_insights(df: pd.DataFrame, goal: str, score: float) -> list:
    r30       = df.tail(30)
    avg_sleep = safe_num(r30["total_sleep"].mean()) or 7.0
    avg_rhr   = safe_num(r30["rhr"].dropna().mean()) or 62.0
    avg_deep  = safe_num(r30["deep_sleep"].mean())  or 1.2

    if avg_sleep >= 7.5:
        s_text = (f"Promediaste {avg_sleep:.1f}h de sueño — por encima del umbral mínimo. "
                  "Esto maximiza la síntesis de creatina y la consolidación neuromotora para tus rodajes.")
    else:
        s_text = (f"Tu promedio de {avg_sleep:.1f}h está bajo las 8h ideales para tu carga laboral. "
                  "Cada hora menos eleva el cortisol ~15%, bloqueando parcialmente la recuperación muscular.")

    rhr_text = (f"Tu FC reposo de {avg_rhr:.0f} bpm es tu termómetro diario de recuperación. "
                "Si sube >4–5 bpm sobre tu línea base, tu sistema nervioso aún está procesando el estrés acumulado — ese día, reduce la intensidad.")

    if "30K" in goal:
        g_text = ("Para el 30K de Septiembre, el volumen de rodaje debe escalar ~10% por semana con una semana de descarga cada 4. "
                  "Con tu ritmo de Senior Manager, los miércoles y viernes son tus días de mayor cortisol — programa sesiones suaves esos días.")
    else:
        g_text = (f"Para tu meta ({goal}), el descanso activo no es debilidad — es parte del protocolo. "
                  "La beta-alanina acumula su efecto en 4–6 semanas de uso consistente.")

    return [
        {"tag": "SUEÑO",    "color": "blue",   "text": s_text},
        {"tag": "FC BASAL", "color": "green",  "text": rhr_text},
        {"tag": "META",     "color": "orange", "text": g_text},
    ]



# ═══════════════════════════════════════════════════════════════
# WEEKLY SUMMARY + AI QUICK TIP
# ═══════════════════════════════════════════════════════════════

def weekly_stats(df: pd.DataFrame) -> dict:
    """Calculate this week vs last week stats from the dataframe."""
    today = pd.Timestamp.now().normalize()
    week_start = today - pd.Timedelta(days=today.dayofweek)      # Monday this week
    prev_start = week_start - pd.Timedelta(weeks=1)

    this_week = df[df["date"] >= week_start]
    last_week = df[(df["date"] >= prev_start) & (df["date"] < week_start)]

    def avg(d, col):
        if col not in d.columns or d.empty:
            return None
        return safe_num(d[col].mean())

    def pct_delta(curr, prev):
        if curr is None or prev is None or prev == 0:
            return None
        return round((curr - prev) / prev * 100, 1)

    def arrow(val):
        if val is None:
            return ""
        return "▲" if val >= 0 else "▼"

    curr_sleep = avg(this_week, "total_sleep")
    prev_sleep = avg(last_week, "total_sleep")
    curr_deep  = avg(this_week, "deep_sleep")
    prev_deep  = avg(last_week, "deep_sleep")
    curr_rhr   = avg(this_week, "rhr")
    prev_rhr   = avg(last_week, "rhr")
    curr_steps = avg(this_week, "steps")
    prev_steps = avg(last_week, "steps")
    curr_cal   = avg(this_week, "active_kcal")
    prev_cal   = avg(last_week, "active_kcal")
    curr_eff   = avg(this_week, "sleep_eff")
    prev_eff   = avg(last_week, "sleep_eff")
    curr_rem   = avg(this_week, "rem_sleep")
    prev_rem   = avg(last_week, "rem_sleep")

    # Readiness trend this week
    scores_this = []
    for _, row in this_week.iterrows():
        scores_this.append(compute_readiness(row, gp, 3)["score"])
    avg_readiness = round(sum(scores_this) / len(scores_this), 1) if scores_this else None

    return {
        "sleep":      curr_sleep,   "sleep_delta":  round((curr_sleep or 0) - (prev_sleep or 0), 2),
        "deep":       curr_deep,    "deep_delta":   round((curr_deep  or 0) - (prev_deep  or 0), 2),
        "rem":        curr_rem,     "rem_delta":    round((curr_rem   or 0) - (prev_rem   or 0), 2),
        "sleep_eff":  curr_eff,     "eff_delta":    round((curr_eff   or 0) - (prev_eff   or 0), 1),
        "rhr":        curr_rhr,     "rhr_delta":    round((curr_rhr   or 0) - (prev_rhr   or 0), 1),
        "steps":      curr_steps,   "steps_delta":  round((curr_steps or 0) - (prev_steps or 0), 0),
        "cal":        curr_cal,     "cal_delta":    round((curr_cal   or 0) - (prev_cal   or 0), 1),
        "readiness":  avg_readiness,
        "n_days":     len(this_week),
        "arrow": arrow,
    }


def build_conclusion(stats: dict, tab: str, goal: str) -> str:
    """Build a data-driven conclusion string for each tab."""
    a = stats["arrow"]
    n = stats["n_days"]
    days_word = f"{'hoy' if n == 1 else f'los últimos {n} días'}"

    if tab == "readiness":
        r = stats["readiness"]
        sl = stats["sleep"]
        rhr = stats["rhr"]
        rd = stats["rhr_delta"]
        conclusion = f"Tu score promedio esta semana fue <b>{r if r else '—'}/100</b>. "
        if sl and sl < 7:
            conclusion += f"Dormiste un promedio de <b>{sl:.1f}h</b> — por debajo del umbral de recuperación óptima (7.5h+). "
        elif sl:
            conclusion += f"Tu sueño de <b>{sl:.1f}h promedio</b> está sosteniendo bien tu disposición. "
        if rhr and rd:
            if rd > 2:
                conclusion += f"Tu FC reposo subió <b>{rd:+.1f} bpm</b> vs la semana pasada — señal de fatiga acumulada."
            elif rd < -2:
                conclusion += f"Tu FC reposo bajó <b>{rd:+.1f} bpm</b> vs la semana pasada — buena señal de recuperación."
            else:
                conclusion += f"Tu FC reposo se mantuvo estable en <b>{rhr:.0f} bpm</b>."

    elif tab == "sleep":
        sl   = stats["sleep"]
        sd   = stats["sleep_delta"]
        deep = stats["deep"]
        dd   = stats["deep_delta"]
        rem  = stats["rem"]
        eff  = stats["sleep_eff"]
        conclusion = f"Dormiste un promedio de <b>{sl:.1f}h</b> esta semana "
        if sd and abs(sd) > 0.1:
            conclusion += f"(<b>{a(sd)}{abs(sd):.1f}h</b> vs semana pasada). "
        else:
            conclusion += "(similar a la semana pasada). "
        if deep:
            conclusion += f"Sueño profundo: <b>{deep:.1f}h</b>"
            if dd and dd < -0.2:
                conclusion += f" — bajó {abs(dd):.1f}h, lo que puede explicar sensación de fatiga al despertar. "
            elif dd and dd > 0.2:
                conclusion += f" — mejoró {dd:.1f}h 💪. "
            else:
                conclusion += ". "
        if eff:
            conclusion += f"Eficiencia del sueño: <b>{eff:.1f}%</b>{'  ✅' if eff >= 88 else ' — hay margen de mejora'}."

    elif tab == "load":
        cal   = stats["cal"]
        cd    = stats["cal_delta"]
        steps = stats["steps"]
        sd    = stats["steps_delta"]
        rhr   = stats["rhr"]
        rd    = stats["rhr_delta"]
        conclusion = f"Promediaste <b>{cal:.0f} kcal activas/día</b> esta semana"
        if cd and abs(cd) > 20:
            conclusion += f" ({a(cd)}{abs(cd):.0f} kcal vs semana pasada)"
        conclusion += f". Pasos: <b>{steps:.0f}/día</b>. "
        if rhr and rd:
            if rd > 3:
                conclusion += f"⚠️ Tu FC reposo subió <b>{rd:.0f} bpm</b> — la carga puede estar superando tu recuperación."
            elif rd < -2:
                conclusion += f"✅ Tu FC reposo bajó <b>{abs(rd):.0f} bpm</b> — tu cuerpo está absorbiendo bien la carga."
            else:
                conclusion += "Tu FC reposo se mantuvo estable — buena señal de equilibrio entre carga y recuperación."

    elif tab == "energy":
        sl  = stats["sleep"]
        cal = stats["cal"]
        conclusion = f"Esta semana, con <b>{sl:.1f}h de sueño promedio</b>, generaste <b>{cal:.0f} kcal activas/día</b>. "
        if sl and cal:
            if sl >= 7.5 and cal >= 400:
                conclusion += "La correlación es positiva — tu sueño está traduciendo en energía real al día siguiente. Sigue así."
            elif sl < 7:
                conclusion += "Con menos de 7h de sueño, tu energía activa tiende a caer. El gráfico probablemente lo confirma."
            else:
                conclusion += "El gráfico te muestra qué noches de sueño se tradujeron en más movimiento al día siguiente."

    elif tab == "correlation":
        conclusion = "La matriz muestra cómo se relacionan tus variables esta semana. "
        sl  = stats["sleep"]
        rhr = stats["rhr"]
        if sl and rhr:
            conclusion += f"Con {sl:.1f}h de sueño y FC reposo de {rhr:.0f} bpm, "
            if sl >= 7.5 and rhr <= 65:
                conclusion += "tus dos indicadores principales están en zona verde — tu cuerpo responde bien."
            elif sl < 7 or rhr > 68:
                conclusion += "hay margen de mejora en recuperación que el mapa de calor probablemente refleja."
            else:
                conclusion += "estás en zona de equilibrio."

    return conclusion


def get_ai_tip(tab: str, conclusion: str, stats: dict, goal: str) -> str:
    """Call Gemini Flash for a personalized quick tip based on the tab data."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return ""
    try:
        import urllib.request
        prompt = f"""Eres el coach personal de Alejandra (29 años, Senior Manager, Caracas). Meta: {goal}.
Aquí está el resumen de su semana para la pestaña de {tab}:
{conclusion}

Genera UN quick tip accionable, específico, de máximo 2 oraciones. 
Conéctalo con su estrés laboral, creatina o beta-alanina si es relevante.
Tono: directo, cálido, como un coach experto. Solo el tip, sin introducción."""

        url  = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
        req  = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return ""


STATIC_TIPS = {
    "readiness": "Si tu score es moderado o bajo varios días seguidos, es señal de deuda de recuperación — no de falta de disciplina. Prioriza el sueño antes de aumentar la carga.",
    "sleep":     "Acostarte 30 min antes durante 5 noches seguidas tiene más impacto en tu sueño profundo que cualquier suplemento. La consistencia del horario de sueño regula tu ritmo circadiano.",
    "load":      "Si tu FC reposo sube mientras tu actividad también sube, insertá un día de descanso activo (caminata, movilidad) antes de que la fatiga se acumule y te frene por más tiempo.",
    "energy":    "La beta-alanina mejora el rendimiento en esfuerzos de 1–4 min — como series de velocidad. Para rodajes largos Z2, el impacto es menor. Úsala estratégicamente en días de calidad.",
    "correlation": "La variable con mayor correlación con tu rendimiento es la que más vale proteger. Si el sueño profundo lidera, ese es tu palanca principal — todo lo demás gira alrededor de él.",
}


def render_weekly_block(tab_key: str, stats: dict, goal: str):
    """Render the conclusion + quick tip block for a tab."""
    conclusion = build_conclusion(stats, tab_key, goal)
    
    # Try AI tip, fallback to static
    ai_tip = get_ai_tip(tab_key, conclusion, stats, goal)
    tip = ai_tip if ai_tip else STATIC_TIPS.get(tab_key, "")

    st.markdown(
        f"<div style='background:#18191F;border:1px solid #2A2D3A;border-radius:16px;"
        f"padding:20px 24px;margin-top:16px;'>"
        f"<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;"
        f"color:#5A5D70;margin-bottom:10px;'>📊 ESTA SEMANA</div>"
        f"<div style='font-size:13px;color:#9DA0B0;line-height:1.7;margin-bottom:14px;'>{conclusion}</div>"
        f"<div style='border-top:1px solid #2A2D3A;padding-top:12px;'>"
        f"<div style='font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;"
        f"color:#A78BFA;margin-bottom:8px;'>💡 QUICK TIP</div>"
        f"<div style='font-size:13px;color:#C8CAD8;line-height:1.7;'>{tip}</div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
# CHART HELPERS
# ═══════════════════════════════════════════════════════════════

BG   = "#111318"
CARD = "#18191F"
GRID = "#2A2D3A"
C_GREEN  = "#4ECFA0"
C_BLUE   = "#5B9CF6"
C_PURPLE = "#A78BFA"
C_ORANGE = "#FB923C"
C_PINK   = "#F472B6"
C_RED    = "#F87171"
C_YELLOW = "#FCD34D"

def base_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter", size=14, color="#8B8EA0")),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family="Inter", color="#8B8EA0", size=11),
        xaxis=dict(gridcolor=GRID, linecolor=GRID, zeroline=False),
        yaxis=dict(gridcolor=GRID, linecolor=GRID, zeroline=False),
        margin=dict(l=40, r=24, t=44, b=32),
        hovermode="x unified",
        legend=dict(bgcolor=CARD, bordercolor=GRID, borderwidth=1, font=dict(size=11)),
    )
    return fig


# ── Chart 1: Readiness history ────────────────────────────────
def chart_readiness(df: pd.DataFrame, gp: dict) -> go.Figure:
    scores, colors = [], []
    for _, row in df.iterrows():
        r = compute_readiness(row, gp, stress_level)
        scores.append(r["score"])
        colors.append(r["color"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=scores,
        mode="lines", name="Score",
        line=dict(color=C_PURPLE, width=2),
        fill="tozeroy",
        fillcolor="rgba(167,139,250,0.07)",
        hovertemplate="<b>%{x|%d %b}</b><br>Score: %{y:.0f}/100<extra></extra>",
    ))
    for y_val, label, color in [(75, "Óptima ≥75", C_GREEN), (55, "Moderada ≥55", C_YELLOW)]:
        fig.add_hline(y=y_val, line_dash="dot", line_color=color, opacity=0.45,
                      annotation_text=label, annotation_font_color=color,
                      annotation_position="right")
    fig.update_yaxes(range=[0, 105])
    return base_layout(fig, "Score de Disposición Diario")


# ── Chart 2: Sleep breakdown ──────────────────────────────────
def chart_sleep(df: pd.DataFrame) -> go.Figure:
    d = df.dropna(subset=["total_sleep"])
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d["date"], y=d["deep_sleep"].fillna(0),  name="Profundo",  marker_color=C_PURPLE))
    fig.add_trace(go.Bar(x=d["date"], y=d["rem_sleep"].fillna(0),   name="REM",       marker_color=C_BLUE))
    fig.add_trace(go.Bar(x=d["date"], y=d["awake_hrs"].fillna(0),   name="Despierta", marker_color="rgba(248,113,113,0.45)"))
    fig.update_layout(barmode="stack")
    fig.add_hline(y=8, line_dash="dot", line_color=C_GREEN, opacity=0.4,
                  annotation_text="8h objetivo", annotation_font_color=C_GREEN)
    return base_layout(fig, "Arquitectura del Sueño")


# ── Chart 3: Activity vs RHR ──────────────────────────────────
def chart_load_recovery(df: pd.DataFrame) -> go.Figure:
    d = df.copy()
    d["rhr_roll"] = d["rhr"].rolling(7, min_periods=2).mean()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=d["date"], y=d["active_kcal"].fillna(0),
        name="Cal. activas", marker_color="rgba(91,156,246,0.45)",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=d["date"], y=d["rhr_roll"],
        name="FC Reposo (7d)", mode="lines",
        line=dict(color=C_PINK, width=2),
    ), secondary_y=True)
    fig.update_yaxes(title_text="Calorías activas", gridcolor=GRID, secondary_y=False)
    fig.update_yaxes(title_text="FC Reposo (bpm)", gridcolor=GRID, secondary_y=True)
    fig.update_layout(
        paper_bgcolor=CARD, plot_bgcolor=CARD,
        font=dict(family="Inter", color="#8B8EA0", size=11),
        margin=dict(l=40, r=60, t=44, b=32),
        hovermode="x unified",
        legend=dict(bgcolor=CARD, bordercolor=GRID),
        title=dict(text="Carga de Actividad vs FC Reposo", font=dict(size=14, color="#8B8EA0")),
    )
    return fig


# ── Chart 4: Sleep vs next-day energy scatter ─────────────────
def chart_sleep_energy(df: pd.DataFrame) -> go.Figure:
    d = df.copy()
    d["next_active"] = d["active_kcal"].shift(-1)
    d = d.dropna(subset=["total_sleep", "next_active"])
    d["is_weekend"] = d["date"].dt.dayofweek >= 5

    fig = go.Figure()
    for is_wk, color, label in [(True, C_GREEN, "Fin de semana"), (False, C_PURPLE, "Días laborales")]:
        sub = d[d["is_weekend"] == is_wk]
        fig.add_trace(go.Scatter(
            x=sub["total_sleep"], y=sub["next_active"],
            mode="markers", name=label,
            marker=dict(color=color, size=8, opacity=0.7,
                        line=dict(width=1, color=CARD)),
            text=sub["date"].dt.strftime("%d %b"),
            hovertemplate="<b>%{text}</b><br>Sueño: %{x:.1f}h → Energía día sig: %{y:.0f} kcal<extra></extra>",
        ))

    # Trend line
    clean = d[["total_sleep","next_active"]].dropna()
    if len(clean) > 3:
        z = np.polyfit(clean["total_sleep"], clean["next_active"], 1)
        p = np.poly1d(z)
        xs = np.linspace(clean["total_sleep"].min(), clean["total_sleep"].max(), 50)
        fig.add_trace(go.Scatter(
            x=xs, y=p(xs), mode="lines", name="Tendencia",
            line=dict(dash="dash", color=C_YELLOW, width=1.5),
            hoverinfo="skip",
        ))

    fig.update_xaxes(title_text="Horas de sueño")
    fig.update_yaxes(title_text="Calorías activas día siguiente (kcal)")
    return base_layout(fig, "Sueño → Energía del día siguiente")


# ── Chart 5: Correlation matrix ───────────────────────────────
def chart_correlation(df: pd.DataFrame) -> go.Figure:
    cols = {
        "total_sleep": "Sueño",
        "deep_sleep":  "Prof.",
        "rem_sleep":   "REM",
        "rhr":         "FC Rep.",
        "active_kcal": "Cal. Act.",
        "steps":       "Pasos",
    }
    sub = df[[c for c in cols if c in df.columns]].dropna(how="all")
    sub = sub.rename(columns=cols)
    corr = sub.corr()

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale=[[0, C_RED], [0.5, CARD], [1, C_GREEN]],
        zmid=0, zmin=-1, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}",
        textfont=dict(size=11, color="#E4E6EF"),
        hovertemplate="%{y} ↔ %{x}: <b>%{z:.2f}</b><extra></extra>",
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#8B8EA0"),
            outlinecolor=GRID,
            len=0.8,
        ),
    ))
    fig.update_layout(
        paper_bgcolor=CARD, plot_bgcolor=CARD,
        font=dict(family="Inter", color="#8B8EA0", size=11),
        margin=dict(l=60, r=24, t=44, b=60),
        title=dict(text="Matriz de Correlación entre Variables", font=dict(size=14, color="#8B8EA0")),
        xaxis=dict(tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚡ AI Better Coach")
    st.markdown("<p style='font-size:12px;margin-top:-8px;color:#3A3D4A;'>Alejandra · Caracas 🇻🇪</p>", unsafe_allow_html=True)

    st.markdown("<div class='sb-label'>🎯 Meta actual</div>", unsafe_allow_html=True)
    goal_key = st.selectbox("Meta", list(GOALS.keys()), label_visibility="collapsed")
    gp = GOALS[goal_key]
    st.markdown(f"<p style='font-size:11px;color:#3A3D4A;line-height:1.5;'>{gp['description']}</p>", unsafe_allow_html=True)

    st.markdown("<div class='sb-label'>📋 Decisor de hoy</div>", unsafe_allow_html=True)
    time_avail   = st.slider("Tiempo disponible (min)", 15, 120, 60, step=15)
    time_of_day  = st.radio("¿Cuándo entrenas?", ["Mañana", "Tarde", "Noche"])

    st.markdown("<div class='sb-label'>📊 Ventana de análisis</div>", unsafe_allow_html=True)
    window_sel = st.selectbox("Período", ["Últimos 30 días", "Últimos 60 días", "Todo el historial"],
                               label_visibility="collapsed")
    window = {"Últimos 30 días": 30, "Últimos 60 días": 60, "Todo el historial": 9999}[window_sel]

    st.markdown("---")
    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════

df_all, data_source = get_data()
df_win = df_all.tail(window).copy() if len(df_all) > 0 else df_all

# Latest rows — look back up to 7 days for valid data
def last_valid_row(df, cols):
    """Return the most recent row that has at least one of cols non-null."""
    for _, row in df.iloc[::-1].iterrows():
        if any(safe_num(row.get(c)) is not None for c in cols):
            return row
    return df.iloc[-1] if len(df) > 0 else pd.Series()

today_row = last_valid_row(df_all, ["total_sleep", "rhr", "active_kcal"])
prev_row  = df_all.iloc[-3] if len(df_all) > 2 else today_row

# Compute stress automatically from biometric data
stress_data  = compute_stress_from_data(today_row, df_all)
stress_level = stress_data["level"]

readiness   = compute_readiness(today_row, gp, stress_level)
readiness_p = compute_readiness(prev_row,  gp, stress_level)
rec         = recommend(readiness, time_avail, time_of_day, goal_key, stress_level)


# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.markdown(f"## ⚡ AI Better Coach")
    st.markdown(
        f"<p style='margin-top:-10px;font-size:13px;color:#5A5D70;'>"
        f"{datetime.now().strftime('%A %d de %B, %Y')} · "
        f"Meta: <span style='color:#A78BFA;font-weight:600;'>{goal_key}</span>"
        f"</p>",
        unsafe_allow_html=True,
    )
with hcol2:
    st.markdown(
        f"<p style='text-align:right;font-size:11px;color:#3A3D4A;padding-top:14px;'>{data_source}</p>",
        unsafe_allow_html=True,
    )

# Show auto-computed stress as a visible indicator below header
scol1, scol2, scol3 = st.columns([1, 1, 2])
with scol1:
    s_color = stress_data["color"]
    s_label = stress_data["label"]
    s_expl  = stress_data["explanation"]
    st.markdown(
        f"<div class='oura-card' style='border-top:2px solid {s_color};padding:16px 20px;'>"
        f"<div class='oura-label'>🧠 Estrés biométrico</div>"
        f"<div style='font-size:22px;font-weight:700;color:{s_color};'>{s_label}</div>"
        f"<div class='oura-sub' style='margin-top:6px;font-size:11px;'>{s_expl}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
with scol2:
    dow_names = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    try:
        dow_label = dow_names[pd.to_datetime(today_row.get("date")).dayofweek]
    except Exception:
        dow_label = datetime.now().strftime("%A")
    is_wknd = dow_label in ["Sábado","Domingo"]
    context_label = "Fin de semana 🌿" if is_wknd else "Día laboral 💼"
    context_color = C_GREEN if is_wknd else C_ORANGE
    st.markdown(
        f"<div class='oura-card' style='border-top:2px solid {context_color};padding:16px 20px;'>"
        f"<div class='oura-label'>📅 Contexto</div>"
        f"<div style='font-size:22px;font-weight:700;color:{context_color};'>{context_label}</div>"
        f"<div class='oura-sub' style='margin-top:6px;font-size:11px;'>{dow_label} · El algoritmo ajusta según el día</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
with scol3:
    st.markdown(
        f"<div class='oura-card' style='border-top:2px solid #2A2D3A;padding:16px 20px;'>"
        f"<div class='oura-label'>ℹ️ Cómo se calcula el estrés</div>"
        f"<div style='font-size:12px;color:#5A5D70;line-height:1.7;'>"
        f"La app calcula tu nivel de estrés biológico automáticamente cruzando: "
        f"<b style='color:#8B8EA0'>FC reposo vs tu base personal</b>, "
        f"<b style='color:#8B8EA0'>frecuencia respiratoria</b>, "
        f"<b style='color:#8B8EA0'>eficiencia del sueño</b> y "
        f"<b style='color:#8B8EA0'>tiempo despierta de noche</b>. Sin sesgos subjetivos."
        f"</div></div>",
        unsafe_allow_html=True,
    )
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ROW 1: GAUGE + RECOMMENDATION + 3 KPIs
# ═══════════════════════════════════════════════════════════════

col_g, col_r = st.columns([1, 2])

with col_g:
    score_val = readiness["score"]
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_val,
        number={
            "font": {"family": "JetBrains Mono", "size": 52, "color": readiness["color"]},
            "suffix": "",
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": GRID,
                "tickfont": {"size": 9, "color": "#5A5D70"},
                "nticks": 6,
            },
            "bar": {"color": readiness["color"], "thickness": 0.25},
            "bgcolor": CARD,
            "borderwidth": 0,
            "steps": [
                {"range": [0,  55], "color": "rgba(248,113,113,0.08)"},
                {"range": [55, 75], "color": "rgba(252,211,77,0.08)"},
                {"range": [75, 100],"color": "rgba(78,207,160,0.08)"},
            ],
            "threshold": {
                "line": {"color": readiness["color"], "width": 3},
                "thickness": 0.85,
                "value": score_val,
            },
        },
        title={
            "text": "DISPOSICIÓN HOY",
            "font": {"family": "Inter", "size": 11, "color": "#5A5D70"},
            "align": "center",
        },
    ))
    gauge.update_layout(
        paper_bgcolor=CARD,
        font={"family": "Inter"},
        height=230,
        margin=dict(l=16, r=16, t=36, b=8),
    )
    st.markdown("<div class='score-wrap'>", unsafe_allow_html=True)
    st.plotly_chart(gauge, use_container_width=True)
    delta = readiness["score"] - readiness_p["score"]
    arrow = "▲" if delta >= 0 else "▼"
    cls   = "oura-delta-up" if delta >= 0 else "oura-delta-down"
    st.markdown(
        f"<p style='text-align:center;margin-top:-12px;'>"
        f"<span class='{cls}'>{arrow} {abs(delta):.1f} pts vs antes de ayer</span>"
        f"</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    # Recommendation
    st.markdown(
        f"<div class='rec-card {rec['css']}'>"
        f"<div class='rec-title'>{rec['activity']}</div>"
        f"<div class='rec-body'>{rec['body']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # 3 KPI cards
    k1, k2, k3 = st.columns(3)

    sleep_v = safe_num(today_row.get("total_sleep"))
    deep_v  = safe_num(today_row.get("deep_sleep")) or 0.0
    rem_v   = safe_num(today_row.get("rem_sleep"))  or 0.0
    rhr_v   = safe_num(today_row.get("rhr"))
    steps_v = safe_num(today_row.get("steps"))

    with k1:
        st.markdown(
            f"<div class='oura-card oura-card-accent-blue'>"
            f"<div class='oura-label'>🌙 Sueño</div>"
            f"<div class='oura-value'>{fmt(sleep_v, 1)}<span>h</span></div>"
            f"<div class='oura-sub'>Prof: {fmt(deep_v,1)}h · REM: {fmt(rem_v,1)}h</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"<div class='oura-card oura-card-accent-pink'>"
            f"<div class='oura-label'>❤️ FC Reposo</div>"
            f"<div class='oura-value'>{fmt(rhr_v, 0)}<span>bpm</span></div>"
            f"<div class='oura-sub'>Base Ale: ~62 bpm</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with k3:
        target = gp["target_steps"]
        pct    = (steps_v / target * 100) if steps_v else 0
        st.markdown(
            f"<div class='oura-card oura-card-accent-green'>"
            f"<div class='oura-label'>👟 Pasos</div>"
            f"<div class='oura-value'>{fmt(steps_v, 0)}</div>"
            f"<div class='oura-sub'>Meta: {target:,} · {min(pct,100):.0f}% completado</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<div class='sec-label'>✨ Insights del mes</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ROW 2: INSIGHTS
# ═══════════════════════════════════════════════════════════════

with st.spinner("Analizando tu historial..."):
    ai_ins = get_ai_insights(df_all, goal_key, readiness["score"])

insights = ai_ins if ai_ins else static_insights(df_all, goal_key, readiness["score"])

color_map = {"green": "insight-tag-green", "blue": "insight-tag-blue", "orange": "insight-tag-orange"}
ic1, ic2, ic3 = st.columns(3)
for col, ins in zip([ic1, ic2, ic3], insights[:3]):
    tag_cls = color_map.get(ins.get("color", ""), "insight-tag")
    with col:
        st.markdown(
            f"<div class='insight-wrap'>"
            f"<div class='insight-tag {tag_cls}'>{ins['tag']}</div>"
            f"<div class='insight-text'>{ins['text']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

if not ai_ins:
    st.markdown(
        "<p style='font-size:11px;color:#3A3D4A;margin-top:6px;'>"
        "💡 Agrega <code>GEMINI_API_KEY</code> como variable de entorno para insights personalizados con Gemini AI en tiempo real."
        "</p>",
        unsafe_allow_html=True,
    )


st.markdown("<div class='sec-label'>📈 Análisis de rendimiento</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ROW 3: CHARTS (5 TABS)
# ═══════════════════════════════════════════════════════════════


# Compute weekly stats for all tabs
wstats = weekly_stats(df_win)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Disposición",
    "💤 Sueño",
    "⚡ Carga vs Recuperación",
    "🔗 Sueño → Energía",
    "📊 Correlaciones",
])

with tab1:
    if len(df_win) > 1:
        st.plotly_chart(chart_readiness(df_win, gp), use_container_width=True)
        # Weekly summary table
        dw = df_win.copy()
        dw["semana"] = dw["date"].dt.isocalendar().week.astype(str)
        wk = dw.groupby("semana").agg(
            Sueño_h=("total_sleep", "mean"),
            Pasos=("steps", "mean"),
            Cal_activas=("active_kcal", "mean"),
            FC_reposo=("rhr", "mean"),
        ).tail(4).round(1)
        wk.index = [f"Sem {i}" for i in wk.index]
        st.dataframe(wk, use_container_width=True)
        render_weekly_block('readiness', wstats, goal_key)
    else:
        st.info("No hay suficientes datos para este período.")

with tab2:
    if len(df_win) > 1:
        st.plotly_chart(chart_sleep(df_win), use_container_width=True)
        s1, s2 = st.columns(2)
        with s1:
            avg_t = safe_num(df_win["total_sleep"].mean()) or 0
            avg_d = safe_num(df_win["deep_sleep"].mean())  or 0
            avg_r = safe_num(df_win["rem_sleep"].mean())   or 0
            st.markdown(
                f"<div class='oura-card oura-card-accent-blue'>"
                f"<div class='oura-label'>Promedios del período</div>"
                f"<div style='font-size:13px;color:#9DA0B0;line-height:2;'>"
                f"🌙 Total: <b style='color:#E4E6EF'>{avg_t:.1f}h</b><br>"
                f"🔵 Profundo: <b style='color:#E4E6EF'>{avg_d:.1f}h</b> ({avg_d/avg_t*100 if avg_t else 0:.0f}%)<br>"
                f"🟣 REM: <b style='color:#E4E6EF'>{avg_r:.1f}h</b> ({avg_r/avg_t*100 if avg_t else 0:.0f}%)"
                f"</div></div>",
                unsafe_allow_html=True,
            )
        with s2:
            avg_eff  = safe_num(df_win["sleep_eff"].mean()) or 0
            pct_deep = (df_win["deep_sleep"].dropna() >= 1.5).mean() * 100
            st.markdown(
                f"<div class='oura-card oura-card-accent-purple'>"
                f"<div class='oura-label'>Calidad del sueño</div>"
                f"<div style='font-size:13px;color:#9DA0B0;line-height:2;'>"
                f"✅ Eficiencia prom: <b style='color:#E4E6EF'>{avg_eff:.1f}%</b><br>"
                f"🔵 Noches ≥1.5h profundo: <b style='color:#E4E6EF'>{pct_deep:.0f}%</b><br>"
                f"🎯 Meta: <b style='color:#E4E6EF'>90%+ eficiencia</b>"
                f"</div></div>",
                unsafe_allow_html=True,
            )
        render_weekly_block('sleep', wstats, goal_key)
    else:
        st.info("No hay suficientes datos para este período.")

with tab3:
    if len(df_win) > 1:
        st.plotly_chart(chart_load_recovery(df_win), use_container_width=True)
        st.markdown(
            "<div class='insight-wrap'>"
            "<div class='insight-tag insight-tag-blue'>CÓMO LEERLO</div>"
            "<div class='insight-text'>Cuando las barras azules (actividad) suben varios días seguidos "
            "y la línea rosa (FC reposo) también sube, tu cuerpo acumula fatiga. "
            "Si tu FC reposo sube >4 bpm sobre tu base de ~62 bpm, tu sistema nervioso pide descanso "
            "antes de que tú lo sientas. La creatina atenúa el estrés muscular, pero no el neurológico.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        render_weekly_block('load', wstats, goal_key)
    else:
        st.info("No hay suficientes datos para este período.")

with tab4:
    if len(df_win) > 5:
        st.plotly_chart(chart_sleep_energy(df_win), use_container_width=True)
        st.markdown(
            "<div class='insight-wrap'>"
            "<div class='insight-tag insight-tag-green'>CORRELACIÓN</div>"
            "<div class='insight-text'>Cada punto es un día. La línea amarilla muestra si dormir más "
            "se traduce en más energía activa al día siguiente. "
            "Los puntos verdes (fin de semana) vs morados (días laborales) revelan el impacto real "
            "del cortisol laboral en tu movimiento diario.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        render_weekly_block('energy', wstats, goal_key)
    else:
        st.info("No hay suficientes datos para este período.")

with tab5:
    clean = df_win[["total_sleep","deep_sleep","rem_sleep","rhr","active_kcal","steps"]].dropna(how="all")
    if len(clean) > 5:
        st.plotly_chart(chart_correlation(df_win), use_container_width=True)
        st.markdown(
            "<div class='insight-wrap'>"
            "<div class='insight-tag insight-tag-orange'>GUÍA DE LECTURA</div>"
            "<div class='insight-text'>"
            "<b style='color:#E4E6EF'>Verde (+1)</b> = relación positiva fuerte · "
            "<b style='color:#E4E6EF'>Rojo (−1)</b> = relación inversa fuerte · "
            "<b style='color:#E4E6EF'>Gris (0)</b> = sin correlación. "
            "Ejemplo: si Sueño y Cal. Act. tienen correlación positiva, dormir más = más energía al día siguiente."
            "</div></div>",
            unsafe_allow_html=True,
        )
        render_weekly_block('correlation', wstats, goal_key)
    else:
        st.info("No hay suficientes datos para calcular correlaciones en este período.")


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:11px;color:#2A2D3A;padding:8px 0;'>"
    "AI Better Coach · Alejandra Eugenia Guzmán Morros · "
    "Garmin + Oura via Apple Health · Motor de disposición basado en sueño, FC reposo y carga laboral"
    "</p>",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════
# WEEKLY CONCLUSION + QUICK TIP ENGINE
# ═══════════════════════════════════════════════════════════════
