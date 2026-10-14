from pathlib import Path

import pandas as pd
import streamlit as st

from control_center_common import load_demo


TEXT = {
    "en": {
        "page_title": "AI Accident Detection",
        "organization": "Jeddah Municipality",
        "title": "AI Accident Detection",
        "subtitle": "Live CCTV monitoring and triggered accident recordings",
        "live_feeds": "Live Camera Feeds",
        "recordings": "Triggered Accident Recordings",
        "location": "Location",
        "live": "● LIVE",
        "accident": "🚨 ACCIDENT DETECTED",
        "recording": "Accident Recording",
        "no_recordings": "No triggered accident recordings are available.",
        "video_missing": "Camera video is not available.",
        "footer": "Jeddah Municipality · AI Accident Detection Prototype",
    },
    "ar": {
        "page_title": "رصد الحوادث بالذكاء الاصطناعي",
        "organization": "أمانة جدة",
        "title": "رصد الحوادث بالذكاء الاصطناعي",
        "subtitle": "مراقبة مباشرة للكاميرات وتسجيلات الحوادث المكتشفة",
        "live_feeds": "البث المباشر للكاميرات",
        "recordings": "تسجيلات الحوادث المكتشفة",
        "location": "الموقع",
        "live": "● مباشر",
        "accident": "🚨 تم اكتشاف حادث",
        "recording": "تسجيل الحادث",
        "no_recordings": "لا توجد تسجيلات حوادث مكتشفة.",
        "video_missing": "فيديو الكاميرا غير متاح.",
        "footer": "أمانة جدة · النموذج التجريبي لرصد الحوادث بالذكاء الاصطناعي",
    },
}

AR_CAMERA = {i: f"الكاميرا {i:02d}" for i in range(1, 11)}
AR_LOCATION = {
    1: "الطريق الرئيسي – شمال",
    2: "الطريق الرئيسي – جنوب",
    3: "مدخل النفق",
    4: "داخل النفق – أ",
    5: "داخل النفق – ب",
    6: "التقاطع الشرقي",
    7: "التقاطع الغربي",
    8: "طريق الخدمة",
    9: "مخرج الطريق الرئيسي",
    10: "مخرج النفق",
}


def cam_name(camera, lang):
    number = int(camera["camera_number"])
    if lang == "ar":
        return AR_CAMERA.get(number, f"الكاميرا {number:02d}")
    return str(camera.get("camera_name", f"Camera {number:02d}"))


def loc_name(camera, lang):
    number = int(camera["camera_number"])
    if lang == "ar":
        return AR_LOCATION.get(number, "")
    value = camera.get("location_name", "")
    return "" if pd.isna(value) else str(value)


