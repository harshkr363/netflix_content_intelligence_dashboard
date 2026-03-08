import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


# PAGE CONFIG


st.set_page_config(page_title="Netflix Content Intelligence Dashboard", layout="wide")

st.title("Netflix Content Intelligence Dashboard")
st.write("Interactive dashboard analyzing Netflix Movies and TV Shows dataset.")


# LOAD DATA


df = pd.read_csv("netflix_titles.csv")

# Data Cleaning
df.fillna("Unknown", inplace=True)

# Convert date column
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year


# KPI METRICS


total_titles = len(df)
total_movies = len(df[df["type"] == "Movie"])
total_shows = len(df[df["type"] == "TV Show"])
unique_countries = df["country"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", total_movies)
col3.metric("TV Shows", total_shows)
col4.metric("Countries", unique_countries)

st.divider()


# SIDEBAR FILTERS


st.sidebar.header("Filters")

content_type = st.sidebar.multiselect(
    "Select Content Type",
    df["type"].unique(),
    default=df["type"].unique()
)

country = st.sidebar.multiselect(
    "Select Country",
    df["country"].unique()
)

year_range = st.sidebar.slider(
    "Select Release Year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2000, 2020)
)

# Apply filters
filtered_df = df[df["type"].isin(content_type)]

if country:
    filtered_df = filtered_df[filtered_df["country"].isin(country)]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= year_range[0]) &
    (filtered_df["release_year"] <= year_range[1])
]


# SEARCH


search = st.text_input("Search Movie or TV Show")

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False)
    ]


# DATASET PREVIEW


st.header("Dataset Explorer")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_netflix_data.csv",
    mime="text/csv"
)

st.divider()


# MOVIES VS TV SHOWS


col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")

    fig, ax = plt.subplots()
    filtered_df["type"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Content Rating Distribution")

    fig, ax = plt.subplots()
    filtered_df["rating"].value_counts().head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)


# TOP COUNTRIES


st.subheader("Top Countries Producing Netflix Content")

fig, ax = plt.subplots()
filtered_df["country"].value_counts().head(10).plot(kind="bar", ax=ax)
st.pyplot(fig)


# CONTENT GROWTH


st.subheader("Content Growth Over Years")

year_data = filtered_df["release_year"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.plot(year_data.index, year_data.values)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Titles")

st.pyplot(fig)


# CONTENT ADDED PER YEAR


st.subheader("Content Added to Netflix Per Year")

added_data = filtered_df["year_added"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.plot(added_data.index, added_data.values)

ax.set_xlabel("Year Added")
ax.set_ylabel("Number of Titles")

st.pyplot(fig)


# GENRE ANALYSIS


st.subheader("Top Genres")

genres = filtered_df["listed_in"].str.split(", ")
genre_list = [g for sublist in genres for g in sublist]

top_genres = pd.Series(genre_list).value_counts().head(10)

fig, ax = plt.subplots()
top_genres.plot(kind="bar", ax=ax)

st.pyplot(fig)


# MOVIE DURATION ANALYSIS


st.subheader("Most Common Movie Durations")

movies = filtered_df[filtered_df["type"] == "Movie"]

fig, ax = plt.subplots()

movies["duration"].value_counts().head(10).plot(kind="bar", ax=ax)

st.pyplot(fig)


# TV SHOW SEASONS ANALYSIS


st.subheader("Most Common TV Show Seasons")

shows = filtered_df[filtered_df["type"] == "TV Show"]

fig, ax = plt.subplots()

shows["duration"].value_counts().head(10).plot(kind="bar", ax=ax)

st.pyplot(fig)


# ACTOR ANALYSIS


st.subheader("Top Actors Appearing on Netflix")

actors = filtered_df["cast"].str.split(", ")
actor_list = [actor for sublist in actors for actor in sublist]

top_actors = Counter(actor_list).most_common(10)

actor_names = [actor[0] for actor in top_actors]
actor_counts = [actor[1] for actor in top_actors]

fig, ax = plt.subplots()

ax.bar(actor_names, actor_counts)

plt.xticks(rotation=45)

st.pyplot(fig)
