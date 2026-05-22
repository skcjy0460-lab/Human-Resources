import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
import io
from datetime import datetime, date, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="병원 인사관리 시스템",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 메인 배경 */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8eef5 100%);
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2744 0%, #0f1c35 100%);
        border-right: none;
    }
    section[data-testid="stSidebar"] * {
        color: #e0e8f0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #a0b4cc !important;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* 헤더 카드 */
    .header-card {
        background: linear-gradient(135deg, #1a2744 0%, #2d4a7a 100%);
        border-radius: 16px;
        padding: 28px 36px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(26,39,68,0.18);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .header-card h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .header-card p {
        font-size: 0.9rem;
        opacity: 0.7;
        margin: 4px 0 0 0;
    }

    /* KPI 카드 */
    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 5px solid;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6b7280;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a2744;
        line-height: 1;
    }
    .kpi-sub {
        font-size: 0.82rem;
        color: #9ca3af;
        margin-top: 6px;
    }

    /* 섹션 헤더 */
    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1a2744;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 10px;
        margin: 20px 0 16px 0;
        letter-spacing: -0.01em;
    }

    /* 근무표 셀 */
    .schedule-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
    }
    .schedule-table th {
        background: #1a2744;
        color: white;
        padding: 10px 8px;
        text-align: center;
        font-weight: 600;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        position: sticky;
        top: 0;
    }
    .schedule-table td {
        padding: 8px 6px;
        text-align: center;
        border-bottom: 1px solid #f1f5f9;
        vertical-align: middle;
    }
    .schedule-table tr:hover td { background: #f8fafc; }
    .schedule-table tr:nth-child(even) td { background: #fafbfd; }
    .schedule-table tr:nth-child(even):hover td { background: #f1f5f9; }

    /* 근무 유형 배지 */
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .badge-day    { background:#dbeafe; color:#1d4ed8; }
    .badge-night  { background:#ede9fe; color:#6d28d9; }
    .badge-off    { background:#f3f4f6; color:#6b7280; }
    .badge-annual { background:#fef3c7; color:#92400e; }
    .badge-halfam { background:#dcfce7; color:#166534; }
    .badge-halfpm { background:#d1fae5; color:#065f46; }
    .badge-sick   { background:#fee2e2; color:#991b1b; }
    .badge-holiday{ background:#ffedd5; color:#92400e; }
    .badge-work   { background:#e0f2fe; color:#0369a1; }

    /* 알림 카드 */
    .alert-card {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f97316;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 0.85rem;
        color: #7c2d12;
    }
    .alert-card.info {
        background: #eff6ff;
        border-color: #bfdbfe;
        border-left-color: #3b82f6;
        color: #1e3a5f;
    }
    .alert-card.success {
        background: #f0fdf4;
        border-color: #bbf7d0;
        border-left-color: #22c55e;
        color: #14532d;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: white;
        padding: 6px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 8px 20px;
        color: #6b7280;
    }
    .stTabs [aria-selected="true"] {
        background: #1a2744 !important;
        color: white !important;
    }

    /* 데이터프레임 */
    .dataframe { border-radius: 10px; overflow: hidden; }

    /* 업로드 영역 */
    .uploadedFile { border-radius: 10px; }

    /* 버튼 */
    .stButton > button {
        background: linear-gradient(135deg, #1a2744, #2d4a7a);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.88rem;
        letter-spacing: 0.02em;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26,39,68,0.25);
    }

    /* 다운로드 버튼 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    /* 메트릭 숨기기 */
    [data-testid="stMetricDelta"] { display: none; }

    /* 반응형 */
    @media (max-width: 768px) {
        .kpi-value { font-size: 1.5rem; }
        .header-card h1 { font-size: 1.3rem; }
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 상수 정의
# ─────────────────────────────────────────────
WORK_TYPES = {
    "근무": "work",   "day": "day",   "D": "day",
    "야간": "night",  "night": "night","N": "night",
    "오프": "off",    "OFF": "off",   "휴무": "off",
    "연차": "annual", "연휴": "annual","휴가": "annual",
    "반차(오전)": "halfam","반오프(오전)":"halfam","오전반차":"halfam",
    "반차(오후)": "halfpm","반오프(오후)":"halfpm","오후반차":"halfpm",
    "병가": "sick",   "병결": "sick",
    "공휴일": "holiday","공가":"holiday",
}
TYPE_LABELS = {
    "work":"근무","day":"주간","night":"야간","off":"오프",
    "annual":"연차","halfam":"반차(오전)","halfpm":"반차(오후)",
    "sick":"병가","holiday":"공휴일","":" - "
}
TYPE_COLORS = {
    "work":"#3b82f6","day":"#3b82f6","night":"#8b5cf6","off":"#9ca3af",
    "annual":"#f59e0b","halfam":"#10b981","halfpm":"#059669",
    "sick":"#ef4444","holiday":"#f97316","":"#e5e7eb"
}
BADGE_CLASS = {
    "work":"badge-work","day":"badge-day","night":"badge-night","off":"badge-off",
    "annual":"badge-annual","halfam":"badge-halfam","halfpm":"badge-halfpm",
    "sick":"badge-sick","holiday":"badge-holiday","":"badge-off"
}


# ─────────────────────────────────────────────
# 유틸리티 함수
# ─────────────────────────────────────────────
def normalize_type(val):
    if pd.isna(val) or str(val).strip() == "":
        return ""
    s = str(val).strip()
    return WORK_TYPES.get(s, "work" if s else "")


def get_korean_holidays(year):
    """간단한 공휴일 목록 (법정 공휴일)"""
    holidays = []
    fixed = [(1,1),(3,1),(5,5),(6,6),(8,15),(10,3),(10,9),(12,25)]
    for m,d in fixed:
        try:
            holidays.append(date(year,m,d))
        except:
            pass
    return holidays


def load_sample_data():
    """샘플 데이터 생성"""
    rng = np.random.default_rng(42)
    employees = [
        ("EMP001","김민준","원무팀","팀장"),
        ("EMP002","이서연","간호팀","수간호사"),
        ("EMP003","박지호","간호팀","일반"),
        ("EMP004","최수아","간호팀","일반"),
        ("EMP005","정도윤","원무팀","일반"),
        ("EMP006","강하은","약제팀","약사"),
        ("EMP007","윤재원","의료지원팀","방사선사"),
        ("EMP008","임소율","간호팀","일반"),
        ("EMP009","한준서","원무팀","일반"),
        ("EMP010","오지아","간호팀","일반"),
    ]
    year, month = 2024, 6
    days_in_month = calendar.monthrange(year, month)[1]
    holidays = get_korean_holidays(year)

    rows = []
    for emp_id, name, dept, role in employees:
        row = {"사번":emp_id,"성명":name,"부서":dept,"직책":role}
        types = (["night","night","off"] if dept=="간호팀"
                 else ["work","work","off","work","work","off","off"])
        for d in range(1, days_in_month+1):
            dt = date(year, month, d)
            if dt in holidays:
                val = "공휴일"
            elif dt.weekday() >= 5 and dept != "간호팀":
                val = "오프"
            else:
                r = rng.random()
                if r < 0.04:   val = "연차"
                elif r < 0.06: val = "반차(오전)"
                elif r < 0.08: val = "병가"
                else:
                    t = types[d % len(types)]
                    val = TYPE_LABELS.get(t, "근무")
            row[f"{d}일"] = val
        row["입사일"] = f"202{rng.integers(0,4)}-{rng.integers(1,12):02d}-{rng.integers(1,28):02d}"
        row["연차발생일수"] = int(rng.integers(12, 21))
        rows.append(row)
    return pd.DataFrame(rows)


def parse_schedule_df(df):
    """업로드된 데이터프레임 파싱"""
    # 컬럼 자동 감지
    col_map = {}
    for c in df.columns:
        lc = str(c).strip().lower()
        if any(k in lc for k in ["사번","id","번호"]): col_map["사번"] = c
        elif any(k in lc for k in ["성명","이름","name"]): col_map["성명"] = c
        elif any(k in lc for k in ["부서","팀","dept"]): col_map["부서"] = c
        elif any(k in lc for k in ["직책","직급","직위","role"]): col_map["직책"] = c
        elif any(k in lc for k in ["입사","join","hire"]): col_map["입사일"] = c
        elif any(k in lc for k in ["연차발생","발생일수","총연차"]): col_map["연차발생일수"] = c

    result = pd.DataFrame()
    for std, orig in col_map.items():
        result[std] = df[orig]

    # 날짜 컬럼 탐지
    day_cols = []
    for c in df.columns:
        s = str(c).strip()
        if s not in col_map.values():
            if s.replace("일","").isdigit() or (len(s)<=4 and s.isdigit()):
                day_cols.append(c)
            elif "/" in s or "-" in s:
                day_cols.append(c)

    for c in day_cols:
        d_num = str(c).replace("일","").strip()
        col_name = f"{d_num}일"
        result[col_name] = df[c]

    return result, day_cols


def compute_stats(df, day_cols):
    """근무 통계 계산"""
    stats = []
    for _, row in df.iterrows():
        counts = {v:0 for v in ["work","day","night","off","annual","halfam","halfpm","sick","holiday",""]}
        for c in day_cols:
            t = normalize_type(row.get(c if isinstance(c, str) else f"{str(c).replace('일','')}일", ""))
            counts[t] = counts.get(t,0)+1

        work_days = counts["work"]+counts["day"]+counts["night"]
        annual_used = counts["annual"] + counts["halfam"]*0.5 + counts["halfpm"]*0.5
        annual_total = int(row.get("연차발생일수", 15))
        annual_remain = max(0, annual_total - annual_used)

        stats.append({
            "사번":row.get("사번",""),
            "성명":row.get("성명",""),
            "부서":row.get("부서",""),
            "직책":row.get("직책",""),
            "입사일":row.get("입사일",""),
            "근무일수":work_days,
            "야간근무":counts["night"],
            "오프일수":counts["off"],
            "연차사용":annual_used,
            "반차(오전)":counts["halfam"],
            "반차(오후)":counts["halfpm"],
            "병가일수":counts["sick"],
            "연차발생":annual_total,
            "연차잔여":annual_remain,
            **{f"cnt_{k}":v for k,v in counts.items()}
        })
    return pd.DataFrame(stats)


def make_schedule_html(df, day_cols, year, month):
    """근무표 HTML 생성"""
    days_in = calendar.monthrange(year, month)[1]
    holidays = get_korean_holidays(year)
    weekday_kr = ["월","화","수","목","금","토","일"]

    # 날짜 헤더
    header = "<thead><tr><th>사번</th><th>성명</th><th>부서</th><th>직책</th>"
    for d in range(1, days_in+1):
        dt = date(year, month, d)
        wd = weekday_kr[dt.weekday()]
        color = "#ef4444" if dt in holidays else ("#f97316" if dt.weekday()==6 else ("#3b82f6" if dt.weekday()==5 else "white"))
        header += f'<th style="color:{color};min-width:42px">{d}<br><span style="font-size:0.65rem;opacity:0.8">{wd}</span></th>'
    header += "</tr></thead>"

    body = "<tbody>"
    for _, row in df.iterrows():
        body += f'<tr><td style="font-weight:600;white-space:nowrap">{row.get("사번","")}</td>'
        body += f'<td style="font-weight:700;white-space:nowrap">{row.get("성명","")}</td>'
        body += f'<td style="white-space:nowrap">{row.get("부서","")}</td>'
        body += f'<td style="white-space:nowrap">{row.get("직책","")}</td>'

        for d in range(1, days_in+1):
            col_candidates = [f"{d}일", str(d), f"{d:02d}일"]
            val = ""
            for cc in col_candidates:
                if cc in row.index and not pd.isna(row[cc]):
                    val = str(row[cc]).strip()
                    break
            t = normalize_type(val)
            bc = BADGE_CLASS.get(t, "badge-off")
            label = val if val else "-"
            body += f'<td><span class="badge {bc}">{label}</span></td>'
        body += "</tr>"
    body += "</tbody>"

    return f'<div style="overflow-x:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.07)"><table class="schedule-table">{header}{body}</table></div>'


# ─────────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
        <div style='font-size:2.2rem'>🏥</div>
        <div style='font-size:1rem;font-weight:700;letter-spacing:0.02em'>병원 인사관리 시스템</div>
        <div style='font-size:0.72rem;opacity:0.5;margin-top:4px'>Hospital HR Management</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.1);margin:8px 0 16px'>
    """, unsafe_allow_html=True)

    st.markdown("##### 📅 기준 연월")
    col_y, col_m = st.columns(2)
    with col_y:
        sel_year = st.selectbox("연도", list(range(2020, 2030)), index=4, label_visibility="collapsed")
    with col_m:
        sel_month = st.selectbox("월", list(range(1, 13)), index=5, label_visibility="collapsed")

    st.markdown("##### 📂 엑셀 파일 업로드")
    uploaded = st.file_uploader(
        "근무표 엑셀 업로드",
        type=["xlsx","xls","csv"],
        label_visibility="collapsed",
        help="사번, 성명, 부서, 직책, 날짜별 근무유형이 포함된 파일"
    )

    st.markdown("##### 🔍 필터")
    use_sample = st.checkbox("샘플 데이터 사용", value=(uploaded is None))

    dept_filter = st.multiselect("부서 필터", [], placeholder="전체 부서")
    type_filter = st.multiselect(
        "근무 유형",
        ["근무","야간","오프","연차","반차(오전)","반차(오후)","병가","공휴일"],
        placeholder="전체 유형"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;opacity:0.4;text-align:center;padding:8px 0'>
        근무유형: 근무·야간·오프·연차<br>반차(오전/오후)·병가·공휴일
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 데이터 로드
# ─────────────────────────────────────────────
@st.cache_data
def get_sample():
    return load_sample_data()

if uploaded is not None:
    try:
        if uploaded.name.endswith(".csv"):
            raw_df = pd.read_csv(uploaded, encoding="utf-8-sig")
        else:
            raw_df = pd.read_excel(uploaded)
        df_main, day_cols_raw = parse_schedule_df(raw_df)
        day_cols = [f"{str(c).replace('일','').strip()}일" for c in day_cols_raw]
        data_source = f"📎 {uploaded.name}"
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
        df_main = get_sample()
        days_in_month = calendar.monthrange(sel_year, sel_month)[1]
        day_cols = [f"{d}일" for d in range(1, days_in_month+1) if f"{d}일" in df_main.columns]
        data_source = "🔬 샘플 데이터"
elif use_sample:
    df_main = get_sample()
    days_in_month = calendar.monthrange(sel_year, sel_month)[1]
    day_cols = [f"{d}일" for d in range(1, days_in_month+1) if f"{d}일" in df_main.columns]
    data_source = "🔬 샘플 데이터"
else:
    st.info("사이드바에서 파일을 업로드하거나 '샘플 데이터 사용'을 선택하세요.")
    st.stop()

# 부서 필터 옵션 업데이트
all_depts = sorted(df_main["부서"].dropna().unique().tolist()) if "부서" in df_main.columns else []
if dept_filter:
    df_filtered = df_main[df_main["부서"].isin(dept_filter)]
else:
    df_filtered = df_main.copy()

# 통계 계산
stats_df = compute_stats(df_filtered, day_cols)


# ─────────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="header-card">
    <div style="font-size:2.8rem">🏥</div>
    <div>
        <h1>병원 인사관리 시스템</h1>
        <p>{sel_year}년 {sel_month}월 &nbsp;|&nbsp; {data_source} &nbsp;|&nbsp; 총 {len(df_filtered)}명</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI 카드
# ─────────────────────────────────────────────
total_staff = len(stats_df)
avg_work = round(stats_df["근무일수"].mean(), 1) if total_staff else 0
avg_night = round(stats_df["야간근무"].mean(), 1) if total_staff else 0
total_annual_used = stats_df["연차사용"].sum()
avg_annual_remain = round(stats_df["연차잔여"].mean(), 1) if total_staff else 0
sick_count = (stats_df["병가일수"] > 0).sum()
days_in_month = calendar.monthrange(sel_year, sel_month)[1]

c1, c2, c3, c4, c5 = st.columns(5)
kpi_data = [
    (c1, "👥 총 직원 수", f"{total_staff}명", f"{len(all_depts)}개 부서", "#3b82f6"),
    (c2, "📅 평균 근무일", f"{avg_work}일", f"전체 {days_in_month}일 기준", "#10b981"),
    (c3, "🌙 평균 야간근무", f"{avg_night}회", "1인 평균", "#8b5cf6"),
    (c4, "🏖️ 연차 사용 합계", f"{total_annual_used:.0f}일", f"잔여 평균 {avg_annual_remain}일", "#f59e0b"),
    (c5, "🤒 병가 발생 인원", f"{sick_count}명", f"전체의 {sick_count/total_staff*100:.0f}%" if total_staff else "-", "#ef4444"),
]
for col, label, val, sub, color in kpi_data:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{color}">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 근무표", "📊 통계 분석", "👤 직원별 현황", "⚠️ 알림/이슈", "📥 다운로드"
])


# ══════════════════════════════════════════════
# TAB 1: 근무표
# ══════════════════════════════════════════════
with tab1:
    st.markdown(f'<div class="section-header">📋 {sel_year}년 {sel_month}월 근무표</div>', unsafe_allow_html=True)

    # 범례
    legend_html = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px">'
    for t, label in [("work","근무"),("night","야간"),("off","오프"),("annual","연차"),
                     ("halfam","반차(오전)"),("halfpm","반차(오후)"),("sick","병가"),("holiday","공휴일")]:
        bc = BADGE_CLASS[t]
        legend_html += f'<span class="badge {bc}">{label}</span>'
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    schedule_html = make_schedule_html(df_filtered, day_cols, sel_year, sel_month)
    st.markdown(schedule_html, unsafe_allow_html=True)

    # 일별 근무 인원 현황
    st.markdown('<div class="section-header">📊 일별 근무 현황</div>', unsafe_allow_html=True)
    daily = []
    for d in range(1, days_in_month+1):
        col_n = f"{d}일"
        if col_n not in df_filtered.columns: continue
        types_counts = df_filtered[col_n].apply(normalize_type).value_counts().to_dict()
        daily.append({
            "일": d,
            "근무": types_counts.get("work",0)+types_counts.get("day",0),
            "야간": types_counts.get("night",0),
            "연차/반차": types_counts.get("annual",0)+types_counts.get("halfam",0)+types_counts.get("halfpm",0),
            "오프": types_counts.get("off",0),
            "병가": types_counts.get("sick",0),
        })
    daily_df = pd.DataFrame(daily)

    fig_daily = go.Figure()
    colors_ = {"근무":"#3b82f6","야간":"#8b5cf6","연차/반차":"#f59e0b","오프":"#9ca3af","병가":"#ef4444"}
    for col in ["근무","야간","연차/반차","오프","병가"]:
        fig_daily.add_trace(go.Bar(
            name=col, x=daily_df["일"], y=daily_df[col],
            marker_color=colors_[col], opacity=0.85
        ))
    fig_daily.update_layout(
        barmode="stack", height=280, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
        font=dict(family="Noto Sans KR"),
        xaxis=dict(showgrid=False, tickmode="linear", tick0=1, dtick=1),
        yaxis=dict(gridcolor="#f1f5f9", title="인원(명)")
    )
    st.plotly_chart(fig_daily, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 2: 통계 분석
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">📊 근무 유형 분포</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # 파이 차트: 전체 근무 유형 분포
        type_totals = {}
        for _, row in df_filtered.iterrows():
            for c in day_cols:
                t = normalize_type(row.get(c,""))
                if t:
                    type_totals[t] = type_totals.get(t,0)+1

        labels = [TYPE_LABELS.get(k,k) for k in type_totals]
        values = list(type_totals.values())
        colors_pie = [TYPE_COLORS.get(k,"#ccc") for k in type_totals]

        fig_pie = go.Figure(go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors_pie, line=dict(color="white",width=2)),
            hole=0.45, textinfo="label+percent",
            textfont=dict(family="Noto Sans KR", size=12)
        ))
        fig_pie.update_layout(
            title="전체 근무 유형 분포", height=320,
            margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        # 부서별 근무일수 비교
        dept_stats = stats_df.groupby("부서")[["근무일수","야간근무","연차사용","병가일수"]].mean().round(1).reset_index()
        fig_dept = go.Figure()
        for metric, color in [("근무일수","#3b82f6"),("야간근무","#8b5cf6"),("연차사용","#f59e0b")]:
            fig_dept.add_trace(go.Bar(
                name=metric, x=dept_stats["부서"], y=dept_stats[metric],
                marker_color=color, opacity=0.85
            ))
        fig_dept.update_layout(
            title="부서별 평균 근무 현황", barmode="group", height=320,
            margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9", title="일/회"),
            legend=dict(orientation="h", yanchor="top", y=-0.15)
        )
        st.plotly_chart(fig_dept, use_container_width=True)

    # 연차 현황
    st.markdown('<div class="section-header">🏖️ 연차 사용 현황</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns(2)

    with col_c:
        annual_df = stats_df[["성명","부서","연차발생","연차사용","연차잔여"]].sort_values("연차사용", ascending=False)
        fig_annual = go.Figure()
        fig_annual.add_trace(go.Bar(
            name="사용", x=annual_df["성명"], y=annual_df["연차사용"],
            marker_color="#f59e0b", opacity=0.85
        ))
        fig_annual.add_trace(go.Bar(
            name="잔여", x=annual_df["성명"], y=annual_df["연차잔여"],
            marker_color="#fde68a", opacity=0.7
        ))
        fig_annual.update_layout(
            title="직원별 연차 사용/잔여", barmode="stack", height=320,
            margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
            xaxis=dict(showgrid=False, tickangle=-30),
            yaxis=dict(gridcolor="#f1f5f9", title="일"),
            legend=dict(orientation="h", yanchor="top", y=-0.3)
        )
        st.plotly_chart(fig_annual, use_container_width=True)

    with col_d:
        # 연차 소진율 게이지
        avg_used_rate = (stats_df["연차사용"].sum() / stats_df["연차발생"].sum() * 100) if stats_df["연차발생"].sum() > 0 else 0
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_used_rate,
            number=dict(suffix="%", font=dict(size=40, family="Noto Sans KR")),
            title=dict(text="평균 연차 소진율", font=dict(size=14, family="Noto Sans KR")),
            delta=dict(reference=60, increasing=dict(color="#10b981")),
            gauge=dict(
                axis=dict(range=[0,100], tickfont=dict(family="Noto Sans KR")),
                bar=dict(color="#f59e0b"),
                steps=[
                    dict(range=[0,40], color="#fef3c7"),
                    dict(range=[40,70], color="#fde68a"),
                    dict(range=[70,100], color="#fbbf24"),
                ],
                threshold=dict(line=dict(color="#ef4444",width=3), thickness=0.75, value=80)
            )
        ))
        fig_gauge.update_layout(
            height=320, margin=dict(l=20,r=20,t=50,b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # 야간 근무 분포
    st.markdown('<div class="section-header">🌙 야간 근무 분포</div>', unsafe_allow_html=True)
    night_data = stats_df[stats_df["야간근무"] > 0].sort_values("야간근무", ascending=False)
    if not night_data.empty:
        fig_night = px.bar(
            night_data, x="성명", y="야간근무", color="부서",
            color_discrete_sequence=["#8b5cf6","#6d28d9","#a78bfa","#4c1d95"],
            labels={"야간근무":"야간 근무 횟수","성명":"직원"}
        )
        fig_night.update_layout(
            height=280, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
            xaxis=dict(showgrid=False, tickangle=-30),
            yaxis=dict(gridcolor="#f1f5f9"),
        )
        st.plotly_chart(fig_night, use_container_width=True)
    else:
        st.info("야간 근무 데이터가 없습니다.")


# ══════════════════════════════════════════════
# TAB 3: 직원별 현황
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">👤 직원별 상세 현황</div>', unsafe_allow_html=True)

    # 요약 테이블
    display_stats = stats_df[[
        "사번","성명","부서","직책","근무일수","야간근무","오프일수",
        "연차발생","연차사용","연차잔여","반차(오전)","반차(오후)","병가일수"
    ]].copy()
    display_stats.columns = [
        "사번","성명","부서","직책","근무일수","야간근무","오프일수",
        "연차발생(일)","연차사용(일)","연차잔여(일)","반차(오전)","반차(오후)","병가(일)"
    ]

    st.dataframe(
        display_stats.style
        .background_gradient(subset=["근무일수"], cmap="Blues", vmin=0)
        .background_gradient(subset=["야간근무"], cmap="Purples", vmin=0)
        .background_gradient(subset=["연차사용(일)"], cmap="YlOrBr", vmin=0)
        .background_gradient(subset=["병가(일)"], cmap="Reds", vmin=0)
        .format({"연차사용(일)":"{:.1f}","연차잔여(일)":"{:.1f}"}),
        use_container_width=True, height=400
    )

    # 개별 직원 상세
    st.markdown('<div class="section-header">🔎 개별 직원 상세</div>', unsafe_allow_html=True)
    emp_names = stats_df["성명"].tolist()
    sel_emp = st.selectbox("직원 선택", emp_names)

    emp_row = stats_df[stats_df["성명"]==sel_emp].iloc[0]
    emp_sched = df_filtered[df_filtered["성명"]==sel_emp]

    if not emp_sched.empty:
        e1, e2, e3 = st.columns(3)
        with e1:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:#1a2744">
                <div class="kpi-label">👤 기본 정보</div>
                <div style="margin-top:8px;font-size:0.88rem;line-height:2">
                    <b>사번:</b> {emp_row.get('사번','-')}<br>
                    <b>부서:</b> {emp_row.get('부서','-')}<br>
                    <b>직책:</b> {emp_row.get('직책','-')}<br>
                    <b>입사일:</b> {emp_row.get('입사일','-')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with e2:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:#3b82f6">
                <div class="kpi-label">📅 근무 현황</div>
                <div style="margin-top:8px;font-size:0.88rem;line-height:2">
                    <b>근무일수:</b> {emp_row['근무일수']}일<br>
                    <b>야간근무:</b> {emp_row['야간근무']}회<br>
                    <b>오프일수:</b> {emp_row['오프일수']}일<br>
                    <b>병가일수:</b> {emp_row['병가일수']}일
                </div>
            </div>
            """, unsafe_allow_html=True)
        with e3:
            rate = emp_row['연차사용']/emp_row['연차발생']*100 if emp_row['연차발생']>0 else 0
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color:#f59e0b">
                <div class="kpi-label">🏖️ 연차 현황</div>
                <div style="margin-top:8px;font-size:0.88rem;line-height:2">
                    <b>연차 발생:</b> {emp_row['연차발생']}일<br>
                    <b>연차 사용:</b> {emp_row['연차사용']}일<br>
                    <b>연차 잔여:</b> {emp_row['연차잔여']}일<br>
                    <b>소진율:</b> {rate:.0f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 해당 직원 월 캘린더
        st.markdown(f'<div class="section-header">📅 {sel_emp} 월 근무 현황</div>', unsafe_allow_html=True)
        emp_html = make_schedule_html(emp_sched, day_cols, sel_year, sel_month)
        st.markdown(emp_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4: 알림/이슈
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">⚠️ 주요 알림 및 이슈</div>', unsafe_allow_html=True)

    alerts = []

    # 연차 소진 부족 (80% 미만)
    for _, r in stats_df.iterrows():
        rate = r["연차사용"]/r["연차발생"]*100 if r["연차발생"]>0 else 0
        if rate < 30 and r["연차발생"] > 0:
            alerts.append(("warning", f"⚠️ [{r['부서']}] {r['성명']} — 연차 소진율 {rate:.0f}% (잔여 {r['연차잔여']}일 남음)"))

    # 병가 다수
    for _, r in stats_df.iterrows():
        if r["병가일수"] >= 3:
            alerts.append(("warning", f"🤒 [{r['부서']}] {r['성명']} — 병가 {r['병가일수']}일 사용 (관리 필요)"))

    # 야간 과다
    night_avg = stats_df["야간근무"].mean()
    for _, r in stats_df.iterrows():
        if r["야간근무"] > night_avg * 1.5 and r["야간근무"] > 0:
            alerts.append(("warning", f"🌙 [{r['부서']}] {r['성명']} — 야간 근무 {r['야간근무']}회 (평균의 {r['야간근무']/night_avg:.1f}배)"))

    # 일별 최소 근무인원 미달
    for d in range(1, days_in_month+1):
        col_n = f"{d}일"
        if col_n not in df_filtered.columns: continue
        work_count = df_filtered[col_n].apply(
            lambda v: normalize_type(v) in ["work","day","night"]
        ).sum()
        dt = date(sel_year, sel_month, d)
        if dt.weekday() < 5 and work_count < max(1, total_staff // 3):
            alerts.append(("info", f"📋 {sel_month}월 {d}일(평일) — 근무 인원 {work_count}명 (주의 필요)"))

    # 연차 발생일 고갈 임박
    for _, r in stats_df.iterrows():
        if 0 < r["연차잔여"] <= 1:
            alerts.append(("info", f"📌 [{r['부서']}] {r['성명']} — 연차 잔여 {r['연차잔여']}일 (거의 소진)"))

    if not alerts:
        st.markdown('<div class="alert-card success">✅ 현재 특이사항이 없습니다. 근무 현황이 정상입니다.</div>', unsafe_allow_html=True)
    else:
        for atype, msg in alerts:
            cls = "alert-card" if atype=="warning" else "alert-card info"
            st.markdown(f'<div class="{cls}">{msg}</div>', unsafe_allow_html=True)

    # 통계 요약
    st.markdown('<div class="section-header">📈 이달 요약 지표</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        fig_box = px.box(stats_df, y="근무일수", color="부서",
                         color_discrete_sequence=["#3b82f6","#8b5cf6","#10b981","#f59e0b"],
                         labels={"근무일수":"근무일수(일)","부서":"부서"})
        fig_box.update_layout(
            title="부서별 근무일수 분포", height=300,
            margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"), showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with c2:
        fig_scatter = px.scatter(
            stats_df, x="근무일수", y="연차사용",
            color="부서", size="야간근무",
            hover_data=["성명","병가일수"],
            color_discrete_sequence=["#3b82f6","#8b5cf6","#10b981","#f59e0b"],
            labels={"근무일수":"근무일수","연차사용":"연차사용일"}
        )
        fig_scatter.update_layout(
            title="근무일수 vs 연차사용 (버블=야간)", height=300,
            margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR")
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c3:
        fig_heat_data = stats_df[["성명","근무일수","야간근무","연차사용","병가일수"]].set_index("성명")
        fig_heat = px.imshow(
            fig_heat_data.T,
            color_continuous_scale="Blues",
            aspect="auto",
            labels=dict(color="횟수/일")
        )
        fig_heat.update_layout(
            title="직원별 지표 히트맵", height=300,
            margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR")
        )
        st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 5: 다운로드
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">📥 보고서 및 데이터 다운로드</div>', unsafe_allow_html=True)

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        # 통계 요약 CSV
        csv_buf = io.StringIO()
        display_stats = stats_df[[
            "사번","성명","부서","직책","근무일수","야간근무","오프일수",
            "연차발생","연차사용","연차잔여","반차(오전)","반차(오후)","병가일수"
        ]].copy()
        display_stats.to_csv(csv_buf, index=False, encoding="utf-8-sig")
        st.download_button(
            label="📊 통계 요약 CSV 다운로드",
            data=csv_buf.getvalue().encode("utf-8-sig"),
            file_name=f"병원인사통계_{sel_year}{sel_month:02d}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_d2:
        # 엑셀 다운로드
        excel_buf = io.BytesIO()
        with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
            df_filtered.to_excel(writer, sheet_name="근무표", index=False)
            display_stats.to_excel(writer, sheet_name="통계요약", index=False)
        st.download_button(
            label="📋 전체 데이터 Excel 다운로드",
            data=excel_buf.getvalue(),
            file_name=f"병원인사관리_{sel_year}{sel_month:02d}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # 알림 리포트
    st.markdown('<div class="section-header">📝 알림 리포트 미리보기</div>', unsafe_allow_html=True)
    report_lines = [
        f"# 병원 인사관리 보고서",
        f"## {sel_year}년 {sel_month}월",
        f"",
        f"### 📊 기본 현황",
        f"- 총 직원 수: {total_staff}명",
        f"- 평균 근무일수: {avg_work}일",
        f"- 평균 야간근무: {avg_night}회",
        f"- 연차 소진율: {(stats_df['연차사용'].sum()/stats_df['연차발생'].sum()*100):.1f}%" if stats_df['연차발생'].sum()>0 else "- 연차 소진율: -",
        f"",
        f"### ⚠️ 주요 알림 ({len(alerts)}건)",
    ]
    for _, msg in alerts:
        report_lines.append(f"- {msg}")
    if not alerts:
        report_lines.append("- 특이사항 없음")
    report_lines += [
        f"",
        f"### 📋 부서별 평균",
    ]
    for _, dr in stats_df.groupby("부서")[["근무일수","야간근무","연차사용"]].mean().round(1).iterrows():
        report_lines.append(f"- **{_}**: 근무 {dr['근무일수']}일, 야간 {dr['야간근무']}회, 연차 {dr['연차사용']}일")

    report_text = "\n".join(report_lines)
    st.markdown(report_text)

    report_buf = io.BytesIO(report_text.encode("utf-8"))
    st.download_button(
        label="📄 보고서 텍스트 다운로드",
        data=report_buf,
        file_name=f"인사관리보고서_{sel_year}{sel_month:02d}.md",
        mime="text/markdown",
        use_container_width=True
    )

    # 샘플 엑셀 양식 다운로드
    st.markdown('<div class="section-header">📌 입력 양식 다운로드</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="alert-card info">
    📎 아래 양식을 다운로드한 후 데이터를 입력하고, 사이드바에서 업로드하세요.<br>
    <b>필수 컬럼:</b> 사번, 성명, 부서, 직책, 입사일, 연차발생일수, 1일~31일<br>
    <b>근무유형 입력값:</b> 근무 / 야간 / 오프 / 연차 / 반차(오전) / 반차(오후) / 병가 / 공휴일
    </div>
    """, unsafe_allow_html=True)

    sample_buf = io.BytesIO()
    sample_df = get_sample()
    with pd.ExcelWriter(sample_buf, engine="openpyxl") as writer:
        sample_df.to_excel(writer, sheet_name="근무표양식", index=False)
    st.download_button(
        label="📥 샘플 양식 Excel 다운로드",
        data=sample_buf.getvalue(),
        file_name="병원근무표_양식.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ─────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────
st.markdown("""
<hr style='margin:32px 0 16px;border-color:#e5e7eb'>
<div style='text-align:center;font-size:0.78rem;color:#9ca3af;padding-bottom:20px'>
    🏥 병원 인사관리 시스템 &nbsp;|&nbsp; Hospital HR Management System &nbsp;|&nbsp;
    근무유형: 근무·야간·오프·연차·반차(오전/오후)·병가·공휴일
</div>
""", unsafe_allow_html=True)
