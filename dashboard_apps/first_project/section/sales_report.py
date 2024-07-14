import streamlit as st
import pendulum
from first_project.chart import streamlit_bar_chart, streamlit_line_chart

def get_date_range():
    default_end_date = pendulum.today().date()
    default_start_date = default_end_date.start_of('month')
        
    dates = st.date_input(label='Dates', value=(default_start_date, default_end_date), key='date_input')

    if len(dates) != 2:
        st.stop()

    start_date, end_date = dates
    return start_date, end_date

def app():
    start_date, end_date = get_date_range()
    streamlit_bar_chart.app(start_date, end_date)
    streamlit_line_chart.app(start_date, end_date)
    