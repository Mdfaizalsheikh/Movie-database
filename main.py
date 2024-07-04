import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class MovieDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Database")

        self.movies = []
        self.load_movies()

        self.create_widgets()
        self.display_movies()

    def load_movies(self):
        if os.path.exists("movies.txt"):
            with open("movies.txt", "r") as file:
                for line in file:
                    if line.strip():
                        self.movies.append(line.strip().split(","))

    def save_movies(self):
        with open("movies.txt", "w") as file:
            for movie in self.movies:
                file.write(",".join(movie) + "\n")

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, height=10, width=50)
        self.listbox.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Movie", command=self.add_movie)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Movie", command=self.edit_movie)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Movie", command=self.delete_movie)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.search_button = tk.Button(self.button_frame, text="Search Movies", command=self.search_movies)
        self.search_button.grid(row=0, column=3, padx=5)

    def display_movies(self, movies=None):
        self.listbox.delete(0, tk.END)
        for movie in movies or self.movies:
            self.listbox.insert(tk.END, f"{movie[0]} ({movie[2]}) - {movie[3]} by {movie[1]}")

    def add_movie(self):
        title = simpledialog.askstring("Input", "Enter movie title:")
        director = simpledialog.askstring("Input", "Enter movie director:")
        year = simpledialog.askstring("Input", "Enter release year:")
        genre = simpledialog.askstring("Input", "Enter genre:")

        if title and director and year and genre:
            self.movies.append([title, director, year, genre])
            self.save_movies()
            self.display_movies()
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    def edit_movie(self):
        selected_movie_index = self.listbox.curselection()
        if selected_movie_index:
            selected_movie_index = selected_movie_index[0]
            movie = self.movies[selected_movie_index]

            title = simpledialog.askstring("Input", "Enter movie title:", initialvalue=movie[0])
            director = simpledialog.askstring("Input", "Enter movie director:", initialvalue=movie[1])
            year = simpledialog.askstring("Input", "Enter release year:", initialvalue=movie[2])
            genre = simpledialog.askstring("Input", "Enter genre:", initialvalue=movie[3])

            if title and director and year and genre:
                self.movies[selected_movie_index] = [title, director, year, genre]
                self.save_movies()
                self.display_movies()
            else:
                messagebox.showwarning("Input Error", "All fields are required.")
        else:
            messagebox.showwarning("Selection Error", "Please select a movie to edit.")

    def delete_movie(self):
        selected_movie_index = self.listbox.curselection()
        if selected_movie_index:
            selected_movie_index = selected_movie_index[0]
            del self.movies[selected_movie_index]
            self.save_movies()
            self.display_movies()
        else:
            messagebox.showwarning("Selection Error", "Please select a movie to delete.")

    def search_movies(self):
        search_term = simpledialog.askstring("Search", "Enter search term:")
        if search_term:
            search_results = [movie for movie in self.movies if search_term.lower() in " ".join(movie).lower()]
            if search_results:
                self.display_movies(search_results)
            else:
                messagebox.showinfo("Search Results", "No movies found matching the search term.")
        else:
            self.display_movies()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieDatabaseApp(root)
    root.mainloop()
