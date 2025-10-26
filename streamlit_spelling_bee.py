import streamlit as st
import random
import json
from streamlit.components.v1 import html

st.set_page_config(page_title="Spelling Bee Coach", page_icon="🐝", layout="centered")

# ------------------------------
# Default word banks by grade (editable)
# ------------------------------
DEFAULT_BANK = {
    "1": [
        "cat", "dog", "hat", "map", "sun", "fish", "book", "cake", "tree", "milk",
        "apple", "ball", "desk", "frog", "gate", "hand", "island", "jump", "kite", "leaf"
    ],
    "2": [
        "bright", "carry", "chalk", "circle", "cover", "cousin", "dollar", "eleven", "family", "feather",
        "garden", "happen", "honey", "jacket", "kitten", "lemon", "market", "monkey", "napkin", "pocket"
    ],
    "3": [
        "ability", "ancient", "arrive", "battery", "calendar", "capture", "central", "chimney", "decide", "double",
        "energy", "exact", "factory", "feather", "general", "harbor", "instant", "journey", "kingdom", "library"
    ],
    "4": [
        "across", "anxious", "audience", "avenue", "bargain", "believe", "boundary", "calendar", "candidate", "collapse",
        "culture", "delicate", "evidence", "festival", "flourish", "govern", "harvest", "horizon", "identity", "journey"
    ],
    "5": [
        "accelerate", "acquaintance", "adequate", "adventure", "aerobic", "ancestors", "apparent", "articulate", "assemble", "assignment",
        "astonish", "atmosphere", "available", "barrier", "beneficial", "brilliant", "cautious", "celebration", "challenge", "character",
        "citizen", "collaborate", "colossal", "combine", "commotion", "companion", "competition", "comprehend", "conclude", "confident",
        "conservation", "considerate", "consistent", "construct", "continent", "cooperate", "courageous", "creative", "critique", "curiosity",
        "declaration", "dedicate", "definite", "demonstrate", "describe", "determine", "dilemma", "disastrous", "distinguish", "economy",
        "efficient", "elaborate", "election", "elegant", "essential", "evidence", "excellent", "exhaust", "experiment", "extraordinary"
    ],
    "6": [
        "accommodate", "acknowledge", "allegiance", "ambition", "apparent", "artifact", "bibliography", "chaotic", "chronicle", "coincidence",
        "competent", "compose", "concise", "consequence", "coordinate", "courteous", "criteria", "deceive", "deteriorate", "dimension",
        "dominant", "eloquent", "emphasize", "endeavor", "equation", "exaggerate", "exemplary", "fatigue", "formulate", "futile"
    ],
    "7": [
        "aesthetic", "alleviate", "ambiguous", "anachronism", "anecdote", "anomaly", "antagonist", "apathy", "arbitrary", "benevolent",
        "coherent", "conundrum", "credibility", "cumulative", "deduction", "definitive", "derivative", "diligent", "discern", "eloquence",
        "empirical", "epiphany", "equitable", "exacerbate", "fluctuate", "fortuitous", "hypothesis", "impeccable", "inevitable", "juxtapose"
    ],
    "8": [
        "aberration", "abstinence", "acquiesce", "adulation", "aesthetic", "alacrity", "analogous", "anachronistic", "capitulate", "censure",
        "clairvoyant", "collaborative", "convergence", "deleterious", "demagogue", "digression", "disdain", "exemplify", "extenuating", "fortuitous",
        "hedonist", "impute", "inconsequential", "intrepid", "longevity", "nonchalant", "opulent", "perfidious", "prosperity", "substantiate"
    ],
}

# ------------------------------
# Helpers
# ------------------------------

def init_state():
    st.session_state.setdefault("word_bank", DEFAULT_BANK.copy())
    st.session_state.setdefault("grade", "5")
    st.session_state.setdefault("current_word", "")
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("avoid_repeats", True)


def pick_new_word():
    bank = st.session_state["word_bank"].get(st.session_state["grade"], [])
    if not bank:
        st.warning("No words available for this grade. Upload a list or pick another grade.")
        return
    candidates = [w for w in bank if (not st.session_state["avoid_repeats"]) or (w not in st.session_state["history"])]
    if not candidates:
        st.session_state["history"] = []
        candidates = bank[:]
    st.session_state["current_word"] = random.choice(candidates)
    st.session_state["history"].append(st.session_state["current_word"])


