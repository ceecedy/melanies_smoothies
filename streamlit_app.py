# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
        Choose the fruits you want in your custom Smoothie!.
    """
)

# Name box 
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
# will get a data from the database with the use of snowpark. 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

# Multi-select 
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections = 5
)

# check if the ingredients_list has values 
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        # increment the values to the ingredient_strings.
        ingredients_string += fruit_chosen + ' '
        # request from api
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        # display the response on api request with its subheader.
        st.subheader(fruit_chosen + ' Nutrition Information')
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # output the ingredients_string after incrementing 
    st.write(ingredients_string)

    # SQL script after building the ingredients string 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

    # create a button 
    time_to_insert = st.button(
        'Submit Button'
    )
    # if time to insert was clicked 
    if time_to_insert:
        # function to insert sql script. 
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!',  icon="✅")









