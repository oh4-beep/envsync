# envsync

Securely share `.env` files with teammates using encryption and Firebase.

## Why this exists

Sharing `.env` files over Slack or email is a security risk. Git is not an option either. envsync encrypts your secrets locally before they ever leave your machine, pushes the encrypted blob to Firestore, and lets teammates pull and decrypt with a shared key.

## Install

```bash
pip install envsync
```

## Quickstart

**Step 1 - Set up on your machine:**
```bash
envsync init
```
You will be asked for a project name and the path to your Firebase service account JSON.

**Step 2 - Generate a secret key:**
```bash
envsync keygen
```
Copy the key and share it with your teammates securely (see below).

**Step 3 - Push your `.env` to Firestore:**
```bash
envsync push --key YOUR_KEY
```

**Step 4 - Teammate pulls and decrypts:**
```bash
envsync pull --key YOUR_KEY
```

**Check your current config:**
```bash
envsync status
```

## Config reference

envsync stores your config at `~/.envsync/config.toml`:

```toml
[settings]
project_name = "my-project"
service_account_path = "/absolute/path/to/serviceAccountKey.json"
```

The secret key is never stored here. You manage and share it yourself.

## How to share the key with teammates

Never share the key over Slack, email, or any chat tool. Use a password manager that supports secure sharing, such as 1Password, Bitwarden, or Dashlane. Send the key through the password manager's built-in share feature so it never appears in plaintext in a message thread.

## Security rules

- Your `.env` is encrypted locally before it is sent anywhere
- Firestore only ever holds the encrypted blob, which is useless without the key
- The key is your responsibility to share securely
- Never commit your service account JSON to git

## .gitignore warning

Add this to your `.gitignore` immediately:

```
.env
serviceAccountKey.json
*.json
```

The service account JSON gives full access to your Firebase project. Treat it like a password.

## License

MIT License

Copyright (c) 2026 Hillel Ilany Freedman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
