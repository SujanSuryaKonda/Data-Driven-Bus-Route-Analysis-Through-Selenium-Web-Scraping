# Data-Driven-Bus-Route-Analysis-Through-Selenium-Web-Scraping
## 📖 Project Overview

This project provides a web application for analyzing bus routes through data collected via Selenium web scraping. The application allows users to filter and sort bus route information based on various criteria, including route names, prices, star ratings, and bus types.

## 🚀 Features

- **Route Name Filtering**: Search for bus routes starting with a specific letter.
- **Price Sorting**: Sort bus routes by price in ascending or descending order.
- **Dynamic Filtering**: Filter results by star ratings and bus types.
- **User-Friendly Interface**: Built using Streamlit for an interactive experience.

## 🛠️ Technologies Used

- **Python**: Programming language for the application.
- **Streamlit**: Framework for creating the web application.
- **Pandas**: Library for data manipulation and analysis.
- **PyMySQL**: Library for connecting to MySQL database.
- **Selenium**: Tool for web scraping (assumed to be used in data collection).

## 🔗 Getting Started

### Prerequisites

- Python 3.x installed on your machine.
- MySQL server running and accessible.
- Required Python libraries (install via pip):
-Set up the MySQL database:
-Create a database named redbus.
-Create a table bus_routes with the appropriate schema to store bus route data.
```bash
pip install streamlit pandas pymysql selenium

def get_connection():    
    return pymysql.connect(host='127.0.0.1', user='your_username', passwd='your_password', database='redbus')
