
# Advanced Interactive Job Market Dashboard

## Overview

The Advanced Interactive Job Market Dashboard is a web application developed using Streamlit and Plotly. It provides an in-depth analysis of job market data, including job descriptions, locations, company sizes, and other relevant details. The dashboard offers interactive visualizations and real-time job search functionality using the Adzuna API.

## Features

- **Job Search Portal**: Allows users to search for jobs based on keywords and location.
- **Job Data Visualization**: Provides insights into job trends, skills demand, salary distributions, and company sizes through interactive charts and graphs.
- **Interactive Visualizations**: Scatter plots, bar charts, histograms, and pie charts to explore job market data.
- **Real-time Data**: Integration with the Adzuna API to fetch current job postings.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/saharanm/MSc-Data-Analysis-Project.git
    cd job-market-dashboard
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit application:
    ```bash
    streamlit run finalcode.py
    ```

## Usage

- **Job Search Portal**: Enter the job title and location to search for job postings. The results will display job titles, companies, locations, and brief descriptions with links to detailed job postings.
- **Job Data Visualization**: Use the filters to customize the data displayed, such as selecting a specific country or adjusting the range of experience required. Explore various visualizations to gain insights into job trends and market dynamics.

## Data Source

The job market dataset used in this project is sourced from Kaggle and includes job descriptions, locations, company sizes, and other relevant details.

## Technologies Used

- **Streamlit**: A web application framework for developing interactive data applications.
- **Plotly**: A graphing library used to create interactive charts and graphs.
- **Pandas**: A data manipulation library used for data cleaning and preprocessing.
- **Adzuna API**: An API used to fetch real-time job postings based on user inputs.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.



