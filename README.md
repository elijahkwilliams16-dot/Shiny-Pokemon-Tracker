# ✨ Shiny Pokémon Tracker

A web-based Pokémon shiny tracker built with **Python, Flask, PostgreSQL, and PokéAPI**.

The project started as a command-line application using a JSON file and was later converted into a full web application with a relational database. The goal is to create a fast, scalable, and user-friendly way to keep track of shiny Pokémon caught across different Pokémon games.

---

## 🚀 Features

- ✨ Add shiny Pokémon to your collection
- 🎮 Record the game where each shiny was caught
- 🔎 Search your collection by Pokémon name
- 🧩 Filter shinies by game
- 🧬 Filter shinies by generation
- 📅 Record the date a Pokémon was caught
- 🎯 Record the shiny hunting method used
- 🖼️ Automatically retrieve Pokémon sprites from PokéAPI
- ✨ Retrieve game-specific shiny sprites when available
- 🔤 Pokémon name autocomplete
- 🚫 Prevent duplicate shiny Pokémon entries for the same game
- 📊 Display collection statistics
- 🗑️ Delete shiny Pokémon from the collection
- 🗄️ Store collection data using PostgreSQL

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- SQLAlchemy

### Frontend
- HTML
- CSS
- JavaScript
- Jinja2 templates

### API
- PokéAPI

### Development Tools
- Git
- GitHub
- pgAdmin
- VS Code

---

## 📁 Project Structure

```text
Shiny-Pokemon-Tracker/
│
├── static/
│   ├── pokemon_names.json
│   └── style.css
│
├── templates/
│   ├── add.html
│   └── index.html
│
├── .env
├── .gitignore
├── app.py
├── config.py
├── extensions.py
├── get_pokemon_names.py
├── models.py
├── README.md
├── shinies.json
└── tracker.py
```

### Important files

**`app.py`**  
Main Flask application. Handles routes, database queries, adding Pokémon, deleting Pokémon, searching, and filtering.

**`models.py`**  
Contains the SQLAlchemy database models:

- `Pokemon`
- `Game`
- `Shiny`

**`config.py`**  
Loads database configuration and environment variables.

**`extensions.py`**  
Creates the Flask-SQLAlchemy database extension.

**`tracker.py`**  
Contains Pokémon API functionality, game/generation information, validation, and sprite retrieval.

**`templates/`**  
Contains the HTML pages used by Flask.

**`static/`**  
Contains CSS and the locally stored Pokémon name list used by the autocomplete feature.

**`get_pokemon_names.py`**  
Utility script that downloads Pokémon species names from PokéAPI and saves them to `static/pokemon_names.json`.

**`.env`**  
Stores local environment variables such as PostgreSQL credentials.

> `.env` should never be committed to GitHub.

---

## 🗄️ Database

The application uses **PostgreSQL** as its database.

The database currently contains three main tables:

### Pokémon

Stores information about Pokémon.

```text
Pokemon
├── id
├── pokedex_id
├── name
├── generation
├── sprite_url
└── shiny_sprite_url
```

### Games

Stores Pokémon games.

```text
Game
├── id
├── name
└── generation
```

### Shinies

Stores individual shiny Pokémon records.

```text
Shiny
├── id
├── pokemon_id
├── game_id
├── method
├── date_caught
└── shiny_sprite_url
```

The `Shiny` table connects Pokémon and games using foreign keys.

---

## 🔗 Relationships

The database uses relationships between the tables:

```text
Pokemon
   │
   │
   └──────< Shiny >────── Game
```

This allows multiple shiny records to reference the same Pokémon and multiple shiny records to reference the same game.

For example:

```text
Charizard
   │
   ├── Charizard → Pokémon Red
   ├── Charizard → Pokémon Sun
   └── Charizard → Pokémon Violet
```

---

## 🌐 PokéAPI

The application uses **PokéAPI** to retrieve Pokémon information.

When a Pokémon is added, the application can retrieve:

- Pokédex number
- Pokémon generation
- Normal sprite
- Shiny sprite
- Game-specific shiny sprite

Pokémon names used for autocomplete are downloaded separately and stored locally in:

```text
static/pokemon_names.json
```

This prevents the application from making an API request every time a user types into the Pokémon search box.

---

## 🔎 Search and Filtering

The homepage supports server-side searching and filtering.

Users can:

### Search by Pokémon

