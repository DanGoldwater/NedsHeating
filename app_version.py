from email.mime import base
import math
import pandas as pd
import streamlit as st
import altair as alt
import plotly

import house_rent_functions
import further_functions
import housemates_and_settings

slide_step = 0.05
st.title('Rent Scaling for Neds')

intro_area = st.container()
parameters_area = st.container()
due_area = st.container()

dictsa = {'aa': 44}

with intro_area:
    st.subheader('This is to scale the rents')

with parameters_area:
    st.subheader('This is where we set our parameters')
    rent_col, bills_col = st.columns(2)
    rent_col.subheader('Parameters for the rent')
    RENT_ALPHA = rent_col.slider('alpha', 0.0, 1.0, step=slide_step)
    RENT_BETA = rent_col.slider('beta', 0.0, 1.0)
    RENT_GAMMA = rent_col.slider('gamma', 0.0, 100.0, step=slide_step, value=25.0)
    MAX_RATIO = rent_col.slider('maximum ratio', 1.0, 2.0, step=slide_step)

    bills_col.subheader('Parameters for the bills')
    BILLS_ALPHA = bills_col.slider('How progressive the scaling is', 0.0, 2.0, step=slide_step)
    BILLS_BETA = bills_col.slider('How big the scaling is', 0.0, 5.0, step=slide_step)
    
    RENT_OUTGOING = st.number_input(label='Rent outgoing per month', value=2000)
    BILLS_OUTGOING = st.number_input(label='Bills outgoing per month', value=1593)
    BUFFER_OUTGOING = st.number_input(label='buffer', min_value=0.0, max_value=.5, step=slide_step)
    st.write(f'Bills gathered per month = {BILLS_OUTGOING * (1 + BUFFER_OUTGOING):.2f}, for a profit of {BILLS_OUTGOING * BUFFER_OUTGOING:.2f}')
    
def get_excess(savings, adjusted_income):
    savings_excess = max(savings - housemates_and_settings.savings_threshold, 0) / 5
    income_excess = max((adjusted_income )  - housemates_and_settings.income_threshold, 0)
    return max((savings_excess + income_excess) / 1000, 0)

def get_rent(excess): 
    extra = RENT_ALPHA * math.exp(RENT_BETA * excess) + RENT_GAMMA * excess 
    if extra > base_rent * (MAX_RATIO - 1):
        extra = base_rent * (MAX_RATIO - 1)
    rent = base_rent + extra
    return round(rent)
    
def get_extra_bills(excess):
    return BILLS_ALPHA  *  math.exp(BILLS_BETA) * excess
    

with due_area:
    base_rent = RENT_OUTGOING / len(housemates_and_settings.Housemates_2022)
    st.write(f'Base rent = {base_rent:.2f}')
    df = pd.DataFrame(housemates_and_settings.Housemates_2022)
    df['excess'] = df.apply(lambda x: get_excess(savings=x['savings'], adjusted_income=x['adjusted_income']), axis=1)
    TOTAL_EXCESS = df['excess'].sum()
    df['rent'] = df.apply(lambda x: get_rent(excess=x['excess']), axis=1)
    df['bills_extra'] = df.apply(lambda x: get_extra_bills(excess=x['excess']), axis=1)
    B_0 = (BILLS_OUTGOING - df['bills_extra'].sum()) / len(housemates_and_settings.Housemates_2022)
    st.write(f'Base Bills are {B_0:.2f}')
    df['bills'] = df['bills_extra'] + B_0
    df['outgoings'] = df['bills'] + df['rent']
    # df.drop(['bills_extra'])
    
    RENT_PROFIT = max(0, (df['rent'].sum() - RENT_OUTGOING) * 12)
    
    st.dataframe(df)
                #  [['name', 'bills','rent','outgoings']])
    # df.head()
    
                                   
    
    
    
# form_bit = st.empty()
if 'housemates' not in st.session_state:
    st.session_state['housemates'] = []
with st.sidebar:
    st.metric(label='Rent profit per year', value=RENT_PROFIT)
    st.metric(label='Lowest outgoings per month', value=round(df['outgoings'].min()))
    st.metric(label='Highest Outgoings per month', value=round(df['outgoings'].max()))
    st.subheader('Ratios; maximum to minimum')
    st.metric(label='Total', value=round(df['outgoings'].max()/df['outgoings'].min(), 2) )
    st.metric(label='Rent', value=round(df['rent'].max()/df['rent'].min(), 3) )
    st.metric(label='Bills', value=round(df['bills'].max()/df['bills'].min(), 3) )

    


chart = alt.Chart(df[['name','rent','bills']]).mark_bar().encode(
    x='name',
    y='rent'
)

chart2 = plotly.graph_objs.Figure(
    data=[
     plotly.graph_objs.Bar(
         name='rent',
         x=df['name'],
         y=df['rent'],
         offsetgroup=0
     ),
     plotly.graph_objs.Bar(
         name='bills',
         x=df['name'],
         y=df['bills'],
         offsetgroup=1
     )
     ],
    
)

# chart = alt.Chart(df, title='Outgoings').mark_bar(
#     # opacity=0.3,
#     ).encode(
#     column = alt.Column('variable'),
#     x = alt.X('name:O'),
#     y = alt.Y('rent:Q'),
    # color = alt.Color('variable:N')
# )
    # .properties(width= 400, height = 400)

st.plotly_chart(chart2, use_container_width=True)


# st.altair_chart(chart, use_container_width=True)
# st.bar_chart(
    # data=df.set_index('name')[['rent', 'bills']]
    # x='name',
    # y=('rent', 'bills')
    # )
    
    # st.write(st.session_state.housemates)
with st.expander('add housemate'):
    # with form_bit.container():
# with st.button('add housemate'):
    disp = st.number_input('Disposable income per calendar month')
    savings = st.number_input('Housemate Savings')
    name = st.text_input('Name')
    if st.button('Add housemate'):
        st.session_state.housemates += [
            {'disp': disp,
                'savings': savings,
                'name': name}
        ]
        # st.sidebar.write(housemates)
            
if st.button('show'):
    st.write(st.session_state.housemates)