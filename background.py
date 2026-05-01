import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ================= DATA =================
def load_data():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_data():
    with open("users.json", "w") as f:
        json.dump(st.session_state.users, f)


# ================= INIT =================
if "users" not in st.session_state:
    st.session_state.users = load_data()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "show_profile" not in st.session_state:
    st.session_state.show_profile = False


# ================= LOGIN =================
def login_page():
    st.title("🌌 ExoHabit Login")

    option = st.radio("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            st.session_state.users[username] = {
                "password": password,
                "xp": 0,
                "completed": 0,
                "streak": 1,
                "avatar": "🚀"
            }
            save_data()
            st.success("Account created!")

    if option == "Login":
        if st.button("Login"):
            if username in st.session_state.users and \
               st.session_state.users[username]["password"] == password:

                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("Invalid login")


# ================= HARD GATE =================
if not st.session_state.logged_in:
    login_page()
    st.stop()


# ================= USER =================
user = st.session_state.current_user
user_data = st.session_state.users[user]


# ================= SIDEBAR BUTTON =================
if st.sidebar.button("👤 Profile"):
    st.session_state.show_profile = not st.session_state.show_profile


# ================= STREAK SYSTEM =================
today = datetime.now().date()

if "last_login" not in user_data:
    user_data["last_login"] = str(today)
    user_data["streak"] = 1
else:
    last_login = datetime.strptime(user_data["last_login"], "%Y-%m-%d").date()

    if today == last_login:
        pass
    elif today == last_login + timedelta(days=1):
        user_data["streak"] += 1
        bonus = 5 * user_data["streak"]
        user_data["xp"] += bonus
        st.sidebar.success(f"+{bonus} XP 🔥")
    else:
        user_data["streak"] = 1

    user_data["last_login"] = str(today)

save_data()


