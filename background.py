import streamlit as st
import json
import os
from datetime import datetime, timedelta
import streamlit.components.v1 as components

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
                "avatar": "🚀",
                "last_login": str(datetime.now().date())
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


user = st.session_state.current_user
user_data = st.session_state.users[user]


# ================= STREAK =================

today = datetime.now().date()

if "last_login" in user_data:
    last = datetime.strptime(user_data["last_login"], "%Y-%m-%d").date()

    if today == last:
        pass
    elif today == last + timedelta(days=1):
        user_data["streak"] += 1
        user_data["xp"] += 5 * user_data["streak"]
    else:
        user_data["streak"] = 1

user_data["last_login"] = str(today)
save_data()


# ================= PROFILE =================

if st.sidebar.button("👤 Profile"):
    st.session_state.show_profile = not st.session_state.show_profile

if st.session_state.show_profile:

    st.title("👤 Profile")

    avatars = ["🚀","🪐","🌌","👩‍🚀","👨‍🚀"]

    user_data["avatar"] = st.selectbox(
        "Avatar",
        avatars,
        index=avatars.index(user_data.get("avatar","🚀"))
    )

    xp = user_data["xp"]
    level = xp // 100 + 1

    st.markdown(f"<h1 style='text-align:center'>{user_data['avatar']}</h1>", unsafe_allow_html=True)
    st.write("User:", user)

    col1, col2, col3 = st.columns(3)
    col1.metric("XP", xp)
    col2.metric("Level", level)
    col3.metric("Streak", user_data["streak"])

    st.stop()


# ================= MODE =================

mode = st.sidebar.radio("Mode", ["🌟 Basic", "🔬 Advanced"])


# =====================================================
# 🌟 BASIC MODE (FULL)
# =====================================================

