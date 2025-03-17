import streamlit as st
import pandas as pd
import requests
import time  # Measure response time





st.set_page_config(layout="wide",page_title="Data Explorer")  

st.title("🤖 Data Explorer App")
st.markdown("---")  # Separator



# Custom CSS for styling
st.markdown(
    """
    <style>

        header {
        background: linear-gradient(to left, #4f5f6e, #4f5f6e) !important;
        box-shadow: none !important;
        }

        .sidebar-title {
            padding-bottom: 15px;  /* Adjust as needed */
            padding-top: 0px !important;  /* Reduce from 20px to 5px */
            margin-top: 0px !important;
            margin-bottom: 10px !important;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            color: #ffffff; /* White text */
            background-color: #4f5f6e; 
            padding: 4px;
            border: 5px solid #000000
            border-radius: 10px;
            border-radius: 25px; /* Rounded corners */
            box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
        }

        .block-container {
        background-color: #d0ddeb;
        padding-top: 65px;
        }

        .stAlert {
            background-color: white !important;  /* Fix background */
            color: black !important;
        }

        /* Global Background */
        .stApp {
            background: linear-gradient(to left, #d0ddeb, #d0ddeb);
        }

        /* Expander Box Customization */
        .st-expander {
            background-color: white !important;
            border-radius: 12px;
            box-shadow: 1px 4px 10px rgba(0, 0, 0, 0.1);
            padding: 5px;
        }

        /* Header Styling */
        h2, h3, h4 {
            color: #ebf4f5;
            font-family: 'Arial', sans-serif;
        }

        /* File Upload Box */
        .stFileUploader {
            border: 2px dashed #1565c0 !important;
            border-radius: 5px;
            background-color: #d0ddeb;
            padding: 20px;
            padding-top: 0px
            

        }

        /* Success Message */
        .stAlert {
            background-color: #dcedc8;
            color: #2e7d32;
            border-radius: 8px;
            font-weight: bold;
        }

        /* Buttons */
        .stButton > button {
            background-color: #37628a;
            color: white;
            border-radius: 10px;
            padding: 10px 18px;
            font-size: 16px;
            border: none;
            transition: 0.3s;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: ##95acc1;
        }

        /* Remove default black border */
        div[data-testid="stDataFrame"] {
            background-color: #EEF2FF !important; /* Light Purple */
            color: #333 !important; /* Dark Text */
            border-radius: 10px !important;
            padding: 10px;
            border: none !important; /* Remove default border */
        }

        /* Change Column Header Background and Text Color */
        /* Target the table header in Streamlit DataFrame */
        div[data-testid="stDataFrame"] thead th {
            background-color: #388e3c !important; /* Green */
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
            padding: 10px;
        }
    
        /* Change Cell Background */
        div[data-testid="stDataFrame"] tbody td {
            background-color: #F8FAFC !important; /* Light Grey */
            color: black !important;
            padding: 10px;
        }


        /* Input Fields */
        input {
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #90caf9;
        }

        /* Dropdown */
        .stSelectbox {
            border-radius: 8px;
            padding: 10px;
        }

        /* Dividers */
        .stDivider {
            border-top: 2px solid #42a5f5;
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App Title
st.write("👈 Please upload a dataset and ask your question about it.")
st.write("⚠️ Ensure personally identifiable (PI) or sensitive information is not included in the uploaded datasets ⚠️")
 
# Sidebar for File Upload

# st.sidebar.header("Explorer Panel",divider=True)

st.sidebar.markdown('<div class="sidebar-title">Explorer Panel</div>', unsafe_allow_html=True)

with st.sidebar:
    


    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📂 **File Upload**", expanded=True):  
        uploaded_file = st.file_uploader('', type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]  # Get file extension

        if file_type == "csv":
            df = pd.read_csv(uploaded_file) 
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file format")
            st.stop()

        ##st.write(f"Loaded the {file_type.upper()} file successfully!")
        st.success("✅ Loaded the file successfully!!!")

    st.divider()    

    with st.sidebar.expander("🔒 **API Key**"):
        API_Key = st.text_input("Enter Your Open Router API Key:",type="password")
    st.divider()


# OpenRouter API Configuration
OPENROUTER_API_KEY = API_Key # Replace with your actual OpenRouter API key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Fetch Available Models from OpenRouter
try:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    
    models_response = requests.get("https://openrouter.ai/api/v1/models", headers=headers,verify=False)
    models_response.raise_for_status()  # Raise HTTPError for bad responses

    models_data = models_response.json()
    model_list = [model["id"] for model in models_data["data"]]  # Extract model IDs

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching model list from OpenRouter: {e}")
    model_list = ["google/gemma-3-4b-it:free"]  # Fallback model
except Exception as e:
    st.error(f"Error processing model list: {e}")
    model_list = ["google/gemma-3-4b-it:free"]  # Fallback model

with st.sidebar:   
    with st.expander("🤖 **Model Selecion**", expanded=True):        
        selected_model = st.selectbox("Choose the Model", model_list)




if uploaded_file is not None:
    st.subheader("Your Dataset:")
    
    st.dataframe(df.head(len(df)), width=3000, height=400)

   

    name = st.text_area(
        "Ask your question:", 
        placeholder="Summarize the dataset for me",
        height=75  # Adjust height for a bigger input box
    )

    col1, col2 = st.columns([5    ,70])


    with col1: 
        ask_button = st.button("Enter")

    with col2:    
        cancel_button = st.button("Cancel")

    # --- OpenRouter Integration ---
    if ask_button and name and not cancel_button:  # Only run if the user has entered a question
        start_time = time.time()

        with st.spinner("Loading..."):
            try:
                # Convert the DataFrame to a string representation
                data_string = df.to_string()  # Or use df.to_json(orient='records') if needed

                # Construct the prompt for OpenRouter
                prompt = (
                    f"Here is the dataset:\n{data_string}\n\n Context:Just give answer, no explanation or breifs \n\nUser Question: {name}\n\nAnswer:"
                )

                # Create the payload for the OpenRouter API
                payload = {
                    "model": selected_model, ##"google/gemma-3-4b-it:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,  # Adjust as needed
                }

                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }

                # Make the API request to OpenRouter
                response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload,verify=False)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                # Parse the response
                try:
                    answer = response.json()["choices"][0]["message"]["content"]
                    end_time = time.time()  # End time tracking
                    response_time = round(end_time - start_time, 2)

                    st.write("Model Response:")
                    st.write(answer,)
                    st.write(f"⏱ **Response Time:** {response_time} seconds")

                except (KeyError, IndexError, TypeError) as e:
                    st.error(f"Error parsing OpenRouter response: {e}. Raw response: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to OpenRouter: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
