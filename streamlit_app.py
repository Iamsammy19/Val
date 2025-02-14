import streamlit as st
import random
import time

def get_letter_meanings():
    return {  # Indentation added
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

    for letter in name:  # Indentation added
        if letter in letter_meanings: # Indentation added
            breakdown.append(f"{letter}: {letter_meanings[letter]}") # Indentation added
        else: # Indentation added
            breakdown.append(f"{letter}: (Special Character)") # Indentation added

    messages = [  # Indentation added
        f"Dear {name.capitalize()},\n\nYou are {random.choice(['amazing', 'wonderful', 'fantastic'])} and I'm so {random.choice(['happy', 'lucky', 'grateful'])} to know you. Wishing you a {random.choice(['joyful', 'lovely', 'sweet'])} Valentine's Day! ❤️",
        f"Dear {name.capitalize()},\n\nYour {random.choice(['smile', 'laughter', 'presence'])} brightens my day.  You're truly {random.choice(['special', 'kind', 'unique'])}. Happy Valentine's Day! 💖",
        f"Dear {name.capitalize()},\n\nI admire your {random.choice(['creativity', 'intelligence', 'warmth'])}. You are {random.choice(['inspiring', 'charming', 'radiant'])}. Happy Valentine's Day! 🌹",
        # ... more Mad Libs-style messages
    ]

    valentine_message = ( # Indentation added
        f"Every letter in your name tells me something special about you:\n"
        "\n".join(breakdown) +
        f"\n\n{random.choice(messages)}"
    )

    return valentine_message  # Indentation added

def get_valentine_riddle():
    riddles = [  # Indentation added
        {"question": "What has an eye, but cannot see?", "answer": "A needle"},
        {"question": "What is full of holes but still holds water?", "answer": "A sponge"},
        # ... (rest of your riddles)
    ]
    return random.choice(riddles)  # Indentation added

def main():
    st.title("Valentine Name Message Generator 💌")

    name = st.text_input("What is your name? (Optional for secret admirer)")
    secret_admirer = st.checkbox("Send as a secret admirer")
    giveaway_entry = st.checkbox("Enter the Valentine's Day Giveaway!")

    if st.button("Generate Message"):  # Indentation added
        if name or secret_admirer or giveaway_entry:  # Indentation added
            display_name = name if name else "My Valentine"  # Indentation added
            message = generate_valentine_message(display_name)  # Indentation added
            st.success(message)  # Indentation added

            if giveaway_entry:  # Indentation added
                riddle = get_valentine_riddle()  # Indentation added
                st.write(riddle["question"])  # Indentation added

                answer_placeholder = st.empty()  # Indentation added
                time_placeholder = st.empty()  # Indentation added

                start_time = time.time()  # Indentation added
                time_limit = 5  # Indentation added
                user_answer = ""  # Indentation added

                while time.time() - start_time <= time_limit:  # Indentation added
                    remaining_time = time_limit - (time.time() - start_time)  # Indentation added
                    time_placeholder.write(f"Time remaining: {int(remaining_time)} seconds")  # Indentation added
                    user_answer = answer_placeholder.text_input("Your answer:")  # Indentation added
                    if user_answer:  # Indentation added
                        break  # Indentation added
                    time.sleep(0.5)  # Indentation added

                if time.time() - start_time > time_limit:  # Indentation added
                    st.error("Time's up!")  # Indentation added
                elif user_answer.lower() == riddle["answer"].lower():  # Indentation added
                    st.success("Correct! You've entered the giveaway!")  # Indentation added
                    # (Handle prize distribution)  # Indentation added
                else:  # Indentation added
                    st.error("Incorrect. Try again!")  # Indentation added

                time_placeholder.empty()  # Indentation added
                answer_placeholder.empty()  # Indentation added

        else:  # Indentation added
            st.error("Please enter your name, check 'Secret Admirer', or enter the Giveaway!")  # Indentation added

if __name__ == "__main__":  # Indentation added
    main()  # Indentation added