def resolve_video_path(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    if not value:
        return None

    p = Path(value)
    if p.exists():
        return p

    p2 = Path(__file__).resolve().parent / p
    if p2.exists():
        return p2

    return None


def apply_css(lang):
    direction = "rtl" if lang == "ar" else "ltr"
    align = "right" if lang == "ar" else "left"

    st.markdown(
        f"""
        <style>
        #MainMenu, footer, header[data-testid="stHeader"] {{
            visibility: hidden;
        }}

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {{
            direction: {direction} !important;
        }}

        .stApp {{
            background: #F6F8FC;
            color: #25285A;
        }}

        .block-container {{
            max-width: 1500px;
            padding: 1.3rem 2rem 3rem 2rem;
        }}

        .brand {{
            background: linear-gradient(115deg, #00B8C8 0%, #087FCE 50%, #342A8C 100%);
            color: white;
            border-radius: 20px;
            padding: 26px 30px;
            margin-bottom: 24px;
            box-shadow: 0 14px 36px rgba(52,42,140,0.17);
            text-align: {align};
        }}

        .brand-org {{
            font-size: 1.0rem;
            font-weight: 750;
            margin-bottom: 8px;
        }}

        .brand-title {{
            font-size: 2rem;
            font-weight: 850;
            margin-bottom: 7px;
        }}

        .brand-subtitle {{
            font-size: 0.95rem;
            opacity: 0.93;
        }}

        .section-title {{
            color: #25285A;
            font-size: 1.35rem;
            font-weight: 850;
            margin: 4px 0 16px 0;
            text-align: {align};
        }}

        .camera-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 8px;
            direction: {direction};
        }}

        .camera-title {{
            color: #25285A;
            font-weight: 850;
            font-size: 1rem;
            text-align: {align};
        }}

        .camera-location {{
            color: #7A8395;
            font-size: 0.80rem;
            margin-top: 3px;
            text-align: {align};
        }}

        .live-badge, .alert-badge {{
            border-radius: 999px;
            padding: 5px 9px;
            font-size: 0.72rem;
            font-weight: 800;
            white-space: nowrap;
        }}

        .live-badge {{
            color: #137A50;
            background: #ECFDF3;
            border: 1px solid #B4E7C8;
        }}

        .alert-badge {{
            color: #C9271C;
            background: #FFF1F0;
            border: 1px solid #FFD0CC;
        }}

        /* Force every camera/recording player into the same 16:9 frame. */
        div[data-testid="stVideo"] {{
            width: 100% !important;
            aspect-ratio: 16 / 9 !important;
            overflow: hidden !important;
            border-radius: 14px !important;
            border: 1px solid #E3E8F1 !important;
            background: #000 !important;
        }}

        div[data-testid="stVideo"] video {{
            direction: ltr !important;
            width: 100% !important;
            height: 100% !important;
            aspect-ratio: 16 / 9 !important;
            object-fit: contain !important;
            background: #000 !important;
            border-radius: 14px !important;
        }}

        .recording-title {{
            color: #25285A;
            font-size: 1rem;
            font-weight: 850;
            text-align: {align};
            margin-bottom: 3px;
        }}

        .recording-meta {{
            color: #7A8395;
            font-size: 0.82rem;
            text-align: {align};
            margin-bottom: 10px;
        }}

        .app-footer {{
            margin-top: 28px;
            padding-top: 12px;
            border-top: 1px solid #DCE4EF;
            color: #7A8395;
            font-size: 0.78rem;
            text-align: {align};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(lang):
    t = TEXT[lang]
    st.markdown(
        (
            '<div class="brand">'
            f'<div class="brand-org">{t["organization"]}</div>'
            f'<div class="brand-title">{t["title"]}</div>'
            f'<div class="brand-subtitle">{t["subtitle"]}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def render_live_camera(camera, lang):
    t = TEXT[lang]
    is_accident = bool(camera["final_alert"])

    badge_class = "alert-badge" if is_accident else "live-badge"
    badge_text = t["accident"] if is_accident else t["live"]

    st.markdown(
        (
            '<div class="camera-row">'
            '<div>'
            f'<div class="camera-title">📹 {cam_name(camera, lang)}</div>'
            f'<div class="camera-location">{loc_name(camera, lang)}</div>'
            '</div>'
            f'<div class="{badge_class}">{badge_text}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    video = resolve_video_path(camera.get("video_path"))
    if video is not None:
        st.video(str(video))
    else:
        st.info(t["video_missing"])


def render_accident_recording(camera, lang):
    t = TEXT[lang]

    st.markdown(
        (
            f'<div class="recording-title">🚨 {cam_name(camera, lang)} — {t["recording"]}</div>'
            f'<div class="recording-meta">{t["location"]}: {loc_name(camera, lang)}</div>'
        ),
        unsafe_allow_html=True,
    )

    video = resolve_video_path(camera.get("video_path"))
    if video is not None:
        st.video(str(video))
    else:
        st.info(t["video_missing"])


def run_app(lang):
    if lang not in TEXT:
        lang = "en"

    t = TEXT[lang]

    st.set_page_config(
        page_title=t["page_title"],
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    apply_css(lang)

    demo_df = load_demo().copy()

    if "camera_number" in demo_df.columns:
        demo_df = demo_df.sort_values("camera_number").reset_index(drop=True)

    render_header(lang)

    # --------------------------------------------------------
    # LIVE CAMERA FEEDS
    # --------------------------------------------------------
    st.markdown(
        f'<div class="section-title">📹 {t["live_feeds"]}</div>',
        unsafe_allow_html=True,
    )

    for start in range(0, len(demo_df), 2):
        cols = st.columns(2, gap="large")

        for offset, col in enumerate(cols):
            idx = start + offset
            if idx >= len(demo_df):
                break

            camera = demo_df.iloc[idx]

            with col:
                with st.container(border=True):
                    render_live_camera(camera, lang)

    # --------------------------------------------------------
    # TRIGGERED ACCIDENT RECORDINGS
    # Only FINAL AI accidents are shown here.
    # AI-rejected candidates remain normal in this simplified UI.
    # --------------------------------------------------------
    st.markdown("---")
    st.markdown(
        f'<div class="section-title">🚨 {t["recordings"]}</div>',
        unsafe_allow_html=True,
    )

    accident_df = (
        demo_df[demo_df["final_alert"].astype(bool)]
        .copy()
        .reset_index(drop=True)
    )

    if len(accident_df) == 0:
        st.info(t["no_recordings"])
    else:
        for start in range(0, len(accident_df), 2):
            cols = st.columns(2, gap="large")

            for offset, col in enumerate(cols):
                idx = start + offset
                if idx >= len(accident_df):
                    break

                camera = accident_df.iloc[idx]

                with col:
                    with st.container(border=True):
                        render_accident_recording(camera, lang)

    st.markdown(
        f'<div class="app-footer">{t["footer"]}</div>',
        unsafe_allow_html=True,
    )
