# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title("Custom Smoothie App")
st.write(
    """Choose the fruits you want in your smoothie
    """
)

#option = st.selectbox (
   # 'What is your favorite fruit?',
   # ('Banana', 'Strawberries', 'Peaches')
#)

#st.write('You favorite fruit is:', option)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
)

#st.dataframe(data=my_dataframe, use_container_width=True)

#if ingredients_list:
ingredients_string = ''

for fruit_chosen in ingredients_list: 
    ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

time_to_insert = st.button("Submit Order")

#st.write(my_insert_stmt)
#if ingredients_string:
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!')
