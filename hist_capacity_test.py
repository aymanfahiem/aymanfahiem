
from operator import index
from turtle import width
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import os
import numpy as np
import pandas as pd
import datetime
import time
from sklearn import linear_model 
from PIL import Image

## page title 
st.set_page_config(page_title='PlantWin', page_icon=':bar_chart:',layout='wide',)

## decrease header of main page to 1.2 rem
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            #MainMenu:after {
                content:'Setting'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
            footer {visibility: hidden;}
            footer:after {
                content:'Copywrite EPROM PRT @ 2022'; 
                visibility: visible;
                display: block;
                position: relative;
            </style>
        
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:0.5rem;}</style>', unsafe_allow_html=True)
st.markdown('<style>.css-hxt7ib{padding-top:0rem;}</style>', unsafe_allow_html=True)

dirname = os.path.dirname(__file__)
left, mid, right = st.columns(3)
logo=Image.open(dirname+'PlanTwin_Logo.png')
# eprom = Image.open(dirname+'/epromlogo.png')
#erc = Image.open(dirname+'/erc.jpg')
col1,col2,col3=st.sidebar.columns(3)
with col1:
    st.image(logo)

def days_ago(days):
    if days == None:
        return datetime.date(day=1, month=6, year=2022),
    return datetime.date.today() - datetime.timedelta(days=days)

date_options = {
    "Today":0,
    "1 day ago": 1,
    "2 days ago": 2,
    "1 week ago": 7,
    "2 weeks ago": 14,
    "1 month ago": 30,
    "3 months ago": 90,
    "6 months ago": 180,
    "1 year ago": 365,
    }


left, right = st.sidebar.columns(2)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
r_date=st.sidebar.checkbox('Relative date')
if r_date:
        start_date = days_ago(
        date_options[
            st.sidebar.selectbox("Start date", list(date_options.keys()),index=1)
                    ])
        end_date = days_ago(
        date_options[
            st.sidebar.selectbox("End date", list(date_options.keys()))
                    ])
else:
        with left:
            start_date = st.sidebar.date_input('Select Start date', yesterday)
        with right:
            end_date = st.sidebar.date_input('Select End date', today)

if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
        st.sidebar.error('Error: End date must be after start date.')


# def hist_cap():
co1,co2=st.columns(2)
r1= st.sidebar.selectbox('Select Dependent Unit' ,('NHT', 'CCR', 'DHT', 'HCU', 'HPU', 'VDU', 'DCU', 'DEU', 'SWS-1', 'SWS-2',
                        'OFF Gas', 'ARU-1', 'ARU-2', 'SRU-1', 'SRU-2', 'SRU-3'),index=4)
col1,col2,col3=st.columns(3)


# sel=col1.radio('Capacity Filteration Criteria:', ('Lower','Higher','Equal to'), horizontal=True)
sel=col1.radio('Capacity Filteration Criteria:', ('Lower','Higher'), horizontal=True)
clicksubmit=col3.button('GetData')

c1,c2,c3=st.columns(3)
f1 = c1.slider('NHT', 0, 120, 100)
f2 = c2.slider('CCR', 0, 120, 100)
f3 = c3.slider('DHT', 0, 120, 100)
f4 = c1.slider('HCU', 0, 120, 100)
f5 = c2.slider('HPU', 0, 120, 100)
f6 = c3.slider('VDU', 0, 120, 100)
f7 = c1.slider('DCU', 0, 120, 100)


# filt=
@st.cache
def retrieving_two_years_data():
        dirname = os.path.dirname(__file__)
        hist_ca=os.path.join(dirname,r'his_capacity.xlsx')
        df=pd.read_excel(hist_ca, index_col='Date')
        num = df._get_numeric_data()
        num[num < 50] = 0
        unit_desc = ['NHT', 'CCR', 'DHT', 'HCU', 'HPU', 'VDU', 'DCU', 'DEU', 'SWS-1', 'SWS-2',
                        'OFF Gas', 'ARU-1', 'ARU-2', 'SRU-1', 'SRU-2', 'SRU-3','Boilers Load','Cooling Water','Flare',
                        'N2','Fuel Gas','TOTAL POWER CONSUMPTION','Natural Gas','Specific Energy Supply (Gcal/ton)',
                        'Total Energy Supply (Gcal/h)','Total NG Fuel','Specific Energy Value','Total Energy Value']  # list of unit names
                # unit_desc['unit']=unit_desc['DESCRIPTION'].apply(lambda x: x.)]=unit_desc['DESCRIPTION'].apply(lambda x: x.)
        df.columns = unit_desc
        return df

