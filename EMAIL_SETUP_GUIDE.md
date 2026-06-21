# Email Report Setup Guide

This document explains how to configure email notifications for test results with HTML report attachments.

## Overview

The test automation pipeline can send automated email reports with:
- ✅ **Beautiful HTML Summary** - Visual test results with pass/fail/skip counts
- 📊 **Detailed Test Breakdown** - Individual test results with duration
- 📎 **HTML Report Attachment** - Full Playwright HTML report
- 🎨 **Color-coded Status** - Green for passed, red for failed, yellow for skipped
- 📧 **Automatic Notifications** - Triggered after every test run

## Prerequisites

1. **Email Account** - Gmail, Outlook, or any SMTP-compatible email provider
2. **GitHub Secrets** - For storing sensitive credentials
3. **SMTP Credentials** - Host, port, email, and password

## Configuration Steps

### Step 1: Generate Email Credentials

**For Gmail:**
1. Enable 2-Factor Authentication on your Gmail account
2. Go to https://myaccount.google.com/apppasswords
3. Create an "App password" for "Mail" and "Other (custom name)"
4. Copy the 16-character password generated

**For Outlook/Office365:**
1. Use your regular Outlook password
2. SMTP Host: `smtp.office365.com`
3. Port: `587`

**For Custom SMTP Server:**
- Use your SMTP provider's credentials
- Note the host, port, sender email, and password

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

| Secret Name | Value | Example |
|---|---|---|
| `SMTP_HOST` | Your SMTP server host | `smtp.gmail.com` |
| `SMTP_PORT` | Your SMTP server port | `587` |
| `SENDER_EMAIL` | Email to send from | `your-email@gmail.com` |
| `SENDER_PASSWORD` | App password or SMTP password | `xxxx xxxx xxxx xxxx` |
| `RECIPIENT_EMAIL` | Email to send reports to | `recipient@example.com` |

### Step 3: Verify Configuration

Add these secrets one by one and verify each is properly saved:

```bash
# In GitHub repo settings, you should see all 5 secrets listed
SENDER_EMAIL
SENDER_PASSWORD
SMTP_HOST
SMTP_PORT
RECIPIENT_EMAIL
```

## How It Works

### Local Development

Test the email setup locally:

```bash
# Set environment variables
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=your-app-password
export RECIPIENT_EMAIL=recipient@example.com

# Run tests
npx playwright test

# Send email report
python email_reporter.py
```

### CI/CD Pipeline

The workflow automatically:
1. Runs all Playwright tests
2. Generates JSON and HTML reports
3. Parses test results
4. Creates a beautiful HTML email summary
5. Attaches the full Playwright HTML report
6. Sends email to recipient

## Email Report Contents

### Header Section
- **Status Badge** - PASSED (green) or FAILED (red)
- **Timestamp** - When the tests ran
- **Repository** - GitHub repo info
- **Branch** - Which branch triggered the tests

### Summary Section
- **Passed Count** - Green box with number
- **Failed Count** - Red box with number
- **Skipped Count** - Yellow box with number
- **Total Count** - Blue box with total tests

### Test Details Table
| Column | Content |
|--------|---------|
| Test Name | Full name of the test |
| Suite | Test suite/describe block |
| Status | Color-coded PASS/FAIL/SKIP badge |
| Duration | Test execution time in seconds |

### Attachments
- **index.html** - Full Playwright HTML report with:
  - Video recordings (if enabled)
  - Screenshots on failure
  - Full test logs
  - Trace files for debugging

## Troubleshooting

### "Email configuration incomplete" Warning

**Cause:** One or more email secrets are missing

**Solution:**
1. Go to GitHub repo Settings → Secrets
2. Verify all 5 secrets are present:
   - SMTP_HOST
   - SMTP_PORT
   - SENDER_EMAIL
   - SENDER_PASSWORD
   - RECIPIENT_EMAIL

### "SMTP Authentication failed"

**Cause:** Incorrect email credentials

**Solution:**
- For Gmail: Use 16-character app password (not regular password)
- For Outlook: Ensure account supports SMTP
- For custom SMTP: Verify host and port with provider

### "Email not received"

**Cause:** Email might be in spam/junk folder

**Solution:**
1. Check spam/junk folder
2. Add sender email to contacts
3. Verify recipient email is correct

### "Connection timeout"

**Cause:** SMTP server not reachable or port blocked

**Solution:**
1. Verify SMTP_HOST and SMTP_PORT are correct
2. Check firewall rules
3. Try alternate port (465 for TLS, 587 for STARTTLS)

## Gmail App Password Setup (Step-by-Step)

1. Go to https://myaccount.google.com/security
2. Find **2-Step Verification** and enable it if not already done
3. Go to https://myaccount.google.com/apppasswords
4. Select:
   - App: **Mail**
   - Device: **Other (custom name)** → Type "GitHub Actions"
5. Click **Generate**
6. Copy the 16-character password (with spaces)
7. Add to GitHub Secret as `SENDER_PASSWORD`

## Customizing the Email Template

Edit `email_reporter.py` to customize the email:

```python
# In create_email_body() method:
- Modify colors (e.g., #28a745 for green)
- Change fonts or styling
- Add company logo or branding
- Adjust layout and spacing
```

## Disabling Email Reports

If you don't want to send emails:

1. Option A: Don't set the email secrets (pipeline skips email silently)
2. Option B: Comment out email step in `.github/workflows/test-automation.yml`:
```yaml
# - name: Generate Email Report
#   if: always()
#   ...
```

## Examples

### Example 1: Gmail Setup

```
SMTP_HOST: smtp.gmail.com
SMTP_PORT: 587
SENDER_EMAIL: qa-team@gmail.com
SENDER_PASSWORD: abcd efgh ijkl mnop
RECIPIENT_EMAIL: team@company.com
```

### Example 2: Office 365 Setup

```
SMTP_HOST: smtp.office365.com
SMTP_PORT: 587
SENDER_EMAIL: qa@company.onmicrosoft.com
SENDER_PASSWORD: your-office-password
RECIPIENT_EMAIL: team@company.com
```

### Example 3: Multiple Recipients

For multiple recipients, comma-separate in RECIPIENT_EMAIL:
```
RECIPIENT_EMAIL: team@company.com,qa-manager@company.com
```

## Best Practices

1. ✅ **Use App Passwords** - More secure than regular passwords
2. ✅ **Enable 2FA** - Required for Gmail app passwords
3. ✅ **Review Reports Regularly** - Check email for trends
4. ✅ **Monitor Failures** - Set up branch protection to require passing tests
5. ✅ **Archive Reports** - Download artifacts from GitHub for records

## Security Considerations

1. **Never commit secrets** - Always use GitHub Secrets
2. **Rotate passwords** - Change app passwords periodically
3. **Limit recipient scope** - Send only to necessary team members
4. **Review logs** - Check GitHub Actions logs for errors (don't save in logs!)
5. **Use SMTP TLS** - Ensure secure connection with port 587

## Additional Resources

- [Playwright HTML Report](https://playwright.dev/docs/test-reporters#html-reporter)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [SMTP Configuration Guide](https://support.google.com/mail/answer/7126229)

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review `email_reporter.py` for detailed error messages
3. Check GitHub Actions workflow logs for debugging
4. Enable test retries in `playwright.config.ts`
