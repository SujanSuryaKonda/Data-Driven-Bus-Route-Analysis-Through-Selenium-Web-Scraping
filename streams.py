import streamlit as st
import pymysql
import pandas as pd

# Set page config for a better layout
st.set_page_config(page_title='Bus Route Analysis', layout='wide')

# Define a function to get a MySQL database connection
def get_connection():    
    return pymysql.connect(host='127.0.0.1', user='root', passwd='Sujan#12345', database='redbus')

# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_route_names(connection, starting_letter):
    query = f"SELECT DISTINCT Route_Name FROM bus_routes WHERE Route_Name LIKE '{starting_letter}%' ORDER BY Route_Name"
    route_names = pd.read_sql(query, connection)['Route_Name'].tolist()
    return route_names

# Function to fetch data from MySQL based on selected Route_Name and price sort order
def fetch_data(connection, route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"SELECT * FROM bus_routes WHERE Route_Name = %s ORDER BY Star_Rating DESC, Price {price_sort_order_sql}"
    df = pd.read_sql(query, connection, params=(route_name,))
    df['Price'] = pd.to_numeric(df['Price'].str.replace('INR ', '').str.replace(',', ''), errors='coerce')
    return df

# Function to filter data based on Star_Rating and Bus_Type
def filter_data(df, star_ratings, bus_types):
    filtered_df = df[df['Star_Rating'].isin(star_ratings) & df['Bus_Type'].isin(bus_types)]
    return filtered_df

# Main Streamlit app
def main():
    # Header and description
    st.title('🚍 Data-Driven Bus Route Analysis Through Selenium Web Scraping')
    st.markdown("""
    Explore bus routes and their details based on user-defined criteria. 
    Filter routes by starting letter, sort by price, and filter based on star ratings and bus types.
    """)

    # Create a sidebar for filtering options
    st.sidebar.header('Filter Options')
    starting_letter = st.sidebar.text_input('Enter starting letter of Route Name', 'A').upper()

    connection = get_connection()

    try:
        # Fetch route names starting with the specified letter
        if starting_letter:
            route_names = fetch_route_names(connection, starting_letter)

            if route_names:
                selected_route = st.sidebar.selectbox('Select Route Name', route_names)

                if selected_route:
                    price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                    # Fetch data based on selected Route_Name and price sort order
                    data = fetch_data(connection, selected_route,price_sort_order)

                    if not data.empty:
                        st.subheader(f"📊 Data for Route: **{selected_route}**")
                        st.dataframe(data.style.set_table_attributes('style="background-color: #f9f9f9; border-radius: 5px;"').set_properties(**{
                            'color': 'black', 
                            'background-color': '#e6f7ff', 
                            'border': '1px solid #007BFF',
                            'border-radius': '5px'
                        }))

                        # Filter by Star_Rating and Bus_Type
                        star_ratings = data['Star_Rating'].unique().tolist()
                        selected_ratings = st.multiselect('Filter by Star Rating', star_ratings, default=star_ratings)

                        bus_types = data['Bus_Type'].unique().tolist()
                        selected_bus_types = st.multiselect('Filter by Bus Type', bus_types, default=bus_types)

                        if selected_ratings or selected_bus_types:
                            filtered_data = filter_data(data, selected_ratings, selected_bus_types)
                            if not filtered_data.empty:
                                st.subheader("🔍 Filtered Results")
                                st.dataframe(filtered_data.style.set_table_attributes('style="background-color: #f9f9f9; border-radius: 5px;"').set_properties(**{
                                    'color': 'black', 
                                    'background-color': '#e6f7ff', 
                                    'border': '1px solid #007BFF',
                                    'border-radius': '5px'
                                }))
                            else:
                                st.warning("No results found with the selected filters.")
                    else:
                        st.error(f"No data found for Route: {selected_route} with the specified price sort order.")
            else:
                st.warning("No routes found starting with the specified letter.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
