import sqlite3
import pandas as pd
from parsers.sentiment_parser import SentimentParser
from parsers.llm_parser import LLMParser
from datetime import datetime

class Database:

    def __init__(self, path= "data/data.db"):
        """
        Constructor for Database
        Arguments:
            path - path to db
        """
        self.path = path
        self._init_db()

    def _init_db(self):
        """
        Initializes the DB if it doesnt exist
        """
        with sqlite3.connect(self.path) as conn:
            # Raw table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uri TEXT UNIQUE,
                    query TEXT,
                    author TEXT,
                    content TEXT,
                    created_at TEXT,
                    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """)
            # Sentiment table
            conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiment (
                id INTEGER PRIMARY KEY,
                uri TEXT UNIQUE,
                query TEXT,
                content TEXT,
                sentiment TEXT,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            # LLM parsed table
            conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_validated (
                id INTEGER PRIMARY KEY,
                uri TEXT UNIQUE,
                query TEXT,
                content TEXT,
                sentiment TEXT,
                correct_context TEXT,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()
        
    def add_posts(self, posts):
        """
        Adds posts to the posts table of the DB
        """
        query = """
            INSERT OR IGNORE INTO posts (uri, query, author, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.executemany(query, posts)
            conn.commit()

        # Creating the sentiment table
        self._generate_sentiment_table()
        # Validating the sentiment table
        self._generate_sentiment_validated_table()
        

    def get_posts(self, query):
        """
        Retrieves posts from the posts table of the DB for a given query
        Arguments:
            query - query to search by
        """
        db_query = f"""
        SELECT id, uri, query, author, content, created_at, fetched_at
        FROM posts
        WHERE query = ?
        ORDER BY id DESC
        """
        with sqlite3.connect(self.path) as conn:
            data = pd.read_sql_query(db_query, conn, params=(query,))
        return data

    def _generate_sentiment_table(self):
        """
        Creates the sentiment table
        """
        query = """
        SELECT p.id, p.uri, p.query, p.content
        FROM posts p
        LEFT JOIN sentiment s on p.id = s.id
        WHERE s.id IS NULL
        """
        with sqlite3.connect(self.path) as conn:
            df_posts = pd.read_sql_query(query, conn)
        
        if df_posts.empty:
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Generating post sentiment...")
        df_posts['sentiment'] = df_posts['content'].apply(lambda x: SentimentParser(x))
        df_sentiment = df_posts[['id', 'uri', 'query', 'content', 'sentiment']]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Sentiment calculated!")

        with sqlite3.connect(self.path) as conn:
            df_sentiment.to_sql('sentiment', conn, if_exists= 'append', index= False)
        
    def _generate_sentiment_validated_table(self):
        '''
        Creates the sentiment validated table
        '''
        query = """
        SELECT s.id, s.uri, s.query, s.content, s.sentiment
        FROM sentiment s
        LEFT JOIN sentiment_validated sv on s.id = sv.id
        WHERE sv.id IS NULL
        """
        with sqlite3.connect(self.path) as conn:
            df_sentiment = pd.read_sql_query(query, conn)

        if df_sentiment.empty:
            return
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Validating context of posts...")
        df_sentiment['correct_context'] = df_sentiment.apply(lambda row: LLMParser(row['query'], row['content']), axis= 1)
        df_validated = df_sentiment[['id', 'uri', 'query', 'content', 'sentiment', 'correct_context']]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Post context validated!")

        with sqlite3.connect(self.path) as conn:
            df_validated.to_sql('sentiment_validated', conn, if_exists= 'append', index= False)
            

        
