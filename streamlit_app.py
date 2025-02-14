import streamlit as st
import random

def get_letter_meanings():
    return {
        'A': 'Amazing',
        'B': 'Brilliant',
        'C': 'Creative',
        'D': 'Dynamic',
        'E': 'Energetic',
        'F': 'Friendly',
        'G': 'Generous',
        'H': 'Helpful',
        'I': 'Inspiring',
        'J': 'Joyful',
        'K': 'Kind',
        'L': 'Lovable',
        'M': 'Magnificent',
        'N': 'Nice',
        'O': 'Outstanding',
        'P': 'Positive',
        'Q': 'Quick-witted',
        'R': 'Radiant',
        'S': 'Supportive',
        'T': 'Thoughtful',
        'U': 'Unique',
        'V': 'Vibrant',
        'W': 'Warmhearted',
        'X': 'Xtra Special',
        'Y': 'Youthful',
        'Z': 'Zealous'
    }

def generate_valentine_message(name):
    letter_meanings = get_letter_meanings()
    name = name.upper()
    breakdown = []

    for letter in name:
        if letter in letter_meanings:
            breakdown.append(f"{letter}: {letter_meanings[letter]}")
        else:
            breakdown.append(f"{letter}: (Special Character)")

    # Randomize the Valentine's message (gender-neutral and universal)
    messages = [
        f"Dear {name.capitalize()},\n\nYou are an incredible person, and I'm so grateful to have you in my life. Wishing you a Valentine's Day filled with love and joy! ❤️",
        f"Dear {name.capitalize()},\n\nYour presence makes the world a better place. Sending you lots of love and happiness this Valentine's Day! 💖",
        f"Dear {name.capitalize()},\n\nYou are truly one of a kind, and I appreciate everything about you. Happy Valentine's Day! 🌹",
        f"Dear {name.capitalize()},\n\nYou bring so much positivity and light into the lives of those around you. Have a wonderful Valentine's Day! 💕",
        f"Dear {name.capitalize()},\n\nYou are an amazing friend, and I cherish the bond we share. Wishing you a day full of love and laughter! 💌",
        f"Dear {name.capitalize()},\n\nYou are a wonderful person, and I'm lucky to know you. Happy Valentine's Day! May your day be as special as you are! 🌟",
    ]

    valentine_message = (
        f"Every letter in your name tells me something special about you:\n"
        "\n".join(breakdown) +
        f"\n\n{random.choice(messages)}"
    )

    return valentine_message

def main():
    st.title("Valentine Name Message Generator 💌")
    name = st.text_input("What is your name?")
    if st.button("Generate Message"):
        if name:
            message = generate_valentine_message(name)
            st.success(message)
        else:
            st.error("Please enter your name!")

if __name__ == "__main__":
    main()
