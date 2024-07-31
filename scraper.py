import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to scrape product information
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    
    # Selectors based on the structure of 'http://books.toscrape.com/'
    for product in soup.select('article.product_pod'):
        name = product.select_one('h3 a').get('title', 'N/A')
        price = product.select_one('.price_color').text
        rating = product.select_one('.star-rating').get('class', [''])[1]  # Second class is the rating
        
        products.append({
            'Name': name,
            'Price': price,
            'Rating': rating
        })
    
    return products

# Function to save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Function to handle button click event
def on_scrape():
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return
    
    try:
        data = scrape_data(url)
        if not data:
            messagebox.showinfo("No Data", "No products found on the given URL")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            save_to_csv(data, file_path)
            messagebox.showinfo("Success", f"Data saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Creating the GUI
root = tk.Tk()
root.title("Web Scraper")

tk.Label(root, text="Enter URL:").pack(pady=5)

entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

btn_scrape = tk.Button(root, text="Scrape and Save", command=on_scrape)
btn_scrape.pack(pady=20)

root.mainloop()
