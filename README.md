# Information Integrity: Fake News Classifier

A Natural Language Processing (NLP) classification pipeline utilizing TF-IDF vectorization and a Random Forest classifier to detect synthetic, misleading, or fraudulent news articles.

## Technology Stack
* **Frontend:** Streamlit
* **Machine Learning:** Scikit-Learn (Random Forest, TF-IDF)
* **Data Processing:** Pandas, NumPy

## Local Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. *(Optional)* If the `.pkl` model file is not included due to size limits, run `python train.py` first to generate the pipeline.
4. Run the application: `streamlit run app.py`
5.