import streamlit as st
import pandas as pd
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

QUESTION_FILE = os.path.join(BASE_DIR, "Questions.txt")
ANSWER_FILE = os.path.join(BASE_DIR, "Answers.txt")


def load_questions():

    questions = []

    if not os.path.exists(QUESTION_FILE):
        st.error("Questions.txt not found")
        st.write("Files available:", os.listdir(BASE_DIR))
        return questions

    with open(QUESTION_FILE, "r") as file:

        for line in file:

            if line.strip() == "":
                continue

            parts = line.strip().split("|")

            q_type = parts[0]

            if q_type == "A":

                question = {
                    "type": "A",
                    "question": parts[1],
                    "options": parts[2:6],
                    "answer": int(parts[6])
                }

            elif q_type == "B":

                question = {
                    "type": "B",
                    "question": parts[1],
                    "image": os.path.join(BASE_DIR, parts[2]),
                    "options": parts[3:7],
                    "answer": int(parts[7])
                }

            questions.append(question)

    return questions


def run_quiz():

    st.title("Malaysian Culinary Food Quiz")

    name = st.text_input("Enter your name")

    questions = load_questions()

    if len(questions) == 0:
        st.stop()

    if name == "":
        st.stop()

    answers = []
    score = 0

    for i, q in enumerate(questions):

        st.subheader(f"Question {i+1}")
        st.write(q["question"])

        if q["type"] == "B":

            if os.path.exists(q["image"]):

                image = Image.open(q["image"])
                st.image(image, width=300)

            else:
                st.warning(f"Image {q['image']} not found")

        user_answer = st.radio(
            "Choose your answer:",
            q["options"],
            key=i
        )

        answers.append(q["options"].index(user_answer) + 1)

        if (q["options"].index(user_answer) + 1) == q["answer"]:
            score += 1

    if st.button("Submit Quiz"):

        st.success(f"Your Score: {score}/{len(questions)}")

        row = [name] + answers + [score]

        df = pd.DataFrame([row])

        df.to_csv(ANSWER_FILE, mode="a", header=False, index=False)


run_quiz()

