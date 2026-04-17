# SecureNotes Security Test Cases

---
Test ID: TC-01
Security Feature: Password Hashing
How to Test: Manual
Setup needed before test: Ensure the application is actively running on `http://127.0.0.1:5000`.
Steps:
  1. Open your browser and navigate to `http://127.0.0.1:5000/register`.
  2. Type the username `TestUser99`.
  3. Type the password `SecurePass123` into both password input fields and submit.
  4. Open a second terminal window inside your project folder and run the SQLite viewer.
Exact input to use: Registration Password: `SecurePass123` | Terminal Command: `sqlite3 securenotes.db "SELECT password_hash FROM users WHERE username='TestUser99';"`
Expected result: The terminal outputs a completely randomized cryptographic string (e.g., `$2b$12$...`). Notice the exact string `SecurePass123` is totally invisible.
Result: PASS / FAIL 
---

---
Test ID: TC-02
Security Feature: Password Hashing
How to Test: Manual
Setup needed before test: Ensure the account `TestUser99` exists from the previous step.
Steps:
  1. Stay in the web browser and browse to `http://127.0.0.1:5000/login`.
  2. Supply the valid registered username `TestUser99`.
  3. Provide an explicitly incorrect password block.
  4. Trigger the submission button natively.
Exact input to use: Username: `TestUser99` | Password: `WrongPassword000`
Expected result: Flask processes the hash asynchronously, triggers a comparison mismatch, and rigidly rejects your connection rendering "Invalid username or password" on the screen natively.
Result: PASS / FAIL 
---

---
Test ID: TC-03
Security Feature: SQL Injection Prevention
How to Test: Manual
Setup needed before test: Navigate to the login page cleanly.
Steps:
  1. Target URL: `http://127.0.0.1:5000/login`.
  2. Enter the widely used boolean SQL bypass payload exactly into the "Username" field.
  3. Set any arbitrary sequence in the password line.
  4. Click the "Login" button securely.
Exact input to use: Username field: `' OR '1'='1' --`
Expected result: The `?` parameterized SQLite execute function intercepts the command logically and checks the database for a literal username named ` ' OR '1'='1' -- ` which fails natively preventing injection.
Result: PASS / FAIL 
---

---
Test ID: TC-04
Security Feature: SQL Injection Prevention
How to Test: Manual
Setup needed before test: Provide fresh inputs at the login configuration.
Steps:
  1. Start squarely upon your `http://127.0.0.1:5000/login` interface.
  2. Provide an arbitrary string strictly on the username line.
  3. Copy the trailing inverted-quote exploit tightly into the lower "Password" section.
  4. Action the form.
Exact input to use: Password field: `admin' OR '1'='1`
Expected result: The connection falls securely backward rendering an "Invalid username or password" error. The trailing commas strictly fail bounding parameters rather than corrupting database logics.
Result: PASS / FAIL 
---

---
Test ID: TC-05
Security Feature: XSS Prevention
How to Test: Manual
Setup needed before test: Log in firmly to the application ensuring you are upon the `/notes` dashboard.
Steps:
  1. Position your cursor logically inside the large "Add a New Note" textarea frame at the top.
  2. Tightly input the Javascript execution block directly exactly as presented below.
  3. Issue the "Save Note" action dynamically.
Exact input to use: `<script>alert('You have been hacked!')</script>`
Expected result: Upon successful submission and layout reload, zero browser popups execute natively. The backend Bleach processor removes the `<script>` array or renders it innocuously as visible code printout.
Result: PASS / FAIL 
---

---
Test ID: TC-06
Security Feature: XSS Prevention
How to Test: Manual
Setup needed before test: Remain logged inside your personal `/notes` viewer interface.
Steps:
  1. Navigate to the fresh "Add a New Note" form submission array once again.
  2. Fill the textarea natively wielding advanced Image tag properties relying on missing origins to trigger an error execution loop natively.
  3. Action the interface.
Exact input to use: `<img src="x" onerror="alert('XSS Exploit Success')">`
Expected result: No alerts will trigger in your browser interface whatsoever. The `tags=[]` enforcement logic completely flushes the `<img>` syntax preventing external origin payloads entirely.
Result: PASS / FAIL 
---

---
Test ID: TC-07
Security Feature: Session Management
How to Test: Manual
Setup needed before test: Ensure you are authenticated smoothly reviewing real notes locally.
Steps:
  1. Navigate your mouse over to the top-right navigation array and locate "Logout".
  2. Select it to naturally purge operations redirecting back to `/login`.
  3. Target your web browser's overarching Localhost URL Address manipulation bar overhead.
Exact input to use: Replace the browser's URL directly to: `http://127.0.0.1:5000/notes` and forcefully hit Enter.
Expected result: The application explicitly blocks manual backdoor routings recognizing the local `session` dictionary acts empty; firing the `@login_required` block back to the `/login` handler.
Result: PASS / FAIL 
---

---
Test ID: TC-08
Security Feature: Session Management
How to Test: Manual
Setup needed before test: Log in directly natively into the dashboard arrays correctly initially.
Steps:
  1. Explicitly invoke the "Logout" logic manually via the application's top button.
  2. After traversing securely back onto `/login`, engage the exact specific physical "Back Arrow" inside the web browser's physical shell interface (Chrome/Safari directly).
Exact input to use: Only the browser's physical "← Back" History capability feature.
Expected result: The session has been cryptographically purged using `.clear()`. Protected dashboard resources are absolutely inaccessible preventing physical local-device caching vulnerabilities.
Result: PASS / FAIL 
---

---
Test ID: TC-09
Security Feature: Input Validation
How to Test: Manual
Setup needed before test: Reset to the registration form securely.
Steps:
  1. Traverse cleanly over to `http://127.0.0.1:5000/register`.
  2. Deploy a compliant test username like `JohnSmith123` uniformly.
  3. Inject precisely three characters natively targeting identically for "Password" / "Confirm".
  4. Submit execution arrays naturally.
Exact input to use: Set Password fields exclusively as: `abc`
Expected result: The system overrides the database handler catching the payload bounds and flashing the strictly requested "Password must be at least 8 characters." warning element securely.
Result: PASS / FAIL 
---

---
Test ID: TC-10
Security Feature: Input Validation
How to Test: Manual
Setup needed before test: Clean off the registration form endpoints securely.
Steps:
  1. Ensure you are targeting the exact endpoint `http://127.0.0.1:5000/register`.
  2. Intentionally hold the "Username" form block exactly vacant (blank space).
  3. Deploy standard acceptable parameters mapping into both of the underlying password scopes (`GoodPass123!`).
  4. Force browser submission triggers.
Exact input to use: Leave Username strictly blank (` `, empty, nothing).
Expected result: In the highly rare event your browser fails to flag HTML5 "Required" boundaries, the specific Flask logic traps the minimum bounds outputting: "Username must be 3 to 20 characters." safely preventing empty SQLite insertions.
Result: PASS / FAIL 
---

# Automated Testing with Semgrep

To complement these explicit manual test protocols, an automated scan targets logic structures before the compiler even initializes them locally using Semgrep.
From your overarching `securenotes` directory running exactly inside any integrated terminal panel:

```bash
semgrep --config auto .
```

*Semgrep algorithmically targets statically identifiable vulnerabilities securely checking your Python codebase directly against known CVE architectural weaknesses, explicitly locating unescaped outputs, misconfigured session constants, or loose formatting strings circumventing SQL endpoints heavily before deployment!*
