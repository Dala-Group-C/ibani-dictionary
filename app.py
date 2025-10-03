import streamlit as st
import pandas as pd
from collections import defaultdict
import re, unicodedata

# --------------------------
# Data loading & cleaning
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ibani-extracted_text main.csv")

    # Drop PoS if exists
    if "pos" in df.columns:
        df = df.drop(columns=["pos"])
    df = df.dropna(subset=["headword", "gloss"])

    # Cleaning function
    def clean_word(text):
        text = unicodedata.normalize("NFKC", str(text))
        text = re.sub(r"[^a-zA-Z0-9À-ÿ\s\-]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower()

    df["headword"] = df["headword"].apply(clean_word)
    df["gloss"] = df["gloss"].apply(clean_word)
    df["gloss"] = df["gloss"].apply(lambda x: x.split()[0] if isinstance(x, str) else x)

    return df

df = load_data()

# Build dictionaries
ibani_to_eng = dict(zip(df["headword"], df["gloss"]))
eng_to_ibani = defaultdict(list)
for _, row in df.iterrows():
    eng_to_ibani[row["gloss"]].append(row["headword"])

# --------------------------
# Streamlit UI
# --------------------------
st.title("🌍 Ibani ↔ English Dictionary Translator")

# User selects direction
direction = st.radio("Choose translation direction:", ["Ibani → English", "English → Ibani"])

# User input
word = st.text_input("Enter a word:")

if st.button("Translate"):
    if direction == "Ibani → English":
        translation = ibani_to_eng.get(word.lower(), "[Not found]")
        st.success(f"**{word} → {translation}**")
    else:  # English → Ibani
        translation = eng_to_ibani.get(word.lower(), ["[Not found]"])
        st.success(f"**{word} → {', '.join(translation)}**")
