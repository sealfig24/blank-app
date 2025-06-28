import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns

def grow_tree(daily_rain):
  height = 1
  tree_heights = []
  for inches_of_rain in daily_rain:
    height += inches_of_rain
    tree_heights.append(height)
  return tree_heights

daily_rain = [.2, .1, 0, 0, .1, .2, .3, 0, .05]
daily_tree_height = grow_tree(daily_rain)
print(daily_tree_height)

days = list(range(len(daily_rain)))
print(days)

df = pd.DataFrame({"tree height": daily_tree_height, "daily rain": daily_rain})

# Create a Seaborn pairplot
plot = sns.lineplot(df)
st.pyplot(plot.get_figure())