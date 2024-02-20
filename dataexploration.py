import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard",
    page_icon="✅",
    layout="wide",
)

# Read data
df = pd.read_csv("megaGymDataset.csv")

# Set page title
st.title('Exercises distribution')

# Replacing null ratings with average
df = df.fillna(value={'Rating': df['Rating'].mean()})

# Dropping useless columns
df.drop(['RatingDesc', 'Unnamed: 0'], axis=1, inplace=True)

# Quantitative variables
count_exercises = df.groupby(['BodyPart']).size().reset_index(name='Count')

# Set up full-screen container
container = st.container()

# Display distribution per Bodypart and Exercises distribution per Level
with container:
    st.subheader('Exercises distribution per Bodypart')
    st.write('---')
    # Border for the section
    with st.container():
        # Set up columns for layout
        col1, col2, col3 = st.columns(3)

        # Chart 1: Number of exercises per body part
        with col1:
            # Bar chart for number of exercises per body part
            fig, ax = plt.subplots()
            ax.bar(count_exercises['BodyPart'], count_exercises['Count'])
            ax.set_xlabel('Body Part')
            ax.set_ylabel('Number of Exercises')
            ax.set_title('Number of Exercises per Body Part')
            ax.set_xticklabels(count_exercises['BodyPart'], rotation=45, ha='right')
            st.pyplot(fig)

        # Chart 2: Pie chart for distribution of exercises according to body part
        with col2:
            # Pie chart for distribution of exercises according to body part
            count_exercises_level = df.groupby(['BodyPart']).size().reset_index(name='Count')
            fig, ax = plt.subplots()
            ax.pie(count_exercises_level['Count'], labels=count_exercises_level['BodyPart'], autopct='%1.1f%%', startangle=90)
            ax.set_title('Distribution of Exercises According to Body Part')
            st.pyplot(fig)

        # Chart 3: Number of exercises per level
        with col3:
            t = pd.crosstab(df['BodyPart'], df['Rating'], margins=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            t.plot(kind='bar', stacked=True, ax=ax)
            ax.set_xlabel('Body Part')
            ax.set_ylabel('Count')
            ax.set_title('Stacked Bar Chart of Ratings by Body Part')
            ax.legend([])
            st.pyplot(fig)


    st.subheader('Exercises distribution per Level')
    st.write('---')

    with st.container():
        # Set up columns for layout
            col1, col2, col3 = st.columns(3)
            with col1 :
                count_exercises_level = df.groupby(['Level']).size().reset_index(name='Count')
                fig, ax = plt.subplots(figsize=(8, 6))  # Ajustez la taille du graphique pour l'aligner avec les autres
                ax.bar(count_exercises_level['Level'], count_exercises_level['Count'])
                ax.set_xlabel('Level')
                ax.set_ylabel('Number of Exercises')
                ax.set_title('Number of Exercises per Level')
                ax.set_xticklabels(count_exercises_level['Level'], rotation=45, ha='right')
                st.pyplot(fig)
            with col2:
                count_exercises_level = df.groupby(['Level']).size().reset_index(name='Count')
                fig, ax = plt.subplots(figsize=(8, 6))  # Ajustez la taille du graphique pour l'aligner avec les autres
                ax.plot(count_exercises_level['Level'], count_exercises_level['Count'], marker='o')
                ax.set_xlabel('Level')
                ax.set_ylabel('Number of Exercises')
                ax.set_title('Line Chart of Exercises per Level')
                ax.set_xticklabels(count_exercises_level['Level'], rotation=45, ha='right')
                st.pyplot(fig)
            with col3: 
                fig, ax = plt.subplots(figsize=(8, 6))  # Ajustez la taille du graphique pour l'aligner avec les autres
                ax.pie(count_exercises_level['Count'], labels=count_exercises_level['Level'], autopct='%1.1f%%', startangle=90)
                ax.set_title('Distribution of Exercises According to Levels')
                st.pyplot(fig)



    # Border for the section
    #with st.container():
     #   st.subheader('Top 5 exercises per Bodypart')

        # Top 5 exercises per Bodypart
      #  for part in count_exercises['BodyPart']:
      #      exercises = df[(df['BodyPart'] == part) & (df['Type'] == 'Strength')].sort_values(by='Rating', ascending=False).head(5)
       #     fig, ax = plt.subplots(figsize=(6, 4))
        #    ax.bar(exercises['Title'], exercises['Rating'])
         #   ax.set_title('Top 5 Strength Exercises for ' + part)
          #  ax.set_xticklabels(exercises['Title'], rotation=45, ha='right')
           # st.pyplot(fig)

    # Border for the section
    st.subheader('Exercises distribution per Rating')
    st.write('---')
    with st.container():
            # Set up columns for layout
            col1, col2 = st.columns(2)
            # Rounding the Rating values
            df['Rating'] = df['Rating'].round()
            quantiles = df['Rating'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            with col1:
                # Histogram of the 'Rating' column
                fig, ax = plt.subplots(figsize=(10, 6))
                df['Rating'].hist(ax=ax)
                ax.set_xlabel('Rating')
                ax.set_ylabel('Frequency')
                ax.set_title('Histogram of Ratings')
                st.pyplot(fig)

            with col2:
                # Kernel density estimate plot
                fig, ax = plt.subplots(figsize=(10, 6))
                df['Rating'].plot(kind="kde", ax=ax)
                ax.set_xlabel('Rating')
                ax.set_ylabel('Density')
                ax.set_title('Kernel Density Estimate (KDE) of Ratings')
                st.pyplot(fig)

        # Stacked bar chart of 'Rating' by 'BodyPart'
        