def render_speaker(word: str):
    # Safe JSON-escaped string for JS
    word_js = json.dumps(word)
    html(
        f"""
        <div style='display:flex; gap:1rem; align-items:center; flex-wrap:wrap;'>
          <button id="speakBtn" style="padding:0.6rem 1rem; font-size:1rem; border-radius:12px; border:1px solid #ddd; cursor:pointer;">🔊 Speak</button>
          <label>Rate <input id="rate" type="range" min="0.5" max="1.5" step="0.05" value="1.0"></label>
          <label>Pitch <input id="pitch" type="range" min="0.5" max="1.5" step="0.05" value="1.0"></label>
        </div>
        <script>
          const WORD = {word_js};
          function getUSVoice() {{
            const voices = window.speechSynthesis.getVoices();
            return voices.find(v => v.lang === 'en-US') ||
                   voices.find(v => v.lang && v.lang.startsWith('en-US')) ||
                   voices.find(v => /US|American/i.test(v.name)) || voices[0];
          }}
          function speakNow() {{
            if (!WORD) return;
            const u = new SpeechSynthesisUtterance(WORD);
            u.lang = 'en-US';
            u.rate = parseFloat(document.getElementById('rate').value || '1.0');
            u.pitch = parseFloat(document.getElementById('pitch').value || '1.0');
            const v = getUSVoice();
            if (v) u.voice = v;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(u);
          }}
          // Ensure voices are loaded on some browsers
          window.speechSynthesis.onvoiceschanged = () => {{}};
          document.getElementById('speakBtn').addEventListener('click', speakNow);
        </script>
        """,
        height=80,
    )


# ------------------------------
# UI
# ------------------------------
init_state()

st.markdown(
    """
    <style>
      .big {font-size: 2.2rem; font-weight: 700; letter-spacing: .5px}
      .muted {color:#666}
      .pill {display:inline-block;padding:.2rem .6rem;border:1px solid #eee;border-radius:999px;background:#fafafa}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🐝 Spelling Bee Coach")

with st.sidebar:
    st.header("Settings")
    grade = st.selectbox("Grade level", options=["1","2","3","4","5","6","7","8"], index=4, help="Default is 5th grade.")
    st.session_state["grade"] = grade
    st.session_state["avoid_repeats"] = st.toggle("Avoid repeats until all words used", value=st.session_state["avoid_repeats"])

    st.markdown("### Use your own word list (optional)")
    st.caption("Upload a CSV with columns: grade, word. Example: 5, phenomenon")
    file = st.file_uploader("Upload CSV", type=["csv"]) 
    if file is not None:
        import csv, io
        decoded = file.read().decode("utf-8", errors="ignore")
        rdr = csv.DictReader(io.StringIO(decoded))
        bank = st.session_state["word_bank"].copy()
        added = 0
        for row in rdr:
            g = str(row.get("grade", "")).strip()
            w = str(row.get("word", "")).strip()
            if g and w:
                bank.setdefault(g, [])
                if w not in bank[g]:
                    bank[g].append(w)
                    added += 1
        st.session_state["word_bank"] = bank
        st.success(f"Loaded {added} words from your CSV.")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("🎲 New word", use_container_width=True):
        pick_new_word()
with col2:
    reveal = st.button("👀 Reveal", use_container_width=True)
with col3:
    clear = st.button("🧹 Clear", use_container_width=True)

if clear:
    st.session_state["current_word"] = ""
    st.session_state["history"] = []

# Current word display (hidden until reveal)
word = st.session_state.get("current_word", "")

if not word:
    st.info("Click **New word** to begin.")
else:
    render_speaker(word)

    st.markdown("---")
    st.markdown("**Your word:**")
    if reveal:
        st.markdown(f"<div class='big'>{word}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='muted pill'>hidden</span>", unsafe_allow_html=True)

    with st.expander("History"):
        if st.session_state["history"]:
            st.write(", ".join(st.session_state["history"]))
        else:
            st.caption("No words yet.")

st.markdown(
    """
    ---
    **Tips**
    - Use the **Rate** and **Pitch** sliders to fine‑tune the American accent voice.
    - Upload your own CSV to extend the word list by grade.
    - Turn off *Avoid repeats* if you want fully random selection each time.
    """
)
