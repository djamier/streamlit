import streamlit as st
import pandas as pd
import os
import snowflake.connector
import plotly.express as px
import pendulum

def app(start_date, end_date):

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


    @st.cache_data
    def read_query_file(query_file): 
        with open(query_file, 'r') as file:
            query = file.read()
        return query


    @st.cache_data
    def execute_query(
        _conn, 
        query :str, 
        start_date, 
        end_date
    ):
        replace_filter = {
            'start_date_str': f"'{start_date}'",
            'end_date_str': f"'{end_date}'"
        }

        formatted_query = query.format(**replace_filter)
        result = pd.read_sql(formatted_query,_conn)
        return result


    @st.cache_data
    def create_sales_line_chart(result):
        result['ORDER_DATE'] = pd.to_datetime(result['ORDER_DATE']).dt.day

        fig = px.line(
            result, 
            x='ORDER_DATE', 
            y='TOTAL_SALES', 
            color='ORDER_SOURCE',
            width=1200, 
            color_discrete_map={
                'Offline': '#ff9d5c',
                'Online': '#028A0F'
            }
        )
        for x, y in zip(result['ORDER_DATE'], result['TOTAL_SALES']):
            max_yaxis = max(result['TOTAL_SALES'])
            text = f'Rp. {y:,.0f}'
            fig.add_annotation(
                x=x,
                y=y,
                text = text,
                showarrow=False,
                font=dict(color='black', size=12),
                xshift=0,
                yshift=15
            )

            fig.update_xaxes(dtick='D1', tickformat='%Y-%m-%d')
            fig.update_layout(
                title='',
                xaxis_title='Days',
                yaxis_title='Sales',
                yaxis_range=[0, max_yaxis],
                xaxis_range=[0, 31],
                xaxis=dict(
                    tickangle=1,
                    tickfont=dict(size=10)
                )
            )
        return fig


    conn = get_snowflake_connection()

    query = read_query_file('first_project/sql/sales_line_chart.sql')
    result = execute_query(conn, query, start_date, end_date)
    fig = create_sales_line_chart(result)

    with st.container():
        st.plotly_chart(fig)
