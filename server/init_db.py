from db import init_db, import_questions

def main():
    print("Initializing database...")
    init_db()
    print("Importing questions...")
    import_questions()
    print("Database setup complete!")

if __name__ == "__main__":
    main() 