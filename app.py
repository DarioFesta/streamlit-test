import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
#import modin.pandas as pd
import random
import base64
from plotly.subplots import make_subplots
import plotly.express as px
#import numpy as np
import plotly.graph_objects as go




@st.cache(allow_output_mutation=True)
def load_multiple_csv_files_horizontally(uploaded_csv_files):
    for file in uploaded_csv_files:
        file.seek(0)
        uploaded_data_read = (pd.read_csv(file) for file in uploaded_csv_files)
        combined_csv_files = pd.concat(uploaded_data_read, axis = 1)
        return combined_csv_files

@st.cache(allow_output_mutation=True)
def load_multiple_csv_files_vertically(uploaded_csv_files):
    for file in uploaded_csv_files:
        file.seek(0)
        uploaded_data_read = (pd.read_csv(file) for file in uploaded_csv_files)
        combined_csv_files = pd.concat(uploaded_data_read, axis = 0)
        return combined_csv_files

def file_download_stats(df, parameters):
    try:
        time_column = [s for s in parameters if 'time' in s.lower()][0]
        parameters.remove(time_column)

    except:
        pass

    finally:
        if parameters:
            stats_raw = df[parameters].agg(["min", "max", "mean", "median", "std"])
            stats = stats_raw.T
            csv = stats.to_csv(index=True)
            b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
            href = f'<a href="data:file/csv;base64,{b64}" download="stats.csv">Download CSV File with Stats</a>'
            return href
        else:
            # in case only the "time parameter" is selected we don't need to show stats
            return None

def show_stats(df, parameters):
    try:
        time_column = [s for s in parameters if 'time' in s.lower()][0]
        parameters.remove(time_column)

    except:
        pass

    finally:
        if parameters:
            stats = df[parameters].agg(["min", "max", "mean", "median", "std"])
            return stats
        else:
            # in case only the "time parameter" is selected we don't need to show stats
            return None

