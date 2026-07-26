import os
import zipfile
import glob
import pandas as pd
import joblib
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

zip_file_name = 'archive (2).zip'
extracted_dir = 'extracted_dataset'

# 1. Extract the ZIP file
if os.path.exists(zip_file_name):
    print(f"Status: Found '{zip_file_name}'. Extracting...")
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)
else:
    print(f"Error: '{zip_file_name}' not found. Please ensure it is in the same folder as this script.")
    exit()

# 2. Find the CSV file(s) inside the extracted folder
csv_files = glob.glob(f"{extracted_dir}/**/*.csv", recursive=True)

if not csv_files:
    print("Error: No CSV files were found inside the zip archive.")
    exit()

# 3. Load and merge the data
# Kaggle fake news datasets often come split into 'Fake.csv' and 'True.csv'
if len(csv_files) == 2:
    print(f"Status: Found multiple CSVs. Merging {csv_files[0]} and {csv_files[1]}...")
    df1 = pd.read_csv(csv_files[0])
    df2 = pd.read_csv(csv_files[1])
    
    # Assign labels based on file names (1 for Fake, 0 for Real)
    if 'fake' in csv_files[0].lower():
        df1['label'] = 1
        df2['label'] = 0
    else:
        df1['label'] = 0
        df2['label'] = 1
        
    df = pd.concat([df1, df2], axis=0, ignore_index=True)
else:
    print(f"Status: Loading dataset from '{csv_files[0]}'...")
    df = pd.read_csv(csv_files[0])

# 4. Standardize Column Names
# Convert all columns to lowercase to avoid case-sensitivity issues
df.columns = [col.lower() for col in df.columns]

# Ensure we have a 'text' column
if 'text' not in df.columns:
    if 'title' in df.columns:
        df['text'] = df['title']
    elif 'tweet' in df.columns:
        df['text'] = df['tweet']
    else:
        print(f"Error: Could not find a 'text' column. Available columns are: {df.columns.tolist()}")
        exit()

# Ensure we have a 'label' column
if 'label' not in df.columns:
    if 'class' in df.columns:
        df['label'] = df['class']
    elif 'target' in df.columns:
        df['label'] = df['target']
    else:
        print(f"Error: Could not find a 'label' column. Available columns are: {df.columns.tolist()}")
        exit()

# 5. Clean missing values
df = df.dropna(subset=['text', 'label'])

# 6. Fast text normalization
print("Status: Normalizing text...")
def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()

df['text'] = df['text'].apply(clean_text)

X = df['text']
# Ensure labels are integers
y = df['label'].astype(int)

# 7. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. Scikit-Learn Pipeline
print("Status: Training model pipeline... (This may take a minute depending on dataset size)")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
])

pipeline.fit(X_train, y_train)

# 9. Metrics
y_pred = pipeline.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# 10. Save single pipeline file
joblib.dump(pipeline, 'fake_news_pipeline.pkl')
print("\nStatus: Saved successfully as 'fake_news_pipeline.pkl'")