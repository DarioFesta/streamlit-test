import streamlit as st
import pandas as pd
import random
import base64
from plotly.subplots import make_subplots
import plotly.express as px
#import numpy as np
import plotly.graph_objects as go


#st.set_page_config(layout="wide")
st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
st.title('Data Plots / Stats')
st.subheader('Create plots and show main stats for each parameter')



