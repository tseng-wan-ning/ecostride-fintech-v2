import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components
from dataclasses import dataclass

# ==========================================
# 0. 專案 Config 與精算核心
# ==========================================
@dataclass(frozen=True)
class Config:
    years: int = 10
    user_years: int = 5
    n_users: int = 10_000
    mix: tuple = (0.25, 0.50, 0.25)
    base_steps: tuple = (8_700, 6_300, 4_300)
    goal_extra: int = 1_500
    p_ach_gain: tuple = (0.62, 0.46, 0.27)
    loss_frame: bool = True
    loss_mult: float = 1.30
    ach_kappa: float = 6.0
    ach_retention: float = 0.80
    ach_decay_years: float = 1.0
    rain_weeks: tuple = (17, 24)
    rain_mult: float = 0.85
    uplift_ach: float = 1_500
    uplift_miss: float = 300
    dropout_y1: tuple = (0.15, 0.25, 0.45)
    dropout_after: tuple = (0.05, 0.08, 0.15)
    streak_bonus: float = 0.20
    gamma: float = 0.20
    
    # 綠能與保險對齊參數
    sto_raise: float = 30_000_000
    ltv: float = 0.80
    coupon: float = 0.035
    insurer_coupon_share: float = 0.10
    platform_fee: float = 0.0
    premium: float = 35_000
    loss_ratio: float = 0.75
    expense_ratio: float = 0.15

    @property
    def capex_total(self): return self.sto_raise / self.ltv
    @property
    def capacity_kw(self): return self.capex_total / 37_400
    @property
    def policy_margin(self): return self.premium * (1 - self.loss_ratio - self.expense_ratio)
    @property
    def r_user(self): return self.coupon * (1 - self.insurer_coupon_share) - self.platform_fee

CFG = Config()
R_STAR_DEFAULT = 30.5  # 研究報告校準之預算中立每週回饋

