import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Anonymization System", layout="wide")

st.title("🔐 Privacy-Preserving Data Anonymization System")
st.markdown("Upload your dataset, apply anonymization techniques, and protect sensitive information.")

def anonymize_dataset(file, k):

    file.seek(0)
    df = pd.read_csv(file)

    df = df.drop(columns=['first','last','street','cc_num','trans_num'], errors='ignore')

    # age generalization
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

    # zip masking
    df['zip'] = df['zip'].astype(str).str[:3] + "**"

    # k-anonymity
    qi_columns = ['age_group','gender','city']
    group_counts = df.groupby(qi_columns).size().reset_index(name='count')

    df = df.merge(group_counts, on=qi_columns)

    df_k = df[df['count'] >= k].drop(columns=['count'])

    # Suppression
    job_counts = df_k['job'].value_counts()
    rare_jobs = job_counts[job_counts < 20].index

    df_k['job'] = df_k['job'].replace(rare_jobs, '*')

    return df_k

# upload Section
st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    st.header("📊 Dataset Overview")

    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

    # column validation
    required_columns = ['age', 'gender', 'city', 'zip', 'job']
    if not all(col in df.columns for col in required_columns):
        st.error("Dataset must contain: age, gender, city, zip, job")
        st.stop()

    st.write("Dataset Shape:", df.shape)
    st.dataframe(df.head(), use_container_width=True)

    st.header("⚙️ Anonymization Settings")

    k = st.slider("🔢 Select K value (Higher = More Privacy)", 2, 10, 5)
    st.caption("Higher K increases privacy but may reduce data utility.")
    
    # run Process
    if st.button("🚀 Run Anonymization"):

        with st.spinner("🔄 Processing anonymization..."):
            result = anonymize_dataset(uploaded_file, k)

        # result
        st.header("📈 Results")

        # metrics
        st.subheader("📊 Summary")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Original Records", len(df))

        with col2:
            st.metric("Anonymized Records", len(result))

        # comparison
        st.subheader("🔍 Before vs After Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Original Data**")
            st.dataframe(df.head(), use_container_width=True)

        with col2:
            st.markdown("**Anonymized Data**")
            st.dataframe(result.head(), use_container_width=True)

        # download
        csv = result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Anonymized Dataset",
            data=csv,
            file_name='anonymized_dataset.csv',
            mime='text/csv'
        )
        st.success(f"✅ Anonymization successfully completed with K = {k}")
