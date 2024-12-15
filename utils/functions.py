import sqlite3

def save_complaint(name, location, complaint, emotion_level, resolution, topic):
    conn = sqlite3.connect("complaints.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO complaints (name, location, complaint, emotion_level, resolution, topic) VALUES (?, ?, ?, ?, ?, ?)",
              (name, location, complaint, emotion_level, resolution, topic))
    conn.commit()
    conn.close()
