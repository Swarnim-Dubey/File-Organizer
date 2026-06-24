# 📂 Automated File Organizer

An automated Python application that monitors a folder (such as **Downloads**) in real time and automatically organizes files into categorized folders based on their file extensions.

---

## 📌 Features

-  Monitors a folder continuously
-  Detects newly added files in real time
-  Sorts files based on their extensions, like .pdf, .xl, .ppt, etc.
-  Creates folders automatically if they don't exist
-  Prevents duplicate filename conflicts
-  Easy to customize with your own categories

---

## 🛠️ Technologies Used

- Python 3.x
- `os`
- `shutil`
- `pathlib`
- `watchdog`

---

🚀 Installation


### 1. Clone the Repository

```bash
git clone https://github.com/Swarnim-Dubey/File-Organizer.git
```

### 2. Move into the Project Folder

```bash
cd File-Organizer
```

### 3. Create a Virtual Environment (Recommended)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

```bash
uv run main.py
```

The application will start monitoring the configured folder and automatically organize files.

---

## 📖 How It Works

1. User starts the application.
2. The program watches a specified folder.
3. A new file is detected.
4. The file extension is identified.
5. If the destination folder does not exist, it is created.
6. The file is moved to its respective category.
7. The application continues monitoring for new files.

---

## 📚 Learning Outcomes 

* Python File Handling
* Working with Directories
* Object-Oriented Programming (OOP)
* Exception Handling
* Modular Programming
* Real-time File Monitoring
* Python Packages
* Virtual Environments
* Clean Code Practices

---

## Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a new branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Added a new feature"
```

4. Push to your branch.

```bash
git push origin feature-name
```

5. Create a Pull Request.

##
