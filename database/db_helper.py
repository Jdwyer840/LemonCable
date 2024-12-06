

class DBHelper:

    print()

    """DEMO CODE:
    
    from tinydb import TinyDB, Query

# Initialize database
db = TinyDB("gui_database.json")

# Add albums
albums_table = db.table("albums")
albums_table.insert({
    "album_1": {
        "title": "Back in Black",
        "artist": "AC/DC",
        "tracks": ["Hells Bells", "Shoot to Thrill"]
    },
    "album_2": {
        "title": "Highway to Hell",
        "artist": "AC/DC",
        "tracks": ["Highway to Hell", "If You Want Blood"]
    }
})

# Add GUI settings
settings_table = db.table("settings")
settings_table.insert({
    "theme": "dark",
    "volume": 75,
    "language": "en"
})

# Add user preferences
preferences_table = db.table("user_preferences")
preferences_table.insert({
    "favorite_artist": "AC/DC",
    "playback_speed": 1.0
})
    """