"""
Mock Test Server for Playwright E2E Tests
Provides endpoints needed by PROD-742 and coupon_validation tests
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Test Mock Server")

# ==========================================
# MOBILE BANKING LOGIN PAGE
# ==========================================
@app.get('/mobile-banking/login', response_class=HTMLResponse)
async def mobile_banking_login():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Mobile Banking Login</title></head>
    <body>
        <h1>Sign In</h1>
        <div data-testid="failed-attempt-counter">0</div>
        <div data-testid="account-status">active</div>
        <button role="button" name="authenticate with face id">Authenticate with FaceID</button>
        <select data-testid="faceid-result">
            <option value="success">Success</option>
            <option value="failure">Failure</option>
        </select>
        <button role="button" name="confirm authentication">Confirm Authentication</button>
        <div data-testid="push-notifications-status">enabled</div>
        <div data-testid="push-notification-warning" style="display:none;">Warning</div>
        <div data-testid="push-notification-lockout" style="display:none;">Lockout</div>
        <div data-testid="lockout-message" style="display:none;">Account Locked</div>
        <div data-testid="lockout-timer">15:00</div>
        <div data-testid="lockout-remaining-time">14:59</div>
        <div data-testid="lockout-duration">15:00</div>
        <div data-testid="faceid-scan-processed" style="display:none;">Scanned</div>
    </body>
    </html>
    """

# ==========================================
# ADMIN DASHBOARD
# ==========================================
@app.get('/admin/dashboard', response_class=HTMLResponse)
async def admin_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Admin Dashboard</title></head>
    <body>
        <h1>Admin Dashboard</h1>
        <input type="text" aria-label="Admin Username" />
        <input type="password" aria-label="Admin Password" />
        <button role="button" name="log in">Log In</button>
        <input type="text" placeholder="Search user by name or ID" />
        <button role="button" name="search">Search</button>
        <div data-testid="user-profile-card" style="display:none;">User Profile</div>
        <div data-testid="account-status">locked</div>
        <button role="button" name="manual override unlock">Manual Override Unlock</button>
        <button role="button" name="confirm unlock">Confirm Unlock</button>
        <a role="link" name="audit log">Audit Log</a>
        <div data-testid="audit-log-entry" style="display:none;">Audit Entry</div>
        <div data-testid="audit-log-timestamp" style="display:none;">2026-06-21T15:00:00Z</div>
        <div data-testid="lockout-timer">0:00</div>
        <div data-testid="failed-attempt-counter">0</div>
    </body>
    </html>
    """

# ==========================================
# CHECKOUT PAGE
# ==========================================
@app.get('/checkout', response_class=HTMLResponse)
async def checkout():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Checkout</title></head>
    <body>
        <h1>Checkout</h1>
        <input type="text" placeholder="Coupon code" />
        <button role="button" name="apply">Apply</button>
        <div data-testid="coupon-success-message" style="display:none;">Coupon Applied</div>
        <div data-testid="coupon-error-message" style="display:none;">Error</div>
        <div data-testid="discount-amount">$0.00</div>
        <div data-testid="order-total">$100.00</div>
        <div data-testid="denim-jacket-discount" style="display:none;">$9.00</div>
        <div data-testid="clearance-shirt-price" style="display:none;">$15.00</div>
    </body>
    </html>
    """

# ==========================================
# CART PAGE
# ==========================================
@app.get('/cart', response_class=HTMLResponse)
async def cart():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Shopping Cart</title></head>
    <body>
        <h1>Shopping Cart</h1>
        <div>Running Shoes</div>
        <div>$80.00</div>
        <div>Water Bottle</div>
        <div>$20.00</div>
        <div>Yoga Mat</div>
        <div>$50.00</div>
        <div>Denim Jacket</div>
        <div>$60.00</div>
        <div>Clearance Shirt</div>
        <div>$15.00</div>
        <div>Socks</div>
        <div>$10.00</div>
        <div>Headband</div>
        <div>$15.00</div>
        <div data-testid="cart-subtotal">$100.00</div>
    </body>
    </html>
    """

# ==========================================
# HOME / LANDING PAGE
# ==========================================
@app.get('/', response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Home</title></head>
    <body>
        <h1>Welcome</h1>
        <a role="link" name="sign in">Sign In</a>
        <a role="link" name="log in">Log In</a>
        <div class="status">premium</div>
        <div class="status">standard</div>
    </body>
    </html>
    """

# ==========================================
# LOGIN PAGE
# ==========================================
@app.get('/login', response_class=HTMLResponse)
async def login_page():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Login</title></head>
    <body>
        <h1>Sign In</h1>
        <input type="email" aria-label="Email" />
        <input type="password" aria-label="Password" />
        <button role="button" name="sign in">Sign In</button>
        <button role="button" name="log in">Log In</button>
    </body>
    </html>
    """

# ==========================================
# DASHBOARD
# ==========================================
@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Dashboard</title></head>
    <body>
        <h1>Dashboard</h1>
    </body>
    </html>
    """

# ==========================================
# HEALTH CHECK
# ==========================================
@app.get('/health')
async def health():
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=3000)
