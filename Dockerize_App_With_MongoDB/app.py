import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from playwright.async_api import async_playwright
import logging
from datetime import datetime
from pymongo import MongoClient
import streamlit as st
import pandas as pd
import plotly.express as px

# Configure logging
logging.basicConfig(level=logging.INFO)

MONGO_URI = "mongodb+srv://houetchenougabin:houetchenougabin@cluster0.n8d671j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "coupon_data"
COLLECTION_NAME = "coupons"

class RealDiscountUdemyCoursesCouponCodeScraper:
    def __init__(self):
        self.url = "https://www.real.discount/udemy-coupon-code/"
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        logging.info("Connected to the database successfully")

    async def load_webpage(self):
        logging.info(f"Opening URL: {self.url}")

    async def scrape_coupons(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # Set headless to True for background execution
            logging.info(f"Browser launched: {browser.is_connected()}")
            page = await browser.new_page()
            await page.goto(self.url)
            logging.info("Page loaded successfully")

            await page.wait_for_selector('ul#myList li')
            logging.info("Page elements loaded")

            try:
                logging.info("Starting coupon scraping")
                coupons_data_list = []
                course_elements = await page.query_selector_all('ul#myList li')
                logging.info(f"Number of courses found: {len(course_elements)}")

                for index, element in enumerate(course_elements):
                    try:
                        async def safe_query(selector):
                            el = await element.query_selector(selector)
                            if el:
                                return el
                            else:
                                logging.warning(f"Element not found with selector: {selector} for course index: {index}")
                                return None
                        
                            
                        if element:
                            course_url = await element.get_attribute('href')
                            print("-------------------------------------------------------------------------")
                            print(course_url)
                            print("-------------------------------------------------------------------------")
                            # if 'https://www.real.discount' not in course_url or 'https://www.real.discount/ads/' in course_url:
                            #     continue
                        else:
                            course_url = "N/A"

                        course_url = await (await safe_query('a')).get_attribute('href') if await safe_query('a') else "N/A"
                        img_src = await (await safe_query('img')).get_attribute('src') if await safe_query('img') else "N/A"
                        title = await (await safe_query('h3')).inner_text() if await safe_query('h3') else "N/A"
                        category = await (await safe_query('h5')).inner_text() if await safe_query('h5') else "N/A"
                        provider = await (await safe_query('div.p-2:nth-child(1) div.mt-1')).inner_text() if await safe_query('div.p-2:nth-child(1) div.mt-1') else "N/A"
                        duration = await (await safe_query('div.p-2:nth-child(2) div.mt-1')).inner_text() if await safe_query('div.p-2:nth-child(2) div.mt-1') else "N/A"
                        rating = await (await safe_query('div.p-2:nth-child(3) div.mt-1')).inner_text() if await safe_query('div.p-2:nth-child(3) div.mt-1') else "N/A"
                        language = await (await safe_query('div.p-2:nth-child(4) div.mt-1')).inner_text() if await safe_query('div.p-2:nth-child(4) div.mt-1') else "N/A"
                        students_enrolled = await (await safe_query('div.p-2:nth-child(5) div.mt-1')).inner_text() if await safe_query('div.p-2:nth-child(5) div.mt-1') else "N/A"
                        price_discounted = await (await safe_query('span')).inner_text() if await safe_query('span') else "N/A"
                        price_original = await (await safe_query('span.card-price-full')).inner_text() if await safe_query('span.card-price-full') else "N/A"
                        views = await (await safe_query('div.p-2:nth-child(7) div.ml-1')).inner_text() if await safe_query('div.p-2:nth-child(7) div.ml-1') else "N/A"
                        
                        coupon_data = {
                           "date": datetime.now().strftime("%Y-%m-%d"),
                            "title": title.strip(),
                            "course": course_url.strip(),
                            "image": img_src.strip(),
                            "category": category.strip(),
                            "provider": provider.strip(),
                            "duration": duration.strip(),
                            "rating": rating.strip(),
                            "language": language.strip(),
                            "students_enrolled": students_enrolled.strip(),
                            "price_discounted": price_discounted.strip(),
                            "price_original": price_original.strip(),
                            "views": views.strip()
                        }
                        coupons_data_list.append(coupon_data)
                        logging.info(f"Coupon data: {coupon_data}")
                    except Exception as e:
                        logging.error(f"Error scraping course element index {index}: {e}")

                logging.info("Data scraped successfully")
                await self.save_to_db(coupons_data_list)
            except Exception as e:
                logging.error(f"Error occurred: {e}")
            finally:
                await browser.close()

    async def save_to_db(self, data):
        logging.info("Saving data to MongoDB")
        for row in data:
            if self.collection.count_documents({"title": row["title"], "course": row["course"], "date": row["date"]}, limit=1) == 0:
                self.collection.insert_one(row)
                logging.info(f"Data inserted successfully: {row}")

    async def close_driver(self):
        logging.info("Closing MongoDB connection")
        self.client.close()




















# import asyncio
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from playwright.async_api import async_playwright
# import logging
# from datetime import datetime
# from pymongo import MongoClient
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# MONGO_URI = "mongodb+srv://houetchenougabin:houetchenougabin@cluster0.n8d671j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# DATABASE_NAME = "coupon_data"
# COLLECTION_NAME = "coupons"

# class RealDiscountUdemyCoursesCouponCodeScraper:
#     def __init__(self):
#         self.url = "https://www.real.discount/udemy-coupon-code/"
#         self.client = MongoClient(MONGO_URI)
#         self.db = self.client[DATABASE_NAME]
#         self.collection = self.db[COLLECTION_NAME]
#         logging.info("Connected to the database successfully")

#     async def load_webpage(self):
#         logging.info(f"Opening URL: {self.url}")

#     async def scrape_coupons(self):
#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=True)  # Set headless to True for background execution
#             logging.info(f"Browser launched: {browser.is_connected()}")
#             page = await browser.new_page()
#             await page.goto(self.url)
#             logging.info("Page loaded successfully")

#             await page.wait_for_selector('ul#myList li')
#             logging.info("Page elements loaded")

#             try:
#                 logging.info("Starting coupon scraping")
#                 coupons_data_list = []
#                 course_elements = await page.query_selector_all('ul#myList li')
#                 logging.info(f"Number of courses found: {len(course_elements)}")

#                 for index, element in enumerate(course_elements):
#                     try:
#                         async def safe_query(selector):
#                             el = await element.query_selector(selector)
#                             if el:
#                                 return el
#                             else:
#                                 logging.warning(f"Element not found with selector: {selector} for course index: {index}")
#                                 return None

#                         course_url = await (await safe_query('a')).get_attribute('href') if await safe_query('a') else "N/A"
#                         img_src = await (await safe_query('img')).get_attribute('src') if await safe_query('img') else "N/A"
#                         title = await (await safe_query('h3')).inner_text() if await safe_query('h3') else "N/A"
#                         category = await (await safe_query('h5')).inner_text() if await safe_query('h5') else "N/A"
#                         provider = await (await safe_query('div.d-flex:nth-child(1) div.mt-1')).inner_text() if await safe_query('div.d-flex:nth-child(1) div.mt-1') else "N/A"
#                         duration = await (await safe_query('div.d-flex:nth-child(2) div.mt-1')).inner_text() if await safe_query('div.d-flex:nth-child(2) div.mt-1') else "N/A"
#                         rating = await (await safe_query('div.d-flex:nth-child(3) div.mt-1')).inner_text() if await safe_query('div.d-flex:nth-child(3) div.mt-1') else "N/A"
#                         language = await (await safe_query('div.d-flex:nth-child(4) div.mt-1')).inner_text() if await safe_query('div.d-flex:nth-child(4) div.mt-1') else "N/A"
#                         students_enrolled = await (await safe_query('div.d-flex:nth-child(5) div.mt-1')).inner_text() if await safe_query('div.d-flex:nth-child(5) div.mt-1') else "N/A"
#                         price_discounted = await (await safe_query('span')).inner_text() if await safe_query('span') else "N/A"
#                         price_original = await (await safe_query('span.card-price-full')).inner_text() if await safe_query('span.card-price-full') else "N/A"
#                         views = await (await safe_query('div.d-flex:nth-child(7) div.ml-1')).inner_text() if await safe_query('div.d-flex:nth-child(7) div.ml-1') else "N/A"
                        
#                         coupon_data = {
#                             "date": datetime.now().strftime("%Y-%m-%d"),
#                             "title": title.strip(),
#                             "course": course_url.strip(),
#                             "image": img_src.strip(),
#                             "category": category.strip(),
#                             "provider": provider.strip(),
#                             "duration": duration.strip(),
#                             "rating": rating.strip(),
#                             "language": language.strip(),
#                             "students_enrolled": students_enrolled.strip(),
#                             "price_discounted": price_discounted.strip(),
#                             "price_original": price_original.strip(),
#                             "views": views.strip()
#                         }
#                         coupons_data_list.append(coupon_data)
#                         logging.info(f"Coupon data: {coupon_data}")
#                     except Exception as e:
#                         logging.error(f"Error scraping course element index {index}: {e}")

#                 logging.info("Data scraped successfully")
#                 await self.save_to_db(coupons_data_list)
#             except Exception as e:
#                 logging.error(f"Error occurred: {e}")
#             finally:
#                 await browser.close()

#     async def save_to_db(self, data):
#         logging.info("Saving data to MongoDB")
#         for row in data:
#             if self.collection.count_documents({"title": row["title"], "course": row["course"], "date": row["date"]}, limit=1) == 0:
#                 self.collection.insert_one(row)
#                 logging.info(f"Data inserted successfully: {row}")

#     async def close_driver(self):
#         logging.info("Closing MongoDB connection")
#         self.client.close()

        
        
        
        
        
        
        
        
# class Dashboard:
#     def __init__(self):
#         self.title = ":bar_chart: Real-Time Udemy Course Discounts Scraper Dashboard"
#         self.df = None
#         self.df_selected = None
#         self.client = MongoClient(MONGO_URI)
#         self.db = self.client[DATABASE_NAME]
#         self.collection = self.db[COLLECTION_NAME]

#     def set_settings_session(self):
#         st.set_page_config(page_title="Real-Time Udemy Course Discounts Scraper", page_icon=":bar_chart:", layout="wide")

#     def set_sidebar_session(self):
#         st.sidebar.header("Choose your filter: ")
#         dates = self.collection.distinct("date")
#         self.current_date = st.sidebar.multiselect("Select date(s):", dates, default=dates)

#         if self.current_date:
#             query = {"date": {"$in": self.current_date}}
#             self.df = pd.DataFrame(list(self.collection.find(query)))

#             if not self.df.empty:
#                 category = st.sidebar.multiselect("Select category(ies):", self.df['category'].unique(), default=self.df['category'].unique())
#                 duration = st.sidebar.multiselect("Select duration(s):", self.df['duration'].unique(), default=self.df['duration'].unique())
#                 provider = st.sidebar.multiselect("Select provider(s):", self.df['provider'].unique(), default=self.df['provider'].unique())
#                 rating = st.sidebar.multiselect("Select rating(s):", self.df['rating'].unique(), default=self.df['rating'].unique())
#                 language = st.sidebar.multiselect("Select language(s):", self.df['language'].unique(), default=self.df['language'].unique())
#                 students_enrolled = st.sidebar.multiselect("Select students enrolled:", self.df['students_enrolled'].unique(), default=self.df['students_enrolled'].unique())
#                 price_discounted = st.sidebar.multiselect("Select discounted price:", self.df['price_discounted'].unique(), default=self.df['price_discounted'].unique())
#                 price_original = st.sidebar.multiselect("Select original price:", self.df['price_original'].unique(), default=self.df['price_original'].unique())
#                 views = st.sidebar.multiselect("Select views:", self.df['views'].unique(), default=self.df['views'].unique())

#                 self.df_selected = self.df.query(
#                     "category == @category & duration == @duration & provider == @provider & rating == @rating & language == @language & students_enrolled == @students_enrolled & price_discounted == @price_discounted & price_original == @price_original & views == @views"
#                 )

#                 if self.df_selected.empty:
#                     st.print("No data available based on the current filter settings!")
#             else:
#                 st.title(self.title)
#                 st.markdown("##")
#                 st.markdown("""---""")
#                 st.subheader("No data available for the selected date(s)")
#         else:
#             st.title(self.title)
#             st.markdown("##")
#             st.markdown("""---""")
#             st.subheader("No date selected, so please select a date")

#     def set_title_session(self):
#         st.title(self.title)
#         st.markdown("##")

#     def set_date_selected_session(self):
#         if len(self.current_date) == 1:
#             st.subheader("Current date: **" + self.current_date[0] + "**")
#         elif len(self.current_date) > 1:
#             dates = ", ".join(f"**{date}**" for date in self.current_date)
#             st.subheader(f"Current dates: {dates}")
#         else:
#             st.subheader("No date selected, so please select a date")

#     def set_courses_prices_statics_session(self):
#         self.df_selected['price_original'] = self.df_selected['price_original'].str.replace('$', '').astype(float)
#         total_original_courses_price = round(self.df_selected['price_original'].sum(), 3)
#         average_rating = round(self.df_selected['rating'].astype(float).mean(), 1)
#         star_rating = ":star:" * int(round(average_rating, 0))
#         average_original_courses_price = round(self.df_selected['price_original'].mean(), 3)

#         start_column, middle_column, end_column = st.columns(3)
#         with start_column:
#             st.subheader("Total Original Courses Price:")
#             st.subheader(f"US $ {total_original_courses_price:,}")
#         with middle_column:
#             st.subheader("Average Rating:")
#             st.subheader(f"{average_rating} {star_rating}")
#         with end_column:
#             st.subheader("Average Original Courses Price:")
#             st.subheader(f"US $ {average_original_courses_price}")

#     def show_data_table_session(self):
#         show_table = st.checkbox("Show your filtered data as a table")
#         if show_table:
#             st.table(self.df_selected)

#     def coupon_code_courses_application_session(self):
#         today_coupons = list(self.collection.find({"date": datetime.now().strftime("%Y-%m-%d")}))
#         for row in today_coupons:
#             title_column, link_column = st.columns(2)
#             with title_column:
#                 st.subheader(row["title"])
#             with link_column:
#                 st.markdown(f"[Apply]({row['course']})")

#     def price_original_by_category_bar_chart_dashboard(self):
#         price_original_by_category = self.df_selected.groupby(by=["category"])[["price_original"]].sum().sort_values(by="price_original")
#         st.subheader("Price Original by Category")
#         fig = px.bar(
#             price_original_by_category,
#             x="price_original",
#             y=price_original_by_category.index,
#             orientation="h",
#             height=1000, 
#             width=1000,
#             color_discrete_sequence=["#0083B8"] * len(price_original_by_category),
#             template="plotly_white",
#         )
#         st.plotly_chart(fig)

#     def price_original_by_provider_bar_chart_dashboard(self):
#         price_original_by_provider = self.df_selected.groupby(by=["provider"])[["price_original"]].sum().sort_values(by="price_original")
#         st.subheader("Price Original by Provider")
#         fig = px.bar(
#             price_original_by_provider,
#             x="price_original",
#             y=price_original_by_provider.index,
#             orientation="h",
#             height=1000,
#             width=1000,
#             color_discrete_sequence=["#0083B8"] * len(price_original_by_provider),
#             template="plotly_white",
#         )
#         st.plotly_chart(fig)

#     def price_original_by_language_bar_chart_dashboard(self):
#         price_original_by_language = self.df_selected.groupby(by=["language"])[["price_original"]].sum().sort_values(by="price_original")
#         st.subheader("Price Original by Language")
#         fig = px.bar(
#             price_original_by_language,
#             x="price_original",
#             y=price_original_by_language.index,
#             orientation="h",
#             height=1000,
#             width=1000,
#             color_discrete_sequence=["#0083B8"] * len(price_original_by_language),
#             template="plotly_white",
#         )
#         st.plotly_chart(fig)

#     def __del__(self):
#         self.client.close()
            
            

# async def run_scraper():
#     scraper = RealDiscountUdemyCoursesCouponCodeScraper()
#     await scraper.load_webpage()
#     await scraper.scrape_coupons()
#     await scraper.close_driver()
#     print("Scraper run completed and database updated.")
    
    

# def run():
#     dashboard = Dashboard()
#     dashboard.set_settings_session()
#     dashboard.set_sidebar_session()
#     dashboard.set_title_session()
#     dashboard.set_date_selected_session()
#     if dashboard.df_selected is not None and not dashboard.df_selected.empty:
#         dashboard.set_courses_prices_statics_session()
#         dashboard.show_data_table_session()
#         dashboard.coupon_code_courses_application_session()
#         dashboard.price_original_by_category_bar_chart_dashboard()
#         dashboard.price_original_by_provider_bar_chart_dashboard()
#         dashboard.price_original_by_language_bar_chart_dashboard()
#     else:
#         st.print("No data available based on the current filter settings!")

# def schedule_scraper():
#     scheduler = BackgroundScheduler()
    
#     # Define job IDs
#     job_ids = {
#         'run_scraper': 'run_scraper',
#         'run': 'run'
#     }
    
#     # Add jobs
#     scheduler.add_job(lambda: asyncio.run(run_scraper()), IntervalTrigger(minutes=1), id=job_ids['run_scraper'], replace_existing=True)
#     scheduler.add_job(run, IntervalTrigger(minutes=1), id=job_ids['run'], replace_existing=True)
    
#     try:
#        # Start the scheduler
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
        
# def main():
#     # Create database and start Streamlit app
#     # create_db()
#     schedule_scraper()
#     run()

# if __name__ == "__main__":
#     main()




class Dashboard:
    def __init__(self):
        self.title = ":bar_chart: Real-Time Udemy Course Discounts Scraper Dashboard"
        self.df = None
        self.df_selected = None
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def clean_data(self):
        # Remove rows with 'N/A' in any column
        self.collection.delete_many({"$or": [{"category": "N/A"}, {"duration": "N/A"}, {"provider": "N/A"}, {"rating": "N/A"}, {"language": "N/A"}, {"students_enrolled": "N/A"}, {"price_discounted": "N/A"}, {"price_original": "N/A"}, {"views": "N/A"}]})

    def set_settings_session(self):
        st.set_page_config(page_title="Real-Time Udemy Course Discounts Scraper", page_icon=":bar_chart:", layout="wide")

    def set_sidebar_session(self):
        self.clean_data()  # Ensure data is cleaned before querying
        st.sidebar.header("Choose your filter: ")
        dates = self.collection.distinct("date")
        self.current_date = st.sidebar.multiselect("Select date(s):", dates, default=dates)

        if self.current_date:
            query = {"date": {"$in": self.current_date}}
            self.df = pd.DataFrame(list(self.collection.find(query)))

            if not self.df.empty:
                self.apply_filters()
            else:
                self.display_no_data_message()
        else:
            self.display_no_data_message()

    def apply_filters(self):
        # Apply filters based on user input
        filters = {
            'category': st.sidebar.multiselect("Select category(ies):", self.df['category'].unique(), default=self.df['category'].unique()),
            'duration': st.sidebar.multiselect("Select duration(s):", self.df['duration'].unique(), default=self.df['duration'].unique()),
            'provider': st.sidebar.multiselect("Select provider(s):", self.df['provider'].unique(), default=self.df['provider'].unique()),
            'rating': st.sidebar.multiselect("Select rating(s):", self.df['rating'].unique(), default=self.df['rating'].unique()),
            'language': st.sidebar.multiselect("Select language(s):", self.df['language'].unique(), default=self.df['language'].unique()),
            'students_enrolled': st.sidebar.multiselect("Select students enrolled:", self.df['students_enrolled'].unique(), default=self.df['students_enrolled'].unique()),
            'price_discounted': st.sidebar.multiselect("Select discounted price:", self.df['price_discounted'].unique(), default=self.df['price_discounted'].unique()),
            'price_original': st.sidebar.multiselect("Select original price:", self.df['price_original'].unique(), default=self.df['price_original'].unique()),
            'views': st.sidebar.multiselect("Select views:", self.df['views'].unique(), default=self.df['views'].unique())
        }

        query_str = " & ".join([f"{key} == @filters['{key}']" for key in filters])
        self.df_selected = self.df.query(query_str)

        if self.df_selected.empty:
            st.warning("No data available based on the current filter settings!")

    def display_no_data_message(self):
        st.title(self.title)
        st.markdown("##")
        st.markdown("""---""")
        st.subheader("No data available for the selected date(s)" if self.current_date else "No date selected, so please select a date")

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
        if self.df_selected.empty:
            return

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
        today_coupons = list(self.collection.find({"date": datetime.now().strftime("%Y-%m-%d")}))
        for row in today_coupons:
            title_column, link_column = st.columns(2)
            with title_column:
                st.subheader(row["title"])
            with link_column:
                st.markdown(f"[Apply]({row['course']})")

    def price_original_by_category_bar_chart_dashboard(self):
        if self.df_selected.empty:
            return

        price_original_by_category = self.df_selected.groupby(by=["category"])[["price_original"]].sum().sort_values(by="price_original")
        st.subheader("Price Original by Category")
        fig = px.bar(
            price_original_by_category,
            x="price_original",
            y=price_original_by_category.index,
            orientation="h",
            height=1000,
            width=1000,
            color_discrete_sequence=["#0083B8"] * len(price_original_by_category),
            template="plotly_white",
        )
        st.plotly_chart(fig)

    def price_original_by_provider_bar_chart_dashboard(self):
        if self.df_selected.empty:
            return

        price_original_by_provider = self.df_selected.groupby(by=["provider"])[["price_original"]].sum().sort_values(by="price_original")
        st.subheader("Price Original by Provider")
        fig = px.bar(
            price_original_by_provider,
            x="price_original",
            y=price_original_by_provider.index,
            orientation="h",
            height=1000,
            width=1000,
            color_discrete_sequence=["#0083B8"] * len(price_original_by_provider),
            template="plotly_white",
        )
        st.plotly_chart(fig)

    def price_original_by_language_bar_chart_dashboard(self):
        if self.df_selected.empty:
            return

        price_original_by_language = self.df_selected.groupby(by=["language"])[["price_original"]].sum().sort_values(by="price_original")
        st.subheader("Price Original by Language")
        fig = px.bar(
            price_original_by_language,
            x="price_original",
            y=price_original_by_language.index,
            orientation="h",
            height=1000,
            width=1000,
            color_discrete_sequence=["#0083B8"] * len(price_original_by_language),
            template="plotly_white",
        )
        st.plotly_chart(fig)

    def __del__(self):
        self.client.close()

async def run_scraper():
    scraper = RealDiscountUdemyCoursesCouponCodeScraper()
    await scraper.load_webpage()
    await scraper.scrape_coupons()
    await scraper.close_driver()
    print("Scraper run completed and database updated.")

def run():
    dashboard = Dashboard()
    dashboard.set_settings_session()
    dashboard.set_sidebar_session()
    dashboard.set_title_session()
    dashboard.set_date_selected_session()
    if dashboard.df_selected is not None and not dashboard.df_selected.empty:
        dashboard.set_courses_prices_statics_session()
        dashboard.show_data_table_session()
        dashboard.coupon_code_courses_application_session()
        dashboard.price_original_by_category_bar_chart_dashboard()
        dashboard.price_original_by_provider_bar_chart_dashboard()
        dashboard.price_original_by_language_bar_chart_dashboard()
    else:
        st.warning("No data available based on the current filter settings!")

def schedule_scraper():
    scheduler = BackgroundScheduler()

    # Define job IDs
    job_ids = {
        'run_scraper': 'run_scraper',
        'run': 'run'
    }

    # Add jobs
    scheduler.add_job(lambda: asyncio.run(run_scraper()), IntervalTrigger(minutes=1), id=job_ids['run_scraper'], replace_existing=True)
    scheduler.add_job(run, IntervalTrigger(minutes=1), id=job_ids['run'], replace_existing=True)

    try:
        # Start the scheduler
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

def main():
    # Create database and start Streamlit app
    # create_db()
    schedule_scraper()
    run()

if __name__ == "__main__":
    main()
