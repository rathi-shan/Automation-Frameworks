# Complete Email Notification System - Setup & Usage Guide

## System Overview

Your test automation pipeline now includes a complete email notification system that:
- Runs tests automatically on GitHub Actions
- Generates beautiful HTML reports
- Sends formatted emails with test results
- Attaches full Playwright HTML report
- Works with Gmail, Outlook, or any SMTP server

## What You Get

### 1. Automated Test Execution
- Tests run on every push to `main` branch
- Parallel execution on Node.js 18 and 20
- Mock server auto-starts before tests
- Results captured in JSON and HTML formats

### 2. Beautiful Email Reports
```
┌─────────────────────────────────┐
│  Test Execution Report          │
│  Status: PASSED                 │
│  Timestamp: 2026-06-21 15:09:00 │
├─────────────────────────────────┤
│  PASSED: 15  │  FAILED: 2       │
│  SKIPPED: 3  │  TOTAL: 20       │
├─────────────────────────────────┤
│  Test Results Table             │
│  ✓ Test 1 - 2.45s              │
│  ✗ Test 2 - 1.89s              │
│  ⊘ Test 3 - 0.00s              │
├─────────────────────────────────┤
│  Attachments:                   │
│  📎 index.html (Playwright)     │
└─────────────────────────────────┘
```

### 3. One-Time Setup
Configure 5 GitHub Secrets and you're done!

## Quick Start (5 Minutes)

### Step 1: Generate Email Credentials

**Option A: Gmail (Recommended)**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (custom name)"
3. Copy the 16-character password

**Option B: Outlook**
- Use your regular Outlook password
- SMTP: `smtp.office365.com`

**Option C: Custom SMTP**
- Get credentials from your email provider

### Step 2: Add GitHub Secrets

1. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add each:

```
Name: SMTP_HOST
Value: smtp.gmail.com

Name: SMTP_PORT
Value: 587

Name: SENDER_EMAIL
Value: your-email@gmail.com

Name: SENDER_PASSWORD
Value: xxxx xxxx xxxx xxxx

Name: RECIPIENT_EMAIL
Value: recipient@example.com
```

### Step 3: Done!

Next push to main branch will trigger the pipeline and send an email report.

## System Architecture

```
┌──────────────────┐
│  GitHub Push     │
│  (main branch)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│  GitHub Actions CI/CD            │
│  ├─ Setup Node.js 18 & 20        │
│  ├─ Setup Python 3.11            │
│  ├─ Install Dependencies         │
│  ├─ Start Mock Server            │
│  ├─ Run Playwright Tests         │
│  ├─ Generate Reports             │
│  └─ Send Email                   │
└────────┬─────────────────────────┘
         │
    ┌────┴─────┐
    │           │
    ▼           ▼
┌─────────┐  ┌──────────────────┐
│  Email  │  │  GitHub Reports  │
│ Report  │  │  - HTML Report   │
└─────────┘  │  - JSON Results  │
             │  - JUnit XML     │
             └──────────────────┘
```

## File Structure

```
TestCaseAgent/
├── .github/workflows/
│   └── test-automation.yml          ← Updated with email step
├── email_reporter.py                ← Email sender (NEW)
├── test-server.py                   ← Mock server
├── playwright.config.ts             ← Test configuration
├── PROD-742.spec.ts                 ← Test suite 1
├── coupon_validation.spec.ts        ← Test suite 2
├── EMAIL_QUICK_START.md             ← Quick reference (NEW)
├── EMAIL_SETUP_GUIDE.md             ← Detailed guide (NEW)
├── EMAIL_IMPLEMENTATION.md          ← System overview (NEW)
└── Readme.md                        ← Updated with pipeline
```

## Email Content Breakdown

### Header
- Status badge (PASSED/FAILED with color)
- Timestamp of test execution
- Repository URL
- Branch name

### Summary Statistics
Four colored cards showing:
- **Passed**: Count with green background
- **Failed**: Count with red background
- **Skipped**: Count with yellow background
- **Total**: Count with blue background

