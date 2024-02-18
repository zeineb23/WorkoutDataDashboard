import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("megaGymDataset.csv")

st.title('Exercise Dashboard')

# Replacing null ratings with average
df = df.fillna(value={'Rating': df['Rating'].mean()})

# Dropping useless columns
df.drop(['RatingDesc', 'Unnamed: 0'], axis=1, inplace=True)

# Quantitative variables
count_exercises = df.groupby(['BodyPart']).size().reset_index(name='Count')

# Bar chart for number of exercises per body part
fig, ax = plt.subplots()
ax.bar(count_exercises['BodyPart'], count_exercises['Count'])
ax.set_xlabel('Body Part')
ax.set_ylabel('Number of Exercises')
ax.set_title('Number of Exercises per Body Part')
ax.set_xticklabels(count_exercises['BodyPart'], rotation=45, ha='right')
st.pyplot(fig)

# Pie chart for distribution of exercises according to body part
fig, ax = plt.subplots()
ax.pie(count_exercises['Count'], labels=count_exercises['BodyPart'], autopct='%1.1f%%', startangle=90)
ax.set_title('Distribution of Exercises According to Body Part')
st.pyplot(fig)

# Top 5 exercises for each body part
for part in count_exercises['BodyPart']:
    exercises = df[(df['BodyPart'] == part) & (df['Type'] == 'Strength')].sort_values(by='Rating', ascending=False).head(5)
    fig, ax = plt.subplots()
    ax.bar(exercises['Title'], exercises['Rating'])
    ax.set_title('Top 5 Strength Exercises for ' + part)
    ax.set_xticklabels(exercises['Title'], rotation=45, ha='right')
    st.pyplot(fig)

# Exercises for each level
count_exercises_level = df.groupby(['Level']).size().reset_index(name='Count')
fig, ax = plt.subplots()
ax.bar(count_exercises_level['Level'], count_exercises_level['Count'])
ax.set_xlabel('Level')
ax.set_ylabel('Number of Exercises')
ax.set_title('Number of Exercises per Level')
ax.set_xticklabels(count_exercises_level['Level'], rotation=45, ha='right')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.pie(count_exercises_level['Count'], labels=count_exercises_level['Level'], autopct='%1.1f%%', startangle=90)
ax.set_title('Distribution of Exercises According to Levels')
st.pyplot(fig)

# Continuous variables
# Exercices per Rating

# Rounding the Rating values
df['Rating'] = df['Rating'].round()
quantiles = df['Rating'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

# Histogram of the 'Rating' column
fig, ax = plt.subplots()
df['Rating'].hist(ax=ax)
ax.set_xlabel('Rating')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Ratings')
st.pyplot(fig)

# Kernel density estimate plot
fig, ax = plt.subplots()
df['Rating'].plot(kind="kde", ax=ax)
ax.set_xlabel('Rating')
ax.set_ylabel('Density')
ax.set_title('Kernel Density Estimate (KDE) of Ratings')
st.pyplot(fig)

# Stacked bar chart of 'Rating' by 'BodyPart'
t = pd.crosstab(df['BodyPart'], df['Rating'], margins=True)
fig, ax = plt.subplots()
t.plot(kind='bar', stacked=True, ax=ax)
ax.set_xlabel('Body Part')
ax.set_ylabel('Count')
ax.set_title('Stacked Bar Chart of Ratings by Body Part')
st.pyplot(fig)