if mode == "🌟 Basic":

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌍 Create Planet",
        "🧠 Quiz",
        "🏆 Progress",
        "🥇 Leaderboard"
    ])

    # ---------------- TAB 1 ----------------
    with tab1:
        st.header("🌍 Create Planet")

        star_type = st.selectbox("Star Type", ["G-Type", "M-Type"])
        distance = st.slider("Distance (AU)", 0.1, 3.0, 1.0)
        albedo = st.slider("Albedo", 0.0, 1.0, 0.3)

        L = 1.0 if star_type == "G-Type" else 0.04
        flux = L / (distance ** 2)
        temp = ((flux * (1 - albedo)) / 4) ** 0.25 * 278

        score = int(max(0, min(100, 100 - abs(temp - 288))))

        st.metric("Flux", round(flux, 2))
        st.metric("Temp", round(temp, 1))
        st.metric("Score", score)
        st.progress(score)


    # ---------------- TAB 2 ----------------
    with tab2:
        st.header("🧠 Quiz Zone")

        quiz_data = {

        "Quiz 1": [
            ("Closest planet to Sun?", ["Mercury","Venus","Earth","Mars"], "Mercury"),
            ("Hottest planet?", ["Earth","Venus","Mercury","Mars"], "Venus"),
            ("Red planet?", ["Mars","Jupiter","Earth","Venus"], "Mars"),
            ("Largest planet?", ["Earth","Saturn","Jupiter","Mars"], "Jupiter"),
            ("Planet with rings?", ["Mars","Earth","Saturn","Venus"], "Saturn")
        ],

        "Quiz 2": [
            ("What powers stars?", ["Fusion","Fission","Electricity","Gravity"], "Fusion"),
            ("Our galaxy?", ["Milky Way","Andromeda","Orion","Pegasus"], "Milky Way"),
            ("Moon is?", ["Planet","Star","Satellite","Comet"], "Satellite"),
            ("Orbit means?", ["Path","Speed","Mass","Energy"], "Path"),
            ("Comets mostly?", ["Ice","Rock","Metal","Gas"], "Ice")
        ],

        "Quiz 3": [
            ("Exoplanet?", ["Outside system","Inside system","Moon","Star"], "Outside system"),
            ("Albedo?", ["Reflectivity","Heat","Mass","Speed"], "Reflectivity"),
            ("Habitable zone?", ["Liquid water","Gas","Ice","Metal"], "Liquid water"),
            ("Temp unit?", ["Kelvin","Meter","Second","Joule"], "Kelvin"),
            ("Flux?", ["Energy received","Mass","Speed","Distance"], "Energy received")
        ],

        "Quiz 4": [
            ("Sun type?", ["G-type","M-type","K-type","O-type"], "G-type"),
            ("Closest star?", ["Proxima Centauri","Sirius","Vega","Betelgeuse"], "Proxima Centauri"),
            ("Speed of light?", ["3e8 m/s","1e6","1e3","1e2"], "3e8 m/s"),
            ("Orbit shape?", ["Ellipse","Square","Triangle","Line"], "Ellipse"),
            ("Mars color?", ["Red","Blue","Green","White"], "Red")
        ],

        "Quiz 5": [
            ("TRAPPIST-1 planets?", ["7","5","9","3"], "7"),
            ("Red dwarfs?", ["Small stars","Planets","Gas","Moons"], "Small stars"),
            ("Life needs?", ["Water","Metal","Dust","Gas"], "Water"),
            ("Earth temp?", ["288K","100K","500K","50K"], "288K"),
            ("Sun age?", ["4.6B","1B","10B","100M"], "4.6B")
        ],

        "Quiz 6": [
            ("Jupiter type?", ["Gas giant","Rocky","Ice","Metal"], "Gas giant"),
            ("Saturn has?", ["Rings","Moons only","None","No gravity"], "Rings"),
            ("Neptune winds?", ["Fast","Slow","None","Calm"], "Fast"),
            ("Mercury moons?", ["0","1","2","3"], "0"),
            ("Venus rotation?", ["Slow","Fast","Normal","None"], "Slow")
        ],

        "Quiz 7": [
            ("Black hole?", ["Gravity trap","Light","Energy","Gas"], "Gravity trap"),
            ("Supernova?", ["Explosion","Cooling","Orbit","Fusion"], "Explosion"),
            ("Nebula?", ["Gas cloud","Planet","Star","Rock"], "Gas cloud"),
            ("Galaxy shape?", ["Spiral","Square","Flat","Triangle"], "Spiral"),
            ("Dark matter?", ["Invisible","Visible","Solid","Liquid"], "Invisible")
        ],

        "Quiz 8": [
            ("ISS?", ["Space station","Planet","Star","Rocket"], "Space station"),
            ("Hubble?", ["Telescope","Planet","Rocket","Satellite"], "Telescope"),
            ("JWST sees?", ["Infrared","Radio","X-ray","UV"], "Infrared"),
            ("Rocket fuel?", ["Chemical","Water","Air","Electric"], "Chemical"),
            ("Escape velocity?", ["Min speed","Mass","Force","Energy"], "Min speed")
        ],

        "Quiz 9": [
            ("Orbit shape?", ["Ellipse","Circle","Square","Line"], "Ellipse"),
            ("Gravity?", ["Force","Light","Energy","Wave"], "Force"),
            ("Mass unit?", ["kg","m","s","J"], "kg"),
            ("Distance unit?", ["AU","kg","s","W"], "AU"),
            ("Time unit?", ["Second","Meter","AU","kg"], "Second")
        ],

        "Quiz 10": [
            ("Life needs?", ["Water","Iron","Dust","Gas"], "Water"),
            ("Gold formed?", ["Supernova","Earth","Moon","Sun"], "Supernova"),
            ("Hot stars?", ["Blue","Red","Yellow","White"], "Blue"),
            ("Cool stars?", ["Red","Blue","White","Yellow"], "Red"),
            ("Universe expanding?", ["Yes","No","Maybe","Unknown"], "Yes")
        ]

        }

        choice = st.selectbox("Choose Quiz", list(quiz_data.keys()))
        qset = quiz_data[choice]

        answers = []
        for i, (q, opt, ans) in enumerate(qset):
            answers.append(st.radio(q, opt, key=f"{choice}_{i}"))

        if st.button("Submit Quiz"):
            score = sum([1 for i,(_,_,ans) in enumerate(qset) if answers[i] == ans])
            st.success(f"Score {score}/5")

            user_data["xp"] += score * 10
            user_data["completed"] += 1
            save_data()


    # ---------------- TAB 3 ----------------
    with tab3:
        st.header("🏆 Progress")
        st.write("XP:", user_data["xp"])
        st.write("Level:", user_data["xp"] // 100 + 1)


    # ---------------- TAB 4 ----------------
    with tab4:
        st.header("🥇 Leaderboard")

        users = st.session_state.users
        sorted_users = sorted(users.items(), key=lambda x: x[1]["xp"], reverse=True)

        for i,(u,d) in enumerate(sorted_users):
            st.write(f"{i+1}. {u} - {d['xp']} XP")
    # =====================================================
# 🔬 ADVANCED MODE
# =====================================================

if mode == "🔬 Advanced":

    tab1, tab2, tab3 = st.tabs([
        "🪐 Planet Cards",
        "🌌 Exoplanet Simulator",
        "🔥 Habitability Calculator"
    ])

    # ================= TAB 1: PLANET CARDS =================
    with tab1:
        st.header("🪐 Exoplanet Cards")

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
            {"name": "LHS 1140 b", "temp": 230, "type": "Dense rocky"},
            {"name": "Gliese 667 Cc", "temp": 277, "type": "Potentially habitable"},
            {"name": "HD 209458 b", "temp": 1450, "type": "Hot Jupiter"},
            {"name": "WASP-12b", "temp": 2500, "type": "Ultra hot Jupiter"},
            {"name": "55 Cancri e", "temp": 2400, "type": "Lava world"},
        ]

        index = st.session_state.get("planet_index", 0)

        col1, col2, col3 = st.columns([1,2,1])

        if col1.button("⬅️ Prev"):
            index -= 1
        if col3.button("Next ➡️"):
            index += 1

        index = index % len(planets)
        st.session_state.planet_index = index

        p = planets[index]

        st.markdown(f"""
        <div style="border:1px solid gray;padding:20px;border-radius:15px;text-align:center;">
            <h2>{p['name']}</h2>
            <p>🌡 Temperature: {p['temp']} K</p>
            <p>🪐 Type: {p['type']}</p>
        </div>
        """, unsafe_allow_html=True)


    # ================= TAB 2: SIMULATOR =================
    with tab2:
        st.header("🌌 Exoplanet System Simulator")

        import streamlit.components.v1 as components

        solar_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        body {
            margin:0;
            background:black;
            overflow:hidden;
        }

        .space {
            width:100%;
            height:900px;
            position:relative;
            background:black;
        }

        .sun {
            position:absolute;
            top:50%;
            left:50%;
            width:70px;
            height:70px;
            margin-left:-35px;
            margin-top:-35px;
            background:radial-gradient(circle,yellow,orange);
            border-radius:50%;
            box-shadow:0 0 120px yellow;
        }

        .orbit {
            position:absolute;
            top:50%;
            left:50%;
            border:1px solid rgba(255,255,255,0.2);
            border-radius:50%;
            transform:translate(-50%,-50%);
            animation:spin linear infinite;
        }

        @keyframes spin {
            from {transform:translate(-50%,-50%) rotate(0deg);}
            to {transform:translate(-50%,-50%) rotate(360deg);}
        }

        .earth-orbit { width:250px; height:250px; animation-duration:20s; }
        .mars-orbit { width:320px; height:320px; animation-duration:30s; }
        .jupiter-orbit { width:450px; height:450px; animation-duration:50s; }

        .planet {
            position:absolute;
            top:50%;
            left:100%;
            width:12px;
            height:12px;
            border-radius:50%;
        }

        .earth { background:blue; }
        .mars { background:red; }
        .jupiter { background:orange; width:20px; height:20px; }

        </style>
        </head>

        <body>
        <div class="space">
            <div class="sun"></div>

            <div class="orbit earth-orbit">
                <div class="planet earth"></div>
            </div>

            <div class="orbit mars-orbit">
                <div class="planet mars"></div>
            </div>

            <div class="orbit jupiter-orbit">
                <div class="planet jupiter"></div>
            </div>
        </div>
        </body>
        </html>
        """

        components.html(solar_html, height=600)


    # ================= TAB 3: CALCULATOR =================
    with tab3:
        st.header("🔥 Habitability Calculator")

        star = st.selectbox("Star Type", ["G-Type", "M-Type"])
        distance = st.slider("Distance (AU)", 0.1, 5.0, 1.0)
        albedo = st.slider("Albedo", 0.0, 1.0, 0.3)

        L = 1 if star == "G-Type" else 0.04

        flux = L / (distance ** 2)
        temp = ((flux * (1 - albedo)) / 4) ** 0.25 * 278

        st.write("🌟 Flux:", round(flux, 2))
        st.write("🌡 Temperature:", round(temp, 1))

        if temp > 320:
            st.error("🔥 Too Hot")
        elif 273 <= temp <= 310:
            st.success("🌍 Habitable Zone")
        else:
            st.warning("❄️ Too Cold")
