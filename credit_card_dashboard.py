import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ------------------ Sample Data Loading ------------------

def load_data():
    data = {
        "Date": [
            "2023-01-15", "2023-01-20", "2023-02-05", "2023-02-18", 
            "2023-03-01", "2023-03-15", "2023-03-25", "2023-04-10", 
            "2023-05-05", "2023-05-15", "2023-06-01", "2023-06-18",
            "2024-01-10", "2024-01-25", "2024-02-08", "2024-03-18", 
            "2024-04-05", "2024-05-25", "2024-06-12", "2024-07-01"
        ],
        "Merchant": [
            "Amazon", "Uber", "Netflix", "Dominos", "Gym", "Amazon", "Uber", "Zomato", 
            "Starbucks", "Uber", "Spotify", "Amazon", "Flipkart", "Big Bazaar", "Hotstar", 
            "Pizza Hut", "Decathlon", "Swiggy", "MakeMyTrip", "BookMyShow"
        ],
        "Amount": [100, 50, 15, 20, 50, 200, 40, 60, 10, 45, 7, 300, 150, 100, 12, 30, 80, 55, 500, 25],
        "Category": [
            "Shopping", "Travel", "Entertainment", "Food", "Fitness", "Shopping", "Travel", "Food", 
            "Food", "Travel", "Entertainment", "Shopping", "Shopping", "Groceries", "Entertainment", 
            "Food", "Fitness", "Food", "Travel", "Entertainment"
        ]
    }
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# ------------------ Data Aggregation ------------------

def aggregate_data(df):
    df['Month'] = df['Date'].dt.to_period('M')
    df['Year'] = df['Date'].dt.year
    monthly_spend = df.groupby('Month')['Amount'].sum().reset_index()
    yearly_spend = df.groupby('Year')['Amount'].sum().reset_index()
    category_spend = df.groupby('Category')['Amount'].sum().reset_index()
    return monthly_spend, yearly_spend, category_spend

# ------------------ Visualization Functions ------------------

def plot_monthly_spending(monthly_spend):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(monthly_spend['Month'].astype(str), monthly_spend['Amount'], marker='o', color='skyblue')
    ax.set_title('Monthly Spending')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_yearly_spending(yearly_spend):
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(yearly_spend['Year'], yearly_spend['Amount'], color=['orange', 'teal'])
    ax.set_title('Yearly Spending')
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount')
    ax.set_xticks(yearly_spend['Year'])
    ax.set_xticklabels(yearly_spend['Year'].astype(int))
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 10, f"{yval}", ha="center", va="bottom")
    st.pyplot(fig)

def display_category_tables(df):
    for category, group in df.groupby("Category"):
        st.write(f"### {category} Spending")
        st.dataframe(group[['Date', 'Merchant', 'Amount']])

# ------------------ Navigation Function ------------------

def navigate_to_section(selected_section, df, monthly_spend, yearly_spend):
    if selected_section == "Overview":
        st.subheader("Overview of Your Spending")
        st.write("This dashboard provides insights into your credit card spending habits.")
    elif selected_section == "Monthly Spending":
        st.subheader("📅 Monthly Spending")
        plot_monthly_spending(monthly_spend)
    elif selected_section == "Yearly Spending":
        st.subheader("📆 Yearly Spending")
        plot_yearly_spending(yearly_spend)
    elif selected_section == "Category Spending":
        st.subheader("📋 Spending by Individual Categories")
        display_category_tables(df)
    elif selected_section == "Raw Data":
        st.subheader("📄 Raw Data")
        st.dataframe(df)
   

# ------------------ Streamlit UI ------------------

def main():
    st.set_page_config(page_title="Spending Dashboard", layout="wide")
    st.markdown("<style>.sidebar .sidebar-content {width: 230px;}</style>", unsafe_allow_html=True)

    st.title("💳 Credit Card Spending Dashboard")

    # Sidebar navigation
    menu = ["Overview", "Monthly Spending", "Yearly Spending", "Category Spending", "Raw Data"]
    choice = st.sidebar.radio("Navigate to", menu)

    st.sidebar.header("Upload Your Credit Card Data")
    
    # Upload data
    uploaded_file = st.sidebar.file_uploader("Upload a file (CSV or Excel)", type=["csv", "xlsx"])
    
    # Load sample data or user-uploaded data
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is parsed correctly
    else:
        st.info("No file uploaded. Using sample data.")
        df = load_data()

    # Aggregate data
    monthly_spend, yearly_spend, category_spend = aggregate_data(df)

    # Navigation logic
    navigate_to_section(choice, df, monthly_spend, yearly_spend)

    # Footer
    st.sidebar.subheader("Downloadable Reports")
    st.download_button(
        label="Download Raw Data CSV",
        data=df.to_csv(index=False),
        file_name="credit_card_raw_data.csv",
        mime="text/csv"
    )
    st.download_button(
        label="Download Aggregated Data CSV",
        data=pd.concat([monthly_spend, yearly_spend, category_spend], axis=1).to_csv(index=False),
        file_name="credit_card_aggregated_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
