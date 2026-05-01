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
    import streamlit.components.v1 as components

    st.header("🌌 Exoplanet System Simulator")

    system = st.selectbox(
        "Choose System",
        ["TRAPPIST-1", "Kepler-90", "Proxima Centauri", "Solar System"],
        key="sim_system"
    )

    # ================= ☀️ SOLAR SYSTEM =================
    if system == "Solar System":

        st.subheader("☀️ Real Solar System View")

        import streamlit.components.v1 as components

        st.markdown("""
            <style>
            iframe {
                background-color: black !important;
                border-radius: 15px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.subheader("🌌 Planetarium View")

        solar_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        body{
            margin:0;
            background:black;
            overflow:hidden;
        }

        .space{
            position:relative;
            width:1250px;
            height:950px;
            margin:auto;
            background:black;
            overflow:hidden;
        }

        .star{
            position:absolute;
            background:white;
            border-radius:50%;
            animation:twinkle 4s infinite alternate;
        }

        @keyframes twinkle{
            from{opacity:0.25;}
            to{opacity:1;}
        }

        .sun{
            position:absolute;
            top:50%;
            left:50%;
            width:75px;
            height:75px;
            margin-left:-37px;
            margin-top:-37px;
            background:radial-gradient(circle,yellow,orange,darkorange);
            border-radius:50%;
            box-shadow:0 0 140px yellow;
        }

        .orbit{
            position:absolute;
            border:1px solid rgba(255,255,255,0.22);
            border-radius:50%;
            top:50%;
            left:50%;
            transform:translate(-50%,-50%);
        }

        .planet{
            position:absolute;
            border-radius:50%;
            transition:0.3s;
            box-shadow: inset -4px -4px 6px rgba(0,0,0,0.45);
        }

        .planet:hover{
            transform:scale(1.35);
            box-shadow:0 0 22px white;
        }

        .label{
            position:absolute;
            color:white;
            font-size:12px;
            left:24px;
            top:-2px;
            white-space:nowrap;
        }

        .mercury-orbit{width:130px;height:130px;animation:spin 12s linear infinite;}
        .venus-orbit{width:200px;height:200px;animation:spin 18s linear infinite;}
        .earth-orbit{width:270px;height:270px;animation:spin 24s linear infinite;}
        .mars-orbit{width:340px;height:340px;animation:spin 32s linear infinite;}
        .jupiter-orbit{width:470px;height:470px;animation:spin 48s linear infinite;}
        .saturn-orbit{width:610px;height:610px;animation:spin 64s linear infinite;}
        .uranus-orbit{width:760px;height:760px;animation:spin 82s linear infinite;}
        .neptune-orbit{width:900px;height:900px;animation:spin 100s linear infinite;}

        .mercury{width:10px;height:10px;top:50%;left:-5px;background:radial-gradient(circle,lightgray,gray);}
        .venus{width:14px;height:14px;top:50%;left:-7px;background:radial-gradient(circle,#ffd27f,orange);}
        .earth{width:17px;height:17px;top:50%;left:-8px;background:radial-gradient(circle,#66ccff,blue);}
        .mars{width:13px;height:13px;top:50%;left:-6px;background:radial-gradient(circle,#ff9999,red);}
        .jupiter{width:30px;height:30px;top:50%;left:-15px;background:radial-gradient(circle,#d2b48c,brown);}
        .saturn{width:26px;height:26px;top:50%;left:-13px;background:radial-gradient(circle,#ffe680,gold);}
        .uranus{width:21px;height:21px;top:50%;left:-10px;background:radial-gradient(circle,#ccffff,lightblue);}
        .neptune{width:21px;height:21px;top:50%;left:-10px;background:radial-gradient(circle,#6699ff,darkblue);}

        .ring{
            position:absolute;
            width:38px;
            height:12px;
            border:2px solid rgba(255,255,255,0.45);
            border-radius:50%;
            top:7px;
            left:-6px;
            transform:rotate(20deg);
        }

        .moon-orbit{
            position:absolute;
            width:34px;
            height:34px;
            border:1px dashed rgba(255,255,255,0.15);
            border-radius:50%;
            top:-8px;
            left:-8px;
            animation:spin 5s linear infinite;
        }

        .moon{
            position:absolute;
            width:5px;
            height:5px;
            background:white;
            border-radius:50%;
            top:50%;
            left:-2px;
        }

        .iss-orbit{
            position:absolute;
            width:50px;
            height:50px;
            border:1px dotted rgba(255,255,255,0.10);
            border-radius:50%;
            top:-16px;
            left:-16px;
            animation:spin 4s linear infinite;
        }

        .iss{
            position:absolute;
            width:10px;
            height:4px;
            background:silver;
            top:50%;
            left:-5px;
            box-shadow:0 0 8px white;
        }

        .iss::before{
            content:'';
            position:absolute;
            width:18px;
            height:2px;
            background:royalblue;
            left:-4px;
            top:1px;
        }

        .iss::after{
            content:'';
            position:absolute;
            width:2px;
            height:8px;
            background:white;
            left:4px;
            top:-2px;
        }

        .hubble-orbit{
            position:absolute;
            width:64px;
            height:64px;
            border:1px dotted rgba(255,255,255,0.08);
            border-radius:50%;
            top:-23px;
            left:-23px;
            animation:spin 6s linear infinite;
        }

        .hubble{
            position:absolute;
            width:5px;
            height:10px;
            background:silver;
            top:50%;
            left:-2px;
            box-shadow:0 0 6px white;
        }

        .hubble::before{
            content:'';
            position:absolute;
            width:14px;
            height:2px;
            background:royalblue;
            left:-4px;
            top:4px;
        }

        .comet{
            position:absolute;
            width:12px;
            height:12px;
            background:red;
            border-radius:50%;
            box-shadow:0 0 35px red;
            animation:cometmove 9s linear infinite;
        }

        .comet-tail{
            position:absolute;
            width:90px;
            height:3px;
            background:linear-gradient(to left,red,transparent);
            top:4px;
            left:-85px;
        }

        @keyframes cometmove{
            0%{left:-100px;top:120px;}
            50%{left:600px;top:350px;}
            100%{left:1300px;top:850px;}
        }

        @keyframes spin{
            from{transform:translate(-50%,-50%) rotate(0deg);}
            to{transform:translate(-50%,-50%) rotate(360deg);}
        }
        </style>
        </head>

        <body>
        <div class="space">

        <script>
        for(let i=0;i<350;i++){
            let s=document.createElement('div');
            s.className='star';
            s.style.width=(Math.random()*3)+'px';
            s.style.height=(Math.random()*3)+'px';
            s.style.top=(Math.random()*950)+'px';
            s.style.left=(Math.random()*1250)+'px';
            document.currentScript.parentElement.appendChild(s);
        }

        for(let i=0;i<120;i++){
            let a=document.createElement('div');
            a.style.position='absolute';
            a.style.width='2px';
            a.style.height='2px';
            a.style.background='gray';
            a.style.borderRadius='50%';
            let angle=Math.random()*360;
            let r=410+Math.random()*35;
            let x=625+r*Math.cos(angle*Math.PI/180);
            let y=475+r*Math.sin(angle*Math.PI/180);
            a.style.left=x+'px';
            a.style.top=y+'px';
            document.currentScript.parentElement.appendChild(a);
        }
        </script>

        <div class="sun"></div>

        <div class="orbit mercury-orbit"><div class="planet mercury"><div class="label">Mercury</div></div></div>
        <div class="orbit venus-orbit"><div class="planet venus"><div class="label">Venus</div></div></div>

        <div class="orbit earth-orbit">
            <div class="planet earth">
                <div class="label">Earth</div>
                <div class="moon-orbit"><div class="moon"></div></div>
                <div class="iss-orbit"><div class="iss"></div></div>
                <div class="hubble-orbit"><div class="hubble"></div></div>
            </div>
        </div>

        <div class="orbit mars-orbit"><div class="planet mars"><div class="label">Mars</div></div></div>
        <div class="orbit jupiter-orbit"><div class="planet jupiter"><div class="label">Jupiter</div></div></div>

        <div class="orbit saturn-orbit">
            <div class="planet saturn">
                <div class="ring"></div>
                <div class="label">Saturn</div>
            </div>
        </div>

        <div class="orbit uranus-orbit"><div class="planet uranus"><div class="label">Uranus</div></div></div>
        <div class="orbit neptune-orbit"><div class="planet neptune"><div class="label">Neptune</div></div></div>

        <div class="comet"><div class="comet-tail"></div></div>

        </div>
        </body>
        </html>
        """

        components.html(solar_html, height=950)  
html = """
<html>
<body style='margin:0;background:black;overflow:hidden;'>

<style>
.space{
    position:relative;
    width:650px;
    height:650px;
    margin:auto;
    background:black;
}

/* stars */
.star{
    position:absolute;
    background:white;
    border-radius:50%;
    animation:twinkle 3s infinite alternate;
}
@keyframes twinkle{
    from{opacity:0.2;}
    to{opacity:1;}
}

/* main star */
.main-star{
    position:absolute;
    top:50%;
    left:50%;
    width:22px;
    height:22px;
    margin-left:-11px;
    margin-top:-11px;
    background:radial-gradient(circle,yellow,orange,red);
    border-radius:50%;
    box-shadow:0 0 60px orange, 0 0 120px red;
}

/* orbit path */
.orbit{
    position:absolute;
    border:1px solid rgba(255,255,255,0.2);
    border-radius:50%;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
}

/* independent spin */
.spin{
    position:absolute;
    width:100%;
    height:100%;
    animation:spin linear infinite;
}

@keyframes spin{
    from{transform:rotate(0deg);}
    to{transform:rotate(360deg);}
}

/* planet */
.planet{
    position:absolute;
    border-radius:50%;
    transition:0.3s;
}
.planet:hover{
    transform:scale(1.4);
    box-shadow:0 0 20px white;
}

/* label */
.label{
    position:absolute;
    color:white;
    font-size:11px;
    left:18px;
    top:-4px;
    background:rgba(0,0,0,0.6);
    padding:2px 6px;
    border-radius:6px;
    white-space:nowrap;
}
</style>

<div class="space">
"""

# ⭐ STAR FIELD
import random
for _ in range(140):
    x = random.randint(0,650)
    y = random.randint(0,650)
    size = random.randint(1,2)
    html += f"<div class='star' style='width:{size}px;height:{size}px;top:{y}px;left:{x}px;'></div>"

html += "<div class='main-star'></div>"
for i, (r, c, n) in enumerate(zip(radii, colors, names)):

    # 🌍 size scaling
    size = 6 + (i * 2)

    # 🐢 slow realistic speed
    speed = 30 + (i * 12)

    html += f"""
    <div class="orbit" style="width:{r*2}px;height:{r*2}px;">

        <div class="spin" style="animation-duration:{speed}s;">

            <div class="planet"
                 style="
                 width:{size}px;
                 height:{size}px;
                 top:50%;
                 left:-{size/2}px;

                 background:radial-gradient(circle at 30% 30%, white, {c});
                 box-shadow:0 0 12px {c};
                 ">

                <div class="label">{system}-{n}</div>

            </div>

        </div>
    </div>
    """
html += """
</div>
</body>
</html>
""" 
components.html(html, height=650)
with tab3:
  st.header("🔥 Habitability Calculator")
  star = st.selectbox("Star Type", ["G-Type", "M-Type"], key="calc_star")
  d = st.slider("Distance (AU)", 0.1, 5.0, 1.0, key="calc_distance")
  a = st.slider("Albedo", 0.0, 1.0, 0.3, key="calc_albedo")

    # luminosity 
  L = 1 if star == "G-Type" else 0.04

    # calculations
  flux = L / (d ** 2)
  temp = ((flux * (1 - a)) / 4) ** 0.25 * 278

  st.write("Stellar Flux:", round(flux, 2))
  st.write("Equilibrium Temp:", round(temp, 1))

  if temp > 320:
        st.error("🔥 Too Hot")
  elif 273 <= temp <= 310:
        st.success("🌍 Habitable")
  else:
        st.warning("❄️ Not Ideal")
