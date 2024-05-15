import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import json
import requests
import plotly.io as pio

# Set Plotly to use the standard json library instead of orjson
pio.json.config.default_engine = 'json'

# Function to load data with error handling for JSON


@st.cache_data
def load_data():
    df = pd.read_csv(r'/Users/manoj/Downloads/project/web/filtered_data.csv')

    def parse_json(data):
        try:
            return json.loads(data.replace("'", '"'))
        except json.JSONDecodeError:
            return {}  # Return an empty dictionary if error occurs
    df['Benefits'] = df['Benefits'].apply(parse_json)
    return df


data = load_data()

# When modifying the data, work on a copy
data_to_use = data.copy()

# Function to fetch jobs from the Adzuna API


def fetch_jobs(what, where, results_per_page=10):
    API_ID = "63530e90"
    API_KEY = "7334ab91b98448e9a96114e129acf4b2"
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={API_ID}&app_key={API_KEY}&what={what}&where={where}&results_per_page={results_per_page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to display job search results


def display_jobs(jobs):
    for job in jobs['results']:
        st.markdown(f"### {job['title']}")
        st.markdown(f"Company: {job['company']['display_name']}")
        st.markdown(f"Location: {job['location']['display_name']}")
        # Displaying the first 200 characters
        st.markdown(f"Description: {job['description'][:200]}...")
        st.markdown(
            f"[Read more]({job['redirect_url']})", unsafe_allow_html=True)
        st.markdown("---")


# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Dashboard", "Job Search"])

if app_mode == "Dashboard":
    data = load_data()
    data['Job Posting Date'] = pd.to_datetime(data['Job Posting Date'])
    st.title('Advanced Interactive Job Market Dashboard')
    st.sidebar.header('Filters')
    selected_country = st.sidebar.selectbox(
        'Select Country', options=data['Country'].unique())
    filtered_data = data[data['Country'] == selected_country]
    st.header('Filtered Job Data')
    st.write(
        filtered_data[['Job Title', 'Company', 'Salary Range', 'Experience']])

    # 2D Salary Ranges by Job Role
    st.header('2D Salary Visualization by Job Role and Experience')
    fig = px.scatter(filtered_data, x='Job Title', y='Salary Range',
                     color='Job Title', symbol='Job Title')
    st.plotly_chart(fig)

    # Experience Required for Each Job Type with an interactive slider
    st.header('Experience Required for Each Job Type')
    experience_years = st.slider('Select range of experience', 0, 20, (1, 10))
    filtered_data['Experience_Min'] = filtered_data['Experience'].apply(
        lambda x: int(x.split('to')[0].strip().split(' ')[0]))
    filtered_data['Experience_Max'] = filtered_data['Experience'].apply(
        lambda x: int(x.split('to')[-1].strip().split(' ')[0]))
    avg_experience = filtered_data.groupby('Job Title').agg(
        {'Experience_Min': 'mean', 'Experience_Max': 'mean'}).reset_index()
    avg_experience['Average Experience'] = (
        avg_experience['Experience_Min'] + avg_experience['Experience_Max']) / 2
    exp_filtered_data = avg_experience[(avg_experience['Average Experience'] >= experience_years[0]) & (
        avg_experience['Average Experience'] <= experience_years[1])]
    fig = px.bar(exp_filtered_data, x='Job Title',
                 y='Average Experience', color='Job Title')
    st.plotly_chart(fig)

    # Skills Demand Analysis with Dynamic Top N Filter
    st.header('Top N Demanded Skills')
    top_n = st.slider('Select number of top skills to display', 5, 50, 20)
    skills_list = filtered_data['skills'].str.lower().str.split(',').sum()
    skill_counts = Counter(skills_list)
    df_skills = pd.DataFrame(skill_counts.items(), columns=['Skill', 'Count'])
    fig = px.bar(df_skills.nlargest(top_n, 'Count'), x='Skill', y='Count')
    st.plotly_chart(fig)

    

    # Salary Range Distribution
    st.header('Salary Range Distribution')
    fig = px.histogram(filtered_data, x='Salary Range', nbins=20)
    st.plotly_chart(fig)

    # Company Size Distribution
    st.header('Company Size Distribution')
    fig = px.histogram(filtered_data, x='Company Size', nbins=20)
    st.plotly_chart(fig)

elif app_mode == "Job Search":
    st.title("🔍 Job Search Portal")
    cols = st.columns(2)
    what = cols[0].text_input(
        "What job are you looking for?", "software developer")
    where = cols[1].text_input("Where?", "London")
    search_button = st.button("Search Jobs")

    if search_button:
        jobs = fetch_jobs(what, where)
        if jobs and jobs.get('results'):
            display_jobs(jobs)
        else:
            st.error("No jobs found or failed to retrieve jobs.")