For example:

```text
Char
```

can find:

```text
Charmander
Charmeleon
Charizard
```

### Filter by game

For example:

```text
Pokémon Sun
```

### Filter by generation

For example:

```text
Generation 7
```

Multiple filters can be combined.

The filtering is performed through PostgreSQL rather than downloading the entire collection and filtering it in the browser.

---

## 💻 Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd Shiny-Pokemon-Tracker
```

---

### 2. Create a virtual environment

```bash
py -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure PostgreSQL

Create a PostgreSQL database and configure the connection information in your local `.env` file.

Example structure:

```text
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
```

Do **not** commit your `.env` file.

---

### 5. Generate the Pokémon name list

If `static/pokemon_names.json` does not exist, run:

```bash
py get_pokemon_names.py
```

---

### 6. Start the Flask application

```bash
py app.py
```

The application should then be available locally at:

```text
http://127.0.0.1:5000
```

---

## 🔐 Environment Variables

The application uses environment variables for database credentials.

These values should not be hard-coded into the application.

The `.env` file is intended for local development and should be excluded from Git using `.gitignore`.

For deployment, environment variables will be configured through the hosting environment instead of committing credentials to the repository.

---

## ☁️ Deployment

The long-term goal is to deploy the Shiny Pokémon Tracker to **Amazon Web Services (AWS)**.

The planned architecture is:

```text
                 Internet
                    │
                    ▼
             AWS Web Server
                    │
                    ▼
             Flask Application
                    │
                    ▼
          AWS PostgreSQL Database
```

The local PostgreSQL database will remain available for development while the production application uses a cloud-hosted database.

Future deployment improvements may include:

- Production WSGI server
- AWS hosting
- Managed PostgreSQL
- Environment variables
- HTTPS
- Custom domain
- Automated deployment

---

## 🔮 Future Features

Planned features include:

### User Accounts

Allow multiple users to create their own collections.

```text
User
 │
 └── Collection
      ├── Pokémon
      ├── Games
      └── Shinies
```

### Statistics Dashboard

Potential statistics include:

- Total shinies
- Shinies by generation
- Shinies by game
- Most common hunting methods
- Shinies caught over time

### Better Search

Potential improvements:

- Sort by Pokémon
- Sort by date
- Sort by game
- Sort by generation
- More advanced filters

### Shiny Hunting Statistics

Potential features:

- Encounter counts
- Estimated odds
- Hunts completed
- Average encounters
- Longest hunt
- Shortest hunt

### User Experience

Future improvements may include:

- Improved mobile design
- Animations
- Favorites
- Collection progress
- Pokémon completion tracking
- Better error messages

---

## 📚 What I Learned

This project has been used to practice and learn:

- Python
- Flask
- HTML
- CSS
- JavaScript
- REST APIs
- PostgreSQL
- SQL
- SQLAlchemy
- Relational database design
- Foreign keys
- Database relationships
- Server-side filtering
- Environment variables
- Git and GitHub
- Web application architecture
- Cloud deployment

The project is also an opportunity to practice building a complete application independently, from a command-line program to a web application and eventually a cloud-hosted service.

---

## 🎯 Project Goal

The goal of the Shiny Pokémon Tracker is to evolve from a simple personal project into a complete web application that can support multiple users and larger collections.

The current version focuses on establishing a solid foundation with:

**Flask + PostgreSQL + PokéAPI**

Future versions will build on this foundation with authentication, user-specific collections, statistics, and cloud deployment.

---

## 📌 Project Status

**Current status:** Active development

### Completed

- [x] Original command-line tracker
- [x] JSON data storage
- [x] Flask web application
- [x] PostgreSQL database
- [x] SQLAlchemy models
- [x] Pokémon API integration
- [x] Pokémon autocomplete
- [x] Game-specific sprites
- [x] Search
- [x] Game filtering
- [x] Generation filtering
- [x] Delete functionality
- [x] Collection statistics

### In Progress

- [ ] Production error handling
- [ ] Database constraint improvements
- [ ] Production testing
- [ ] AWS deployment
- [ ] Production PostgreSQL database

### Future

- [ ] User accounts
- [ ] Authentication
- [ ] User-specific collections
- [ ] Statistics dashboard
- [ ] Advanced shiny hunting statistics
- [ ] Improved mobile experience
- [ ] Custom domain
- [ ] Automated deployment