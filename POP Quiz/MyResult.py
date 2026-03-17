import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

ANSWER_FILE = "Answers.txt"

st.title("Quiz Results Analysis")

if not os.path.exists(ANSWER_FILE):
    st.warning("No quiz results yet")
    st.stop()

data = pd.read_csv(
    ANSWER_FILE,
    header=None,
    names=["Name", "Q1", "Q2", "Q3", "Q4", "Score"]
)

st.subheader("Participant Data")
st.write(data)

average_score = np.mean(data["Score"])
median_score = np.median(data["Score"])

st.write("Average Score:", average_score)
st.write("Median Score:", median_score)

st.write("Total Participants:", len(data))

fig, ax = plt.subplots()
ax.bar(data["Name"], data["Score"])
ax.set_xlabel("Participants")
ax.set_ylabel("Score")
ax.set_title("Quiz Scores")

st.pyplot(fig)