import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import messagebox

# Load dataset
try:
    df = pd.read_csv("/Users/tusharchhabra/Desktop/codsoft/rs/movies.csv")
except Exception as e:
    messagebox.showerror("File Error", f"Could not read movies.csv:\n{e}")
    raise

# Vectorize descriptions
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['description'].fillna(""))

# Calculate cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Map titles to indices
title_to_index = pd.Series(df.index, index=df['title'].str.lower())

# Recommendation function
def recommend(movie_title):
    movie_title = movie_title.lower()
    if movie_title not in title_to_index:
        return ["Movie not found in dataset."]
    idx = title_to_index[movie_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in sim_scores[1:6]]
    return df['title'].iloc[top_indices].tolist()

# GUI setup
def on_recommend():
    movie = entry.get().strip()
    if not movie:
        messagebox.showwarning("Input Error", "Please enter a movie title.")
        return
    recommendations = recommend(movie)
    listbox.delete(0, tk.END)
    for rec in recommendations:
        listbox.insert(tk.END, rec)

root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("400x350")
root.config(bg="white")

tk.Label(root, text="Enter a Movie Title:", bg="white", font=('Arial', 12)).pack(pady=10)
entry = tk.Entry(root, width=40, font=('Arial', 12))
entry.pack(pady=5)

tk.Button(root, text="Recommend", command=on_recommend, font=('Arial', 12), bg="skyblue").pack(pady=10)

listbox = tk.Listbox(root, width=50, height=10, font=('Arial', 11))
listbox.pack(pady=10)

root.mainloop()
