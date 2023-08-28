from _lib.app import Nav, App
from first_project import intro
from first_project.chart import (
    streamlit_bar_chart, streamlit_line_chart
)
import streamlit as st

st.set_page_config(layout="wide")

app = App(
    nav=Nav(
        title='Streamlit',
        children=[
            Nav(
                title='Report First Project', app=intro.app,
                children=[
                    Nav(title='Sales bar chart', app=streamlit_bar_chart.app),
                    Nav(title='Line bar chart', app=streamlit_line_chart.app),
                ]
            ),
        ]
    )
)
app.run()
