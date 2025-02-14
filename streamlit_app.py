import streamlit as st
import random
import time

def get_letter_meanings():
    return {
        'A': 'Amazing', 'B': 'Brilliant', 'C': 'Creative', 'D': 'Dynamic', 'E': 'Energetic',
        'F': 'Friendly', 'G': 'Generous', 'H': 'Helpful', 'I': 'Inspiring', 'J': 'Joyful',
        'K': 'Kind', 'L': 'Lovable', 'M': 'Magnificent', 'N': 'Nice', 'O': 'Outstanding',
        'P': 'Positive', 'Q': 'Quick-witted', 'R': 'Radiant', 'S': 'Supportive', 'T': 'Thoughtful',
        'U': 'Unique', 'V': 'Vibrant', 'W': 'Warmhearted', 'X': 'Xtra Special', 'Y': 'Youthful',
        'Z': 'Zealous'
    }

def generate_valentine_message(name):
    letter_meanings = get_letter_meanings()
    name = name.upper()
    breakdown = [f"{letter}: {letter_meanings.get(letter, '(Special Character)')}" for letter in name]

    messages = [
        f"Dear {name.capitalize()},\n\nYou are {random.choice(['amazing', 'wonderful', 'fantastic'])} and I'm so {random.choice(['happy', 'lucky', 'grateful'])} to know you. Wishing you a {random.choice(['joyful', 'lovely', 'sweet'])} Valentine's Day! ❤️",
        f"Dear {name.capitalize()},\n\nYour {random.choice(['smile', 'laughter', 'presence'])} brightens my day. You're truly {random.choice(['special', 'kind', 'unique'])}. Happy Valentine's Day! 💖",
        f"Dear {name.capitalize()},\n\nI admire your {random.choice(['creativity', 'intelligence', 'warmth'])}. You are {random.choice(['inspiring', 'charming', 'radiant'])}. Happy Valentine's Day! 🌹",
    ]

    return (
        f"Every letter in your name tells me something special about you:\n"
        "\n".join(breakdown) + f"\n\n{random.choice(messages)}"
    )

def get_valentine_riddle():
    riddles = [
        {"question": "What has an eye, but cannot see?", "answer": "A needle"},
        {"question": "What is full of holes but still holds water?", "answer": "A sponge"},
        {"question": "What has one head, one foot, and four legs?", "answer": "A bed"},
        {"question": "What has to be broken before you can use it?", "answer": "An egg"},
        {"question": "What is always coming, but never arrives?", "answer": "Tomorrow"},
        {"question": "What has no voice but can still tell you stories?", "answer": "A book"},
        {"question": "What can travel the world while staying in a corner?", "answer": "A stamp"},
        {"question": "What gets wetter the more it dries?", "answer": "A towel"},
        {"question": "What is lighter than a feather, yet even the strongest person can't hold it for more than a few minutes?", "answer": "Breath"},
        {"question": "What has cities, mountains, and water, but no houses, trees, or fish?", "answer": "A map"},
        {"question": "I am taken from a mine and shut up in a wooden case, from which I am never released, and used by almost everybody. What am I?", "answer": "Pencil lead"},
        {"question": "What is always in front of you but can’t be seen?", "answer": "The future"},
        {"question": "What has a neck without a head, a body without legs, and can hold the whole world?", "answer": "A bottle"},
        {"question": "What has no beginning, end, or middle?", "answer": "A circle"},
        {"question": "I am tall when I am young, and I am short when I am old. What am I?", "answer": "A candle"},
        {"question": "What can you keep after giving to someone else?", "answer": "Your word"},
    ]
    return random.choice(riddles)

def main():
    st.title("Valentine Name Message Generator 💌")

    # Initialize session state variables
    if "riddle" not in st.session_state:
        st.session_state.riddle = None
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = ""
    if "time_remaining" not in st.session_state:
        st.session_state.time_remaining = 5
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "giveaway_entry" not in st.session_state:
        st.session_state.giveaway_entry = False
    if "message_generated" not in st.session_state:
        st.session_state.message_generated = False

    # Message Generation Form
    with st.form("message_form"):
        name = st.text_input("What is your name? (Optional for secret admirer)")
        secret_admirer = st.checkbox("Send as a secret admirer")
        giveaway_entry = st.checkbox("Enter the Valentine's Day Giveaway!")
        generate_button = st.form_submit_button("Generate Message")

    if generate_button:
        if name or secret_admirer or giveaway_entry:
            display_name = name if name else "My Valentine"
            message = generate_valentine_message(display_name)
            st.session_state.message_generated = True
            st.session_state.giveaway_entry = giveaway_entry

            if st.session_state.giveaway_entry:
                st.session_state.riddle = get_valentine_riddle()
                st.session_state.start_time = time.time()
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.session_state.time_remaining = 5

            st.markdown(message)
        else:
            st.error("Please enter your name, check 'Secret Admirer', or enter the Giveaway!")

    # Riddle Challenge (only if giveaway is entered and message is generated)
    if st.session_state.giveaway_entry and st.session_state.message_generated:
        st.write("**Riddle Challenge:**")
        st.write(st.session_state.riddle["question"])

        # Timer logic
        if not st.session_state.answered:
            elapsed_time = time.time() - st.session_state.start_time
            st.session_state.time_remaining = max(5 - int(elapsed_time), 0)

            if st.session_state.time_remaining > 0:
                st.write(f"Time remaining: {st.session_state.time_remaining} seconds")
            else:
                st.error("Time's up!")
                st.session_state.answered = True

        # Riddle Form
        with st.form("riddle_form"):
            user_answer = st.text_input("Your answer:", key="answer_input")
            submit_riddle = st.form_submit_button("Submit Answer")

        if submit_riddle:
            st.session_state.user_answer = user_answer
            st.session_state.answered = True

            if st.session_state.user_answer.lower() == st.session_state.riddle["answer"].lower():
                st.success("🎉 Correct! You've entered the giveaway!")
            else:
                st.error(f"❌ Incorrect. The correct answer was: {st.session_state.riddle['answer']}")

if __name__ == "__main__":
    main()
