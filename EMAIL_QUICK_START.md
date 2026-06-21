# Email Notification Setup - Quick Start

## What Was Added

✅ **Email Report System** - Sends beautiful HTML reports with test results  
✅ **HTML Attachment** - Full Playwright report attached to email  
✅ **Summary Cards** - Visual pass/fail/skip statistics  
✅ **Automatic Trigger** - Runs after every test execution  

## Quick Setup (5 Minutes)

### 1. Get Email Credentials

**Gmail Users:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate an app password for "Mail"
3. Copy the 16-character password

**Outlook Users:**
- Use your regular Outlook password
- SMTP Host: `smtp.office365.com`

### 2. Add GitHub Secrets

Go to: **GitHub Repo** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 5 secrets:

| Secret | Value |
|--------|-------|
| `SMTP_HOST` | `smtp.gmail.com` (or your SMTP host) |
| `SMTP_PORT` | `587` |
| `SENDER_EMAIL` | Your email address |
| `SENDER_PASSWORD` | 16-char app password (no spaces) |
| `RECIPIENT_EMAIL` | Where to send reports |

### 3. Done! 

Next time tests run, email report will be sent automatically.

## Files Added

- **email_reporter.py** - Generates and sends HTML emails
- **EMAIL_SETUP_GUIDE.md** - Detailed configuration guide
- **.github/workflows/test-automation.yml** - Updated with email step

## Test Email

To test locally:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=your-app-password
export RECIPIENT_EMAIL=recipient@example.com

python email_reporter.py
```

## Email Contents

The email includes:
- **Header** - Status (PASSED/FAILED) with timestamp
- **Summary** - 4 cards showing: Passed, Failed, Skipped, Total
- **Details** - Table with all test names, suites, status, duration
- **Attachment** - Full HTML report from Playwright
- **Repository Info** - GitHub repo and branch info

## Troubleshooting

**"Email configuration incomplete"** 
→ Check that all 5 secrets are set in GitHub

**"SMTP Authentication failed"** 
→ For Gmail, use 16-char app password (not regular password)

**"Email not received"** 
→ Check spam folder or verify recipient email is correct

See `EMAIL_SETUP_GUIDE.md` for more details.

## Next Steps

1. Configure the 5 GitHub Secrets
2. Commit and push (will trigger pipeline)
3. Check your email for the test report!
4. Customize email template if needed (in email_reporter.py)

---

For full documentation, see: **EMAIL_SETUP_GUIDE.md**
