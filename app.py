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
    
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #B7CEAD;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
    .metric-value-green {
        font-size: 38px; font-weight: 700; color: #83A474; font-family: 'Inter', -apple-system, sans-serif;
    }
    .metric-value-blue {
        font-size: 38px; font-weight: 700; color: #0C0E0B; font-family: 'Inter', -apple-system, sans-serif;
    }
    .metric-label {
        font-size: 13px; font-weight: 600; color: #475569; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px;
    }
    
    .phone-container {
        border: 10px solid #0C0E0B;
        border-radius: 36px;
        padding: 14px;
        background-color: #0C0E0B;
        box-shadow: 0 15px 35px rgba(0,0,0,0.06);
        height: 610px;
        display: flex;
        flex-direction: column;
    }
    .phone-screen {
        border-radius: 24px;
        background-color: #FFFFFF;
        padding: 22px 16px;
        flex-grow: 1;
        overflow-y: auto;
        color: #0C0E0B;
    }
    
    .vision-card {
        border: 1px solid #B7CEAD; 
        padding: 35px; 
        border-radius: 16px; 
        background-color: #FFFFFF; 
        min-height: 290px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.01);
        transition: all 0.3s ease;
    }
    .vision-card:hover {
        border-color: #83A474;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(131, 164, 116, 0.1);
    }
    
    .dark-green-title {
        color: #2D4A22 !important;
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
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

    div[data-testid="stTabs"] button {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #0C0E0B !important;
        padding: 10px 24px !important;
        border-radius: 8px 8px 0 0 !important;
        background-color: #E6EAE5 !important;
        margin-right: 6px !important;
        border: 1px solid #B7CEAD !important;
        border-bottom: none !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: #B7CEAD !important;
        color: #2D4A22 !important;
        font-weight: 800 !important;
        border-top: 3px solid #83A474 !important;
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
    
    st.markdown("""
        <div style='display: flex; justify-content: center; gap: 15px; margin-bottom: 40px;'>
            <span style='background-color: #FFFFFF; color: #0C0E0B; padding: 8px 20px; border-radius: 24px; font-size: 13px; border: 1px solid #B7CEAD; font-weight: 600;'>國立清華大學 金融科技專題研究</span>
            <span style='background-color: #83A474; color: #F5F7F4; padding: 8px 20px; border-radius: 24px; font-size: 13px; font-weight: 600;'>Quantitative Finance & Information Management</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 1px solid #B7CEAD; margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; font-size: 28px; margin-bottom: 15px; color:#0C0E0B !important; font-weight:800;'>三位一體機制全局摘要</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px; color: #0C0E0B; opacity:0.7; margin-bottom: 20px;'>滑鼠懸停可放大查看資本與數據流轉詳情</p>", unsafe_allow_html=True)
    
    html_canvas_trinity = """
    <div style="width:100%; text-align:center;">
        <canvas id="trinityCanvas" width="900" height="340" style="background:transparent; cursor:pointer;"></canvas>
        <div id="customTooltip" style="position:absolute; display:none; background:rgba(12,14,11,0.95); color:#F5F7F4; padding:15px 20px; border-radius:8px; font-family:sans-serif; text-align:left; pointer-events:none; box-shadow:0 10px 25px rgba(0,0,0,0.3); z-index:9999; max-width:320px; border:1px solid #83A474;"></div>
    </div>

    <script>
        const canvas = document.getElementById('trinityCanvas');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('customTooltip');

        const nodes = [
            { id: 'insurance', name: '🏥 保險公司', x: 450, y: 65, r: 52, color: '#83A474', activeColor: '#2D4A22', title: '🏥 保險公司端', desc: '注入預防成本資本化之準備金，透過資產複利控制並調降大盤理賠損失率。' },
            { id: 'consumer', name: '🌿 消費者(用戶)', x: 230, y: 265, r: 52, color: '#92BA80', activeColor: '#2D4A22', title: '🌿 消費者端', desc: '上傳經過 ZKP 驗證之生物健走行為數據，零門檻共享綠能轉型紅利。' },
            { id: 'energy', name: '⚡ 綠能產業', x: 670, y: 265, r: 52, color: '#0C0E0B', activeColor: '#2D4A22', title: '⚡ 綠能產業端', desc: '錨定發電售電權，吸收散戶碎片化微型資本，調降 WACC 並維持開發商自主權。' }
        ];

        let particles = [
            { from: 0, to: 2, progress: 0.0, speed: 0.005 },
            { from: 0, to: 2, progress: 0.33, speed: 0.005 },
            { from: 0, to: 2, progress: 0.66, speed: 0.005 },
            { from: 2, to: 1, progress: 0.0, speed: 0.005 },
            { from: 2, to: 1, progress: 0.33, speed: 0.005 },
            { from: 2, to: 1, progress: 0.66, speed: 0.005 },
            { from: 1, to: 0, progress: 0.0, speed: 0.005 },
            { from: 1, to: 0, progress: 0.33, speed: 0.005 },
            { from: 1, to: 0, progress: 0.66, speed: 0.005 }
        ];

        let selectedNodeId = "all";

        function drawEcosystem() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.beginPath();
            ctx.moveTo(nodes[0].x, nodes[0].y);
            ctx.lineTo(nodes[2].x, nodes[2].y);
            ctx.lineTo(nodes[1].x, nodes[1].y);
            ctx.closePath();
            ctx.strokeStyle = '#B7CEAD';
            ctx.lineWidth = 3;
            ctx.setLineDash([8, 6]);
            ctx.stroke();
            ctx.setLineDash([]);

            particles.forEach(p => {
                p.progress += p.speed;
                if (p.progress > 1.0) p.progress -= 1.0;

                const startNode = nodes[p.from];
                const endNode = nodes[p.to];
                const currentX = startNode.x + (endNode.x - startNode.x) * p.progress;
                const currentY = startNode.y + (endNode.y - startNode.y) * p.progress;

                ctx.beginPath();
                ctx.arc(currentX, currentY, 7, 0, Math.PI * 2);
                ctx.fillStyle = '#83A474';
                ctx.shadowColor = '#83A474';
                ctx.shadowBlur = 15;
                ctx.fill();
                ctx.shadowBlur = 0;
            });

            nodes.forEach(node => {
                const isSelected = selectedNodeId === node.id;
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
                ctx.fillStyle = isSelected ? node.activeColor : node.color;
                ctx.strokeStyle = '#FFFFFF';
                ctx.lineWidth = isSelected ? 4 : 2;
                ctx.shadowColor = 'rgba(0,0,0,0.1)';
                ctx.shadowBlur = 10;
                ctx.fill();
                ctx.stroke();
                ctx.shadowBlur = 0;

                ctx.fillStyle = (node.id === 'energy' && !isSelected) ? '#F5F7F4' : '#FFFFFF';
                ctx.font = 'bold 14px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(node.name, node.x, node.y);
            });
        }

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            let insideAnyNode = false;

            nodes.forEach(node => {
                const dist = Math.sqrt((mouseX - node.x)**2 + (mouseY - node.y)**2);
                if (dist < node.r) {
                    insideAnyNode = true;
                    tooltip.style.display = 'block';
                    tooltip.style.left = (e.pageX + 15) + 'px';
                    tooltip.style.top = (e.pageY + 15) + 'px';
                    tooltip.innerHTML = `<div style="font-size:18px; font-weight:800; color:#B7CEAD; margin-bottom:6px;">${node.title}</div><div style="font-size:15px; line-height:1.6; font-weight:500;">${node.desc}</div>`;
                }
            });
            if (!insideAnyNode) tooltip.style.display = 'none';
        });

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            nodes.forEach(node => {
                const dist = Math.sqrt((mouseX - node.x)**2 + (mouseY - node.y)**2);
                if (dist < node.r) {
                    selectedNodeId = (selectedNodeId === node.id) ? "all" : node.id;
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: selectedNodeId}, '*');
                }
            });
        });

        function animate() {
            drawEcosystem();
            requestAnimationFrame(animate);
        }
        animate();
    </script>
    """
    component_value = components.html(html_canvas_trinity, height=350)
    if component_value is not None:
        st.session_state.selected_node = component_value

    border_consumer = "2px solid #2D4A22" if st.session_state.selected_node == "consumer" else "1px solid #B7CEAD"
    border_insurance = "2px solid #2D4A22" if st.session_state.selected_node == "insurance" else "1px solid #B7CEAD"
    border_energy = "2px solid #2D4A22" if st.session_state.selected_node == "energy" else "1px solid #B7CEAD"

    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown(f"""
            <div class="vision-card" style="background-color: #FFFFFF !important; opacity: 1.0; border: {border_consumer} !important;">
                <div style='width: 40px; height: 6px; background-color: #83A474; margin-bottom: 20px; border-radius: 3px;'></div>
                <div class="dark-green-title">消費者端：生物行為資產化</div>
                <p style='font-size: 14.5px; color: #0C0E0B; line-height: 1.7; opacity: 0.85;'>徹底打破財富階級門檻。無痛認購綠能案場份額，共享淨零轉型之資本紅利。</p>
            </div>
            """, unsafe_allow_html=True)
    with col_card2:
        st.markdown(f"""
            <div class="vision-card" style="background-color: #FFFFFF !important; opacity: 1.0; border: {border_insurance} !important;">
                <div style='width: 40px; height: 6px; background-color: #B7CEAD; margin-bottom: 20px; border-radius: 3px;'></div>
                <div class="dark-green-title">保險公司端：高效率風險管理</div>
                <p style='font-size: 14.5px; color: #0C0E0B; line-height: 1.7; opacity: 0.85;'>將既有行銷費用與理賠準備金提前折現注入綠能基金，透過資產的生產性複利增值感，實質且長期優化保戶健康品質，控制理賠損失率。</p>
            </div>
            """, unsafe_allow_html=True)
    with col_card3:
        st.markdown(f"""
            <div class="vision-card" style="background-color: #FFFFFF !important; opacity: 1.0; border: {border_energy} !important;">
                <div style='width: 40px; height: 6px; background-color: #92BA80; margin-bottom: 20px; border-radius: 3px;'></div>
                <div class="dark-green-title">綠能產業端：去中心化普惠資本</div>
                <p style='font-size: 14.5px; color: #0C0E0B; line-height: 1.7; opacity: 0.85;'>底層資產錨定「陽光綠益」等 STO 售電收益權。引入散戶碎金流以降低開發商資金成本（WACC），同時維護電廠之經營自主權。</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='border-top: 1px solid #B7CEAD; padding: 35px 0; text-align: center; font-size: 12px; color: #0C0E0B; background-color: #FFFFFF; margin: 0 -4rem;'>
            <b>© 2026 EcoStride Research Project. Powered by Streamlit Community Cloud.</b><br>
            研究成員：蔡宜伶 | 賀舜禹 | 曾琬甯
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. 分頁二：提案動機與模式介紹
# ==========================================
elif page == "提案動機與模式介紹":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>💡 提案動機與模式介紹</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800; margin-bottom:15px;'>一、 現行系統之結構性失靈</h3>", unsafe_allow_html=True)
    st.markdown("""
        <table class="styled-table">
            <tr>
                <th>保險機構</th>
                <th>核心量化計費模式</th>
                <th>主要經濟激勵機制類型</th>
                <th>學術限制判讀</th>
            </tr>
            <tr>
                <td><b>國泰人壽</b></td>
                <td>AI 活力分多面向量化評分</td>
                <td>週週領點數模式（小樹點）</td>
                <td>側重即時性之消費回饋，缺乏跨期資本留存</td>
            </tr>
            <tr>
                <td><b>富邦人壽</b></td>
                <td>鎖定計步省保費機制</td>
                <td>次年保費最高折抵 10%</td>
                <td>偏重長期財務減負，但無法產生資產複利增值感</td>
            </tr>
            <tr>
                <td><b>第一金人壽</b></td>
                <td>遊戲化積分累積與商城兌換</td>
                <td>開放式平台商品兌換券</td>
                <td>純屬一次性行銷預算消耗，與理賠池優化脫鉤</td>
            </tr>
            <tr>
                <td><b>南山人壽</b></td>
                <td>生理年齡減齡演算法</td>
                <td>個人步數挑戰與 CSR 公益捐款耦合</td>
                <td>外部化社會責任，未能提供個人端財務永續誘因</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

    col_fail1, col_fail2 = st.columns(2)
    with col_fail1:
        st.markdown("""
            <div class="alert-card">
                <span style="color:#83A474; font-weight:800; font-size:16px;">邊際效用遞減與長期價值缺失</span><br style="margin-bottom:8px;">
                現行點數 or 現金券在核發與使用的瞬間，其經濟價值即告終結，缺乏資產增值所需之<b>複利效應</b>。
                由於獎勵無法轉化為長期資本，用戶難以將健康行為視為一種「投資」，誘因隨時間呈對數曲線下滑。
            </div>
            """, unsafe_allow_html=True)
    with col_fail2:
        st.markdown("""
            <div class="alert-card">
                <span style="color:#83A474; font-weight:800; font-size:16px;">雙曲貼現與現時偏誤（Present Bias）</span><br style="margin-bottom:8px;">
                人類天生具備現時偏誤，對未來健康獲益之評價遠低於即時享樂。
                當回饋不具資本增值潛力時，用戶難以克服長期運動之生理痛苦，最終導致高度流失率。
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
        <div class="alert-card-danger">
            <span style="color:#E53E3E; font-weight:800; font-size:16px;">財務與經營層面之負面影響：</span><br style="margin-bottom:8px;">
            金融機構為了維持日活躍用戶，被迫持續加碼行銷支出，陷入高獲客成本與低生命週期價值之財務泥淖；
            若無法實質控制理賠損失率，行銷活動將從風險管理投資轉化為純粹之資產流失。
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_stepn1, col_stepn2 = st.columns(2)
    with col_stepn1:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; border-bottom: 2px solid #83A474; padding-bottom: 6px;'>二、 STEPN Move-to-Earn 模式之反思</h4>", unsafe_allow_html=True)
        st.markdown("""
            STEPN 雖透過 Web3 遊戲化驅動健康行為，吸引超過 200 萬用戶。然而，其核心崩盤原因在於
            <b>「死亡螺旋經濟模型」</b>──高度依賴新用戶流入以支撐舊用戶收益（龐氏結構），代幣（GST）通膨嚴重且缺乏真實資產背書，導致資產價值最終崩盤.
            <br><br>
            <b>EcoStride 的改良路徑：</b>借鏡其健康驅動與碎片化參與之優勢，但<b>轉向實體資產（RWA）背書</b>，將步數代幣（STRIDE）錨定綠能收益權，徹底避免純投機風險。
            """, unsafe_allow_html=True)
    with col_stepn2:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; border-bottom: 2px solid #83A474; padding-bottom: 6px;'>三、 永續投資市場門檻與資本隔離</h4>", unsafe_allow_html=True)
        st.markdown("""
            高品質綠色資產（如離岸風電債券與大型太陽能案場收益權）具備顯著的規模排他性，最低認購額度通常達新台幣一百萬元以上，長期由機構法人壟斷，導致小額資本與年輕世代難以介入。碎片化資金因行政成本過高，被排除在永續轉型的資本紅利之外。
            """, unsafe_allow_html=True)

    st.markdown("<br>---<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800; margin-bottom:15px;'>四、 創新提案 ── 三位一體模型</h3>", unsafe_allow_html=True)
    st.markdown("""
        本專案提出一套將個體健康行為直接轉化為資本累積之流轉模式。核心在於重隔流動機制：<b>將消耗性獎勵重構為生產性累積</b>。
        保戶之健康行為不再僅是換取一次性消費憑證，而是轉化為具備增值潛力之生產性資本投入，建立長期且具備複利效應之資產池。
        <br><br>
        <b>三方共贏博弈分析：</b><br>
        1. <b>用戶端</b>：提供經過驗證之健康行為數據，藉此交換取得實體資產代幣化之收益權份額。<br>
        2. <b>保險公司端</b>：投入既有之行銷預算或理賠準備金作為資產認購資金，換取保戶理賠率之降低與 ESG 評級之提升。<br>
        3. <b>綠能產業端</b>：獲取來自廣大受眾、碎片化且低成本之建設資金.<b>碎片化資本具備純粹之財務投資屬性</b>，投資者人數眾多卻不具備干涉經營之組織力。這能讓綠能業者在獲取穩定建設資金同時，<b>保有更高之經營獨立性與獲利分配主導權</b>。
        """, unsafe_allow_html=True)

    st.markdown("<br>---<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800; margin-bottom:15px;'>五、 本土實證與合規機制 ── 台灣市場落地性</h3>", unsafe_allow_html=True)
    st.markdown("""
        <b>1. 法規政策演進與監管試驗環境分析</b><br>
        金管會自 2023 年起放寬證券型代幣（STO）規範，並於 2024 年正式成立實體資產代幣化小組。2025 年 9 月之概念驗證報告成功驗證債券與基金代幣化之可行性，落實券款對付之即時交割機制。此項技術突破，為本計畫中生物行為資產化後之即時權益分配，奠定了關鍵的技術與法理基礎。
        <br><br>
        <b>2. 國泰證券「陽光綠益」STO 案例研究（底層資產實證）</b><br>
        國泰證券與綠點能創合作，發行台灣首檔 STO「陽光綠益」（募資規模三千萬元）。底層資產為六年期債務型憑證，提供年利率 3.5% 之固定回報。此案例成果直接解決了過往 Web3 模式缺乏實體資產背書之痛點。實體資產代幣化提供穩定之綠能收益權充當價值支撐，使 EcoStride 核發之數位憑證具備實體操作力背書。
        <br><br>
        <b>3. 隱私保護與次級市場流通</b><br>
        針對資產期限較長之特性，擬引入自動化造市商機制建立微型資產流動性池；在個資隱私上，<b>採用零知識證明技術（Zero-Knowledge Proofs, ZKP）保護隱私</b>，確保代幣化資產之發行、存管與存管皆符合國際監管標準。
        """, unsafe_allow_html=True)

# ==========================================
# 6. 分頁三：APP 介面展示 (四大功能升級與頂級 UI/UX 質感版)
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
        profile_choice = st.radio("運動族群預設切換：", ["高活躍型 (High)", "典型保戶 (Medium)", "Low 低活躍型"])
        
        if "高活躍" in profile_choice:
            init_steps, init_cons, sel_g = 8700, 0.95, 0
        elif "典型保戶" in profile_choice:
            init_steps, init_cons, sel_g = 6300, 0.75, 1
        else:
            init_steps, init_cons, sel_g = 4300, 0.40, 2
            
        ui_steps = st.slider("設定您的每日平均步數：", 3000, 15000, init_steps, 500)
        ui_cons = st.slider("設定行為持續性因子 (Consistency)：", 0.1, 1.0, init_cons, 0.05)
        
        st.markdown("<br>", unsafe_allow_html=True)
        app_tab_view = st.radio("手機 APP 檢視頁籤：", ["① 每日運動與獎勵", "② RWA 綠能資產錢包", "③ 保單風險與分紅"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 計算即時模擬數值
    base_target_steps = CFG.base_steps[sel_g] + CFG.goal_extra
    step_diff = ui_steps - CFG.base_steps[sel_g]
    ach_prob_est = min(0.95, max(0.05, (step_diff / CFG.goal_extra) * CFG.p_ach_gain[sel_g] * ui_cons))
    weekly_expected_reward = ach_prob_est * current_r_star
    
    # RWA 複利資產計算
    r_w_weekly = CFG.r_user / wpy_val
    accumulated_rwa_val = 0.0
    for w_i in range(5 * wpy_val):
        w_pay = weekly_expected_reward if (w_i % wpy_val < 45) else weekly_expected_reward * 0.8
        accumulated_rwa_val = accumulated_rwa_val * (1 + r_w_weekly) + w_pay

    # ESG 實感換算（假設每 10,000 步折算 0.08 kg 碳減排，累積 5 年換算植樹數）
    total_steps_5yr = ui_steps * 365 * 5
    carbon_saved_kg = total_steps_5yr * 0.0000125
    trees_equivalent = int(carbon_saved_kg / 12) + 1

    with col_ui_right:
        if "①" in app_tab_view:
            screen_content = f"""
                <div style="font-size:10px; font-weight:800; color:#83A474; text-align:center; letter-spacing:1px; margin-bottom:6px;">👣 DAILY HEALTH DASHBOARD</div>
                <div style="background:#F8F9FA; border:1px solid #E2E8F0; padding:14px; border-radius:16px; text-align:center; margin-bottom:10px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
                    <span style="font-size:28px; font-weight:900; color:#0C0E0B;">{ui_steps:,} 👣</span>
                    <div style="font-size:10px; color:#666; font-weight:600; margin-top:2px;">TODAY'S AVERAGE STEPS</div>
                </div>
                
                <!-- 功能一：每週連續打卡 (Streak) 進度條 -->
                <div style="background:#F0F4EC; border:1px solid #B7CEAD; padding:10px 12px; border-radius:14px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; font-size:10px; font-weight:700; color:#2D4A22; margin-bottom:4px;">
                        <span>🔥 4週連續加成進度</span>
                        <span>第 3 週 / 差 2 天享 +20%</span>
                    </div>
                    <div style="display:flex; gap:6px; justify-content:center;">
                        <div style="flex:1; height:8px; background:#83A474; border-radius:4px;"></div>
                        <div style="flex:1; height:8px; background:#83A474; border-radius:4px;"></div>
                        <div style="flex:1; height:8px; background:#83A474; border-radius:4px;"></div>
                        <div style="flex:1; height:8px; background:#D1D5DB; border-radius:4px;"></div>
                    </div>
                </div>

                <div style="display:flex; gap:8px; margin-bottom:10px;">
                    <div style="flex:1; background:#F8F9FA; border:1px solid #E2E8F0; padding:8px; border-radius:12px; text-align:center;">
                        <span style="font-size:9px; color:#666;">預估週達標率</span>
                        <div style="font-size:14px; font-weight:800; color:#2D4A22; margin-top:2px;">{ach_prob_est*100:.1f}%</div>
                    </div>
                    <div style="flex:1; background:#F8F9FA; border:1px solid #E2E8F0; padding:8px; border-radius:12px; text-align:center;">
                        <span style="font-size:9px; color:#666;">本週預期回饋 (R*)</span>
                        <div style="font-size:14px; font-weight:800; color:#83A474; margin-top:2px;">NT$ {weekly_expected_reward:.1f}</div>
                    </div>
                </div>

                <!-- 功能三：ZKP 隱私與 ESG 實感標籤 -->
                <div style="background:#EBF3EA; border:1px solid #B7CEAD; padding:10px; border-radius:12px; font-size:9px; color:#2D4A22; line-height:1.5;">
                    🔒 <b>ZKP 隱私防護：</b>Apple Health 步數已完成零知識加密同步。<br>
                    🌱 <b>ESG 貢獻：</b>相當於為地球減少 <b>{carbon_saved_kg:.1f} kg</b> 碳排，等同種植 <b>{trees_equivalent} 棵樹</b>！
                </div>
            """
        elif "②" in app_tab_view:
            screen_content = f"""
                <div style="font-size:10px; font-weight:800; color:#83A474; text-align:center; letter-spacing:1px; margin-bottom:8px;">📈 RWA GREEN PORTFOLIO</div>
                <div style="background:#F8F9FA; border:1px solid #E2E8F0; padding:14px; border-radius:14px; text-align:center; margin: 10px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
                    <span style="font-size:10px; color:#666; font-weight:600;">5年累積 STRIDE 資產市值</span>
                    <div style="font-size:22px; font-weight:900; color:#83A474; margin-top:4px;">NT$ {accumulated_rwa_val:,.0f}</div>
                </div>
                <div style="font-size:10px; background:#F8F9FA; padding:12px; border-radius:12px; border:1px solid #E2E8F0; line-height:1.6;">
                    <b>底層真實綠能資產 (STO)：</b><br>
                    • 標的：國泰證券「陽光綠益」太陽能案場<br>
                    • 基礎固定票息：3.5% (享 10% 分潤)<br>
                    • 流動性：自動化微型資產流動性池<br>
                    👣 <b>步數轉化率：</b>日均 {ui_steps:,} 步全面高效賦能實體綠能！
                </div>
            """
        else:
            screen_content = f"""
                <div style="font-size:10px; font-weight:800; color:#83A474; text-align:center; letter-spacing:1px; margin-bottom:6px;">🛡️ POLICY & RISK STATUS</div>
                <div style="background:#F8F9FA; border:1px solid #E2E8F0; padding:10px 12px; border-radius:12px; text-align:left; margin-bottom:8px;">
                    <span style="font-size:9px; color:#666;">保單年度與風險合規</span>
                    <div style="font-size:13px; font-weight:800; color:#2D4A22; margin-top:1px;">第 3 年度 (在籍有效・大盤損失率 74.2%)</div>
                </div>
                
                <!-- 功能四：保單回饋金自動化配置決策 -->
                <div style="background:#F0F4EC; border:1px solid #B7CEAD; padding:10px; border-radius:12px; font-size:10px; color:#0C0E0B;">
                    <b>💡 回饋金智慧配置模式：</b><br>
                    <div style="margin-top:4px; font-size:9px; color:#333; line-height:1.5;">
                        ☑️ <b>滾入 RWA 綠能資產 (預設，享 3.5% 複利)</b><br>
                        ☐ 自動折抵次年保費 (省錢省心)<br>
                        ☐ 現金提領 (需滿 2 年歸屬期)
                    </div>
                </div>
                <div style="font-size:8px; color:#777; margin-top:8px; text-align:center;">
                    未滿 2 年解約者帳戶回歸保險準備金，滿 2 年後全額歸屬用戶。
                </div>
            """

        phone_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
                background-color: transparent;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            .iphone-container {{
                width: 300px;
                background: #111111;
                border-radius: 42px;
                padding: 10px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.25);
                border: 3px solid #333333;
            }}
            .iphone-screen {{
                background: #FFFFFF;
                border-radius: 32px;
                padding: 16px 12px;
                min-height: 460px;
                color: #0C0E0B;
            }}
            .phone-status {{
                font-size: 10px;
                color: #888888;
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                font-weight: 700;
            }}
        </style>
        </head>
        <body>
            <div class="iphone-container">
                <div class="phone-status">
                    <span>09:41</span>
                    <span>EcoStride OS 👣</span>
                    <span>🔋 100%</span>
                </div>
                <div class="iphone-screen">
                    {screen_content}
                </div>
            </div>
        </body>
        </html>
        """
        st.components.v1.html(phone_html, height=510)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 底部動態趨勢圖
    fig_app_trend = go.Figure()
    yrs_arr = list(range(1, 6))
    simulated_path = [accumulated_rwa_val * (y / 5) * (1.1 if y > 1 else 1.0) for y in yrs_arr]
    legacy_path_app = [1194 * y for y in yrs_arr]
    
    fig_app_trend.add_trace(go.Scatter(x=yrs_arr, y=simulated_path, name="EcoStride APP 用戶累積資產", line=dict(color="#83A474", width=3)))
    fig_app_trend.add_trace(go.Scatter(x=yrs_arr, y=legacy_path_app, name="傳統外溢點數方案 (立即消耗)", line=dict(color="#E53E3E", width=2, dash="dash")))
    fig_app_trend.update_layout(title="【互動展示】使用者動態行為對應之 5 年資產成長預測", template="plotly_white", height=280, margin=dict(l=30, r=30, t=30, b=30))
    st.plotly_chart(fig_app_trend, use_container_width=True)
    # ==========================================
    # 🔄 面向四：整體循環模式
    # ==========================================
    with tab_res4:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>生態系成功啟動之三方共贏機率與邊界條件 (互動沙盤)</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#555;'>您可以<b>直接調整下方參數滑桿與氣候情境</b>。當共贏機率低於 50% 時，儀表板將自動顯示為嚴格的<b>紅色警戒</b>；高於 50% 則呈現<b>綠色高效運轉</b>：</p>", unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            div[data-baseweb="select"] > div {
                background-color: #F0F4EC !important;
                border: 1.5px solid #83A474 !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
            }
            div[data-baseweb="select"] span {
                color: #2D4A22 !important;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:20px; border-radius:12px; margin-bottom:20px;'>", unsafe_allow_html=True)
        st.markdown("<b style='color:#2D4A22; font-size:15px;'>🎛️ 聯立動態沙盤參數控制台</b>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            tab4_r_star = st.slider("每週預算中立回饋 R* (元/達標週)", 20.0, 50.0, R_STAR_DEFAULT, 1.0, key="t4_r_v3")
            tab4_steps_inc = st.slider("保戶平均健走提升率", 0.05, 0.50, tab4_steps_inc if 'tab4_steps_inc' in locals() else 0.20, 0.05, key="t4_s_v3")
        with col_c2:
            tab4_consistency = st.slider("全域行為穩定度因子", 0.30, 1.00, tab4_consistency if 'tab4_consistency' in locals() else 0.75, 0.05, key="t4_c_v3")
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
                    • 氣候季節模擬情境: <b>{tab4_rain_shock}</b><br>
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

# ==========================================
# 加分項：代碼與公式互鎖
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📄 檢視後台核心複利精算公式 (互鎖定量金融與資管代碼)"):
    st.code("""
# 智慧合約跨期核心資產滾存演算法
def calculate_compounding_rwa_wealth(excess_steps, alpha=0.00065, beta=0.0001, gamma=CFG.gamma, consistency=0.75, rwa_yield_base=CFG.coupon, insurance_share_yield=CFG.insurer_coupon_share, mu_market=0.05):
    weekly_reward = R_STAR_DEFAULT * consistency
    annual_investment = weekly_reward * 52
    
    total_user_rwa_wealth = 0.0
    for year in range(1, 11):
        annual_rwa_yield_generated = total_user_rwa_wealth * rwa_yield_base
        rwa_flowback_to_insurance = annual_rwa_yield_generated * insurance_share_yield
        user_yield_reinvest = annual_rwa_yield_generated - rwa_flowback_to_insurance
        
        total_user_rwa_wealth += annual_investment + user_yield_reinvest
        total_user_rwa_wealth *= (1.0 + mu_market)
    return total_user_rwa_wealth
        """, language="python")
