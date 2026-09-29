import pandas as pd
import os

df1 = pd.DataFrame({
    "Item": ["A", "B", "C", "D"],
    "Weight": [0.50, 0.75, 1.00, 1.25],
    "Volume": [40, 30, 20, 10],
    "Tax": [1, 1, 1, 1],
    "Revenue": [20.00, 22.50, 20.00, 12.50]
})

df2 = pd.DataFrame({
    "Item": ["B", "C", "D", "E"],
    "Weight": [0.75, 1.00, 0.75, 1.00],
    "Volume": [10, 20, 20, 30],
    "Tax": [2, 2, 2, 2],
    "Revenue": [15.00, 40.00, 30.00, 60.00]
})

def new_items(df1, df2):
    return (
        df2.loc[~df2["Item"].isin(df1["Item"]), ["Item", "Revenue"]]
           .assign(Driver="New Item")
           .rename(columns={"Revenue": "Impact"})
           [["Item", "Driver", "Impact"]]
    )

def removed_items(df1, df2):
    return (
        df1.loc[~df1["Item"].isin(df2["Item"]), ["Item", "Revenue"]]
           .assign(Driver="Removed Item")
           .rename(columns={"Revenue": "Impact"})
           .assign(Impact=lambda x: -x["Impact"])
           [["Item", "Driver", "Impact"]]
    )


def changed_items(df1, df2, *columns):
    merged = df1.merge(
        df2,
        on="Item",
        suffixes=("_df1", "_df2")
    )

    impact_cols = []

    for i, column in enumerate(columns):

        # Variance for this column
        merged[f"{column}_variance"] = (
            merged[f"{column}_df2"]
            - merged[f"{column}_df1"]
        )

        # Impact starts with the variance
        impact = merged[f"{column}_variance"]

        # Use df2 values for variables before this one
        for prev_col in columns[:i]:
            impact *= merged[f"{prev_col}_df2"]

        # Use df1 values for variables after this one
        for next_col in columns[i + 1:]:
            impact *= merged[f"{next_col}_df1"]

        impact_col = f"{column}_impact"
        merged[impact_col] = impact
        impact_cols.append(impact_col)

    pivoted = merged.melt(
        id_vars=["Item"],
        value_vars=impact_cols,
        var_name="Driver",
        value_name="Impact"
    )

    pivoted["Driver"] = pivoted["Driver"].str.replace(
        "_impact", "", regex=False
    )

    return pivoted.sort_values(["Item", "Driver"]).reset_index(drop=True)

def union_impacts(df1, df2, *columns):
    return pd.concat([
            new_items(df1,df2),
            changed_items(df1,df2,"Weight","Volume","Tax"),
            removed_items(df1,df2)]
        ).sort_values(["Item", "Driver"]).reset_index(drop=True)

def save_to_csv(df, filename):
    filename = os.path.join(
        os.path.dirname(__file__),
        "diagnostic_analysis.csv"
    )

    df.to_csv(filename, index=False)

result = union_impacts(df1,df2,"Weight","Volume","Tax")

save_to_csv(result,"diagnostic_analysis.csv")