def file_download_raw_data(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="raw_data.csv">Download CSV File with Raw Data</a>'
    return href

#@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def display_plots_no_time(df_csv, parameters):
    fig = go.Figure()
    for param in parameters:
        fig.add_trace(go.Scatter(y = df_csv[param], name=param))
    fig.update_layout(legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"),
            plot_bgcolor='rgb(255, 255, 251)',                #title_text='Plot'
            xaxis=dict(
            linecolor="#BCCCDC",
            showspikes=True,
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across"))
    fig.update_xaxes(title_text='Samples', showgrid=True, gridwidth=0.01, gridcolor='LightPink',
        zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.01, gridcolor='LightPink',
        zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    #st.plotly_chart(fig)
    return fig


def display_plots_with_time(df_csv, parameters, column_name_time = None):
    # dorp duplicate columns (same name) - it happens when concatenating multipe dataframes with the same time column
    df_csv = df_csv.loc[:, ~df_csv.columns.duplicated()]
    if df_csv[column_name_time].dtypes == 'object':
        df_csv[column_name_time] =  pd.to_datetime(df_csv[column_name_time],
         format = '%d-%m-%Y %H-%M-%S', infer_datetime_format = True, dayfirst = True)
    else:
    # convert the column with time info in a datetime object
        df_csv[column_name_time] =  pd.to_datetime(df_csv[column_name_time], unit = 's', infer_datetime_format = True)
    fig = go.Figure()
    for param in parameters:
        fig.add_trace(go.Scatter(x = df_csv[column_name_time], y = df_csv[param], name=param))
    fig.update_layout(legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"),
            plot_bgcolor='rgb(255, 255, 251)',                #title_text='Plot'
            xaxis=dict(
            linecolor="#BCCCDC",
            showspikes=True,
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across"))
    fig.update_xaxes(title_text='Time', showgrid=True, gridwidth=0.01, gridcolor='LightPink',
        zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.01, gridcolor='LightPink',
        zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    #st.plotly_chart(fig)
    return fig

#@st.cache(suppress_st_warning=True)
def display_subplots_no_time(df_csv, parameters):
    rows = len(parameters)
    fig = make_subplots(rows = rows,  cols = 1, shared_xaxes = True, subplot_titles = parameters)
    for param in parameters:
        fig.add_trace(go.Scatter(y = df_csv[param], name=param), row=parameters.index(param) +1, col=1)
        fig.update_layout(showlegend= False, plot_bgcolor='rgb(255, 255, 255)')
        fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    #st.plotly_chart(fig)
    return fig

def display_subplots_with_time(df_csv, parameters, column_name_time = None):
    df_csv = df_csv.loc[:, ~df_csv.columns.duplicated()]
    # convert the column with time info in a datetime object
    if df_csv[column_name_time].dtypes == 'object':
        df_csv[column_name_time] =  pd.to_datetime(df_csv[column_name_time],
         format = '%d-%m-%Y %H-%M-%S', infer_datetime_format = True, dayfirst = True)
    else:
    # convert the column with time info in a datetime object
        df_csv[column_name_time] =  pd.to_datetime(df_csv[column_name_time], unit = 's', infer_datetime_format = True)
    rows = len(parameters)
    fig = make_subplots(rows = rows,  cols = 1, shared_xaxes = True, subplot_titles = parameters)
    for param in parameters:
        fig.add_trace(go.Scatter(x =df_csv[column_name_time], y = df_csv[param], name=param),
                        row=parameters.index(param) + 1, col=1)
        fig.update_layout(showlegend= False, plot_bgcolor='rgb(255, 255, 255)')
        fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    #st.plotly_chart(fig)
    return fig


#@st.cache(suppress_st_warning=True)
def display_single_plots_no_time(df_csv, parameters):

    for param in parameters:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y = df_csv[param], name= param,
                                    line=dict(color=random.choice(px.colors.qualitative.Plotly))))
        fig.update_layout(showlegend= True, plot_bgcolor='White',
                            legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"))
        fig.update_xaxes(title_text='Samples',showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
                            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
                            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        st.plotly_chart(fig)


def display_single_plots_with_time(df_csv, parameters, column_name_time = None):
    df_csv = df_csv.loc[:, ~df_csv.columns.duplicated()]
    if df_csv[column_name_time].dtypes == 'object':
        df_csv[column_name_time] =  pd.to_datetime(df_csv[column_name_time],
         format = '%d-%m-%Y %H-%M-%S', infer_datetime_format = True, dayfirst = True)
    else:
    # convert the column with time info in a datetime object
        df_csv[column_name_time] =  pd.to_datetime(df_csv[column_name_time], unit = 's', infer_datetime_format = True)
    for param in parameters:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df_csv[column_name_time], y = df_csv[param], name= param,
                                    line=dict(color=random.choice(px.colors.qualitative.Plotly))))
        fig.update_layout(showlegend= True, plot_bgcolor='White',
                            legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"))
        fig.update_xaxes(title_text='Time',showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
                            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
                            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        st.plotly_chart(fig)

def display_time(df_csv, column_name_time = None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y = df_csv[column_name_time], name= column_name_time))
    fig.update_layout(showlegend= True, plot_bgcolor='White',
                            legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"))
    fig.update_xaxes(title_text='Samples',showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
                            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
                            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    return fig


def data_info(combined_csv_files):
    st.write('Dataset size (rows, columns) = ', combined_csv_files.shape)
    st.markdown('👈 **Select parameters to start the analysis**')
    param_names = combined_csv_files.columns.tolist()
    if any(s for s in param_names if 'time' in s.lower()):
        #column_name_time = "".join(s for s in param_names if 'time' in s.lower())
        column_name_time = [s for s in param_names if 'time' in s.lower()]
        for time_column in column_name_time:
            param_names.remove(time_column)
        st.sidebar.title("List of Parameters")
        list_of_parameters = st.sidebar.multiselect(label = "Parameters to plot", options = param_names)
        st.sidebar.title("Time object found")
        time_option = st.sidebar.checkbox(f"{column_name_time[0]}")
        #time_parameters = st.sidebar.multiselect(label = "Time object for x-axis", options = column_name_time)
    else:
        st.sidebar.title("List of Parameters")
        list_of_parameters = st.sidebar.multiselect(label = "Parameters to plot", options = param_names)
    return  list_of_parameters, time_option, column_name_time


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




