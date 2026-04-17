# SecureNotes Security Implementation Guide

This document explains the 5 major security features protecting the SecureNotes app in simple terms. It outlines what the risk is, how we fixed it, and exactly where you can find the coding logic.

---

### 1. Password Hashing
**What it means:** We never save your real password (like "password123") into the database. If a hacker ever steals the database file, they will only see a scrambled mathematical hash instead of your real text.
**How we did it:** We used a cryptographic library called `bcrypt` to mathematically scramble the password making it impossible to reverse or read. 
**Where the code is:** 
- Open **`app.py`** and look at the `/register` route: `hashed = bcrypt.generate_password_hash(password)`.
- Also in `/login`: `bcrypt.check_password_hash(...)`.

---

### 2. SQL Injection Prevention
**What it means:** Hackers often try to type malicious database commands (like `' OR '1'='1`) directly into the username or password boxes to trick the database into logging them in illegally as an admin.
**How we did it:** We used "Parameterized Queries." Instead of directly pasting exactly what the user types into our database command, we use safe placeholders (the `?` symbol). This forces the database to specifically treat the hacker's input strictly as regular plain text, not as an executable database command.
**Where the code is:** 
- Open **`database.py`**. Look inside every single function (like `create_user` and `get_user_by_username`). You will see questions marks like `VALUES (?, ?)` locking down the SQL code.

---

### 3. XSS (Cross-Site Scripting) Prevention
**What it means:** Hackers try to submit harmful HTML or hidden JavaScript code into a text field (like inside a Note). When you view that Note, the hidden script executes automatically (which could steal your session or show fake popups).
**How we did it:** We use the `bleach` library to aggressive "sanitize" and scrub away any HTML tags exactly at the moment you submit a note. We also rely on Jinja2 (the HTML template language) which automatically disables execution characters on the frontend visually.
**Where the code is:**
- Open **`app.py`** and look at the `/notes` POST route: `content = bleach.clean(content, tags=[], strip=True)`.

---

### 4. Session Management
**What it means:** After you log in, your browser gets a temporary "ticket" (a cookie) proving you are authenticated securely so you don't have to keep typing your password. If mismanaged, attackers can steal this ticket, or the browser's "back button" might show protected notes natively after you officially log out.
**How we did it:** We configured the Flask cookie system strictly. We set `HTTPONLY` so browser JavaScript cannot steal the cookie, and `SAMESITE` to prevent external websites from attacking your session. We also destroy the session dictionary entirely the moment you log out natively.
**Where the code is:**
- Open **`app.py`** at the very top: `app.config['SESSION_COOKIE_HTTPONLY'] = True`.
- In **`app.py`**, look at the `/logout` route: `session.clear()`.

---

### 5. Input Validation
**What it means:** We must explicitly measure and verify all data entering the system *before* trying to save it. If users type usernames that are too long, completely blank, or full of weird symbols, it can break the database or bypass protections.
**How we did it:** We use strict server-side Python checks and Regex pattern matching to enforce rigid boundaries, blocking bad data natively.
**Where the code is:**
- Open **`app.py`** and look at the `/register` route. You will see several sequence checks measuring array lengths (`len(password) < 8`) and strictly enforcing alphabetical symbols natively (`re.match('^[a-zA-Z0-9]+$', username)`).
- In the `/notes` route, it checks for completely empty string submissions and strictly limits maximum sizes heavily to 500 characters.
