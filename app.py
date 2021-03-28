from helper import *
import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
import random
import base64
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title=" Curtiss-Wright Data Analysis App",page_icon="CW.png")
st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
st.title('Data Plots / Stats')
st.subheader('Create plots and show main stats for each parameter')

uploaded_csv_file = st.file_uploader(label = "Choose a file/files in csv format",
                                    accept_multiple_files = True, type = ["csv"])


if uploaded_csv_file:
    if len(uploaded_csv_file) > 1:
        st.markdown("**Multiple files loaded, how do you want to concatenate them?**")
        choice_concat = st.radio("", ("Horizontally", "Vertically"))
        if choice_concat == "Horizontally":
            file = load_multiple_csv_files_horizontally(uploaded_csv_file)
            list_of_parameters, time_option, column_name_time = data_info(file)

        if choice_concat == "Vertically":
            file = load_multiple_csv_files_vertically(uploaded_csv_file)
            list_of_parameters, time_option, column_name_time = data_info(file)
    else:
            file = load_multiple_csv_files_horizontally(uploaded_csv_file)
            list_of_parameters, time_option, column_name_time = data_info(file)


    if list_of_parameters:
        check_box_raw_data = st.checkbox("Display raw data")
        if check_box_raw_data:
            st.subheader("Raw data")
            st.dataframe(file[list_of_parameters])
            st.markdown(file_download_raw_data(file[list_of_parameters]), unsafe_allow_html=True)

        check_box_stats = st.checkbox("Display Stats")
        if check_box_stats:
            st.subheader("Stats")
            stats = show_stats(file[list_of_parameters], list_of_parameters)
            stats = file[list_of_parameters].agg(["min", "max", "mean", "median", "std"])
            st.table(stats.T)
            st.markdown(file_download_stats(file[list_of_parameters], list_of_parameters), unsafe_allow_html=True)

        check_box_plots = st.checkbox("Display Plots")
        if check_box_plots:
            st.markdown("**Select the type of plot:**")
            choice_plots = st.radio("", ("NO PLOT", "SHARED X and Y AXIS",
                                    "SHARED X-AXIS ONLY (Subplots)","ONE FIGURE FOR EACH PARAMETER"))

            if choice_plots == "SHARED X and Y AXIS":

                st.subheader("Display Data based on the selected parameters")
                st.markdown("* **Plot with shared x and y axis**")
                st.info("Note: If a time object exists on the sidebar, if you select it then time will be plotted on x-axis")
                if "time_option" in globals() and time_option:
                    st.plotly_chart(display_plots_with_time(file, list_of_parameters, column_name_time[0]))
                    check_box_time_plot = st.checkbox("Do you want to plot the time object?")
                    if check_box_time_plot:
                        st.plotly_chart(display_time(file, column_name_time[0]))
                else:
                    st.plotly_chart(display_plots_no_time(file, list_of_parameters))

            if choice_plots == "SHARED X-AXIS ONLY (Subplots)":

                st.subheader("Display Data based on the selected parameters")
                st.markdown("* **Plot with shared x-axis only**")
                st.info("Note: If a time object exists on the sidebar, if you select it then time will be plotted on x-axis")

                if "time_option" in globals() and time_option:
                    st.plotly_chart(display_subplots_with_time(file, list_of_parameters, column_name_time[0]))
                else:
                    st.plotly_chart(display_subplots_no_time(file, list_of_parameters))

            if choice_plots == "ONE FIGURE FOR EACH PARAMETER":

                st.subheader("Display Data based on the selected parameters")
                st.markdown("* **One figure for each parameter**")
                st.info("Note: If a time object exists on the sidebar, if you select it then time will be plotted on x-axis")
                if "time_option" in globals() and time_option:
                    display_single_plots_with_time(file, list_of_parameters, column_name_time[0])
                else:
                    display_single_plots_no_time(file, list_of_parameters)


st.markdown('<style>body{background-color: #d4ffff;}</style>',unsafe_allow_html=True)

hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)




