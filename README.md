Certainly! Below is a **README.md** file for the **Twarc Reader** project. This file provides an overview of the project, instructions for setting it up, and details about its features.

---

# Twarc Reader

**Twarc Reader** is a web application built with **Flask** that allows users to upload JSONL files containing tweet data, view the tweets, and apply filters and sorting options. It also includes a **dark mode** toggle and supports **reply detection** to count the number of replies for each tweet.

---

## Features

1. **Upload JSONL Files**:
   - Upload JSONL files containing tweet data.
   - Store tweets in a SQLite database.

2. **View Tweets**:
   - Display tweets with user details, tweet text, and timestamps.
   - Show the number of replies for each tweet.

3. **Filtering and Sorting**:
   - Filter tweets by date, day, month, and year.
   - Sort tweets by date (oldest/newest) or time (earliest/latest).

4. **Dark Mode**:
   - Toggle between light and dark modes.
   - Persistent dark mode preference using `localStorage`.

5. **Reply Detection**:
   - Identify replies using the `in_reply_to_status_id` field.
   - Count and display the number of replies for each tweet.

6. **Responsive Design**:
   - Clean and modern UI inspired by Apple's website.
   - Fully responsive for desktop and mobile devices.

---

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask (`pip install flask`)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/twarc-reader.git
   cd twarc-reader
   ```

2. **Install Dependencies**:
   ```bash
   pip install flask
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   - Open your browser and go to `http://127.0.0.1:5000`.

---

## Project Structure

```
twarc_reader/
│
├── app.py                  # Flask application
├── templates/              # HTML templates
│   ├── upload.html         # Upload page
│   └── tweets.html         # Tweets page
├── tweets.db               # SQLite database
└── README.md               # Project documentation
```

---

## Usage

### Upload JSONL Files

1. Go to the **Upload Tweets** page.
2. Select a JSONL file containing tweet data.
3. Click **Upload** to process the file and store the tweets in the database.

### View Tweets

1. Go to the **View Tweets** page.
2. Use the filters and sorting options to customize the view:
   - **Date Range**: Filter tweets by start and end dates.
   - **Day**: Filter tweets by day of the week.
   - **Month**: Filter tweets by month.
   - **Year**: Filter tweets by year.
   - **Sort By**: Sort tweets by date or time.
3. Click **Apply** to update the results.

### Dark Mode

- Click the **☀️/🌙** button in the top-right corner to toggle between light and dark modes.

  
---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## Acknowledgments

- Inspired by **Twarc** for JSONL tweet data.
- UI design inspired by **Apple's website**.

---

## Contact

For questions or feedback, please contact:

- **Shivinder**  
- **Email**: me@shivindersharma.com  
- **GitHub**: [Twarc-Reader](https://github.com/Shivinder-s/Twarc-Reader)

---

Enjoy using **Twarc Reader**! 🚀

---
