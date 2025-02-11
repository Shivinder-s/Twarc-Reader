from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import json

app = Flask(__name__)

# Database configuration
DATABASE = 'tweets.db'

def init_db():
    """Initialize the database and create tables."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            tweet_id TEXT,
            full_text TEXT,
            user_name TEXT,
            user_screen_name TEXT,
            in_reply_to_status_id TEXT,
            reply_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def save_tweet_to_db(tweet):
    """Save a single tweet to the database and update reply counts."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Save the tweet
    cursor.execute('''
        INSERT INTO tweets (created_at, tweet_id, full_text, user_name, user_screen_name, in_reply_to_status_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        tweet['created_at'],
        tweet['id_str'],
        tweet['full_text'],
        tweet['user']['name'],
        tweet['user']['screen_name'],
        tweet.get('in_reply_to_status_id', None)  # Use None if the field is missing
    ))

    # If this tweet is a reply, increment the reply count of the parent tweet
    if 'in_reply_to_status_id' in tweet and tweet['in_reply_to_status_id']:
        cursor.execute('''
            UPDATE tweets
            SET reply_count = reply_count + 1
            WHERE tweet_id = ?
        ''', (tweet['in_reply_to_status_id'],))

    conn.commit()
    conn.close()

def get_tweets(page=1, per_page=10, filters=None, sort_by=None):
    """Fetch tweets from the database with pagination, filtering, and sorting."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Base query
    query = 'SELECT created_at, full_text, user_name, user_screen_name, reply_count FROM tweets'
    params = []

    # Apply filters
    if filters:
        filter_conditions = []
        if 'start_date' in filters:
            filter_conditions.append('created_at >= ?')
            params.append(filters['start_date'])
        if 'end_date' in filters:
            filter_conditions.append('created_at <= ?')
            params.append(filters['end_date'])
        if 'day' in filters:
            filter_conditions.append("strftime('%w', created_at) = ?")
            params.append(str(filters['day']))
        if 'month' in filters:
            filter_conditions.append("strftime('%m', created_at) = ?")
            params.append(f"{filters['month']:02d}")
        if 'year' in filters:
            filter_conditions.append("strftime('%Y', created_at) = ?")
            params.append(str(filters['year']))
        if filter_conditions:
            query += ' WHERE ' + ' AND '.join(filter_conditions)

    # Apply sorting
    if sort_by == 'date_asc':
        query += ' ORDER BY created_at ASC'
    elif sort_by == 'date_desc':
        query += ' ORDER BY created_at DESC'
    elif sort_by == 'time_asc':
        query += ' ORDER BY strftime("%H:%M:%S", created_at) ASC'
    elif sort_by == 'time_desc':
        query += ' ORDER BY strftime("%H:%M:%S", created_at) DESC'

    # Add pagination
    offset = (page - 1) * per_page
    query += ' LIMIT ? OFFSET ?'
    params.extend([per_page, offset])

    cursor.execute(query, params)
    tweets = cursor.fetchall()
    conn.close()
    return tweets

def count_tweets(filters=None):
    """Count the total number of tweets in the database with optional filters."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = 'SELECT COUNT(*) FROM tweets'
    params = []

    if filters:
        filter_conditions = []
        if 'start_date' in filters:
            filter_conditions.append('created_at >= ?')
            params.append(filters['start_date'])
        if 'end_date' in filters:
            filter_conditions.append('created_at <= ?')
            params.append(filters['end_date'])
        if 'day' in filters:
            filter_conditions.append("strftime('%w', created_at) = ?")
            params.append(str(filters['day']))
        if 'month' in filters:
            filter_conditions.append("strftime('%m', created_at) = ?")
            params.append(f"{filters['month']:02d}")
        if 'year' in filters:
            filter_conditions.append("strftime('%Y', created_at) = ?")
            params.append(str(filters['year']))
        if filter_conditions:
            query += ' WHERE ' + ' AND '.join(filter_conditions)

    cursor.execute(query, params)
    total = cursor.fetchone()[0]
    conn.close()
    return total

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.jsonl'):
            for line in file:
                tweet = json.loads(line.decode('utf-8'))
                save_tweet_to_db(tweet)
            return redirect(url_for('upload_file'))
    return render_template('upload.html')

@app.route('/tweets')
def view_tweets():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Get filters from query parameters
    filters = {}
    if 'start_date' in request.args:
        filters['start_date'] = request.args['start_date']
    if 'end_date' in request.args:
        filters['end_date'] = request.args['end_date']
    if 'day' in request.args:
        filters['day'] = int(request.args['day'])
    if 'month' in request.args:
        filters['month'] = int(request.args['month'])
    if 'year' in request.args:
        filters['year'] = int(request.args['year'])

    # Get sorting option
    sort_by = request.args.get('sort_by')

    tweets = get_tweets(page, per_page, filters, sort_by)
    total_tweets = count_tweets(filters)
    total_pages = (total_tweets + per_page - 1) // per_page

    return render_template('tweets.html', tweets=tweets, page=page, total_pages=total_pages, filters=filters, sort_by=sort_by)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)