### Test Results Table
Columns:
1. **Test Name** - Full test description
2. **Suite** - Test group/describe
3. **Status** - Color-coded badge (PASS/FAIL/SKIP)
4. **Duration** - Execution time in seconds

### Attachments
- **index.html** - Full Playwright HTML report with:
  - Interactive test results
  - Screenshots on failure
  - Video recordings (if enabled)
  - Trace files for debugging

## Configuration Examples

### Gmail Setup
```
SMTP_HOST: smtp.gmail.com
SMTP_PORT: 587
SENDER_EMAIL: qa-team@gmail.com
SENDER_PASSWORD: abcd efgh ijkl mnop
RECIPIENT_EMAIL: team@company.com
```

### Outlook Setup
```
SMTP_HOST: smtp.office365.com
SMTP_PORT: 587
SENDER_EMAIL: qa@company.onmicrosoft.com
SENDER_PASSWORD: your-outlook-password
RECIPIENT_EMAIL: team@company.com
```

### Multiple Recipients
```
RECIPIENT_EMAIL: qa@company.com,manager@company.com,lead@company.com
```

## Workflow Execution

### When Tests Pass
```
✓ Tests run
✓ All pass
✓ Email sent: "Test Report - PASSED" (green)
✓ Summary shows: 20 Passed, 0 Failed, 0 Skipped
```

### When Tests Fail
```
✓ Tests run
✗ Some fail
✓ Email sent: "Test Report - FAILED" (red)
✓ Summary shows: 18 Passed, 2 Failed, 0 Skipped
✓ Failed tests highlighted in red
```

### When Tests Skip
```
✓ Tests run
⊘ Some skip (expected)
✓ Email sent: "Test Report - PASSED" (green if no failures)
✓ Skipped tests shown in yellow
```

## Local Testing

### Test Email Locally
```bash
# Set environment variables
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx
export RECIPIENT_EMAIL=recipient@example.com

# Run tests
npx playwright test

# Send email (uses test results)
python email_reporter.py
```

### Debug Email Sending
```bash
# Check if config is loaded
python -c "import os; print('SENDER_EMAIL:', os.getenv('SENDER_EMAIL'))"

# Test SMTP connection
python -c "
import smtplib
try:
    smtplib.SMTP('smtp.gmail.com', 587).starttls()
    print('SMTP connection OK')
except Exception as e:
    print('SMTP error:', e)
"
```

## Customization

### Change Email Template
Edit `email_reporter.py`, function `create_email_body()`:
- Modify colors (hex values like `#28a745`)
- Change fonts (Arial, Courier, etc.)
- Adjust spacing and padding
- Add company logo or branding

### Change Report Style
Edit `playwright.config.ts`:
```typescript
reporter: [
  ['html', { outputFolder: 'playwright-report' }],
  ['json', { outputFile: 'test-results/results.json' }],
  // Add more reporters as needed
]
```

### Conditional Email Sending
Edit `.github/workflows/test-automation.yml`:
```yaml
- name: Generate Email Report
  if: failure()  # Only on failure
  # or: if: success()  # Only on success
```

## Troubleshooting

### Email Not Received

**Check 1: Spam Folder**
- Email might be in spam/junk
- Add sender to contacts
- Mark as "not spam"

**Check 2: Recipient Email**
```bash
# Verify recipient email is correct
git log --grep="RECIPIENT_EMAIL" -n 1
echo $RECIPIENT_EMAIL  # Local testing
```

**Check 3: GitHub Secrets**
- Verify all 5 secrets are set
- No typos in secret names
- Values not truncated or modified

### SMTP Authentication Failed

**For Gmail:**
- Use 16-character app password (not regular password)
- No spaces in the password
- Ensure 2FA is enabled on account

**For Outlook:**
- Use regular Outlook password
- Verify email account is active
- Check if account has SMTP enabled

**For Custom SMTP:**
- Verify host and port from provider
- Test connection with `telnet`:
  ```bash
  telnet smtp.gmail.com 587
  ```

