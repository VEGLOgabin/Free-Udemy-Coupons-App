import streamlit as st # pip install streamlit
import time
import os
import pandas as pd
import plotly.express as px # pip install plotly-express
from glob import glob
from datetime import datetime
from requests_html import HTMLSession, AsyncHTMLSession # pip install requests-html
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import asyncio

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

DATABASE_NAME = "coupons.db"

class RealDiscountUdemyCoursesCouponCodeScraper:
    def __init__(self):
        self.url = "https://www.real.discount/udemy-coupon-code/"
        self.session = AsyncHTMLSession()
        self.conn = sqlite3.connect(DATABASE_NAME)
        
    async def load_webpage(self):
        self.response = await self.session.get(self.url)
        await self.response.html.arender(timeout=20)  # Allow time for JavaScript to render
        
    async def scrape_coupons(self):
        try:
            await self.load_webpage()
            coupons_data_list = []
            header = ["date", "title", "course", "category", "provider", "duration", "rating", "language", "students_enrolled", "price_discounted", "price_original", "views"]
            courses_container = self.response.html.find('.list-unstyled', first=True)
            courses = courses_container.find("a")
            for course in reversed(courses):
                if 'https://www.real.discount' not in course.attrs['href']:
                    continue
                if 'https://www.real.discount/ads/' in course.attrs['href']:
                    continue
                coupon_data = [
                    datetime.now().strftime("%Y-%m-%d"),
                    course.find('h3', first=True).text.strip(),
                    course.attrs['href'],
                    course.find('h5', first=True).text.strip(),
                    course.find('.p-2:nth-child(1) .mt-1', first=True).text.strip(),
                    course.find('.p-2:nth-child(2) .mt-1', first=True).text.strip(),
                    course.find('.p-2:nth-child(3) .mt-1', first=True).text.strip(),
                    course.find('.p-2:nth-child(4) .mt-1', first=True).text.strip(),
                    course.find('.p-2:nth-child(5) .mt-1', first=True).text.strip(),
                    course.find('span', first=True).text.strip(),
                    course.find('.card-price-full', first=True).text.strip(),
                    course.find('.p-2:nth-child(7) .ml-1', first=True).text.strip()
                ]
                coupons_data_list.append(coupon_data)
            self.save_to_db(coupons_data_list)
        except Exception as e:
            print(f"Error occurred: {e}")
    
    def save_to_db(self, data):
        cursor = self.conn.cursor()
        for row in data:
            cursor.execute('''SELECT 1 FROM coupons WHERE title = ? AND course = ? AND date = ?''', (row[1], row[2], row[0]))
            if cursor.fetchone() is None:
                cursor.execute('''INSERT INTO coupons (date, title, course, category, provider, duration, rating, language, students_enrolled, price_discounted, price_original, views) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)
        self.conn.commit()
        
    def close_session(self):
        self.session.close()
        self.conn.close()
        
class Dashboard:
    def __init__(self):
        self.title = ":bar_chart: Real-Time Udemy Course Discounts Scraper Dashboard"
        self.df = None
        self.df_selected = None
        self.conn = sqlite3.connect(DATABASE_NAME)
        
    def set_settings_session(self):
        st.set_page_config(page_title="Real-Time Udemy Course Discounts Scraper", page_icon=":bar_chart:", layout="wide")
        
    def set_sidebar_session(self):
        st.sidebar.header("Choose your filter: ")
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT date FROM coupons")
        dates = [row[0] for row in cursor.fetchall()]
        self.current_date = st.sidebar.multiselect("Select date(s):", dates, default=dates)
        
        if self.current_date:
            query = "SELECT * FROM coupons WHERE date IN ({})".format(','.join('?' * len(self.current_date)))
            self.df = pd.read_sql_query(query, self.conn, params=self.current_date)
            
            if not self.df.empty:
                category = st.sidebar.multiselect("Select category(ies):", self.df['category'].unique(), default=self.df['category'].unique())
                duration = st.sidebar.multiselect("Select duration(s):", self.df['duration'].unique(), default=self.df['duration'].unique())
                provider = st.sidebar.multiselect("Select provider(s):", self.df['provider'].unique(), default=self.df['provider'].unique())
                rating = st.sidebar.multiselect("Select rating(s):", self.df['rating'].unique(), default=self.df['rating'].unique())
                language = st.sidebar.multiselect("Select language(s):", self.df['language'].unique(), default=self.df['language'].unique())
                students_enrolled = st.sidebar.multiselect("Select students enrolled:", self.df['students_enrolled'].unique(), default=self.df['students_enrolled'].unique())
                price_discounted = st.sidebar.multiselect("Select discounted price:", self.df['price_discounted'].unique(), default=self.df['price_discounted'].unique())
                price_original = st.sidebar.multiselect("Select original price:", self.df['price_original'].unique(), default=self.df['price_original'].unique())
                views = st.sidebar.multiselect("Select views:", self.df['views'].unique(), default=self.df['views'].unique())
                
                self.df_selected = self.df.query(
                    "category == @category & duration == @duration & provider == @provider & rating == @rating & language == @language & students_enrolled == @students_enrolled & price_discounted == @price_discounted & price_original == @price_original & views == @views"
                )
                
                if self.df_selected.empty:
                    st.warning("No data available based on the current filter settings!")
            else:
                st.title(self.title)
                st.markdown("##")
                st.markdown("""---""")
                st.subheader("No data available for the selected date(s)")
        else:
            st.title(self.title)
            st.markdown("##")
            st.markdown("""---""")
            st.subheader("No date selected, so please select a date")

    def set_title_session(self):
        st.title(self.title)
        st.markdown("##")
    
    def set_date_selected_session(self):
        if len(self.current_date) == 1:
            st.subheader("Current date: **" + self.current_date[0] + "**")
        elif len(self.current_date) > 1:
            dates = ", ".join(f"**{date}**" for date in self.current_date)
            st.subheader(f"Current dates: {dates}")
        else:
            st.subheader("No date selected, so please select a date")

    def set_courses_prices_statics_session(self):
        self.df_selected['price_original'] = self.df_selected['price_original'].str.replace('$', '').astype(float)
        total_original_courses_price = round(self.df_selected['price_original'].sum(), 3)
        average_rating = round(self.df_selected['rating'].astype(float).mean(), 1)
        star_rating = ":star:" * int(round(average_rating, 0))
        average_original_courses_price = round(self.df_selected['price_original'].mean(), 3)
        
        start_column, middle_column, end_column = st.columns(3)
        with start_column:
            st.subheader("Total Original Courses Price:")
            st.subheader(f"US $ {total_original_courses_price:,}")
        with middle_column:
            st.subheader("Average Rating:")
            st.subheader(f"{average_rating} {star_rating}")
        with end_column:
            st.subheader("Average Original Courses Price:")
            st.subheader(f"US $ {average_original_courses_price}")

    def show_data_table_session(self):
        show_table = st.checkbox("Show your filtered data as a table")
        if show_table:
            st.table(self.df_selected)

    def coupon_code_courses_application_session(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM coupons WHERE date = ?", (datetime.now().strftime("%Y-%m-%d"),))
        today_coupons = cursor.fetchall()
        for row in today_coupons:
            title_column, link_column = st.columns(2)
            with title_column:
                st.subheader(row[1])
            with link_column:
                st.link_button("Apply", row[2])

    def price_original_by_category_bar_chart_dashboard(self):
        price_original_by_category = self.df_selected.groupby(by=["category"])[["price_original"]].sum().sort_values(by="price_original")
        st.subheader("Price Original by Category")
        fig = px.bar(
            price_original_by_category,
            x="price_original",
            y=price_original_by_category.index,
            orientation="h",
            title="<b>Price Original by Category</b>",
            color_discrete_sequence=["#0083B8"] * len(price_original_by_category),
            template="plotly_white",
        )
        st.plotly_chart(fig)
        
    def price_original_by_category_pie_chart_dashboard(self):
        price_original_by_category_pie_chart = self.df_selected.groupby(by=["category"])[["price_original"]].sum()
        fig2 = px.pie(price_original_by_category_pie_chart, values="price_original", names=price_original_by_category_pie_chart.index)
        st.plotly_chart(fig2)
    
    def run(self):
        self.set_settings_session()
        self.set_sidebar_session()
        if self.df is not None and not self.df.empty:
            self.set_title_session()
            self.set_date_selected_session()
            self.set_courses_prices_statics_session()
            self.show_data_table_session()
            self.coupon_code_courses_application_session()
            self.price_original_by_category_bar_chart_dashboard()
            self.price_original_by_category_pie_chart_dashboard()

def create_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS coupons (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        title TEXT,
                        course TEXT,
                        category TEXT,
                        provider TEXT,
                        duration TEXT,
                        rating TEXT,
                        language TEXT,
                        students_enrolled TEXT,
                        price_discounted TEXT,
                        price_original TEXT,
                        views TEXT
                      )''')
    conn.commit()
    conn.close()

async def run_scraper():
    scraper = RealDiscountUdemyCoursesCouponCodeScraper()
    await scraper.scrape_coupons()
    scraper.close_session()

def schedule_scraper():
    scheduler = BackgroundScheduler()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Add jobs
    scheduler.add_job(lambda: loop.create_task(run_scraper()), IntervalTrigger(minutes=2), id='run_scraper', replace_existing=True)

    scheduler.start()

def main():
    create_db()
    schedule_scraper()
    dashboard = Dashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
