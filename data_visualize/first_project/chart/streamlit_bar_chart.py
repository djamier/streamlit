import streamlit as st
import pandas as pd
import os
import snowflake.connector
import plotly.express as px
import pendulum

def app():

    @st.cache_resource
    def get_snowflake_connection():
        account = os.getenv('SNOWFLAKE_ACCOUNT_ID')
        user = os.getenv('SNOWFLAKE_USER')
        password = os.getenv('SNOWFLAKE_PASS')
        role = os.getenv('SNOWFLAKE_ROLE')
        warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        database = os.getenv('SNOWFLAKE_DATABASE')
        schema = os.getenv('SNOWFLAKE_SCHEMA')

        conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            role=role,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        return conn


    @st.cache_data(experimental_allow_widgets=True)
    def get_date_range():
        default_end_date = pendulum.today().date()
        default_start_date = default_end_date.start_of('month')
            
        dates = st.date_input(
            label='Dates',
            value=(default_start_date, default_end_date),
            key='date_input'
        )

        if len(dates) != 2:
            st.stop()

        start_date, end_date = dates
        return start_date, end_date


    @st.cache_data
    def read_query_file(query_file):
        with open(query_file, 'r') as file:
            query = file.read()
        return query


    @st.cache_data
    def execute_query(
        _conn, query,
        start_date,
        end_date
    ):
        replace_filter = {
            'start_date_str': f"'{start_date}'",
            'end_date_str': f"'{end_date}'"
        }

        formatted_query = query.format(**replace_filter)
        result = pd.read_sql(formatted_query, _conn)
        return result


    @st.cache_data
    def create_sales_bar_chart(result):
        result = result.sort_values('TOTAL_SALES')

        fig = px.bar(
            result,
            x='ORDER_SOURCE',
            y='TOTAL_SALES',
            orientation='v',
            width=10,
            color_discrete_sequence=['#4ADEDE']
        )
        for x, y in zip(result['ORDER_SOURCE'], result['TOTAL_SALES']):
            fig.add_annotation(
                x=x,
                y=y,
                text=f'Rp. {y:,.2f}',
                showarrow=False,
                font=dict(color='black', size=12),
                xshift=0,
                yshift=20,
                align='center'
            )
        fig.update_layout(
            title='',
            xaxis_title='Channel',
            yaxis_title='Sales',
            barmode='group'
        )
        return fig


    conn = get_snowflake_connection()

    start_date, end_date = get_date_range()
    query = read_query_file('first_project/sql/sales_bar_chart.sql')
    result = execute_query(conn, query, start_date,end_date )
    fig = create_sales_bar_chart(result)

    with st.container():
        st.plotly_chart(fig, use_container_width=True)
