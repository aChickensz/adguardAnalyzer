import json
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import datetime
from collections import Counter
import tldextract

class DNSQueryAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("AdGuard DNS Query Analyzer")

        self.label = tk.Label(root, text="Enter DNS to search:")
        self.label.pack()

        self.entry = tk.Entry(root, width=50)
        self.entry.pack()

        self.search_button = tk.Button(root, text="Search & Graph", command=self.search_dns)
        self.search_button.pack()

        self.load_button = tk.Button(root, text="Load JSON File", command=self.load_json)
        self.load_button.pack()

        self.data = []

    def load_json(self):
        file_path = filedialog.askopenfilename(title="Select AdGuard Queries JSON", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
    
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
    
            # Ensure we extract only the relevant list of queries
            if isinstance(json_data, dict) and "data" in json_data:
                self.data = json_data["data"]  # Extract only the query records
            else:
                self.data = json_data  # Assume it's a direct list if no "data" key
    
            messagebox.showinfo("Success", "JSON file loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")

      
    def get_base_domain(self, domain):
        extracted = tldextract.extract(domain)
        return f"{extracted.domain}.{extracted.suffix}"  # Returns 'snapchat.com' from 'us-east4-gcp.api.snapchat.com'
    
    def search_dns(self):
        if not self.data:
            messagebox.showerror("Error", "No JSON data loaded.")
            return
    
        query = self.entry.get().strip().lower()
        query = self.get_base_domain(query)  # Normalize user input to base domain
    
        if not query:
            messagebox.showerror("Error", "Please enter a DNS query to search.")
            return
    
        timestamps = []
        now = datetime.datetime.now()
        three_days_ago = now - datetime.timedelta(days=3)
    
        for record in self.data:
            if isinstance(record, dict) and "question" in record and isinstance(record["question"], dict):
                logged_query = record["question"].get("name", "").rstrip(".").lower()
                logged_query = self.get_base_domain(logged_query)  # Normalize logged domain
    
                if logged_query == query:
                    time_str = record.get("time")
                    if time_str:
                        try:
                            dt = datetime.datetime.fromisoformat(time_str.split(".")[0])  # Remove microseconds
                            if dt >= three_days_ago:  
                                dt = dt.replace(minute=0, second=0)  # Normalize to the hour
                                dt = dt.replace(hour=(dt.hour // 2) * 2)  # Round to the nearest 2-hour block
                                timestamps.append(dt)
                        except ValueError:
                            continue  # Skip malformed date entries
    
        if not timestamps:
            messagebox.showinfo("No Data", f"No queries found for '{query}'")
            return
    
        # Count occurrences per 2-hour interval
        time_counts = Counter(timestamps)
        sorted_times = sorted(time_counts.keys())
        counts = [time_counts[t] for t in sorted_times]
    
        plt.figure(figsize=(10, 5))
        plt.plot(sorted_times, counts, marker="o", linestyle="-")
        plt.xlabel("Time")
        plt.ylabel("Number of Queries")
        plt.title(f"Query Frequency for {query} (Last 3 Days)")
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()






if __name__ == "__main__":
    root = tk.Tk()
    app = DNSQueryAnalyzer(root)
    root.mainloop()
