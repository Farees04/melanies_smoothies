# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  


# Write directly to the app
st.title(f":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose upto 5 ingradients: ', my_dataframe
    , max_selections=5
    )
name_on_order = st.text_input('Name on Smoothie: ')
if ingredient_list:
          
     ingredients_string = ''
     for fruit_chosen in ingredient_list:
         ingredients_string += fruit_chosen + ' '
         st.subheader(fruit_chosen + 'Nutrition Information')
         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
         sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
       

     # st.write(ingredient_list)    

# insert into smoothies.public.orders values ('Guava', 'ABC');
     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+ name_on_order + """')"""
     st.write(ingredient_list) 
     time_to_insert = st.button('Submit Order')
     # st.text(smoothiefroot_response.json())

     if time_to_insert:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")
