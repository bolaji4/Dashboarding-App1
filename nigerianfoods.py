import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt




print("installation is ready.")

# get the data

#@st.cache # it save the data to the browser.
def get_data():
    url = './datasets/nigeria_food_prices.csv'
    df = pd.read_csv(url)
    cols_to_drop = ['adm0_id','adm1_id','mkt_id',
                'cm_id','cur_id','pt_id','um_id',
                'mp_commoditysource']
    df = df.drop(columns=cols_to_drop)
    new_names = {'adm0_name': 'country',
            'adm1_name': 'state',
            'cm_name': 'produce',
            'mp_month': 'month',
            'mp_year': 'year',
            'mp_price': 'price',
            'pt_name': 'market_type',
            'um_name': 'quantity',
            'mkt_name': 'market'}
    df = df.rename(columns=new_names)
    df = df.drop(columns=df.columns[0])
    return df

# display the result using python
print(get_data())

#title
st.write("# Nigeria Food Prices App")

# display the data using streamlit
#df = get_data()

#df # magic command and is actually == st.write(df)



#to clean the data now we will need to take it to jupiterlab and reajust it
# sidebar
with st.container():
    try:
        st.sidebar.header("User input controls") # what ever 
        df = get_data()
        states = st.sidebar.multiselect("Choose state",df.state.unique(),"Abia") #,#"Abia" you can put a defult value and u must make sure it is in the list
        produce = st.sidebar.selectbox("Choose produce",df.produce.unique())
    
    # error checking
        if not states:
            st.sidebar.error("Please select at least one State")
        else:
            for i, index in enumerate(states):
                data = df[df.state == states[i]]
                st.write(f"### Prices of Goods in {states[i]} Markets")
                st.write(data.head(60))
      #pass .. this is use to pass in function if to show if not select
    # using the data let's build a line chart
    # we build a pivot table
                pvt = pd.pivot_table(data, index=['state','market','produce','year'],values=['price'], aggfunc='mean')
                pvt_df = pvt.reset_index()
                pvt_df
                selected_state = states[i]
                st.write(selected_state)
                pvt_df = pvt_df[pvt_df['state'] == selected_state]
    # selected product
                selected_produce = produce
                pvt_df = pvt_df[pvt_df["produce"] == selected_produce]
    #line chart
                chart = alt.Chart(pvt_df).mark_line().encode(
                x='year', y='price', tooltip=['market','price'])
                st.write(f"### Price Chart {selected_produce} in {selected_state}")
                st.altair_chart(chart, use_container_width=True)
    # area chart for different markets
                                
                chart = alt.Chart(pvt_df).mark_area().encode(
                x='year', y='price', tooltip=['market','price'])
                st.write(f"### Price Chart {selected_produce} in {selected_state}")
                st.altair_chart(chart, use_container_width=True)
    # area chart with different market
                chart = alt.Chart(pvt_df).mark_area().encode(
                x='year', color='market', y='price', tooltip=['market','price']).interactive()
                st.write(f"### Price Chart {selected_produce} in {selected_state}")
                st.altair_chart(chart, use_container_width=True)
                st.write("-----")
    except RuntimeError as e: # try and except
        st.error(e.reason)
    #st.error("""Error: %s""" %error.reason)
    #st.error(""" ** Error ** """)