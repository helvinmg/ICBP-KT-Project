import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt
 
rand = np.random.normal(1, 2, size=20)
fig, ax = plt.subplots()
ax.hist(rand, bins=15)
st.pyplot(fig)
 
 
df = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
st.line_chart(df)
 
st.bar_chart(df)
 
st.area_chart(df)
 
df1 = pd.DataFrame(np.random.randn(500, 3), columns=['x', 'y', 'z'])
chart = alt.Chart(df1).mark_circle().encode(x='x', y='y', size='z', color='z', tooltip=['x', 'y', 'z'])
st.altair_chart(chart, use_container_width=True)
 
 
df3 = pd.DataFrame(np.random.randn(600, 2) / [50, 50] + [37.76, -87.4], columns=['lat', 'lon'])
st.map(df3)