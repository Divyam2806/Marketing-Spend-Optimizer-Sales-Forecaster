import sqlite3
import pandas as pd


def get_connection(db_path='data/marketing.db'):
    """Creates and returns a connection to the SQLite database."""
    return sqlite3.connect(db_path)


def save_data(df, db_path='data/marketing.db'):
    """Stores the marketing dataframe as a table in the database."""
    conn = get_connection(db_path)
    df.to_sql('marketing_data', conn, index=False, if_exists='append')
    conn.close()


def run_queries(db_path='data/marketing.db'):
    """Runs analytics queries and returns results as dataframes."""
    conn = get_connection(db_path)

    # Q1: Total spend per channel ranked highest to lowest
    spend_by_channel = pd.read_sql("""
        SELECT 'TV'      AS channel, SUM(tv_spend)      AS total_spend FROM marketing_data
        UNION ALL
        SELECT 'Digital',            SUM(digital_spend)               FROM marketing_data
        UNION ALL
        SELECT 'Radio',              SUM(radio_spend)                 FROM marketing_data
        UNION ALL
        SELECT 'Print',              SUM(print_spend)                 FROM marketing_data
        ORDER BY total_spend DESC
    """, conn)

    # Q2: Average and maximum revenue across all campaigns
    revenue_stats = pd.read_sql("""
        SELECT ROUND(AVG(revenue), 2) AS avg_revenue,
               ROUND(MAX(revenue), 2) AS max_revenue
        FROM marketing_data
    """, conn)

    # Q3: Count of high-performing campaigns (revenue > 1000)
    high_performers = pd.read_sql("""
        SELECT COUNT(*) AS high_performing_campaigns
        FROM marketing_data
        WHERE revenue > 1000
    """, conn)

    conn.close()
    return spend_by_channel, revenue_stats, high_performers