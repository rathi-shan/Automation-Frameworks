# MANUAL SETUP - Add These 5 GitHub Secrets

## Instructions to Add Secrets (Takes 2 minutes)

### Step 1: Go to GitHub Repository Settings
1. Open: https://github.com/rathi-shan/Automation-Frameworks
2. Click **Settings** (top right)
3. Click **Secrets and variables** (left sidebar)
4. Click **Actions**

### Step 2: Add Each Secret

Click **New repository secret** and add these 5 secrets one by one:

#### Secret 1
```
Name:  SMTP_HOST
Value: smtp.gmail.com
```

#### Secret 2
```
Name:  SMTP_PORT
Value: 587
```

#### Secret 3
```
Name:  SENDER_EMAIL
Value: rathi-sender@gmail.com
```

#### Secret 4
```
Name:  SENDER_PASSWORD
Value: 1my16app-password
```

#### Secret 5
```
Name:  RECIPIENT_EMAIL
Value: rathi.shan@gmail.com
```

### Step 3: Verify All Secrets Are Added

In the "Actions secrets" section, you should see all 5 secrets listed:
- ✓ SMTP_HOST
- ✓ SMTP_PORT
- ✓ SENDER_EMAIL
- ✓ SENDER_PASSWORD
- ✓ RECIPIENT_EMAIL

### Step 4: Done!

Once all 5 secrets are added, the pipeline will automatically trigger when code is pushed and send emails with test results.

---

## What Each Secret Does

| Secret | Purpose | Example |
|--------|---------|---------|
| SMTP_HOST | Email server hostname | smtp.gmail.com |
| SMTP_PORT | Email server port | 587 |
| SENDER_EMAIL | Email address to send from | rathi-sender@gmail.com |
| SENDER_PASSWORD | App password or SMTP password | 1my16app-password |
| RECIPIENT_EMAIL | Email to send reports to | rathi.shan@gmail.com |

---

## Troubleshooting

**Q: Where do I find the Settings tab?**
A: On your GitHub repo page, look for the tabs at the top: Code, Issues, Pull requests, **Settings**

**Q: Can I see my secrets after adding them?**
A: No, GitHub hides secret values for security. You'll only see dots (••••••••).

**Q: What if I make a mistake?**
A: Go back to Actions secrets and click the trash icon to delete, then add the correct one.

**Q: Can I test the secrets?**
A: Yes! Once added, push any commit to main branch and the pipeline will run with email notification.

---

## Next Steps

1. ✅ Add all 5 secrets to GitHub
2. ✅ Verify they appear in Actions secrets list
3. ✅ Push a commit (I'll do this automatically)
4. ✅ Wait 2-3 minutes
5. ✅ Check your email for test report!

