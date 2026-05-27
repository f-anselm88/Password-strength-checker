# 🔐 Password Strength Checker

A command-line Python application that evaluates password strength in real time, featuring a **visual ASCII strength meter** and **actionable improvement hints** — exceeding standard project requirements.

---

## Features

- ✅ Real-time ASCII strength meter that updates after every check
- ✅ Actionable hints that identify exactly what's weak (length, symbols, numbers, casing)
- ✅ Strength levels: **Weak → Fair → Strong → Very Strong**
- ✅ Clean, readable terminal output

---

## Demo

```
Enter a password to check: hello

Strength: [██░░░░░░░░] WEAK

 Hints to improve your password:
  → Add uppercase letters (e.g. A, B, C)
  → Add numbers (e.g. 1, 2, 3)
  → Add special characters (e.g. !, @, #)
  → Use at least 8 characters

Enter a password to check: Hello@2025!

Strength: [██████████] VERY STRONG ✓
```

---

## How to Run

**Requirements:** Python 3.x

```bash
# Clone the repository
git clone https://github.com/f-anselm88/password-strength-checker.git

# Navigate into the project
cd password-strength-checker

# Run the program
python password_strength.py
```

---

## How It Works

The program evaluates passwords against five criteria:

| Criterion | Requirement |
|-----------|-------------|
| Length | At least 8 characters |
| Uppercase | At least one uppercase letter |
| Lowercase | At least one lowercase letter |
| Numbers | At least one digit |
| Special Characters | At least one symbol (`!@#$%^&*`) |

Each passing criterion increases the strength score. The ASCII meter fills proportionally, and hints are generated only for failing criteria.

---

## What I Learned

- String analysis using Python's `re` module and built-in string methods
- Designing user-friendly CLI feedback loops
- Thinking beyond minimum requirements to improve user experience

---

## Author

**Anselm Munango**
[f-anselm88.github.io](https://f-anselm88.github.io) · [GitHub](https://github.com/f-anselm88) · [LinkedIn](https://linkedin.com/in/anselm-munango-bs) · [anselm.mu@gmail.com](mailto:anselm.mu@gmail.com)
