Shiny Pokémon Tracker

A full-stack Python web application for tracking shiny Pokémon across every Pokémon game.

This project started as a command-line application and has evolved into a Flask-powered website that allows users to manage their shiny Pokémon collection through a browser. It also integrates with the PokéAPI to validate Pokémon names and automatically display official shiny artwork.

Features
Add shiny Pokémon through a web interface
View your entire shiny collection
Delete shiny entries
Automatically determine the Pokémon generation from the selected game
Display official shiny artwork using PokéAPI
Validate Pokémon names before saving
Store collection data locally using JSON
View statistics from the terminal version (with plans to bring these to the website)
Technologies Used
Python
Flask
HTML
CSS
JSON
Requests
PokéAPI
Git & GitHub
Project Structure
Shiny-Pokemon-Tracker/
│
├── app.py              # Flask web application
├── tracker.py          # Core application logic & PokéAPI integration
├── shinies.json        # Local database
│
├── templates/
│   ├── index.html
│   └── add.html
│
├── static/
│   └── style.css
│
└── README.md
Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/Shiny-Pokemon-Tracker.git

Move into the project folder:

cd Shiny-Pokemon-Tracker

Install dependencies:

pip install flask requests

Run the application:

python app.py

Open your browser and visit:

http://127.0.0.1:5000
Current Features
Web-based shiny tracker
Automatic PokéAPI validation
Official shiny Pokémon artwork
Add new shiny entries
Delete entries
JSON data persistence
Automatic generation detection
Planned Features
Search and filter Pokémon
Sort by game, generation, date, or method
Statistics dashboard
Charts and graphs
SQLite database
User accounts and cloud saves
AI-powered collection insights
Responsive mobile design
Collection progress tracker
Dark mode
Edit existing entries
Pokémon encounter method analytics
Learning Goals

This project was built to strengthen my skills in:

Python programming
Object-oriented and modular design
REST API integration
Flask web development
HTML & CSS
Data management with JSON
Version control using Git and GitHub
Building a complete software project outside the classroom
Acknowledgements

Pokémon data and artwork are provided by the excellent PokéAPI:

https://pokeapi.co/

Pokémon is © Nintendo, Game Freak, and Creatures Inc. This project is a non-commercial educational fan project.

Author

Elijah Williams