# anonymization-system

 User guidance
1. Get Started 
Step 1: Launch the Application
Start the data anonymization system with the given Streamlit application link or locally run the application. The primary interface will show the system name and how to upload a dataset.
Step 2: Upload Dataset
Select your dataset by clicking on the button 'Upload CSV file'. Then, the system will show a preview of the dataset once uploaded, which will consist of the number of rows, columns, and sample data.
Step 3: Review Dataset Overview
Once uploaded, users can see:
•	Shape (rows and columns) of the data set.
•	Sample records (top few rows)
•	Column data types
This assists users to learn the format of the dataset prior to using anonymization.
2. Main Features
2.1 Column Mapping
Users must map columns in datasets according to their meaning:
•	Numerical column (e.g., Age)
•	Categorical column (e.g., Gender)
•	Location column (e.g., City)
•	Column that contains identifiers (e.g., ZIP code)
•	Sensitive attribute (e.g., Job)
This helps to make sure that the system implements anonymization techniques properly.
2.2 k-value Selection
A k-value can be chosen via the slider. The larger the k-value, the more privacy is gained, at the cost of utility of the data.
2.3 Run Anonymization
Click the Run Anonymization button to run the dataset. The system will:

•	Remove direct identifiers.
•	Apply age generalization.
•	Mask ZIP codes
•	Enforce k-anonymity.
•	Suppress rare values.
2.4 View Results 
Upon processing, the system shows:
•	Original records number.
•	Count of records anonymized.
•	Comparison of original data and anonymized data.
2.5 Download Anonymized Dataset
The anonymized dataset can be downloaded by the users by clicking on the button of Download Anonymized Dataset.
3. System Features Overview
3.1 Privacy Protection
It provides data privacy with:
•	Generalization (e.g., age ranges)
•	Masking (e.g., hiding of ZIP codes)
•	K-anonymity (group-based privacy)
•	Elimination of infrequent values.
3.2 User-Friendly Interface
The system is supposed to be easy and user-friendly and enable a user with little technical expertise to anonymize.
4. Troubleshooting
Issue 	Solution
File not uploading 	Ensure the file is in CSV format
Missing column error	Check if selected columns exist in dataset
No results after anonymization	Reduce k-value
Duplicate column selection	Select different columns for each field

5. System Requirements
Requirement	Minimum
Browser	Chrome, Edge, Firefox( latest version)
Internet	Stable connection required
Environment	Streamlit-supported system
Device	Desktop or laptop recommend