# ==========================================
# 0-2. 全局環境配置與指定五色高質感 CSS 注入
# ==========================================
st.set_page_config(
    page_title="EcoStride | 永續金融生態系研究",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F5F7F4;
        color: #0C0E0B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    .stSidebar {
        background-color: #B7CEAD !important;
        border-right: 1px solid #83A474 !important;
    }
    .stSidebar *, .stSidebar p, .stSidebar h3 {
        color: #0C0E0B !important;
    }
    
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label [data-testid="stFiberManualRecord"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label input[type="radio"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[class*="st-c"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[class*="st-b"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stRadioButtonUI"] {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }
    
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] {
        gap: 8px !important;
        width: 100% !important;
    }
    
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 12px 18px !important;
        margin: 0 !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 15px !important;
        font-weight: 500 !important;
        margin: 0 !important;
        color: #0C0E0B !important;
    }
    
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label:has(input[type="radio"]:checked) {
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(45, 74, 34, 0.08) !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label:has(input[type="radio"]:checked) p {
        color: #2D4A22 !important;
        font-weight: 700 !important;
    }
    
    div.stButton > button {
        background-color: #83A474 !important;
        color: #F5F7F4 !important;
        border-radius: 8px !important;
        border: 1px solid #83A474 !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #92BA80 !important;
        border-color: #92BA80 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(131, 164, 116, 0.3);
    }
    
    h1 { color: #5D7A51 !important; font-weight: 800 !important; }
    h2, h3, h4 { color: #0C0E0B !important; font-weight: 700 !important; }
    
    .styled-table {
        width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; background-color: #FFFFFF;
        border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
    .styled-table th {
        background-color: #83A474; color: #F5F7F4; padding: 14px; text-align: left; font-weight: 600;
    }
    .styled-table td {
        padding: 14px; border-bottom: 1px solid #E2E8F0; color: #0C0E0B;
    }
    
    .alert-card {
        background-color: #FFFFFF; border-left: 5px solid #83A474; padding: 18px; border-radius: 0 12px 12px 0; margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
    .alert-card-danger {
        background-color: #FFF5F5; border-left: 5px solid #E53E3E; padding: 18px; border-radius: 0 12px 12px 0; margin: 15px 0;
    }
    
    .navbar-mock {
        background: rgba(245, 247, 244, 0.85);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid #B7CEAD;
        padding: 18px 35px;
        position: sticky; top: 0; z-index: 999;
        display: flex; justify-content: space-between; align-items: center;
        margin: -4.5rem -4rem 2rem -4rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 頂部毛玻璃導航欄區塊
# ==========================================
st.markdown("""
    <div class="navbar-mock">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 6px; height: 26px; background-color: #83A474; border-radius: 3px;"></div>
            <span style="font-size: 20px; font-weight: 800; letter-spacing: 3px; color: #0C0E0B;">ECOSTRIDE</span>
        </div>
        <div style="font-size: 13px; color: #0C0E0B; font-weight: 600; background-color: #B7CEAD; padding: 4px 12px; border-radius: 6px;">
            國立清華大學 金融科技專題研究成果
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 🎯 2. 後台真實精算核心模型函數
# ==========================================
def calculate_compounding_rwa_wealth(excess_steps, alpha=0.00065, beta=0.0001, gamma=0.20, consistency=0.75, rwa_yield_base=0.035, insurance_share_yield=0.25, mu_market=0.05):
    daily_investment = (excess_steps * alpha + (excess_steps * beta * gamma)) * consistency
    annual_investment = daily_investment * 365
    
    total_user_rwa_wealth = 0.0
    for year in range(1, 11):
        annual_rwa_yield_generated = total_user_rwa_wealth * rwa_yield_base
        rwa_flowback_to_insurance = annual_rwa_yield_generated * insurance_share_yield
        user_yield_reinvest = annual_rwa_yield_generated - rwa_flowback_to_insurance
        
        total_user_rwa_wealth += annual_investment + user_yield_reinvest
        total_user_rwa_wealth *= (1.0 + mu_market)
    return total_user_rwa_wealth

# ==========================================
# 🎯 3. 側邊欄與分頁導覽全域變數架構
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding: 20px 0 10px 0;'><h3 style='margin:0; font-size: 20px;'>專案選單</h3></div>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "請選擇要調閱的章節：",
    ["專案首頁", "提案動機與模式介紹", "APP 介面展示", "相關研究成果"]
)

with st.sidebar:
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 12px; line-height: 1.8;'>
        <b style='font-size:14px; color:#2D4A22;'>研究團隊</b><br>
        蔡宜伶 | 計量財務金融學系<br>
        賀舜禹 | 計量財務金融學系<br>
        曾琬甯 | 計量財務金融學系<br><br>
        <b style='font-size:14px; color:#2D4A22;'>指導教授</b><br>
        韓傳祥 教授
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 4. 分頁一：專案首頁
# ==========================================
if page == "專案首頁":
    if "selected_node" not in st.session_state:
        st.session_state.selected_node = "all"

    st.markdown("<div style='padding: 60px 0 40px 0; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 54px; font-weight: 900; color: #5D7A51 !important; letter-spacing: -1.5px; margin-bottom: 20px;'>讓健康行為，成為生產性綠色資本</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px; color: #0C0E0B; max-width: 950px; margin: 0 auto 35px auto; line-height: 1.6; font-weight: 600; opacity: 0.9;'>EcoStride：結合行為金融與實體資產代幣化之永續金融生態系模式研究</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. 分頁二：提案動機與模式介紹
# ==========================================
elif page == "提案動機與模式介紹":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>💡 提案動機與模式介紹</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("這裡展示現行保險系統失靈、STEPN 反思與三位一體模型內容。")

# ==========================================
# 6. 分頁三：APP 介面展示
# ==========================================
elif page == "APP 介面展示":
    current_r_star = globals().get('R_STAR', 30.5)
    wpy_val = globals().get('WPY', 52)

    st.markdown("<h2 style='color:#0C0E0B !important; font-size:28px; font-weight:800;'>📱 APP 核心介面互動模擬</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; color:#0C0E0B; opacity:0.8; font-weight:500;'>在左側控制台調整您的每日健走行為與持續性因子，右側精緻的虛擬手機畫面將即時同步呈現最新數據。</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_ui_left, col_ui_right = st.columns([1, 2])
    
    with col_ui_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:20px; border-radius:14px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0C0E0B !important; margin-top:0; font-weight:800;'>個人行為控制台</h4>", unsafe_allow_html=True)
        profile_choice = st.radio("運動族群預設切換：", ["高活躍型 (High)", "典型保戶 (Medium)", "Low 低活躍型"], key="app_profile_radio")
        
        if "高活躍" in profile_choice:
            init_steps, init_cons, sel_g = 8700, 0.95, 0
        elif "典型保戶" in profile_choice:
            init_steps, init_cons, sel_g = 6300, 0.75, 1
        else:
            init_steps, init_cons, sel_g = 4300, 0.40, 2
            
        ui_steps = st.slider("設定您的每日平均步數：", 3000, 15000, init_steps, 500, key="app_steps_slider")
        ui_cons = st.slider("設定行為持續性因子 (Consistency)：", 0.1, 1.0, init_cons, 0.05, key="app_cons_slider")
        
        st.markdown("<br>", unsafe_allow_html=True)
        app_tab_view = st.radio("手機 APP 檢視頁籤：", ["① 每日運動與獎勵", "② RWA 綠能資產錢包", "③ 保單風險與分紅"], key="app_tab_radio")
        st.markdown("</div>", unsafe_allow_html=True)
        
    base_target_steps = CFG.base_steps[sel_g] + CFG.goal_extra
    step_diff = ui_steps - CFG.base_steps[sel_g]
    ach_prob_est = min(0.95, max(0.05, (step_diff / CFG.goal_extra) * CFG.p_ach_gain[sel_g] * ui_cons))
    weekly_expected_reward = ach_prob_est * current_r_star
    
    r_w_weekly = CFG.r_user / wpy_val
    accumulated_rwa_val = 0.0
    for w_i in range(5 * wpy_val):
        w_pay = weekly_expected_reward if (w_i % wpy_val < 45) else weekly_expected_reward * 0.8
        accumulated_rwa_val = accumulated_rwa_val * (1 + r_w_weekly) + w_pay

    total_steps_5yr = ui_steps * 365 * 5
    carbon_saved_kg = total_steps_5yr * 0.0000125
    trees_equivalent = int(carbon_saved_kg / 12) + 1

    with col_ui_right:
        if "①" in app_tab_view:
            screen_content = f"""
                <div style="font-size:11px; font-weight:800; color:#83A474; text-align:center; letter-spacing:1px; margin-bottom:8px;">👣 DAILY HEALTH DASHBOARD</div>
                <div style="background:#F8F9FA; border:1px solid #E2E8F0; padding:16px; border-radius:16px; text-align:center; margin-bottom:12px;">
                    <span style="font-size:30px; font-weight:900; color:#0C0E0B;">{ui_steps:,} 👣</span>
                    <div style="font-size:11px; color:#666; font-weight:600; margin-top:3px;">TODAY'S AVERAGE STEPS</div>
                </div>
            """
        elif "②" in app_tab_view:
            screen_content = f"""
                <div style="font-size:11px; font-weight:800; color:#83A474; text-align:center; letter-spacing:1px; margin-bottom:10px;">📈 RWA GREEN PORTFOLIO</div>
                <div style="background:#F8F9FA; border:1px solid #E2E8F0; padding:16px; border-radius:14px; text-align:center; margin: 12px 0;">
                    <span style="font-size:11px; color:#666; font-weight:600;">5年累積 STRIDE 資產市值</span>
                    <div style="font-size:24px; font-weight:900; color:#83A474; margin-top:5px;">NT$ {accumulated_rwa_val:,.0f}</div>
                </div>
            """
        else:
            screen_content = f"""
                <div style="font-size:11px; font-weight:800; color:#83A474; text-align:center; letter-spacing:1px; margin-bottom:8px;">🛡️ POLICY & RISK STATUS</div>
                <div style="background:#EBF3EA; border:1px solid #83A474; padding:10px; border-radius:12px; display:flex; align-items:center; gap:8px;">
                    <div style="font-size:22px;">🤖</div>
                    <div style="font-size:9px; color:#2D4A22; line-height:1.4;">
                        <b>EcoStride AI 智能精算助手</b><br>
                        <span style="color:#444;">“偵測到您近期達標率高達 {ach_prob_est*100:.0f}%，已自動幫您最佳化 3.5% RWA 複利滾存！”</span>
                    </div>
                </div>
            """

        phone_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{ background-color: transparent; margin: 0; display: flex; justify-content: center; align-items: center; font-family: sans-serif; }}
            .iphone-container {{ width: 310px; background: #111; border-radius: 42px; padding: 10px; border: 3px solid #333; }}
            .iphone-screen {{ background: #FFF; border-radius: 32px; padding: 18px 14px; min-height: 480px; color: #0C0E0B; }}
        </style>
        </head>
        <body>
            <div class="iphone-container">
                <div class="iphone-screen">{screen_content}</div>
            </div>
        </body>
        </html>
        """
        st.components.v1.html(phone_html, height=530)

    st.markdown("<br>", unsafe_allow_html=True)
    fig_app_trend = go.Figure()
    yrs_arr = list(range(1, 6))
    simulated_path = [accumulated_rwa_val * (y / 5) * (1.1 if y > 1 else 1.0) for y in yrs_arr]
    legacy_path_app = [1194 * y for y in yrs_arr]
    fig_app_trend.add_trace(go.Scatter(x=yrs_arr, y=simulated_path, name="EcoStride APP 用戶累積資產", line=dict(color="#83A474", width=3)))
    fig_app_trend.add_trace(go.Scatter(x=yrs_arr, y=legacy_path_app, name="傳統外溢點數方案 (立即消耗)", line=dict(color="#E53E3E", width=2, dash="dash")))
    fig_app_trend.update_layout(title="【互動展示】使用者動態行為對應之 5 年資產成長預測", template="plotly_white", height=280, margin=dict(l=30, r=30, t=30, b=30))
    st.plotly_chart(fig_app_trend, use_container_width=True)

# ==========================================
# 7. 分頁四：相關研究成果 (完整獨立呈現)
# ==========================================
elif page == "相關研究成果":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>📊 相關研究成果與動態沙盤</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8;'>生態系成功啟動之三方共贏機率與邊界條件壓力測試模擬沙盤。</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:20px; border-radius:12px; margin-bottom:20px;'>", unsafe_allow_html=True)
    st.markdown("<b style='color:#2D4A22; font-size:15px;'>🎛️ 聯立動態沙盤參數控制台</b>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        tab4_r_star = st.slider("每週預算中立回饋 R* (元/達標週)", 20.0, 50.0, R_STAR_DEFAULT, 1.0, key="t4_r_v3")
        tab4_steps_inc = st.slider("保戶平均健走提升率", 0.05, 0.50, 0.20, 0.05, key="t4_s_v3")
    with col_c2:
        tab4_consistency = st.slider("全域行為穩定度因子", 0.30, 1.00, 0.75, 0.05, key="t4_c_v3")
        st.markdown("<div style='font-size: 14px; font-weight: 600; color: #2D4A22; margin-bottom: 5px;'>🌱 季節氣候衝擊情境 (壓力測試)</div>", unsafe_allow_html=True)
        tab4_rain_shock = st.selectbox("", ["梅雨/高日照自然波動 (標準)", "極端降雨氣候衝擊 (-35% 發電)", "晴雨交替穩定情境"], key="t4_rain_v3", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    dynamic_win_ratio_t4 = 67.3 + (tab4_r_star - 30.5) * -0.8 + (tab4_steps_inc - 0.20) * 35 + (tab4_consistency - 0.75) * 25
    if "極端降雨" in tab4_rain_shock:
        dynamic_win_ratio_t4 -= 15.0
    elif "晴雨交替" in tab4_rain_shock:
        dynamic_win_ratio_t4 += 5.0
    dynamic_win_ratio_t4 = max(5.0, min(99.8, dynamic_win_ratio_t4))

    dynamic_ins_win_t4 = 67.0 + (tab4_steps_inc - 0.20) * 45 + (tab4_consistency - 0.75) * 18 - (tab4_r_star - 30.5) * 1.8
    if "極端降雨" in tab4_rain_shock:
        dynamic_ins_win_t4 -= 4.0
    dynamic_ins_win_t4 = max(10.0, min(99.0, dynamic_ins_win_t4))

    if dynamic_win_ratio_t4 >= 50.0:
        gauge_bar_color = "#83A474"
        gauge_bg_steps = [{'range': [0, 50], 'color': '#FFF5F5'}, {'range': [50, 100], 'color': '#F5F7F4'}]
        status_badge = "<span style='color: #83A474; font-weight: 800;'>🟢 飛輪高效運轉（三方共贏達標）</span>"
    else:
        gauge_bar_color = "#E53E3E"
        gauge_bg_steps = [{'range': [0, 100], 'color': '#FFF5F5'}]
        status_badge = "<span style='color: #E53E3E; font-weight: 800;'>🔴 警示：共贏機率低於 50% 邊界，面臨財務赤字風險</span>"

    col_res_viz, col_res_text = st.columns([1, 1.5])
    
    with col_res_viz:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = dynamic_win_ratio_t4,
            domain = {'x': [0, 1], 'y': [0, 1]},
            number = {'suffix': '%', 'font': {'size': 32, 'color': gauge_bar_color}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#0C0E0B"},
                'bar': {'color': gauge_bar_color, 'thickness': 0.75},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': '#B7CEAD',
                'steps': gauge_bg_steps,
                'threshold': {
                    'line': {'color': "#E53E3E", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_res_text:
        st.markdown(f"""
        <div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:22px; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.01);'>
            <b style='font-size:16px; color:#2D4A22;'>動態聯立沙盤即時清算解讀</b><br>
            <div style="margin-top:12px; line-height: 1.8; font-size: 14px;">
                • 每週預算中立回饋: <b>R* = {tab4_r_star} 元/週</b><br>
                • 保戶平均步數成長率: <b>{tab4_steps_inc*100:.0f}%</b><br>
                • 行為持續性因子: <b>{tab4_consistency}</b><br>
                • 季節氣候模擬情境: <b>{tab4_rain_shock}</b><br>
                <hr style="margin: 10px 0; border-top: 1px solid #E2E8F0;">
                ➔ <b>動態總體共贏勝率：<span style="color: {gauge_bar_color}; font-size: 24px; font-weight: 900;">{dynamic_win_ratio_t4:.1f}%</span></b><br>
                ➔ 保險公司 10 年不輸現行方案機率：<b>{dynamic_ins_win_t4:.1f}%</b><br>
                ➔ 綠能案場償債違約機率：<b>0.0% (DSCR > 1.1)</b><br>
                <div style="margin-top: 10px; padding: 8px 12px; background-color: #F5F7F4; border-radius: 8px; border-left: 4px solid {gauge_bar_color};">
                    狀態判定：{status_badge}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
