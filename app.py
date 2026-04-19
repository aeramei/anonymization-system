import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Anonymization System", layout="wide")

st.title("🔐 Privacy-Preserving Data Anonymization System")
st.markdown("Upload your dataset, apply anonymization techniques, and protect sensitive information.")


def anonymize_dataset(file, k, age_col, gender_col, city_col, zip_col, job_col):

    file.seek(0)
    df = pd.read_csv(file)

    # remove direct identifiers (financial + personal)
    df = df.drop(columns=['first', 'last', 'street', 'cc_num', 'trans_num'], errors='ignore')

    # ensure selected columns exist
    selected_columns = [age_col, gender_col, city_col, zip_col, job_col]
    for col in selected_columns:
        if col not in df.columns:
            st.error(f"❌ Missing column: {col}")
            st.stop()

    # handle missing values
    df = df.dropna(subset=selected_columns)

    # convert age safely
    df[age_col] = pd.to_numeric(df[age_col], errors='coerce')
    df = df.dropna(subset=[age_col])

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

    df['age_group'] = df[age_col].apply(generalize_age)

    # remove original age
    df = df.drop(columns=[age_col])

    # ZIP masking (improved)
    df[zip_col] = df[zip_col].astype(str).str.zfill(5)
    df['zip_masked'] = df[zip_col].str[:3] + "**"

    # remove original zip
    df = df.drop(columns=[zip_col])

    # k-anonymity
    qi_columns = ['age_group', gender_col, city_col]
    qi_columns = [col for col in qi_columns if col in df.columns]

    group_counts = df.groupby(qi_columns).size().reset_index(name='count')
    df = df.merge(group_counts, on=qi_columns)

    df_k = df[df['count'] >= k].drop(columns=['count'])

    # dynamic suppression
    if len(df_k) > 0:
        job_counts = df_k[job_col].value_counts()
        threshold = max(2, int(0.02 * len(df_k)))
        rare_jobs = job_counts[job_counts < threshold].index

        # FIXED warning issue
        df_k.loc[:, job_col] = df_k[job_col].replace(rare_jobs, '*')

    return df_k

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    st.header("📊 Dataset Overview")

    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

    st.write(f"📏 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    st.dataframe(df.head(), use_container_width=True)

    # show column types (bonus)
    st.write("📌 Column Data Types:")
    st.write(df.dtypes)

    # column Mapping
    st.header("⚙️ Anonymization Settings")
    st.info("Map your dataset columns based on their meaning. Column names may differ across datasets (e.g., Age → customer_age, City → location).")

    columns = df.columns.tolist()

    age_col = st.selectbox("Select Numerical Column (e.g., Age)", columns)
    gender_col = st.selectbox("Select Categorical Column (e.g., Gender)", columns)
    city_col = st.selectbox("Select Location Column (e.g., City)", columns)
    zip_col = st.selectbox("Select Identifier Column (e.g., ZIP)", columns)
    job_col = st.selectbox("Select Sensitive Attribute (e.g., Job)", columns)

    # prevent duplicate selection
    if len({age_col, gender_col, city_col, zip_col, job_col}) < 5:
        st.warning("⚠️ Please select different columns for each field.")
        st.stop()

    # k value
    k = st.slider("🔢 Select K value (Higher = More Privacy)", 2, 10, 5)
    st.caption("Higher K increases privacy but may reduce data utility.")

    if st.button("🚀 Run Anonymization"):

        with st.spinner("🔄 Processing anonymization..."):
            result = anonymize_dataset(
                uploaded_file, k,
                age_col, gender_col, city_col, zip_col, job_col
            )

        # handle empty result
        if result.empty:
            st.warning("⚠️ No data satisfies the selected K value. Try reducing K.")
            st.stop()

        # results
        st.header("📈 Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Records", len(df))
        with col2:
            st.metric("Anonymized Records", len(result))

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
