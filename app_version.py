import streamlit as st

import house_rent_functions
import further_functions
slide_step = 0.1
st.title('Rent Scaling for Neds')

intro_area = st.container()
parameters_area = st.container()

dictsa = {'aa': 44}

with intro_area:
    st.subheader('This is to scale the rents')

with parameters_area:
    st.subheader('This is where we set our parameters')
    rent_col, bills_col = st.columns(2)
    rent_col.subheader('Parameters for the rent')
    rent_col.slider('alpha', 0.0, 1.0, step=slide_step)
    rent_col.slider('beta', 0.0, 1.0)
    rent_col.slider('gamma', 0.0, 1.0, step=slide_step)

    bills_col.subheader('Parameters for the bills')
    bills_col.slider('How progressive the scaling is', 0.0, 2.0, step=slide_step)
    bills_col.slider('How big the scaling is', 0.0, 1.0, step=slide_step)
    
# form_bit = st.empty()
if 'housemates' not in st.session_state:
    st.session_state['housemates'] = []
with st.sidebar:
    st.write(st.session_state.housemates)
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