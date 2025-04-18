import streamlit as st
import re
from typing import Tuple, List  # Import Tuple and List from typing

# Custom CSS for dark mode styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background: #121212;  /* Dark background */
        color: #E0E0E0;       /* Light text color */
    }

    .stApp {
        max ```python
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background: #1E1E1E;  /* Darker card background */
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        transition: box-shadow 0.3s ease-in-out;
    }

    .stApp:hover {
        box-shadow: 0 12px 36px rgba(0,0,0,0.7);
    }

    h1 {
        color: #FFFFFF;       /* White text for headings */
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .stTextInput>div>div>input {
        background: #2A2A2A;  /* Dark input background */
        color: #E0E0E0;       /* Light text color */
        border: 2px solid #3b82f6;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        transition: border-color 0.3s ease-in-out;
    }

    .stTextInput>div>div>input:focus {
        border-color: #2563eb;
        outline: none;
        box-shadow: 0 0 8px #2563eb;
    }

    .strength {
        font-weight: 700;
        font-size: 1.3rem;
        margin-top: 1rem;
        text-align: center;
    }

    .strength.Weak {
        color: #ef4444;  /* Red for weak */
    }

    .strength.Moderate {
        color: #f59e0b;  /* Yellow for moderate */
    }

    .strength.Strong {
        color: #10b981;  /* Green for strong */
    }

    .feedback {
        margin-top: 1rem;
        background: #2A2A2A;  /* Dark feedback background */
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.5rem;
        border-radius: 6px;
        font-size: 1rem;
        color: #E0E0E0;       /* Light text color */
        line-height: 1.5;
    }

    .feedback ul {
        padding-left: 1.2rem;
    }

    .feedback li {
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def password_strength(password: str) -> Tuple[str, List[str]]:
    """
    Evaluate the strength of the given password and provide feedback.

    Returns:
        strength (str): One of 'Weak', 'Moderate', 'Strong'
        feedback (list): List of suggestions to improve the password
    """
    feedback = []
    length = len(password)

    # Check length
    if length < 8:
        feedback.append("Password should be at least 8 characters long.")
    elif length > 20:
        feedback.append("Password is quite long, consider if you can remember it easily.")

    # Check character types
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^A-Za-z0-9]', password))

    types_count = sum([has_lower, has_upper, has_digit, has_special])

    if not has_lower:
        feedback.append("Add lowercase letters.")
    if not has_upper:
        feedback.append("Add uppercase letters.")
    if not has_digit:
        feedback.append("Add digits.")
    if not has_special:
        feedback.append("Add special characters.")

    # Check for repeated characters or sequences (basic check)
    if re.search(r'(.)\1\1', password):
        feedback.append("Avoid using the same character three or more times in a row.")

    # Determine strength
    if length >= 8 and types_count >= 3 and not re.search(r'(.)\1\1', password):
        if length >= 12 and types_count == 4:
            strength = "Strong"
        else:
            strength = "Moderate"
    else:
        strength = "Weak"

    return strength, feedback

def main():
    st.title("Password Strength Meter")
    st.write("Enter a password to check its strength and get feedback.")

    password = st.text_input("Password", type="password")

    if password:
        strength, feedback = password_strength(password)
        st.markdown(f'<div class="strength {strength}">Strength: {strength}</div>', unsafe_allow_html=True)

        if feedback:
            feedback_html = "<div class='feedback'><ul>"
            for item in feedback:
                feedback_html += f"<li>{item}</li>"
            feedback_html += "</ul></div>"
            st.markdown(feedback_html, unsafe_allow_html=True)
        else:
            st.markdown("<div class='feedback'>Your password looks good!</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