df=retrieving_two_years_data()
df_new=df.drop(r1, axis=1)
X=df.drop(r1, axis=1)
y=df[r1]

if clicksubmit==True:
        
        
        
        independent_unit=['NHT', 'CCR', 'DHT', 'HCU', 'HPU', 'VDU', 'DCU']
        predicted_values=[f1,f2,f3,f4,f5,f6,f7]
        #remove selected dependent unit from independent units
        if r1 in independent_unit:
                del predicted_values[independent_unit.index(r1)]
                independent_unit.remove(r1)
        X=df[independent_unit]
        y=df[[r1]]
        regr = linear_model.LinearRegression()
        regr.fit(X.values, y)
        predicted_unit = regr.predict([predicted_values])
        expected_unit_capacity=predicted_unit[0][0]
        st.markdown(f'**{r1} Summary:**')
        st.markdown(f'* Expected **{r1}** value at above conditions is around **{expected_unit_capacity:.2f}**')
        if sel =='Lower':
                df_selection=df[(df['NHT']<=f1 ) & (df['CCR']<=f2) & (df['DHT']<=f3) & (df['HCU'] <=f4) &
                (df['HPU']<=f5) & (df['VDU']<=f6) & (df['DCU']<=f7)]

        if sel =='Higher':
                df_selection=df[(df['NHT']>=f1 ) & (df['CCR']>=f2) & (df['DHT']>=f3) & (df['HCU'] >=f4) &
                (df['HPU']>=f5) & (df['VDU']>=f6) & (df['DCU']>=f7)]
        # if sel =='Equal to':
        #         df_selection=df[(df['NHT']>=0.95*f1) &(df['NHT']<=1.05*f1) & (df['CCR']==f2) & (df['DHT']==f3) & (df['HCU'] ==f4) &
                # (df['HPU']==f5) & (df['VDU']==f6) & (df['DCU']==f7)]
        a= df_selection[df_selection[r1]>0][r1]
        a_min=a.min()
        a_max=a.max()
        b_min=df_selection[df_selection[r1]==a_min].index[0]
        b_max=df_selection[df_selection[r1]==a_max].index[0]
        
        # st.markdown(f'* {r1} average capacity was {a.mean():.2f}')
        st.markdown(f'* **{r1}** minimum value was **{a_min}** at {b_min: %Y-%m-%d}')
        st.markdown(f'* **{r1}** maximum value was **{a_max}** at {b_max: %Y-%m-%d}')
        st.table(df_selection[df_selection[r1]>0][r1].describe())

        try:
                fig= px.scatter(df_selection, x=df_selection.index, y=df_selection.columns, title="Unit Capacity")
                fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Capacity vol%"
                        )
                fig1=px.histogram(df_selection,x=r1,title=f'{r1} operation Histogram at above conditions')
                st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig1, use_container_width=True)
        except:
                st.warning('Please try another conditions')
        # st.write(f'the selected capacities were achieved on {df_selection.index}')
        # st.table(df_selection.head(5))
        gb = GridOptionsBuilder.from_dataframe(df_selection)

        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar
        gb.configure_selection('multiple', use_checkbox=False,
                                groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
        gridOptions = gb.build()

        grid_response = AgGrid(
        df_selection,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='blue',  # Add theme color to the table
        enable_enterprise_modules=True,
        height=500,
        reload_data=True
        )

        # disply_df = grid_response['data']
        selected = grid_response['selected_rows']
        # for kpi in selected:
        #     kpis.drop(kpi, axis=0, inplace=True)

        df = pd.DataFrame(selected)  # Pass the selected rows to a new dataframe df
        
        ss = st.session_state
        ss.get(df)
        


st.info('The analysis is based on historian data and not consider catalyst deactivation and hydrogen demand variation')





