# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import random

# Configure Chrome options (Removed headless)
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the webdriver (Now opens a visible Chrome window)
driver = webdriver.Chrome(options=options)

# --- LOGIN SECTION ---
username = ""
# password = ""

# Open LinkedIn login page
driver.get("https://www.linkedin.com/login")
time.sleep(2)

# Enter credentials and log in
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "password").submit()
time.sleep(3)  # Allow time for login
# --- END LOGIN SECTION ---

# Accept the LinkedIn profile URL of the target user
profile_url = input("Enter the LinkedIn profile URL (e.g., https://www.linkedin.com/in/username/): ")

# Construct posts (activity) URL from profile
if profile_url.endswith('/'):
    posts_url = profile_url + "detail/recent-activity/shares/"
else:
    posts_url = profile_url + "/detail/recent-activity/shares/"

print("Navigating to posts URL:", posts_url)
driver.get(posts_url)
time.sleep(3)

# Function to scroll down to load posts
# def scroll_down():
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # for _ in range(15):  # Increase number of scrolls if needed
    #     time.sleep(random.randint(4, 10))
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(random.randint(4, 10))  # Random delay to mimic human behavior
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

import random
import time

def scroll_down_and_up(driver, max_scrolls=15, delay_range=(4, 10)):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(15):  # Increase number of scrolls if needed
        time.sleep(random.randint(4, 10))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(4, 10))  # Random delay to mimic human behavior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("Now scrolling back up...")
    for _ in range(max_scrolls):
        # Scroll up in small steps instead of jumping instantly
        scroll_distance = random.randint(300, 700)
        driver.execute_script(f"window.scrollBy(0, -{scroll_distance});")

        # Wait for a **random amount of time** to mimic human behavior
        time.sleep(random.uniform(*delay_range))

        # Stop if we've reached the top
        if driver.execute_script("window.scrollY") == 0:
            print("Reached the top of the page.")
            break

    print("Scrolling complete.")




# Scroll to load all posts
# scroll_down()
print("Scrolling through the LinkedIn page...")
scroll_down_and_up(driver, max_scrolls=15, delay_range=(4, 10))
print("Finished scrolling.")





# Extract all posts using Selenium
posts = driver.find_elements(By.XPATH, "//div[contains(@class, 'occludable-update')]")  # Update XPath if needed

if not posts:
    print("No posts found! The class names or XPath might need updating.")
    driver.quit()
    exit()

# Lists to store scraped data
post_dates, post_texts, post_likes, post_comments, post_media = [], [], [], [], []

# Loop over each post and extract details
for post in posts:
    # Extract post date
    try:
        date_elem = post.find_element(By.XPATH, ".//span[contains(@class, 'visually-hidden')]")
        post_dates.append(date_elem.text.strip() if date_elem else "N/A")
    except:
        post_dates.append("N/A")

    # Extract post text
    try:
        text_elem = post.find_element(By.XPATH, ".//span[contains(@class, 'break-words')]")
        post_texts.append(text_elem.text.strip() if text_elem else "N/A")
    except:
        post_texts.append("N/A")

    # Extract likes
    try:
        likes_elem = post.find_element(By.XPATH, ".//button[contains(@aria-label, 'like')]")
        post_likes.append(likes_elem.text.strip() if likes_elem else "0")
    except:
        post_likes.append("0")

    # Extract comments
    try:
        comments_elem = post.find_element(By.XPATH, ".//button[contains(@aria-label, 'comment')]")
        post_comments.append(comments_elem.text.strip() if comments_elem else "0")
    except:
        post_comments.append("0")

    # Extract media link
    try:
        media_elem = post.find_element(By.XPATH, ".//img")
        post_media.append(media_elem.get_attribute("src") if media_elem else "N/A")
    except:
        post_media.append("N/A")

# Create a DataFrame from the scraped data
df = pd.DataFrame({
    "Post Date": post_dates,
    "Post Text": post_texts,
    "Likes": post_likes,
    "Comments": post_comments,
    "Media Link": post_media
})

print(df)

# Save to Excel
excel_filename = "linkedin_user_posts1.xlsx"
df.to_excel(excel_filename, index=False)
print("Scraped posts saved to", excel_filename)

# Close the browser
driver.quit()
print("------------")
