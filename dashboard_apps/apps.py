from _lib.app import Nav, App
from first_project import intro
from first_project.section import (
    sales_report
)
import streamlit as st

st.set_page_config(layout="wide")

app = App(
    nav=Nav(
        title='Streamlit',
        children=[
            Nav(
                title='Intro', app=intro.app,
                children=[
                    Nav(title='Sales Report', app=sales_report.app),
                ]
            ),
        ]
    )
)
app.run()
