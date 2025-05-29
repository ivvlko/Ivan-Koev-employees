import pandas as pd
from dateutil import parser


def calculate_pairs_working_time_together(df):
    pairs = []

    for project_id in df['ProjectID'].unique():
        records = df[df['ProjectID'] == project_id]

        for i, emp1 in records.iterrows():
            for j, emp2 in records.iterrows():
                if emp1['EmpID'] >= emp2['EmpID']:
                    continue

                overlap_start = max(emp1['DateFrom'], emp2['DateFrom'])
                overlap_end = min(emp1['DateTo'], emp2['DateTo'])

                if overlap_start <= overlap_end:
                    days = (overlap_end - overlap_start).days
                    pairs.append({
                        'emp1': emp1['EmpID'],
                        'emp2': emp2['EmpID'],
                        'project': project_id,
                        'days': days
                    })

    return sorted(pairs, key=lambda x: x['days'], reverse=True)


def handle_different_datetypes(series):

    def parse_date(val):
        if pd.isna(val) or str(val).strip() == "":
            return pd.NaT
        try:
            return parser.parse(str(val), dayfirst=True)
        except Exception:
            return pd.NaT

    return series.apply(parse_date)