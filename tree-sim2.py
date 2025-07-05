import streamlit as st
import pandas as pd

daily_rain = [.2, .2, .2, 0, .2]
tree_height = [1, 1.2, 1.4, 1.4, 1.6]

df = pd.DataFrame()

# df["days"] = list( range(len(tree_height)) )
df["tree height"] = tree_height
df["daily rain"] = daily_rain

st.title("Daily Rain's Effect on Tree Height")
# st.dataframe(df)
st.line_chart(df, x_label="days")