### Tests Not Running

**Check Mock Server:**
```bash
curl http://127.0.0.1:3000/health
# Should return: {"status":"ok"}
```

**Check Playwright Config:**
```bash
# Verify config syntax
npx playwright --version
npx playwright test --list
```

## Email Providers Guide

| Provider | SMTP Host | Port | Password Type |
|----------|-----------|------|---------------|
| Gmail | smtp.gmail.com | 587 | App password (16 char) |
| Outlook | smtp.office365.com | 587 | Regular password |
| Yahoo | smtp.mail.yahoo.com | 587 | App password |
| SendGrid | smtp.sendgrid.net | 587 | API key |
| Mailgun | smtp.mailgun.org | 587 | SMTP password |

## Security Best Practices

✅ **Use App Passwords** - More secure than regular passwords  
✅ **Enable 2FA** - Required for Gmail app passwords  
✅ **GitHub Secrets** - Never commit credentials  
✅ **TLS/STARTTLS** - Always use encrypted connections  
✅ **Rotate Passwords** - Change app passwords periodically  
✅ **Limit Recipients** - Only necessary team members  

## Next Steps

1. **[IMMEDIATE] Add 5 GitHub Secrets** (5 min)
   - Go to repo Settings → Secrets
   - Add each secret value

2. **[OPTIONAL] Test Locally** (5 min)
   - Set env vars
   - Run `python email_reporter.py`

3. **[OPTIONAL] Customize Email** (10 min)
   - Edit `email_reporter.py`
   - Adjust HTML template
   - Test with local run

4. **[VERIFY] Push & Check Email** (2 min)
   - Push to main branch
   - Wait 2 minutes
   - Check email inbox

## Monitoring & Maintenance

### Monitor Pipeline Health
- Go to: GitHub → **Actions** → **Test Automation Pipeline**
- Check latest runs
- Review failed tests
- Download reports

### Archive Reports
- GitHub keeps artifacts for 30 days
- Download important reports manually
- Store in archive folder for compliance

### Disable Email (Temporary)
Comment out in `.github/workflows/test-automation.yml`:
```yaml
# - name: Generate Email Report
#   ...
```

## Support Resources

| Document | Purpose | Size |
|----------|---------|------|
| EMAIL_QUICK_START.md | 5-minute setup | 2.5 KB |
| EMAIL_SETUP_GUIDE.md | Detailed guide | 7.5 KB |
| EMAIL_IMPLEMENTATION.md | System overview | 9 KB |
| email_reporter.py | Email sender code | 13 KB |

## FAQ

**Q: Do I need to configure email to run tests?**
A: No! Tests run without email. Email is optional. If secrets not set, pipeline continues without errors.

**Q: Can I send to multiple recipients?**
A: Yes! Use comma-separated emails: `qa@company.com,manager@company.com`

**Q: How often are tests run?**
A: Every time you push to `main` branch.

**Q: Can I manually trigger a test run?**
A: Yes! Use GitHub Actions "Run workflow" button (when we add manual trigger option).

**Q: How long are email reports kept?**
A: Indefinitely! They're stored in your email. GitHub keeps artifacts for 30 days.

**Q: Can I change the email format?**
A: Yes! Edit the HTML template in `email_reporter.py`.

**Q: What if tests are skipped?**
A: Email shows skipped count. Tests still report as skipped in the table.

## Success Checklist

After setup, verify:

- [ ] All 5 GitHub Secrets are set
- [ ] Pipeline runs on push to main
- [ ] Email received within 2 minutes
- [ ] Email contains test results
- [ ] HTML report attached
- [ ] Correct pass/fail counts
- [ ] Status badge shows correct color

---

**You're all set!** 

The email notification system is ready to use. Just add the 5 GitHub Secrets and you'll receive beautiful test reports via email after each test run.

For questions, refer to:
- **Quick Setup**: EMAIL_QUICK_START.md
- **Full Guide**: EMAIL_SETUP_GUIDE.md
- **System Details**: EMAIL_IMPLEMENTATION.md
