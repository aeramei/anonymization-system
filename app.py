import streamlit as st
import pandas as pd

# ==============================
# Anonymization Function
# ==============================
def anonymize_dataset(file_path):

    df = pd.read_csv(file_path)

    df = df.drop(columns=['first','last','street','cc_num','trans_num'], errors='ignore')

    def generalize_age(age):
        if age < 20:
            return "0-20"
        elif age < 30:
            return "20-30"
        elif age < 40:
            return "30-40"
        elif age < 50:
            return "40-50"
        elif age < 60:
            return "50-60"
        else:
            return "60+"

    df['age_group'] = df['age'].apply(generalize_age)

    df['zip'] = df['zip'].astype(str).str[:3] + "**"

    qi_columns = ['age_group','gender','city']
    group_counts = df.groupby(qi_columns).size().reset_index(name='count')

    df = df.merge(group_counts, on=qi_columns)

    k = 5
    df_k = df[df['count'] >= k].drop(columns=['count'])

    job_counts = df_k['job'].value_counts()
    rare_jobs = job_counts[job_counts < 20].index

    df_k['job'] = df_k['job'].replace(rare_jobs, '*')

    df_k.to_csv("anonymized_dataset_final.csv", index=False)

    return df_k


# ==============================
# Streamlit Interface
# ==============================
st.title("Privacy-Preserving Data Anonymization System")

uploaded_file = st.file_uploader("Upload CSV file")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.write("Original Dataset Preview")
    st.dataframe(df.head())

    if st.button("Run Anonymization"):

        result = anonymize_dataset(uploaded_file)

        st.write("Anonymized Dataset Preview")
        st.dataframe(result.head())

        st.success("Anonymization Completed!")