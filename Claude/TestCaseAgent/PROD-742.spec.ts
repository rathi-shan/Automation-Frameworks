import { test, expect } from '@playwright/test';

test.describe('Biometric Bi-weekly Authentication Bypass Lockout', () => {

  test('Successful FaceID login on the first attempt clears any prior failed attempt counter', async ({ page }) => {
    // Given the user has a registered FaceID profile linked to their mobile banking account
    // And the user has previously failed FaceID authentication 1 time
    // And the account is not currently locked
    await page.goto('/auth/faceid');
    await page.evaluate(() => {
      window.localStorage.setItem('faceid_fail_count', '1');
      window.localStorage.setItem('account_locked', 'false');
    });

    // When the user presents a valid biometric face scan
    await page.getByRole('button', { name: /scan face|authenticate with faceid/i }).click();
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('biometric:success')));

    // Then the application should authenticate the user successfully
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();

    // And the user should be granted access to the mobile banking dashboard
    await expect(page).toHaveURL(/dashboard/);

    // And the consecutive failed FaceID attempt counter should be reset to 0
    const failCount = await page.evaluate(() => window.localStorage.getItem('faceid_fail_count'));
    expect(failCount).toBe('0');

    // And no lockout warning notification should be dispatched
    await expect(page.getByRole('alert', { name: /lockout warning/i })).not.toBeVisible();
  });

  test('Successful FaceID login on the second attempt after one failure resets the counter', async ({ page }) => {
    // Given the user has a registered FaceID profile linked to their mobile banking account
    // And the user has previously failed FaceID authentication 1 time
    // And the account is not currently locked
    await page.goto('/auth/faceid');
    await page.evaluate(() => {
      window.localStorage.setItem('faceid_fail_count', '1');
      window.localStorage.setItem('account_locked', 'false');
    });

    // When the user presents a valid biometric face scan on the second attempt
    await page.getByRole('button', { name: /scan face|authenticate with faceid/i }).click();
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('biometric:success')));

    // Then the application should authenticate the user successfully
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();

    // And the user should be granted access to the mobile banking dashboard
    await expect(page).toHaveURL(/dashboard/);

    // And the consecutive failed FaceID attempt counter should be reset to 0
    const failCount = await page.evaluate(() => window.localStorage.getItem('faceid_fail_count'));
    expect(failCount).toBe('0');

    // And any pending lockout warning state should be cleared
    await expect(page.getByRole('alert', { name: /lockout/i })).not.toBeVisible();
  });

  test('System administrator successfully unlocks a locked account via the secure admin dashboard', async ({ page }) => {
    // Given a user account is currently locked due to 3 consecutive failed FaceID attempts
    await page.goto('/admin/dashboard');
    await page.evaluate(() => {
      window.localStorage.setItem('target_account_locked', 'true');
      window.localStorage.setItem('target_faceid_fail_count', '3');
    });

    // And a system administrator is authenticated on the secure admin dashboard
    await expect(page.getByRole('heading', { name: /admin dashboard/i })).toBeVisible();

    // When the administrator locates the locked user profile by account ID
    await page.getByLabel(/search account id/i).fill('TEST_ACCOUNT_001');
    await page.getByRole('button', { name: /search|find account/i }).click();
    await expect(page.getByTestId('user-profile-card')).toBeVisible();

    // And the administrator triggers the manual unlock override action
    await page.getByRole('button', { name: /unlock account|manual unlock override/i }).click();
    await page.getByRole('button', { name: /confirm/i }).click();

    // Then the user account status should be updated to unlocked
    await expect(page.getByTestId('account-status')).toHaveText(/unlocked|active/i);

    // And the consecutive failed FaceID attempt counter should be reset to 0
    await expect(page.getByTestId('faceid-fail-count')).toHaveText('0');

    // And the lockout timer should be cleared immediately
    await expect(page.getByTestId('lockout-timer')).not.toBeVisible();

    // And the user should be able to attempt FaceID authentication again
    const accountLocked = await page.evaluate(() => window.localStorage.getItem('target_account_locked'));
    expect(accountLocked).toBe('false');

    // And an audit log entry should be recorded capturing the administrator ID, timestamp, and override action
    await page.getByRole('link', { name: /audit log/i }).click();
    await expect(page.getByTestId('audit-log-entry').first()).toContainText(/unlock override/i);
    await expect(page.getByTestId('audit-log-entry').first()).toContainText(/admin/i);
    await expect(page.getByTestId('audit-log-timestamp').first()).toBeVisible();
  });

  test('Account lockout expires automatically after exactly 15 minutes and user can re-authenticate', async ({ page }) => {
    // Given a user account has been locked due to 3 consecutive failed FaceID attempts
    // And the lockout timer has been running for exactly 15 minutes
    await page.goto('/auth/faceid');
    await page.evaluate(() => {
      const lockoutStart = Date.now() - 15 * 60 * 1000;
      window.localStorage.setItem('account_locked', 'true');
      window.localStorage.setItem('faceid_fail_count', '3');
      window.localStorage.setItem('lockout_start_time', String(lockoutStart));
    });

    // When the lockout duration of 15 minutes elapses
    await page.reload();

    // Then the account should be automatically unlocked by the system
    await expect(page.getByTestId('account-status')).toHaveText(/unlocked|active/i);

    // And the consecutive failed FaceID attempt counter should be reset to 0
    const failCount = await page.evaluate(() => window.localStorage.getItem('faceid_fail_count'));
    expect(failCount).toBe('0');

    // And the user should be able to attempt FaceID authentication again without administrator intervention
    await expect(page.getByRole('button', { name: /scan face|authenticate with faceid/i })).toBeEnabled();
    await expect(page.getByTestId('lockout-message')).not.toBeVisible();
  });

  test('Warning push notification is dispatched on exactly the 2nd consecutive failed FaceID attempt', async ({ page }) => {
    // Given the user has a registered FaceID profile linked to their mobile banking account
    // And the user has previously failed FaceID authentication 1 time
    // And the account is not currently locked
    // And push notifications are enabled for the mobile banking application
    await page.goto('/auth/faceid');
    await page.evaluate(() => {
      window.localStorage.setItem('faceid_fail_count', '1');
      window.localStorage.setItem('account_locked', 'false');
      window.localStorage.setItem('push_notifications_enabled', 'true');
    });

    // When the user presents an invalid biometric face scan for the 2nd consecutive time
    await page.getByRole('button', { name: /scan face|authenticate with faceid/i }).click();
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('biometric:failure')));

    // Then the FaceID authentication should fail
    await expect(page.getByRole('alert', { name: /authentication failed/i })).toBeVisible();

    // And a warning push notification should be dispatched immediately to the user's registered device
    await expect(page.getByTestId('push-notification-indicator')).toBeVisible();

    // And the warning notification message should indicate that one more failed attempt will lock the account
    await expect(page.getByTestId('push-notification-message')).toContainText(/one more.*lock|1 more.*lock/i);

    // And the account should remain unlocked
    await expect(page.getByTestId('account-status')).not.toHaveText(/locked/i);

    // And the consecutive failed FaceID attempt counter should be incremented to 2
    await expect(page.getByTestId('faceid-fail-count')).toHaveText('2');
  });

  test('Account is locked immediately and precisely on the 3rd consecutive failed FaceID attempt', async ({ page }) => {
    // Given the user has a registered FaceID profile linked to their mobile banking account
    // And the user has previously failed FaceID authentication 2 consecutive times
    // And a warning push notification has already been dispatched
    // And the account is not currently locked
    await page.goto('/auth/faceid');
    await page.evaluate(() => {
      window.localStorage.setItem('faceid_fail_count', '2');
      window.localStorage.setItem('account_locked', 'false');
      window.localStorage.setItem('warning_notification_sent', 'true');
    });

    // When the user presents an invalid biometric face scan for the 3rd consecutive time
    await page.getByRole('button', { name: /scan face|authenticate with faceid/i }).click();
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('biometric:failure')));

    // Then the FaceID authentication should fail
    await expect(page.getByRole('alert', { name: /authentication failed/i })).toBeVisible();

    // And the account should be locked immediately
    await expect(page.getByTestId('account-status')).toHaveText(/locked/i);

    // And the 15-minute lockout countdown timer should start at the moment of the 3rd failure
    await expect(page.getByTestId('lockout-countdown-timer')).toBeVisible();

    // And the user should be presented with a message stating the account is locked for 15 minutes
    await expect(page.getByTestId('lockout-message')).toContainText(/locked.*15 minutes|15 minutes.*locked/i);

    // And the user should not be able to attempt FaceID authentication while the account is locked
    await expect(page.getByRole('button', { name: /scan face|authenticate with faceid/i })).toBeDisabled();

    // And the consecutive failed FaceID attempt counter should reflect 3 failed attempts
    await expect(page.getByTestId('faceid-fail-count')).toHaveText('3');
  });

  test('Account remains locked if the user attempts FaceID authentication before the 15-minute lockout expires', async ({ page }) => {
    // Given a user account has been locked due to 3 consecutive failed FaceID attempts
    // And the lockout timer has been running for only 7 minutes and 30 seconds
    await page.goto('/auth/faceid');
    await page.evaluate(() => {
      const lockoutStart = Date.now() - (7 * 60 + 30) * 1000;
      window.localStorage.setItem('account_locked', 'true');
      window.localStorage.setItem('faceid_fail_count', '3');
      window.localStorage.setItem('lockout_start_time', String(lockoutStart));
    });

    // When the user attempts FaceID authentication before the 15-minute lockout period has elapsed
    await page.getByRole('button', { name: /scan face|authenticate with faceid/i }).click();

    // Then the authentication attempt should be rejected without processing the biometric scan
    await expect(page.getByRole('alert', { name: /account locked/i })).