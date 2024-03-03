import streamlit as st
import roster
import pandas as pd
import datetime as dt
import altair as alt

# st.set_page_config(layout="wide")

cols = st.columns(2)
with cols[0]:
    start_dt = st.date_input('Début', dt.date.today() - dt.timedelta(days=10))
with cols[1]:
    end_dt = st.date_input('Fin', dt.date.today())
# st.columns(start_dt,end_dt)

result = roster.fetch_picks_and_bans(start_dt, end_dt)
df = pandas.DataFrame()
for item in result:
    game = item['title']
    df = df._append(game, ignore_index=True)

df_cleaned = df.dropna()
print(df_cleaned)
filter_criteria = df_cleaned['Team1Pick1'] != 'Missing Data'

filtered_df = df_cleaned[filter_criteria]


# Display the DataFrame
st.write('### Historique des picks and bans')

st.dataframe(filtered_df)

grouped_counts = filtered_df.groupby('Team1Ban1').size().reset_index(name='Count')
grouped_counts['Team1Ban1'] = grouped_counts['Team1Ban1'].astype(str)

gr = grouped_counts.set_index('Team1Ban1').sort_values(by='Count', ascending=False).reset_index().head(20)

st.write('### Most frequent first ban champions')

st.write(alt.Chart(gr).mark_bar().encode(
    x=alt.X('Team1Ban1',title='20 Most banned champions',sort=alt.EncodingSortField(field="Count", order='descending', op='max')),
    y=alt.Y('Count'),
).properties(
    width=800,
    height=300
))



# st.bar_chart(grouped_counts.set_index('Team1Ban1').sort_values(by='Count'))
