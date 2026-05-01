import streamlit as st
import random
import math
import json
import os
def load_data():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_data():
    with open("users.json", "w") as f:
        json.dump(st.session_state.users, f)

st.set_page_config(page_title="ExoHabit", layout="wide")

# ================= INIT =================
if "users" not in st.session_state:
    st.session_state.users = load_data()

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "index" not in st.session_state:
    st.session_state.index = 0

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
        "completed": 0
    }

    save_data()   # ✅ RIGHT HERE
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


# ================= SAFE USER =================
user = st.session_state.current_user
if user not in st.session_state.users:
    st.session_state.logged_in = False
    st.rerun()

user_data = st.session_state.users[user]

mode = st.sidebar.radio("Mode", ["🌟 Basic", "🔬 Advanced"])

# =====================================================
# 🌟 BASIC MODE
# =====================================================
if mode == "🌟 Basic":

    tab1, tab2, tab3, tab4 = st.tabs(["🌍 Create Planet", "🧠 Quiz", "🏆 Progress", "🥇 Leaderboard"])

    # -------- CREATE PLANET --------
    with tab1:
        st.header("🌍 Create Your Planet (Fixed System)")

        star_type = st.selectbox(
            "Star Type",
            ["G-Type (Sun-like)", "M-Type (Red Dwarf)"]
        )

        distance = st.slider("Orbital Distance (AU)", 0.1, 3.0, 1.0)
        albedo = st.slider("Albedo (Reflectivity)", 0.0, 1.0, 0.3)

        L = 1.0 if star_type == "G-Type (Sun-like)" else 0.04

        flux = L / (distance ** 2)
        temp = ((flux * (1 - albedo)) / 4) ** 0.25 * 278

        distance_sim = max(0, 1 - abs(distance - 1.0) / 1.5)
        albedo_sim = max(0, 1 - abs(albedo - 0.30) / 0.5)
        temp_sim = max(0, 1 - abs(temp - 288) / 100)

        score = (
            distance_sim * 40 +
            albedo_sim * 30 +
            temp_sim * 30
        )

        score = int(max(0, min(score, 100)))

        is_earth = (abs(distance - 1.0) < 0.05 and abs(albedo - 0.30) < 0.02)

        if is_earth:
            score = 100

        st.metric("🌟 Stellar Flux", round(flux, 2))
        st.metric("🌡 Temperature (K)", round(temp, 1))
        st.metric("🪐 Habitability Score", f"{score}/100")

        st.progress(score)

        if score == 100:
            st.success("🌍 EARTH UNLOCKED!")
            st.balloons()

        elif score >= 80:
            st.info("🪐 Near Habitable Planet Unlocked!")

        elif temp > 320:
            st.error("🔥 Too Hot")

        elif temp < 200:
            st.warning("❄️ Too Cold")

        else:
            st.warning("⚠️ Not Ideal")

    # -------- QUIZ --------
    with tab2:
        st.header("🧠 Quiz Zone")

        user = st.session_state.current_user

        if "xp" not in st.session_state.users[user]:
            st.session_state.users[user]["xp"] = 0
            st.session_state.users[user]["completed"] = 0

        quiz_data = {

            "Quiz 1": [
                ("Which planet is closest to the Sun?", ["Mercury", "Venus", "Earth", "Mars"], "Mercury"),
                ("Which is the hottest planet?", ["Earth", "Venus", "Mercury", "Mars"], "Venus"),
                ("What is the Red Planet?", ["Mars", "Jupiter", "Earth", "Venus"], "Mars"),
                ("Largest planet?", ["Earth", "Saturn", "Jupiter", "Mars"], "Jupiter"),
                ("Which planet has rings?", ["Mars", "Earth", "Saturn", "Venus"], "Saturn")
            ],

            "Quiz 2": [
                ("What powers stars?", ["Fusion", "Fission", "Electricity", "Gravity"], "Fusion"),
                ("Our galaxy name?", ["Milky Way", "Andromeda", "Orion", "Pegasus"], "Milky Way"),
                ("Moon is a?", ["Planet", "Star", "Satellite", "Comet"], "Satellite"),
                ("Orbit means?", ["Path", "Speed", "Mass", "Energy"], "Path"),
                ("Comets are mostly?", ["Ice", "Rock", "Metal", "Gas"], "Ice")
            ],

            "Quiz 3": [
                ("Exoplanet means?", ["Outside solar system", "Inside system", "Moon", "Star"], "Outside solar system"),
                ("Albedo measures?", ["Reflectivity", "Heat", "Mass", "Speed"], "Reflectivity"),
                ("Habitable zone allows?", ["Liquid water", "Gas", "Ice", "Metal"], "Liquid water"),
                ("Temperature unit?", ["Kelvin", "Meter", "Second", "Joule"], "Kelvin"),
                ("Flux means?", ["Energy received", "Mass", "Speed", "Distance"], "Energy received")
            ],

            "Quiz 4": [
                ("Sun type?", ["G-type", "M-type", "K-type", "O-type"], "G-type"),
                ("Closest star?", ["Proxima Centauri", "Sirius", "Vega", "Betelgeuse"], "Proxima Centauri"),
                ("Speed of light?", ["3e8 m/s", "1e6", "1e3", "1e2"], "3e8 m/s"),
                ("Orbit shape?", ["Ellipse", "Square", "Triangle", "Line"], "Ellipse"),
                ("Mars color?", ["Red", "Blue", "Green", "White"], "Red")
            ],

            "Quiz 5": [
                ("TRAPPIST-1 has how many planets?", ["7", "5", "9", "3"], "7"),
                ("Red dwarfs are?", ["Small stars", "Planets", "Gas clouds", "Moons"], "Small stars"),
                ("Life needs?", ["Water", "Metal", "Dust", "Gas"], "Water"),
                ("Earth avg temp?", ["288K", "100K", "500K", "50K"], "288K"),
                ("Sun age?", ["4.6 billion years", "1 billion", "10 billion", "100 million"], "4.6 billion years")
            ],

            "Quiz 6": [
                ("Jupiter type?", ["Gas giant", "Rocky", "Ice", "Metal"], "Gas giant"),
                ("Saturn has?", ["Rings", "Moons only", "No rings", "No gravity"], "Rings"),
                ("Neptune winds?", ["Fast", "Slow", "None", "Calm"], "Fast"),
                ("Mercury moons?", ["0", "1", "2", "3"], "0"),
                ("Venus rotation?", ["Slow", "Fast", "Normal", "None"], "Slow")
            ],

            "Quiz 7": [
                ("Black hole is?", ["Gravity trap", "Light", "Energy", "Gas"], "Gravity trap"),
                ("Supernova?", ["Explosion", "Cooling", "Orbit", "Fusion"], "Explosion"),
                ("Nebula?", ["Gas cloud", "Planet", "Star", "Rock"], "Gas cloud"),
                ("Galaxy shape?", ["Spiral", "Square", "Flat", "Triangle"], "Spiral"),
                ("Dark matter?", ["Invisible", "Visible", "Solid", "Liquid"], "Invisible")
            ],

            "Quiz 8": [
                ("ISS is?", ["Space station", "Planet", "Star", "Rocket"], "Space station"),
                ("Hubble is?", ["Telescope", "Planet", "Rocket", "Satellite"], "Telescope"),
                ("JWST observes?", ["Infrared", "Radio", "X-ray", "UV"], "Infrared"),
                ("Rocket fuel?", ["Chemical", "Water", "Air", "Electric"], "Chemical"),
                ("Escape velocity?", ["Minimum speed", "Mass", "Force", "Energy"], "Minimum speed")
            ],

            "Quiz 9": [
                ("Orbit shape?", ["Ellipse", "Circle only", "Square", "Line"], "Ellipse"),
                ("Gravity is?", ["Force", "Light", "Energy", "Wave"], "Force"),
                ("Mass unit?", ["kg", "m", "s", "J"], "kg"),
                ("Distance unit?", ["AU", "kg", "s", "W"], "AU"),
                ("Time unit?", ["Second", "Meter", "AU", "kg"], "Second")
            ],

            "Quiz 10": [
                ("Life requires?", ["Water", "Iron", "Dust", "Gas"], "Water"),
                ("Gold formed in?", ["Supernova", "Earth", "Moon", "Sun"], "Supernova"),
                ("Hot stars color?", ["Blue", "Red", "Yellow", "White"], "Blue"),
                ("Cool stars?", ["Red", "Blue", "White", "Yellow"], "Red"),
                ("Universe expanding?", ["Yes", "No", "Maybe", "Unknown"], "Yes")
            ]
        }

        choice = st.selectbox("Choose Quiz", list(quiz_data.keys()))
        qset = quiz_data[choice]

        answers = []
        for i, (q, opt, ans) in enumerate(qset):
            answers.append(st.radio(q, opt, key=f"{choice}_{i}"))

        if st.button("Submit Quiz"):
            score = 0
            for i, (q, opt, ans) in enumerate(qset):
                if answers[i] == ans:
                    score += 1

            st.success(f"Score: {score}/5")

            xp_gain = score * 10
            st.session_state.users[user]["xp"] += xp_gain

            if score >= 3:
                st.session_state.users[user]["completed"] += 1
                st.balloons()

            st.info(f"✨ You earned {xp_gain} XP!")
            if st.button("Submit Quiz"):
    score = 0
    for i, (q, opt, ans) in enumerate(qset):
        if answers[i] == ans:
            score += 1

    st.success(f"Score: {score}/5")

    xp_gain = score * 10
    st.session_state.users[user]["xp"] += xp_gain

    if score >= 3:
        st.session_state.users[user]["completed"] += 1
        st.balloons()

    st.info(f"✨ You earned {xp_gain} XP!")

    save_data()   # ✅ THIS IS THE MOST IMPORTANT LINE

    # -------- PROGRESS --------
    with tab3:
        st.header("🏆 Progress, Level & Badges")

        data = st.session_state.users[user]

        xp = data.get("xp", 0)
        completed = data.get("completed", 0)

        level = xp // 100 + 1

        st.metric("Level", level)
        st.metric("XP", xp)
        st.metric("Quizzes Completed", completed)

        st.progress((xp % 100) / 100)

        if completed >= 10:
            st.success("🥇 Exoplanet Master")
        elif completed >= 7:
            st.info("🥈 Astronomer")
        elif completed >= 5:
            st.warning("🥉 Explorer")
        else:
            st.write("Keep going!")

        if level >= 10:
            st.write("🌌 Galactic Legend")
        elif level >= 7:
            st.write("🚀 Space Commander")
        elif level >= 4:
            st.write("🛰️ Explorer")
        else:
            st.write("🌍 Beginner")
