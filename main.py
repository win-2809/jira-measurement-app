from datetime import time
import math
from re import T
import streamlit as st
import pandas as pd
import numpy as np
from streamlit.proto.SessionState_pb2 import SessionState
import tracker
import datetime
import plotly.graph_objs as go
import plotly.express as px

st.set_page_config(
    page_title="Jira Tracker",
    initial_sidebar_state="expanded",
    layout="wide"
)

st.title('Jira Tracker')

@st.cache(allow_output_mutation=True)
def load_data(username, token, domain, projectKey):
    data = tracker.load_data(username, token, domain, projectKey)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data["created"] = pd.to_datetime(data.get("created")).dt.date
    data["updated"] = pd.to_datetime(data.get("updated")).dt.date

    return data

query_params = st.experimental_get_query_params()

# Input area   
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        if "username" not in query_params:
            username = st.text_input("Username")
        else:
            username = st.text_input("Username", value=query_params["username"][0])
    with col2:
        if "token" not in query_params:
            token = st.text_input("Token")
        else:
            token = st.text_input("Token", value=query_params["token"][0])
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        if "domain" not in query_params:
            domain = st.text_input("Domain", help="https://<YOUR-TEAM>.atlassian.net")
        else: 
            domain = st.text_input("Domain", help="https://<YOUR-TEAM>.atlassian.net", value=query_params["domain"][0])
    with col2:
        if "projectkey" not in query_params:
            projectKey = st.text_input("Project Key")
        else:
            projectKey = st.text_input("Project Key", value=query_params["projectkey"][0])

    st.experimental_set_query_params(username=username, token=token, domain=domain, projectkey=projectKey)

if len(username) > 0 and len(token) > 0 and len(domain) > 0 and len(projectKey) > 0:
    # Load 10,000 rows of data into the dataframe.
    data = load_data(username, token, domain, projectKey)
    st.sidebar.subheader('Filter set')
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            min_date = datetime.date.today() - datetime.timedelta(days=90)
            max_date = datetime.date.today()
            datePicker = st.sidebar.date_input(
                "Date picker",
                (min_date, max_date))
        with col2:
            assigneeOptions = st.sidebar.multiselect(
                "Assignee",
                data["assignee"].unique(),
                [])
        with col3:
            priorityOptions = st.sidebar.multiselect(
                "Priority",
                data["priority"].unique(),
                [])
        with col4:
            statusOptions = st.sidebar.multiselect(
                "Status",
                data["status"].unique(),
                [])
        with col5:
            issueTypeOptions = st.sidebar.multiselect(
                "Issue type",
                data["issuetype"].unique(),
                [])

    if len(datePicker) == 2:
        data = data[(data["created"] >= datePicker[0]) & (data["created"] <= datePicker[1])]
    else:
        data = data

    if len(assigneeOptions) > 0:
        data = data[(data["assignee"].isin(assigneeOptions))]
    else:
        data = data

    if len(priorityOptions) > 0:
        data = data[(data["priority"].isin(priorityOptions))]
    else:
        data = data

    if len(statusOptions) > 0:
        data = data[(data["status"].isin(statusOptions))]
    else:
        data = data

    if len(issueTypeOptions) > 0:
        data = data[(data["issuetype"].isin(issueTypeOptions))]
    else:
        data = data

    # General numbers
    with st.container():
        ## Get total issue of the project
        numberOfRows = len(data.index)
        ## Get time range of the project
        timeRange = ((data["created"].max()) - (data["created"].min())).days
        if timeRange <= (365/12):
            timeRange = str(timeRange) + " days" 
        else:
            timeRange = str(int(timeRange/30)) + " month(s)"  
        ## Get assignee issue of the project
        numberOfAssignee = data.assignee.nunique(dropna=True)
        ## Get bug issue of the project
        numberOfBug = len(data[data["issuetype"] == "Bug"])

        st.subheader('General')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Time Range", timeRange)
        col2.metric("Number of Assignees", numberOfAssignee)
        col3.metric("Number of Issues", numberOfRows)
        col4.metric("Number of Bugs", numberOfBug)

    # Inspect the raw data
    with st.container():
        st.subheader('Details')
        st.write(data)

    # Number of Tickets by Month
    with st.container():
        st.subheader('Number of Tickets by Month')
        dataMonthIndex = (data['created'].sort_index().value_counts()).to_frame()
        dataMonthIndex.index = pd.to_datetime(dataMonthIndex.index)
        dataMonthIndex = dataMonthIndex.groupby(pd.Grouper(freq='M')).sum()
        dataMonthIndex.index = dataMonthIndex.index.strftime('%B %Y')
        fig = go.Figure([go.Bar(x=dataMonthIndex.index, y=dataMonthIndex['created'])])
        st.plotly_chart(fig, use_container_width=True)  

    # Number of Tickets by Day
    with st.container():
        st.subheader('Number of Tickets by Day')
        dataMonthIndex = (data['created'].sort_index().value_counts()).to_frame().sort_index()
        dataMonthIndex.index = pd.to_datetime(dataMonthIndex.index)
        fig = go.Figure([go.Scatter(x=dataMonthIndex.index, y=dataMonthIndex['created'])])
        st.plotly_chart(fig, use_container_width=True)  

    # Priority and assignee segmentation
    with st.container():
        col1, col2 = st.columns(2)

        # Priority segmentation
        with col1:
            labels = data['priority'].value_counts().index
            values = data['priority'].value_counts().values

            st.subheader('Priority segmentation')
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
            st.plotly_chart(fig, use_container_width=True)

        # Assignee segmentation
        with col2:
            labels = data['assignee'].value_counts().index
            values = data['assignee'].value_counts().values

            st.subheader('Assignee segmentation')
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
            st.plotly_chart(fig, use_container_width=True)

    # Number of Assignees by Priorities
    with st.container():
        st.subheader('Number of Tickets by Assignees & Priorities')
        fig = go.Figure()
        for assignee, group in data.groupby("assignee"):
            fig.add_trace(go.Bar(x=group['priority'].value_counts().index, y=group['priority'].value_counts().values, name=assignee))
        st.plotly_chart(fig, use_container_width=True)    
