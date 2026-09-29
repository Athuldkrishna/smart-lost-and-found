# Smart Lost & Found



An AI-powered Lost & Found system designed for campus communities.



## Features



- User Login and Sign Up

- Report Lost Items

- Report Found Items

- AI-based Image Matching

- View Possible Matches

- Database Storage

- Reports Management



## Technologies Used



- Python

- Streamlit

- Supabase (PostgreSQL + Storage)

- CLIP / Image Matching

- HTML and CSS



## Supabase Setup

1\. Create a project at https://supabase.com.

2\. Open **SQL Editor**, paste the contents of `supabase_schema.sql`, and click **Run**. This creates the `users` and `reports` tables and the `item-images` storage bucket.

3\. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in `SUPABASE_URL` and `SUPABASE_KEY` (Project Settings → API; use the secret / service_role key).

## How to Run



1\. Create and activate a virtual environment.

2\. Install the required dependencies.

3\. Run the application:



&#x20;   streamlit run app.py



## Project Structure



- app.py - Main Streamlit application

- database.py - Supabase database and storage operations

- supabase_schema.sql - Tables and storage bucket setup (run once in Supabase)

- image_matcher.py - Image matching functionality

- clip_test.py - CLIP image comparison/testing

- .gitignore - Files excluded from Git