# ================= PROFILE PAGE =================
if st.session_state.show_profile:

    st.title("👤 My Profile")

    avatars = ["🚀","🪐","🌌","👩‍🚀","👨‍🚀"]

    user_data["avatar"] = st.selectbox(
        "Choose Avatar",
        avatars,
        index=avatars.index(user_data.get("avatar","🚀"))
    )

    xp = user_data.get("xp", 0)
    level = xp // 100 + 1
    completed = user_data.get("completed", 0)
    streak = user_data.get("streak", 1)

    # Center display
    st.markdown(f"""
    <div style="text-align:center;">
        <h1 style="font-size:70px;">{user_data['avatar']}</h1>
        <h2>{user}</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("⭐ XP", xp)
    col2.metric("🎯 Level", level)
    col3.metric("🔥 Streak", streak)

    st.progress((xp % 100) / 100)

    st.write("### 🧠 Quizzes Completed:", completed)

    save_data()

    st.stop()   # 🚨 VERY IMPORTANT

mode = st.sidebar.radio("Mode", ["🌟 Basic", "🔬 Advanced"])

# =====================================================
# 🌟 BASIC MODE
# =====================================================
if mode == "🌟 Basic":

    tab1, tab2, tab3, tab4 = st.tabs(["🌍 Create Planet", "🧠 Quiz", "🏆 Progress", "🥇 Leaderboard"])

    # ================= TAB 1 =================
    with tab1:
        st.header("🌍 Create Your Planet")

        star_type = st.selectbox("Star Type", ["G-Type", "M-Type"])
        distance = st.slider("Distance (AU)", 0.1, 3.0, 1.0)
        albedo = st.slider("Albedo", 0.0, 1.0, 0.3)

        L = 1.0 if star_type == "G-Type" else 0.04
        flux = L / (distance ** 2)
        temp = ((flux * (1 - albedo)) / 4) ** 0.25 * 278

        score = int(max(0, min(100, 100 - abs(temp - 288))))

        st.metric("🌟 Flux", round(flux, 2))
        st.metric("🌡 Temp", round(temp, 1))
        st.metric("🪐 Score", score)

        st.progress(score)

    # ================= TAB 2 (QUIZ) =================
    with tab2:
        st.header("🧠 Quiz Zone")

        user = st.session_state.current_user

        if "xp" not in st.session_state.users[user]:
            st.session_state.users[user]["xp"] = 0
            st.session_state.users[user]["completed"] = 0

        if "quiz_done" not in st.session_state:
            st.session_state.quiz_done = {}

        quiz_data = {

            "Quiz 1": [
                ("Closest planet to Sun?", ["Mercury", "Venus", "Earth", "Mars"], "Mercury"),
                ("Hottest planet?", ["Earth", "Venus", "Mercury", "Mars"], "Venus"),
                ("Red planet?", ["Mars", "Jupiter", "Earth", "Venus"], "Mars"),
                ("Largest planet?", ["Earth", "Saturn", "Jupiter", "Mars"], "Jupiter"),
                ("Planet with rings?", ["Mars", "Earth", "Saturn", "Venus"], "Saturn")
            ],

            "Quiz 2": [
                ("What powers stars?", ["Fusion", "Fission", "Electricity", "Gravity"], "Fusion"),
                ("Our galaxy?", ["Milky Way", "Andromeda", "Orion", "Pegasus"], "Milky Way"),
                ("Moon is?", ["Planet", "Star", "Satellite", "Comet"], "Satellite"),
                ("Orbit means?", ["Path", "Speed", "Mass", "Energy"], "Path"),
                ("Comets mostly?", ["Ice", "Rock", "Metal", "Gas"], "Ice")
            ],

            "Quiz 3": [
                ("Exoplanet?", ["Outside system", "Inside system", "Moon", "Star"], "Outside system"),
                ("Albedo?", ["Reflectivity", "Heat", "Mass", "Speed"], "Reflectivity"),
                ("Habitable zone?", ["Liquid water", "Gas", "Ice", "Metal"], "Liquid water"),
                ("Temp unit?", ["Kelvin", "Meter", "Second", "Joule"], "Kelvin"),
                ("Flux?", ["Energy received", "Mass", "Speed", "Distance"], "Energy received")
            ],

            "Quiz 4": [
                ("Sun type?", ["G-type", "M-type", "K-type", "O-type"], "G-type"),
                ("Closest star?", ["Proxima Centauri", "Sirius", "Vega", "Betelgeuse"], "Proxima Centauri"),
                ("Speed of light?", ["3e8 m/s", "1e6", "1e3", "1e2"], "3e8 m/s"),
                ("Orbit shape?", ["Ellipse", "Square", "Triangle", "Line"], "Ellipse"),
                ("Mars color?", ["Red", "Blue", "Green", "White"], "Red")
            ],

            "Quiz 5": [
                ("TRAPPIST-1 planets?", ["7", "5", "9", "3"], "7"),
                ("Red dwarfs?", ["Small stars", "Planets", "Gas", "Moons"], "Small stars"),
                ("Life needs?", ["Water", "Metal", "Dust", "Gas"], "Water"),
                ("Earth temp?", ["288K", "100K", "500K", "50K"], "288K"),
                ("Sun age?", ["4.6B", "1B", "10B", "100M"], "4.6B")
            ],

            "Quiz 6": [
                ("Jupiter type?", ["Gas giant", "Rocky", "Ice", "Metal"], "Gas giant"),
                ("Saturn has?", ["Rings", "Moons only", "None", "No gravity"], "Rings"),
                ("Neptune winds?", ["Fast", "Slow", "None", "Calm"], "Fast"),
                ("Mercury moons?", ["0", "1", "2", "3"], "0"),
                ("Venus rotation?", ["Slow", "Fast", "Normal", "None"], "Slow")
            ],

            "Quiz 7": [
                ("Black hole?", ["Gravity trap", "Light", "Energy", "Gas"], "Gravity trap"),
                ("Supernova?", ["Explosion", "Cooling", "Orbit", "Fusion"], "Explosion"),
                ("Nebula?", ["Gas cloud", "Planet", "Star", "Rock"], "Gas cloud"),
                ("Galaxy shape?", ["Spiral", "Square", "Flat", "Triangle"], "Spiral"),
                ("Dark matter?", ["Invisible", "Visible", "Solid", "Liquid"], "Invisible")
            ],

            "Quiz 8": [
                ("ISS?", ["Space station", "Planet", "Star", "Rocket"], "Space station"),
                ("Hubble?", ["Telescope", "Planet", "Rocket", "Satellite"], "Telescope"),
                ("JWST sees?", ["Infrared", "Radio", "X-ray", "UV"], "Infrared"),
                ("Rocket fuel?", ["Chemical", "Water", "Air", "Electric"], "Chemical"),
                ("Escape velocity?", ["Min speed", "Mass", "Force", "Energy"], "Min speed")
            ],

            "Quiz 9": [
                ("Orbit shape?", ["Ellipse", "Circle", "Square", "Line"], "Ellipse"),
                ("Gravity?", ["Force", "Light", "Energy", "Wave"], "Force"),
                ("Mass unit?", ["kg", "m", "s", "J"], "kg"),
                ("Distance unit?", ["AU", "kg", "s", "W"], "AU"),
                ("Time unit?", ["Second", "Meter", "AU", "kg"], "Second")
            ],

            "Quiz 10": [
                ("Life needs?", ["Water", "Iron", "Dust", "Gas"], "Water"),
                ("Gold formed?", ["Supernova", "Earth", "Moon", "Sun"], "Supernova"),
                ("Hot stars?", ["Blue", "Red", "Yellow", "White"], "Blue"),
                ("Cool stars?", ["Red", "Blue", "White", "Yellow"], "Red"),
                ("Universe expanding?", ["Yes", "No", "Maybe", "Unknown"], "Yes")
            ]
        }

        choice = st.selectbox("Choose Quiz", list(quiz_data.keys()))
        qset = quiz_data[choice]

        answers = []
        for i, (q, opt, ans) in enumerate(qset):
            answers.append(st.radio(q, opt, key=f"{choice}_{i}_{user}"))

        quiz_key = f"{user}_{choice}"

        if st.button("Submit Quiz"):

            if st.session_state.quiz_done.get(quiz_key, False):
                st.warning("Already attempted!")
            else:
                score = sum([1 for i, (_, _, ans) in enumerate(qset) if answers[i] == ans])

                st.success(f"Score: {score}/5")

                xp_gain = score * 10
                st.session_state.users[user]["xp"] += xp_gain

                if score >= 3:
                    st.session_state.users[user]["completed"] += 1
                    st.balloons()

                st.info(f"✨ +{xp_gain} XP")

                st.session_state.quiz_done[quiz_key] = True
                save_data()

    # ================= TAB 3 =================
    with tab3:
        st.header("🏆 Progress")

        data = st.session_state.users[user]

        xp = data.get("xp", 0)
        completed = data.get("completed", 0)

        level = xp // 100 + 1

        st.metric("Level", level)
        st.metric("XP", xp)
        st.metric("Completed", completed)

        st.progress((xp % 100) / 100)

    # ================= TAB 4 =================
    with tab4:
        st.header("🥇 Leaderboard")

        users = st.session_state.users

        sorted_users = sorted(users.items(), key=lambda x: x[1].get("xp", 0), reverse=True)

        for i, (username, data) in enumerate(sorted_users):
            xp = data.get("xp", 0)

            if i == 0:
                st.success(f"🥇 {username} — {xp} XP")
            elif i == 1:
                st.info(f"🥈 {username} — {xp} XP")
            elif i == 2:
                st.warning(f"🥉 {username} — {xp} XP")
            else:
                st.write(f"{i+1}. {username} — {xp} XP")
# =====================================================
# 🔬 ADVANCED MODE
# =====================================================
if mode == "🔬 Advanced":

    tab1, tab2, tab3 = st.tabs([
        "🪐 Planet Cards",
        "🌌 Exoplanet System Simulator",
        "🔥 Calculator"
    ])

    # ================= TAB 1: PLANET CARDS =================
    with tab1:
        planets = [
            {"name": "Kepler-22b", "temp": 262, "type": "Ocean world"},
            {"name": "Proxima Centauri b", "temp": 234, "type": "Rocky"},
            {"name": "TRAPPIST-1e", "temp": 251, "type": "Habitable"},
            {"name": "Kepler-452b", "temp": 265, "type": "Earth-like"},
            {"name": "K2-18b", "temp": 265, "type": "Hycean"},
            {"name": "TRAPPIST-1d", "temp": 282, "type": "Warm rocky"},
            {"name": "TRAPPIST-1f", "temp": 219, "type": "Cold rocky"},
            {"name": "TRAPPIST-1g", "temp": 198, "type": "Icy world"},
            {"name": "TRAPPIST-1h", "temp": 173, "type": "Frozen"},
            {"name": "Kepler-186f", "temp": 188, "type": "Habitable candidate"},
            {"name": "Kepler-62f", "temp": 208, "type": "Super-Earth"},
            {"name": "Kepler-62e", "temp": 270, "type": "Ocean world"},
            {"name": "LHS 1140 b", "temp": 230, "type": "Dense rocky"},
            {"name": "Gliese 667 Cc", "temp": 277, "type": "Potentially habitable"},
            {"name": "HD 209458 b", "temp": 1450, "type": "Hot Jupiter"},
            {"name": "WASP-12b", "temp": 2500, "type": "Ultra hot Jupiter"},
            {"name": "WASP-121b", "temp": 2350, "type": "Evaporating giant"},
            {"name": "55 Cancri e", "temp": 2400, "type": "Lava world"},
            {"name": "CoRoT-7b", "temp": 1800, "type": "Molten rocky"},
            {"name": "GJ 1214 b", "temp": 550, "type": "Mini-Neptune"},
            {"name": "HD 189733 b", "temp": 1200, "type": "Stormy gas giant"}
        ]

        index = st.session_state.get("index", 0)

        col1, col2, col3 = st.columns([1, 2, 1])

        if col1.button("⬅️"):
            index -= 1
        if col3.button("➡️"):
            index += 1

        index = index % len(planets)
        st.session_state.index = index

        p = planets[index]

        st.markdown(f"""
        <div style="border:1px solid #ccc;padding:20px;border-radius:12px;">
            <h2>{p['name']}</h2>
            <p>🌡 Temperature: {p['temp']} K</p>
            <p>🪐 Type: {p['type']}</p>
        </div>
        """, unsafe_allow_html=True)
with tab2:
    st.header("🌌 Exoplanet System Simulator")

    system = st.selectbox(
        "Choose System",
        ["TRAPPIST-1", "Kepler-90", "Proxima Centauri"],
        key="sim_system"   # ✅ prevents duplicate error
    )

    html = """
    <html>
    <body style='background:black;margin:0;overflow:hidden;'>
    <style>

    .container{
        position:relative;
        width:600px;
        height:600px;
        margin:auto;
    }

    .star{
        position:absolute;
        top:50%;
        left:50%;
        width:20px;
        height:20px;
        background: radial-gradient(circle, yellow, orange, red);
        border-radius:50%;
        transform:translate(-50%,-50%);
        box-shadow:0 0 40px yellow;
    }

    .orbit-path{
        position:absolute;
        top:50%;
        left:50%;
        border:1px solid rgba(255,255,255,0.2);
        border-radius:50%;
        transform:translate(-50%,-50%);
    }

    .orbit{
        position:absolute;
        top:50%;
        left:50%;
        transform-origin:center;
        animation-name:spin;
        animation-timing-function:linear;
        animation-iteration-count:infinite;
    }

    .planet{
        position:absolute;
        top:0;
        left:0;
        transform:translateX(var(--r));
        display:flex;
        align-items:center;
    }

    .dot{
        width:10px;
        height:10px;
        border-radius:50%;
        box-shadow:0 0 10px white;
    }

    .label{
        display:none;
        color:white;
        font-size:11px;
        margin-left:6px;
        background:rgba(0,0,0,0.7);
        padding:2px 5px;
        border-radius:5px;
    }

    .planet:hover .label{
        display:block;
    }

    @keyframes spin{
        from{transform:rotate(0deg);}
        to{transform:rotate(360deg);}
    }

    </style>

    <div class='container'>
        <div class='star'></div>
    """

    # ================= SYSTEM DATA =================
    if system == "TRAPPIST-1":
        radii = [40, 60, 80, 100, 120, 140, 160]
        colors = ["gray", "orange", "yellow", "lightblue", "blue", "cyan", "white"]
        names = ["b", "c", "d", "e", "f", "g", "h"]

    elif system == "Kepler-90":
        radii = [35, 55, 75, 95, 120, 150, 180, 210]
        colors = ["gray", "orange", "yellow", "lightblue", "blue", "cyan", "white", "purple"]
        names = ["b", "c", "i", "d", "e", "f", "g", "h"]

    else:
        radii = [90, 150]
        colors = ["lightblue", "green"]
        names = ["b", "d"]

    # ================= RENDER =================
    for r, c, n in zip(radii, colors, names):

        speed = max(5, int(50 / (r ** 0.5)))   # ✅ ensures movement

        html += f"""
        <div class='orbit-path' style='width:{r*2}px;height:{r*2}px;'></div>

        <div class='orbit' style='animation-duration:{speed}s;'>
            <div class='planet' style='--r:{r}px;'>
                <div class='dot' style='background:{c};'></div>
                <div class='label'>{system}-{n}</div>
            </div>
        </div>
        """

    html += """
    </div>
    </body>
    </html>
    """

    st.components.v1.html(html, height=650)
    # ================= TAB 3: CALCULATOR =================
    with tab3:
        st.header("🔥 Habitability Calculator")

        star = st.selectbox("Star Type", ["G-Type", "M-Type"], key="calc_star")
        st.slider("Distance (AU)", 0.1, 5.0, 1.0, key="calc_distance")
        st.slider("Albedo", 0.0, 1.0, 0.3, key="calc_albedo")
        L = 1 if star == "G-Type" else 0.04
        flux = L / (d ** 2)
        temp = ((flux * (1 - a)) / 4) ** 0.25 * 278

        st.write("Stellar Flux:", round(flux, 2))
        st.write("Equilibrium Temp:", round(temp, 1))

        if temp > 320:
            st.error("🔥 Moist Greenhouse")
        elif 273 <= temp <= 310:
            st.success("🌍 Habitable")
        else:
            st.warning("❄️ Not ideal")
