```typescript
import { test, expect } from '@playwright/test';

test.describe('Biometric Bi-weekly Authentication Bypass Lockout', () => {

  test('Successful FaceID login on the first attempt clears any prior failed attempt counter', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('faceid-status')).toHaveText('0');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();
    await page.getByTestId('biometric-result').selectOption('success');
    await page.getByRole('button', { name: /submit biometric/i }).click();

    await expect(page).toHaveURL(/dashboard/);
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('0');
    await expect(page.getByTestId('account-lockout-status')).not.toHaveText(/locked/i);
  });

  test('Successful FaceID login after 1 prior failed attempt resets the failure counter', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('faceid-status')).toHaveText('1');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();
    await page.getByTestId('biometric-result').selectOption('success');
    await page.getByRole('button', { name: /submit biometric/i }).click();

    await expect(page).toHaveURL(/dashboard/);
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('0');
    await expect(page.getByTestId('account-lockout-status')).not.toHaveText(/locked/i);
    await expect(page.getByTestId('push-notification-warning')).not.toBeVisible();
  });

  test('Successful FaceID login after 2 prior failed attempts resets the failure counter', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('faceid-status')).toHaveText('2');
    await expect(page.getByTestId('warning-notification-sent')).toHaveText('true');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();
    await page.getByTestId('biometric-result').selectOption('success');
    await page.getByRole('button', { name: /submit biometric/i }).click();

    await expect(page).toHaveURL(/dashboard/);
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('0');
    await expect(page.getByTestId('account-lockout-status')).not.toHaveText(/locked/i);
  });

  test('System administrator successfully unlocks a locked account via the secure admin dashboard', async ({ page }) => {
    await page.goto('/admin/dashboard');

    await expect(page.getByTestId('admin-auth-status')).toHaveText('authenticated');

    await page.getByLabel(/account id/i).fill('LOCKED_USER_ACCOUNT_ID');
    await page.getByRole('button', { name: /search/i }).click();

    await expect(page.getByTestId('user-account-status')).toHaveText('locked');
    await expect(page.getByTestId('lockout-active-duration')).toBeVisible();

    await page.getByRole('button', { name: /manual override unlock/i }).click();
    await page.getByRole('button', { name: /confirm unlock/i }).click();

    await expect(page.getByTestId('user-account-status')).toHaveText('unlocked');
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('0');
    await expect(page.getByTestId('lockout-timer')).not.toBeVisible();

    await expect(page.getByTestId('audit-log-entry')).toBeVisible();
    await expect(page.getByTestId('audit-log-admin-id')).not.toBeEmpty();
    await expect(page.getByTestId('audit-log-timestamp')).not.toBeEmpty();
    await expect(page.getByTestId('audit-log-action')).toHaveText(/manual override unlock/i);

    await page.goto('/mobile-banking/login');
    await expect(page.getByRole('button', { name: /authenticate with face id/i })).toBeEnabled();
  });

  test('Account locks after exactly 3 consecutive failed FaceID attempts', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('faceid-status')).toHaveText('2');
    await expect(page.getByTestId('warning-notification-sent')).toHaveText('true');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();
    await page.getByTestId('biometric-result').selectOption('failure');
    await page.getByRole('button', { name: /submit biometric/i }).click();

    await expect(page.getByTestId('account-lockout-status')).toHaveText('locked');
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('3');
    await expect(page.getByTestId('lockout-duration-minutes')).toHaveText('15');

    await expect(
      page.getByText('Your account has been locked due to multiple failed login attempts. Please try again in 15 minutes.')
    ).toBeVisible();

    await expect(page).not.toHaveURL(/dashboard/);
    await expect(page.getByRole('main', { name: /banking dashboard/i })).not.toBeVisible();
  });

  test('Warning push notification is dispatched on exactly the 2nd consecutive failed FaceID attempt', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('faceid-status')).toHaveText('1');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();
    await page.getByTestId('biometric-result').selectOption('failure');
    await page.getByRole('button', { name: /submit biometric/i }).click();

    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('2');
    await expect(page.getByTestId('push-notification-warning')).toBeVisible();
    await expect(page.getByTestId('push-notification-message')).toHaveText(
      'Warning: One more failed Face ID attempt will lock your account.'
    );
    await expect(page.getByTestId('account-lockout-status')).not.toHaveText(/locked/i);
    await expect(page.getByRole('button', { name: /authenticate with face id/i })).toBeEnabled();
  });

  test('No warning push notification is dispatched on the 1st failed FaceID attempt', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('faceid-status')).toHaveText('0');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();
    await page.getByTestId('biometric-result').selectOption('failure');
    await page.getByRole('button', { name: /submit biometric/i }).click();

    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('1');
    await expect(page.getByTestId('push-notification-warning')).not.toBeVisible();
    await expect(page.getByTestId('account-lockout-status')).not.toHaveText(/locked/i);
    await expect(page.getByRole('button', { name: /authenticate with face id/i })).toBeEnabled();
  });

  test('Locked account automatically unlocks after exactly 15 minutes and resets the failure counter', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('account-lockout-status')).toHaveText('locked');
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('3');
    await expect(page.getByTestId('lockout-timer-started')).not.toBeEmpty();

    await page.getByTestId('simulate-time-elapsed').fill('15');
    await page.getByRole('button', { name: /simulate time elapsed/i }).click();

    await expect(page.getByTestId('account-lockout-status')).toHaveText('unlocked');
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('0');
    await expect(page.getByRole('button', { name: /authenticate with face id/i })).toBeEnabled();
    await expect(page.getByTestId('admin-intervention-required')).not.toBeVisible();
  });

  test('Locked account remains locked if fewer than 15 minutes have elapsed', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('account-lockout-status')).toHaveText('locked');
    await expect(page.getByTestId('lockout-active-seconds')).toHaveText('899');

    await page.getByRole('button', { name: /authenticate with face id/i }).click();

    await expect(page).not.toHaveURL(/dashboard/);
    await expect(page.getByRole('main', { name: /banking dashboard/i })).not.toBeVisible();
    await expect(page.getByTestId('remaining-lockout-message')).toBeVisible();
    await expect(page.getByTestId('remaining-lockout-message')).toContainText(/remaining/i);
    await expect(page.getByTestId('account-lockout-status')).toHaveText('locked');
  });

  test('FaceID failure counter does not increment beyond 3 while account is locked', async ({ page }) => {
    await page.goto('/mobile-banking/login');

    await expect(page.getByTestId('account-lockout-status')).toHaveText('locked');
    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('3');
    await expect(page.getByTestId('lockout-active-minutes')).toHaveText('5');

    for (let i = 0; i < 3; i++) {
      await page.getByRole('button', { name: /authenticate with face id/i }).click();
      await expect(page.getByTestId('lockout-message')).toBeVisible();
      await expect(page.getByTestId('lockout-message')).toContainText(/locked/i);
    }

    await expect(page.getByTestId('failed-attempt-counter')).toHaveText('3');
    await expect(page.getByTestId('push-notification-warning')).not.toBeVisible();
    await expect(page.getByTestId('lockout-timer-reset')).not.toHaveText('true');
  });

  test('Unauthorized user cannot access the admin unlock override without valid admin credentials', async ({ page }) => {
    await page.goto('/admin/dashboard/unlock');

    await expect(page).not.toHaveURL(/admin\/dashboard/);
    await expect(page.getByRole('heading', { name: /access denied/i })).toBeVisible();

    await expect(page.getByTestId('security-audit-unauthorized-attempt')).toBeVisible();

    await page.goto('/mobile-banking/login');
    await expect(page.getByRole('button', { name: /authenticate with face id/i })).toBeVisible();
  });

});
```