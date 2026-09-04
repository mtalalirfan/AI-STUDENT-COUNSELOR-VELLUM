import os
import pandas as pd

SOURCES = ["QS", "THE", "ARWU", "US News", "CWUR"]

CSV_PATH = os.path.join(os.path.dirname(__file__), "rankings.csv")

SAMPLE_DATA = [
    {"University": "Massachusetts Institute of Technology", "Country": "United States", "QS": 1, "THE": 5, "ARWU": 3, "US News": 2, "CWUR": 2},
    {"University": "University of Oxford", "Country": "United Kingdom", "QS": 3, "THE": 1, "ARWU": 7, "US News": 5, "CWUR": 6},
    {"University": "University of Cambridge", "Country": "United Kingdom", "QS": 5, "THE": 3, "ARWU": 5, "US News": 8, "CWUR": 9},
    {"University": "Harvard University", "Country": "United States", "QS": 4, "THE": 2, "ARWU": 1, "US News": 1, "CWUR": 1},
    {"University": "Stanford University", "Country": "United States", "QS": 6, "THE": 4, "ARWU": 2, "US News": 3, "CWUR": 3},
    {"University": "ETH Zurich", "Country": "Switzerland", "QS": 7, "THE": 11, "ARWU": 20, "US News": 15, "CWUR": 22},
    {"University": "Imperial College London", "Country": "United Kingdom", "QS": 2, "THE": 10, "ARWU": 24, "US News": 25, "CWUR": 28},
    {"University": "National University of Singapore", "Country": "Singapore", "QS": 8, "THE": 17, "ARWU": 68, "US News": 26, "CWUR": 66},
    {"University": "University of California, Berkeley", "Country": "United States", "QS": 12, "THE": 9, "ARWU": 4, "US News": 4, "CWUR": 4},
    {"University": "Technical University of Munich", "Country": "Germany", "QS": 28, "THE": 30, "ARWU": 53, "US News": 47, "CWUR": 61},
    {"University": "Ludwig Maximilian University of Munich", "Country": "Germany", "QS": 59, "THE": 44, "ARWU": 46, "US News": 55, "CWUR": 70},
    {"University": "RWTH Aachen University", "Country": "Germany", "QS": 106, "THE": 91, "ARWU": 101, "US News": 140, "CWUR": 133},
    {"University": "Heidelberg University", "Country": "Germany", "QS": 87, "THE": 62, "ARWU": 47, "US News": 58, "CWUR": 55},
    {"University": "University of Toronto", "Country": "Canada", "QS": 25, "THE": 21, "ARWU": 23, "US News": 18, "CWUR": 19},
    {"University": "University of British Columbia", "Country": "Canada", "QS": 34, "THE": 41, "ARWU": 38, "US News": 33, "CWUR": 45},
    {"University": "University of Melbourne", "Country": "Australia", "QS": 13, "THE": 34, "ARWU": 35, "US News": 22, "CWUR": 43},
    {"University": "Australian National University", "Country": "Australia", "QS": 30, "THE": 62, "ARWU": 76, "US News": 66, "CWUR": 88},
    {"University": "University of Sydney", "Country": "Australia", "QS": 18, "THE": 54, "ARWU": 65, "US News": 27, "CWUR": 62},
    {"University": "Delft University of Technology", "Country": "Netherlands", "QS": 47, "THE": 55, "ARWU": 88, "US News": 129, "CWUR": 118},
    {"University": "University of Amsterdam", "Country": "Netherlands", "QS": 55, "THE": 66, "ARWU": 74, "US News": 60, "CWUR": 74},
    {"University": "KU Leuven", "Country": "Belgium", "QS": 65, "THE": 45, "ARWU": 82, "US News": 78, "CWUR": 90},
    {"University": "KTH Royal Institute of Technology", "Country": "Sweden", "QS": 78, "THE": 120, "ARWU": 151, "US News": 190, "CWUR": 210},
    {"University": "Uppsala University", "Country": "Sweden", "QS": 116, "THE": 87, "ARWU": 66, "US News": 89, "CWUR": 95},
    {"University": "University of Copenhagen", "Country": "Denmark", "QS": 96, "THE": 96, "ARWU": 30, "US News": 30, "CWUR": 40},
    {"University": "University of Helsinki", "Country": "Finland", "QS": 116, "THE": 106, "ARWU": 79, "US News": 76, "CWUR": 100},
    {"University": "Sciences Po", "Country": "France", "QS": 214, "THE": 301, "ARWU": 401, "US News": 460, "CWUR": 512},
    {"University": "Sorbonne University", "Country": "France", "QS": 63, "THE": 73, "ARWU": 37, "US News": 42, "CWUR": 48},
    {"University": "Technical University of Denmark", "Country": "Denmark", "QS": 76, "THE": 113, "ARWU": 121, "US News": 160, "CWUR": 170},
    {"University": "Istanbul Technical University", "Country": "Turkey", "QS": 401, "THE": 501, "ARWU": 601, "US News": 620, "CWUR": 580},
    {"University": "Middle East Technical University", "Country": "Turkey", "QS": 391, "THE": 401, "ARWU": 501, "US News": 470, "CWUR": 430},
    {"University": "Boğaziçi University", "Country": "Turkey", "QS": 551, "THE": 601, "ARWU": None, "US News": 651, "CWUR": 601},
    {"University": "Tallinn University of Technology", "Country": "Estonia", "QS": 601, "THE": 601, "ARWU": None, "US News": 900, "CWUR": 850},
    {"University": "University of Tartu", "Country": "Estonia", "QS": 355, "THE": 301, "ARWU": 601, "US News": 500, "CWUR": 470},
    {"University": "Universiti Malaya", "Country": "Malaysia", "QS": 60, "THE": 301, "ARWU": 401, "US News": 250, "CWUR": 350},
    {"University": "Universiti Teknologi Malaysia", "Country": "Malaysia", "QS": 188, "THE": 401, "ARWU": 601, "US News": 480, "CWUR": 520},
    {"University": "National University of Sciences and Technology, Pakistan", "Country": "Pakistan", "QS": 355, "THE": 601, "ARWU": None, "US News": 900, "CWUR": 950},
    {"University": "Lahore University of Management Sciences", "Country": "Pakistan", "QS": 501, "THE": 601, "ARWU": None, "US News": None, "CWUR": None},
    {"University": "COMSATS University Islamabad", "Country": "Pakistan", "QS": 801, "THE": 1001, "ARWU": None, "US News": None, "CWUR": None},
    {"University": "FAST National University of Computer and Emerging Sciences", "Country": "Pakistan", "QS": None, "THE": None, "ARWU": None, "US News": None, "CWUR": None},
    {"University": "University of Auckland", "Country": "New Zealand", "QS": 65, "THE": 122, "ARWU": 151, "US News": 173, "CWUR": 180},
]


def load_dataframe() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame(SAMPLE_DATA)


def search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df
    mask = df["University"].str.contains(query, case=False, na=False) | df["Country"].str.contains(query, case=False, na=False)
    return df[mask]


def composite_score(row: pd.Series) -> float:
    ranks = [row.get(s) for s in SOURCES if pd.notna(row.get(s))]
    if not ranks:
        return float("nan")
    return sum(ranks) / len(ranks)
