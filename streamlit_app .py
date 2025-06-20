import streamlit as st
import re

st.set_page_config(page_title="Password Analyzer & Wordlist Generator", layout="centered")
st.title("🔐 Password Strength Analyzer & Wordlist Generator")

tab1, tab2 = st.tabs(["Password Strength Checker", "Custom Wordlist Generator"])

# Password Checker Logic (no external modules)
def check_password_strength(password):
    strength = 0
    remarks = []

    if len(password) >= 8:
        strength += 1
    else:
        remarks.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        remarks.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        strength += 1
    else:
        remarks.append("Add lowercase letters.")

    if re.search(r"[0-9]", password):
        strength += 1
    else:
        remarks.append("Add numbers.")

    if re.search(r"[!@#$%^&*()_+\-={};':\"\\|,.<>/?]", password):
        strength += 1
    else:
        remarks.append("Add special characters.")

    return strength, remarks

with tab1:
    st.header("Check Your Password Strength")
    password = st.text_input("Enter a password", type="password")

    if password:
        score, suggestions = check_password_strength(password)
        st.write(f"Strength Score: {score}/5")

        if score == 5:
            st.success("✅ Strong password!")
        else:
            st.warning("🔒 Weak password. Suggestions:")
            for tip in suggestions:
                st.write(f"- {tip}")

# Wordlist Generator
with tab2:
    st.header("Generate a Custom Wordlist")
    name = st.text_input("Name")
    dob = st.text_input("Date of Birth (YYYYMMDD)")
    pet = st.text_input("Pet Name")
    keyword = st.text_input("Favorite Word or Nickname")

    def generate_wordlist(inputs):
        variants = set()
        for word in inputs:
            if word:
                variants.update({
                    word,
                    word.lower(),
                    word.upper(),
                    word.capitalize(),
                    word[::-1],
                    word + "123",
                    word + "!", word + "@123",
                    word.replace("a", "@").replace("s", "$").replace("o", "0"),
                })
        return variants

    if st.button("Generate Wordlist"):
        base_inputs = [name, dob, pet, keyword]
        wordlist = sorted(generate_wordlist(base_inputs))
        st.success(f"Generated {len(wordlist)} unique words.")

        if wordlist:
            wordlist_text = "\n".join(wordlist)
            st.download_button("Download Wordlist", data=wordlist_text, file_name="custom_wordlist.txt", mime="text/plain")
