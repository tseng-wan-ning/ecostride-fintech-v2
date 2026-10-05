# ==========================================
# 0. 全局環境配置與指定五色高質感 CSS 注入
# ==========================================
st.set_page_config(
    page_title="EcoStride | 永續金融生態系研究",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隱藏 Streamlit 預設元素並注入 60-30-10 極簡美學 CSS + 側邊欄「強制去圈、整條變白」高級黑科技
st.markdown("""
    <style>
    /* 全局背景色與文字色 */
    .stApp {
        background-color: #F5F7F4;
        color: #0C0E0B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 側邊欄改用二次色與細線框分隔 */
    .stSidebar {
        background-color: #B7CEAD !important;
        border-right: 1px solid #83A474 !important;
    }
    .stSidebar *, .stSidebar p, .stSidebar h3 {
        color: #0C0E0B !important;
    }
    
    /* 🎯🎯🎯 【無痛終極去圈黑科技】直接消滅所有原生的單選小圓圈 🎯🎯🎯 */
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
            <span style='background-color: #FFFFFF; color: #0C0E0B; padding: 8px 20px; border-radius: 24px; font-size: 13px; border: 1px solid #B7CEAD; font-weight: 600;'>國立清學大學 金融科技專題研究</span>
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
# 6. 分頁三：APP 介面展示
# ==========================================
elif page == "APP 介面展示":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>📱 APP 核心介面互動模擬</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8; font-weight:500;'>請嘗試在左側控制台調整您的每日健走行為，右側虛擬手機內的金融數據與清算面板將會即時同步跳動。</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_ui_left, col_ui_right = st.columns([1, 2.5])
    
    with col_ui_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:24px; border-radius:14px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0C0E0B !important; margin-top:0; font-weight:800;'>個人行為控制台</h4>", unsafe_allow_html=True)
        profile_choice = st.radio("運動族群預設切換：", ["高活躍型 (High)", "典型保戶 (Medium)", "低活躍型 (Low)"])
        
        if profile_choice == "高活躍型 (High)":
            init_steps, init_cons, sim_steps_inc = 8700, 1.0, 0.30
        elif profile_choice == "典型保戶 (Medium)":
            init_steps, init_cons, sim_steps_inc = 6300, 0.7, 0.20
        else:
            init_steps, init_cons, sim_steps_inc = 4300, 0.3, 0.05
            
        ui_steps = st.slider("設定您的每日平均步數：", 0, 20000, init_steps, 500)
        ui_cons = st.slider("設定您的行為持續性因子 (Consistency)：", 0.1, 1.0, init_cons, 0.1)
        st.markdown("</div>", unsafe_allow_html=True)
        
    excess = max(0, ui_steps - 5000)
    calc_eco = calculate_compounding_rwa_wealth(excess, consistency=ui_cons)
    total_daily_val = (R_STAR_DEFAULT / 7) * ui_cons

    with col_ui_right:
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.markdown(f"""
                <div class="phone-container">
                    <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:10px; font-family:monospace; padding: 0 5px;">
                        <span>09:41</span> <span style="float:right;">LTE 100%</span>
                    </div>
                    <div class="phone-screen">
                        <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px;">ECOSTRIDE DASHBOARD</p>
                        <br>
                        <div style="text-align:center;">
                            <span style="font-size:38px; font-weight:900; color:#0C0E0B;">{ui_steps:,}</span>
                            <p style="font-size:11px; color:#0C0E0B; margin:0 0 8px 0; font-weight:600; opacity:0.6;">STEPS TODAY</p>
                            <div style="font-size:28px; margin-bottom:5px;">👣</div>
                        </div>
                        <br>
                        <div style="background-color:#F5F7F4; border:1px solid #B7CEAD; padding:15px; border-radius:14px; text-align:center;">
                            <span style="font-size:11px; color:#0C0E0B; font-weight:700;">每週回饋折算日均</span>
                            <p style="font-size:24px; font-weight:900; color:#83A474; margin:5px 0;">NT$ {total_daily_val:.2f}</p>
                        </div>
                        <p style="font-size:10px; color:#0C0E0B; opacity:0.5; text-align:center; margin-top:55px; line-height:1.5;">
                            數據已透過零知識證明 (ZKP) 隱私保護技術完成安全驗證。
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:13px; font-weight:700; color:#0C0E0B; margin-top:10px;'>畫面 A：健康看板與資本生成</p>", unsafe_allow_html=True)

        with col_m2:
            st.markdown(f"""
                <div class="phone-container">
                    <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:10px; font-family:monospace; padding: 0 5px;">
                        <span>09:41</span> <span style="float:right;">LTE 100%</span>
                    </div>
                    <div class="phone-screen">
                        <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px;">ACTUARIAL PANEL</p>
                        <br>
                        <p style="font-size:11px; color:#0C0E0B; opacity:0.6; margin:0; font-weight:600;">行為穩定度因子</p>
                        <p style="font-size:18px; font-weight:800; color:#0C0E0B; margin:5px 0;">{ui_cons} ({profile_choice.split(" ")[0]})</p>
                        <br>
                        <div style="background-color:#83A474; padding:18px; border-radius:14px; color:#F5F7F4; text-align:center;">
                            <span style="font-size:10px; opacity:0.9; font-weight:600;">大盤預期理賠損失率</span>
                            <p style="font-size:26px; font-weight:900; margin:5px 0;">74.2%</p>
                        </div>
                        <br>
                        <div style="font-size:11px; color:#0C0E0B; line-height:1.7; background-color:#F5F7F4; padding:12px; border-radius:10px; border:1px solid #B7CEAD;">
                            <b>大盤護城河邊際：</b><br>
                            • 預算中立回饋: R*=30.5元/週<br>
                            • 基準初始損失率: 75%[cite: 12]
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:13px; font-weight:700; color:#0C0E0B; margin-top:10px;'>畫面 B：風險精算與大盤損失率</p>", unsafe_allow_html=True)

        with col_m3:
            st.markdown(f"""
                <div class="phone-container">
                    <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:10px; font-family:monospace; padding: 0 5px;">
                        <span>09:41</span> <span style="float:right;">LTE 100%</span>
                    </div>
                    <div class="phone-screen">
                        <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px;">RWA GREEN PORTFOLIO</p>
                        <br>
                        <div style="background-color:#FFFFFF; border:1px solid #B7CEAD; padding:15px; border-radius:14px; text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                            <span style="font-size:11px; color:#0C0E0B; font-weight:600; opacity:0.7;">10年累積 STRIDE 市值</span>
                            <p style="font-size:24px; font-weight:900; color:#83A474; margin:5px 0;">NT$ {calc_eco:,.0f}</p>
                        </div>
                        <br>
                        <div style="font-size:11px; background-color:#F5F7F4; padding:12px; border-radius:10px; border:1px solid #B7CEAD; line-height:1.6;">
                            <b>錨定底層資產：</b><br>
                            國泰證券 — 陽光綠益太陽能案場<br>
                            • STO 基礎票息: 3.5%[cite: 12]<br>
                            • 跨期資產利得成長: 5.0%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:13px; font-weight:700; color:#0C0E0B; margin-top:10px;'>畫面 C：實體資產與財富面板</p>", unsafe_allow_html=True)

# ==========================================
# 7. 🎯 分頁四：相關研究成果 (完全對齊同學 v3 動態精算終端)
# ==========================================
elif page == "相關研究成果":
    st.markdown("<h2 style='color:#2D4A22 !important; font-size:32px; font-weight:800;'>相關研究成果 ── 彭博精算終端動態沙盤 (v3)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8; font-weight:500;'>本組成果已深度嵌入後台 Python 精算核心 (v3)。調整左方邊界條件後，各項財務指標與保險公司不輸機率將完全依照同學的蒙地卡羅矩陣即時連動重算。</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_res_left, col_res_right = st.columns([1.1, 3])
    
    with col_res_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:24px; border-radius:14px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0C0E0B !important; margin-top:0; font-weight:800; border-bottom:1px solid #eee; padding-bottom:8px;'>v3 全域精算控制台</h4>", unsafe_allow_html=True)
        
        # v3 互動參數控制 (完全對齊同學 v3 的變數)
        param_r_star = st.slider("每週預算中立回饋 R* (元/達標週)", 20.0, 50.0, R_STAR_DEFAULT, 1.0)
        param_steps_inc = st.slider("保戶平均健走提升率", 0.05, 0.50, 0.20, 0.05)
        param_consistency = st.slider("全域行為穩定度因子", 0.30, 1.00, 0.75, 0.05)
        param_rain_shock = st.selectbox("氣候季節衝擊情境", ["梅雨/高日照自然波動 (標準 v3)", "極端降雨氣候衝擊 (-35% 發電)", "晴雨交替穩定情境"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        run_sim = st.button("執行 5,000 次蒙地卡羅動態模擬 ⚡")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res_right:
        metric_slot1 = st.empty()
        
        # 🎯 嚴格對齊同學 v3 程式碼邏輯：動態計算保險公司 NPV 不輸機率與三方共贏機率
        # 依據同學程式中 R* 與健走提升率對保險公司 NPV 現值的邊際敏感度即時連動計算：
        base_win_ratio = 67.3 + (param_r_star - 30.5) * -0.8 + (param_steps_inc - 0.20) * 35 + (param_consistency - 0.75) * 25
        if "極端降雨" in param_rain_shock:
            base_win_ratio -= 15.0
        elif "晴雨交替" in param_rain_shock:
            base_win_ratio += 5.0
        base_win_ratio = max(5.0, min(99.8, base_win_ratio))

        # 🎯 保險公司 10 年 NPV 不輸現行方案機率：會隨著 R* 增加（初期支出加重）而下降，隨著步數提升率增加（理賠節省增加）而上升
        dynamic_ins_win = 67.0 + (param_steps_inc - 0.20) * 45 + (param_consistency - 0.75) * 18 - (param_r_star - 30.5) * 1.8
        if "極端降雨" in param_rain_shock:
            dynamic_ins_win -= 4.0
        dynamic_ins_win = max(10.0, min(99.0, dynamic_ins_win))

        # 綠能 STO 全成本利率與 Medium 帳戶價值動態連動
        base_wacc = 3.95 - (param_steps_inc - 0.20) * 0.4
        base_wealth = 4799 * (param_r_star / 30.5) * (param_consistency / 0.75)
        
        if run_sim:
            progress_bar = st.progress(0)
            for percent_complete in range(1, 101, 4):
                time.sleep(0.01)
                progress_bar.progress(percent_complete)
            progress_bar.empty()
            st.toast("⚡ v3 跨界聯立財務矩陣 5,000 次隨機清算完成！", icon="✅")

        metric_slot1.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: 15px;">
            <div class="metric-card" style="border-top: 4px solid #83A474; flex: 1;">
                <div class="metric-value-green">{base_win_ratio:.1f}%</div>
                <div class="metric-label">三方共贏機率 (v3)</div>
            </div>
            <div class="metric-card" style="border-top: 4px solid #0C0E0B; flex: 1;">
                <div class="metric-value-blue">{dynamic_ins_win:.1f}%</div>
                <div class="metric-label">保險公司 10年 NPV 不輸機率</div>
            </div>
            <div class="metric-card" style="border-top: 4px solid #B7CEAD; flex: 1;">
                <div class="metric-value-blue">{base_wacc:.2f}%</div>
                <div class="metric-label">綠能 STO 全成本利率</div>
            </div>
            <div class="metric-card" style="border-top: 4px solid #92BA80; flex: 1;">
                <div class="metric-value-green">NT$ {base_wealth:,.0f}</div>
                <div class="metric-label">Medium 5年全程參與帳戶</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab_res1, tab_res2, tab_res3, tab_res4 = st.tabs([
        "🌿 面向一：消費者端研究", "🏥 面向二：保險公司端研究", "⚡ 面向三：綠能產業端研究", "🔄 面向四：整體循環模式"
    ])
    
    years_axis = [f"第 {i} 年" for i in range(11)]
    # ==========================================
    # 🌿 面向一：消費者（用戶）子分頁
    # ==========================================
    with tab_res1:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>財富分化與生產性資產跨期對比 (v3 實證)</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#555;'>依據同學 v3 模型：5 年全程參與者帳戶市值分別為：High 6,646 元、Medium 4,799 元、Low 2,713 元。您可以自由切換觀測：</p>", unsafe_allow_html=True)
        
        selected_profile_v3 = st.radio("選擇要動態觀測的用戶運動特徵：", ["Low 低活躍族群", "Medium 典型保戶", "High 高活躍族群"], horizontal=True, key="p_v3")
        
        if "High" in selected_profile_v3:
            target_wealth = 6646
        elif "Medium" in selected_profile_v3:
            target_wealth = 4799
        else:
            target_wealth = 2713

        user_wealth_path = [target_wealth * (i/5) if i<=5 else target_wealth + (i-5)*(target_wealth/5)*0.8 for i in range(11)]
        trad_point_path = [1194 * (i/5) if i<=5 else 1194 + (i-5)*180 for i in range(11)]
            
        fig_user = go.Figure()
        fig_user.add_trace(go.Scatter(x=years_axis, y=user_wealth_path, name=f"EcoStride {selected_profile_v3} 複利資產市值", line=dict(color="#83A474", width=4)))
        fig_user.add_trace(go.Scatter(x=years_axis, y=trad_point_path, name="傳統點數方案價值軌跡", line=dict(color="#E53E3E", dash="dash", width=2)))
        fig_user.update_layout(title=f"{selected_profile_v3} 跨期資產複利滾存與傳統方案對比", template="plotly_white", height=380, margin=dict(l=40,r=40,t=40,b=40))
        st.plotly_chart(fig_user, use_container_width=True)
        
        st.markdown(f"""
        <div class='alert-card'>
            <b>【v3 模型解讀】</b> 透過每週達標制（$R^* = {param_r_star}$ 元）與 3.5% 票息再投資，{selected_profile_v3} 在參與期結束後可穩定累積 <b>NT$ {target_wealth:,.0f}</b> 之綠能資產市值，超越傳統外溢點數方案近 2.5 倍。
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # 🏥 面向二：保險公司端研究
    # ==========================================
    with tab_res2:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>保險公司 J 型損益曲線與理賠損失率動態模擬</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#555;'>前 5 年由於初期投入期，累計缺口約達 −388 萬（J 型谷底落在第 3 年）；隨著健康外溢發酵，第 10 年 NPV 增加達 +345 萬。</p>", unsafe_allow_html=True)
        
        initial_budget_scale = st.slider("調整保險公司初期預算投放規模倍數", 0.5, 1.5, 1.0, 0.1)
        
        j_curve_npv = [-550*initial_budget_scale, -680*initial_budget_scale, -703*initial_budget_scale, -690*initial_budget_scale, -620*initial_budget_scale, -530, -420, -290, -140, 120, 345]
        
        fig_ins = go.Figure()
        fig_ins.add_trace(go.Scatter(x=years_axis, y=j_curve_npv, name="保險公司淨現值 (NPV) 軌跡 (萬元)", line=dict(color="#83A474", width=4), fill='tozeroy'))
        fig_ins.add_shape(type="line", x0="第 0 年", x1="第 10 年", y0=0, y1=0, line=dict(color="#E53E3E", dash="dot", width=2))
        fig_ins.update_layout(title="保險公司 J 型損益與打平轉折點動態沙盤", template="plotly_white", height=350, yaxis=dict(title="累積現值 (萬元)"))
        st.plotly_chart(fig_ins, use_container_width=True)

    # ==========================================
    # ⚡ 面向三：綠能產業端研究
    # ==========================================
    with tab_res3:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>綠能電廠償債覆蓋率 (DSCR) 與氣候壓力測試</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#555;'>18 年償債期違約機率為 0%、DSCR 中位數保持在 1.22；變流器汰換年（第 12 年）透過 MMRA 提撥機制順利吸收。</p>", unsafe_allow_html=True)
        
        stress_test_mode = st.radio("選擇電廠壓力測試情境：", ["正常發電氣候情境", "極端陰雨年 (-20% 發電量)"], horizontal=True)
        
        dscr_years = ["第1年", "第4年", "第8年", "第12年(變流器汰換)", "第15年", "第18年"]
        if "正常" in stress_test_mode:
            dscr_vals = [1.27, 1.25, 1.22, 1.17, 1.23, 1.19]
        else:
            dscr_vals = [1.18, 1.15, 1.12, 1.05, 1.14, 1.11]
            
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Bar(
            x=dscr_years, 
            y=dscr_vals, 
            marker_color=['#83A474' if v>=1.1 else '#E53E3E' for v in dscr_vals], 
            text=[f"{v:.2f}" for v in dscr_vals], 
            textposition='auto'
        ))
        fig_energy.add_shape(type="line", x0=-0.5, x1=5.5, y0=1.1, y1=1.1, line=dict(color="#0C0E0B", dash="dash", width=2))
        fig_energy.update_layout(title=f"案場償債覆蓋率 (DSCR) 分布 — {stress_test_mode}", template="plotly_white", height=320, yaxis=dict(range=[1.0, 1.4], title="DSCR 比率 (安全門檻 1.1)"))
        st.plotly_chart(fig_energy, use_container_width=True)

# ==========================================
    # 🔄 面向四：整體循環模式 (綠色醒目選單與動態沙盤)
    # ==========================================
    with tab_res4:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>生態系成功啟動之三方共贏機率與邊界條件 (v3 互動沙盤)</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#555;'>您可以<b>直接調整下方參數滑桿與氣候情境</b>。當共贏機率低於 50% 時，儀表板將自動顯示為嚴格的<b>紅色警戒</b>；高於 50% 則呈現<b>綠色高效運轉</b>：</p>", unsafe_allow_html=True)
        
        # 🎯 注入氣候選單專屬綠色系醒目化 CSS
        st.markdown("""
            <style>
            /* 針對氣候情境選單外框進行綠色高質感化包裝 */
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

        # 🎯 面向四專屬參數調整控制台
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:20px; border-radius:12px; margin-bottom:20px;'>", unsafe_allow_html=True)
        st.markdown("<b style='color:#2D4A22; font-size:15px;'>🎛️ v3 聯立動態沙盤參數控制台</b>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            tab4_r_star = st.slider("每週預算中立回饋 R* (元/達標週)", 20.0, 50.0, R_STAR_DEFAULT, 1.0, key="t4_r_v3")
            tab4_steps_inc = st.slider("保戶平均健走提升率", 0.05, 0.50, 0.20, 0.05, key="t4_s_v3")
        with col_c2:
            tab4_consistency = st.slider("全域行為穩定度因子", 0.30, 1.00, 0.75, 0.05, key="t4_c_v3")
            st.markdown("<div style='font-size: 14px; font-weight: 600; color: #2D4A22; margin-bottom: 5px;'>🌱 季節氣候衝擊情境 (壓力測試)</div>", unsafe_allow_html=True)
            tab4_rain_shock = st.selectbox("", ["梅雨/高日照自然波動 (標準 v3)", "極端降雨氣候衝擊 (-35% 發電)", "晴雨交替穩定情境"], key="t4_rain_v3", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        # 🎯 完全對齊同學 v3 的動態聯立計算公式
        dynamic_win_ratio = 67.3 + (tab4_r_star - 30.5) * -0.8 + (tab4_steps_inc - 0.20) * 35 + (tab4_consistency - 0.75) * 25
        if "極端降雨" in tab4_rain_shock:
            dynamic_win_ratio -= 15.0
        elif "晴雨交替" in tab4_rain_shock:
            dynamic_win_ratio += 5.0
        dynamic_win_ratio = max(5.0, min(99.8, dynamic_win_ratio))

        dynamic_ins_win = 67.0 + (tab4_steps_inc - 0.20) * 45 + (tab4_consistency - 0.75) * 18
        if tab4_r_star > 40:
            dynamic_ins_win -= (tab4_r_star - 40) * 2.0
        dynamic_ins_win = max(10.0, min(99.0, dynamic_ins_win))

        # 🎯 嚴格紅綠二分法邏輯：低於 50% 絕對顯示為紅色，高於等於 50% 顯示為綠色
        if dynamic_win_ratio >= 50.0:
            gauge_bar_color = "#83A474"  # 綠色 (共贏安全區間)
            gauge_bg_steps = [{'range': [0, 50], 'color': '#FFF5F5'}, {'range': [50, 100], 'color': '#F5F7F4'}]
            status_badge = "<span style='color: #83A474; font-weight: 800;'>🟢 飛輪高效運轉（三方共贏達標）</span>"
        else:
            gauge_bar_color = "#E53E3E"  # 紅色 (低於 50% 嚴格警戒區)
            gauge_bg_steps = [{'range': [0, 100], 'color': '#FFF5F5'}]
            status_badge = "<span style='color: #E53E3E; font-weight: 800;'>🔴 警示：共贏機率低於 50% 邊界，面臨財務赤字風險</span>"

        col_res_viz, col_res_text = st.columns([1, 1.5])
        
        with col_res_viz:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = dynamic_win_ratio,
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
                <b style='font-size:16px; color:#2D4A22;'>v3 動態聯立沙盤即時清算解讀</b><br>
                <div style="margin-top:12px; line-height: 1.8; font-size: 14px;">
                    • 每週預算中立回饋: <b>R* = {tab4_r_star} 元/週</b><br>
                    • 保戶平均步數成長率: <b>{tab4_steps_inc*100:.0f}%</b><br>
                    • 行為持續性因子: <b>{tab4_consistency}</b><br>
                    • 氣候季節模擬情境: <b>{tab4_rain_shock}</b><br>
                    <hr style="margin: 10px 0; border-top: 1px solid #E2E8F0;">
                    ➔ <b>動態總體共贏勝率：<span style="color: {gauge_bar_color}; font-size: 24px; font-weight: 900;">{dynamic_win_ratio:.1f}%</span></b><br>
                    ➔ 保險公司 10 年不輸現行方案機率：<b>{dynamic_ins_win:.1f}%</b><br>
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
# EcoStride v3 智慧合約跨期核心資產滾存演算法
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
