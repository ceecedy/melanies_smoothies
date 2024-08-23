# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col 

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
        Choose the fruits you want in your custom Smoothie!.
    """
)

cnx = st.connection('snowflake')
session = cnx.session()
# will get a data from the database with the use of snowpark. 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Multi-select 
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe
)

# check if the ingredients_list has values 
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        # increment the values to the ingredient_strings.
        ingredients_string += fruit_chosen + ' '

    # output the ingredients_string after incrementing 
    st.write(ingredients_string)

    # SQL script after building the ingredients string 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    # create a button 
    time_to_insert = st.button(
        'Submit Button'
    )
    # if time to insert was clicked 
    if time_to_insert:
        # function to insert sql script. 
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    # st.write(my_insert_stmt)

    # before inserting the sql script. 
    # if ingredients_string: 
    #     # function to insert sql script. 
    #     session.sql(my_insert_stmt).collect()
    #     st.success('Your Smoothie is ordered!', icon="✅")