with tab4:
    st.header("🥇 Leaderboard")

    leaderboard = st.session_state.users

    sorted_lb = sorted(
        leaderboard.items(),
        key=lambda x: x[1].get("xp", 0),
        reverse=True
    )

    if not sorted_lb:
        st.info("No players yet")
    else:
        st.subheader("🌌 Top Explorers")

        for i, (user, data) in enumerate(sorted_lb[:10]):
            xp = data.get("xp", 0)

            if i == 0:
                st.success(f"🥇 {user} — {xp} XP")
            elif i == 1:
                st.info(f"🥈 {user} — {xp} XP")
            elif i == 2:
                st.warning(f"🥉 {user} — {xp} XP")
            else:
                st.write(f"{i+1}. {user} — {xp} XP")

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

    # ================= TAB 2: SYSTEM SIMULATOR =================
    with tab2:
        st.header("🌌 Exoplanet System Simulator")

        system = st.selectbox(
            "Choose System",
            ["TRAPPIST-1", "Kepler-90", "Proxima Centauri"]
        )

        html = "<html><body style='background:black;margin:0;'><style>"
        html += """
        .container{position:relative;width:600px;height:600px;margin:auto;}
        .star{position:absolute;top:50%;left:50%;width:18px;height:18px;background:red;
        border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 30px red;}

        .orbit-path{position:absolute;top:50%;left:50%;
        border:1px solid rgba(255,255,255,0.2);
        border-radius:50%;transform:translate(-50%,-50%);}

        .orbit{position:absolute;top:50%;left:50%;
        transform-origin:center;animation:spin linear infinite;}

        .planet{position:absolute;top:0;left:0;
        transform:translateX(var(--r));display:flex;}

        .dot{width:10px;height:10px;border-radius:50%;}
        .label{color:white;font-size:10px;margin-left:5px;}

        @keyframes spin{
            from{transform:rotate(0deg);}
            to{transform:rotate(360deg);}
        }
        """
        html += "</style><div class='container'><div class='star'></div>"

        # ================= SYSTEM DATA =================
        if system == "TRAPPIST-1":
            radii = [50, 70, 90, 110, 130, 150, 170]
            speeds = [6, 8, 10, 12, 14, 16, 18]
            colors = ["gray", "orange", "yellow", "lightblue", "blue", "cyan", "white"]
            names = ["b", "c", "d", "e", "f", "g", "h"]

        elif system == "Kepler-90":
            radii = [40, 55, 70, 90, 110, 130, 150, 180]
            speeds = [5, 7, 9, 11, 13, 15, 17, 20]
            colors = ["gray", "orange", "yellow", "lightblue", "blue", "cyan", "white", "purple"]
            names = ["b", "c", "i", "d", "e", "f", "g", "h"]

        elif system == "Proxima Centauri":
            radii = [80, 130]
            speeds = [10, 16]
            colors = ["lightblue", "green"]
            names = ["b", "d"]

        # ================= RENDER =================
        for r, s, c, n in zip(radii, speeds, colors, names):
            html += f"""
            <div class='orbit-path' style='width:{r*2}px;height:{r*2}px;'></div>
            <div class='orbit' style='animation-duration:{s}s;'>
                <div class='planet' style='--r:{r}px;'>
                    <div class='dot' style='background:{c};'></div>
                    <div class='label'>{system}-{n}</div>
                </div>
            </div>
            """

        html += "</div></body></html>"

        st.components.v1.html(html, height=650)

    # ================= TAB 3: CALCULATOR =================
    with tab3:
        st.header("🔥 Habitability Calculator")

        star = st.selectbox("Star Type", ["G-Type", "M-Type"])
        d = st.slider("Distance (AU)", 0.1, 5.0, 1.0)
        a = st.slider("Albedo", 0.0, 1.0, 0.3)

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
