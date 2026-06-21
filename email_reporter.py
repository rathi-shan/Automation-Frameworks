"""
Email Reporter - Sends test results via email with HTML report attached
Supports both local SMTP and GitHub Actions environments
"""
import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class EmailReporter:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', '')
        self.test_results_dir = 'test-results'
        self.report_dir = 'playwright-report'
        
    def parse_test_results(self) -> Tuple[int, int, int, List[Dict]]:
        """Parse Playwright test results from JSON"""
        results_file = Path(self.test_results_dir) / 'results.json'
        
        if not results_file.exists():
            return 0, 0, 0, []
        
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            passed = sum(1 for s in data.get('suites', []) 
                        for t in s.get('tests', []) if t.get('status') == 'passed')
            failed = sum(1 for s in data.get('suites', []) 
                        for t in s.get('tests', []) if t.get('status') == 'failed')
            skipped = sum(1 for s in data.get('suites', []) 
                         for t in s.get('tests', []) if t.get('status') == 'skipped')
            
            tests = []
            for suite in data.get('suites', []):
                for test in suite.get('tests', []):
                    tests.append({
                        'name': test.get('title', 'Unknown'),
                        'status': test.get('status', 'unknown'),
                        'duration': test.get('duration', 0),
                        'suite': suite.get('title', 'Suite'),
                    })
            
            return passed, failed, skipped, tests
        except Exception as e:
            print(f"Error parsing results: {e}")
            return 0, 0, 0, []
    
    def create_email_body(self, passed: int, failed: int, skipped: int, 
                         tests: List[Dict], repo_url: str = '', 
                         branch: str = '') -> str:
        """Create HTML email body with test summary"""
        
        status_color = '#28a745' if failed == 0 else '#dc3545'
        status_text = 'PASSED' if failed == 0 else 'FAILED'
        total = passed + failed + skipped
        
        test_rows = ''
        for test in tests:
            if test['status'] == 'passed':
                badge = '<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">PASS</span>'
            elif test['status'] == 'failed':
                badge = '<span style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">FAIL</span>'
            else:
                badge = '<span style="background-color: #ffc107; color: black; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">SKIP</span>'
            
            duration_ms = test.get('duration', 0)
            duration_sec = f"{duration_ms / 1000:.2f}s" if duration_ms else 'N/A'
            
            test_rows += f'''
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{test['name']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{test['suite']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{badge}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{duration_sec}</td>
            </tr>
            '''
        
        repo_info = f'<p><strong>Repository:</strong> {repo_url}</p>' if repo_url else ''
        branch_info = f'<p><strong>Branch:</strong> {branch}</p>' if branch else ''
        
        html_body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .header {{ background-color: {status_color}; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .header p {{ margin: 5px 0 0 0; font-size: 16px; }}
                .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
                .summary-item {{ background-color: #f9f9f9; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #007bff; }}
                .summary-item h3 {{ margin: 0 0 5px 0; color: #666; font-size: 12px; text-transform: uppercase; }}
                .summary-item .number {{ font-size: 24px; font-weight: bold; color: #333; }}
                .summary-item.passed {{ border-left-color: #28a745; }}
                .summary-item.failed {{ border-left-color: #dc3545; }}
                .summary-item.skipped {{ border-left-color: #ffc107; }}
                .summary-item.total {{ border-left-color: #007bff; }}
                .details {{ margin: 20px 0; }}
                .details h2 {{ color: #333; font-size: 18px; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th {{ background-color: #007bff; color: white; padding: 10px; text-align: left; font-weight: bold; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px; }}
                .button {{ display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 10px; }}
                .info {{ background-color: #e7f3ff; border-left: 4px solid #007bff; padding: 10px; margin: 10px 0; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Test Execution Report</h1>
                    <p>Status: {status_text}</p>
                </div>
                
                <div class="info">
                    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    {repo_info}
                    {branch_info}
                </div>
                
                <div class="summary">
                    <div class="summary-item passed">
                        <h3>Passed</h3>
                        <div class="number">{passed}</div>
                    </div>
                    <div class="summary-item failed">
                        <h3>Failed</h3>
                        <div class="number">{failed}</div>
                    </div>
                    <div class="summary-item skipped">
                        <h3>Skipped</h3>
                        <div class="number">{skipped}</div>
                    </div>
                    <div class="summary-item total">
                        <h3>Total</h3>
                        <div class="number">{total}</div>
                    </div>
                </div>
                
                <div class="details">
                    <h2>Test Results</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Test Name</th>
                                <th>Suite</th>
                                <th style="text-align: center;">Status</th>
                                <th style="text-align: right;">Duration</th>
                            </tr>
                        </thead>
                        <tbody>
                            {test_rows}
                        </tbody>
                    </table>
                </div>
                
                <div class="footer">
                    <p>This is an automated test report. Please do not reply to this email.</p>
                    <p>Detailed HTML report is attached to this email.</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        return html_body
    
    def send_email(self, subject: str, html_body: str, attachments: List[str] = None):
        """Send email with attachments"""
        
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("⚠️  Email configuration incomplete. Skipping email sending.")
            print(f"   SENDER_EMAIL: {bool(self.sender_email)}")
            print(f"   SENDER_PASSWORD: {bool(self.sender_password)}")
            print(f"   RECIPIENT_EMAIL: {bool(self.recipient_email)}")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            
            # Attach HTML body
            message.attach(MIMEText(html_body, 'html'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._attach_file(message, file_path)
            
            # Send email
            print(f"📧 Connecting to {self.smtp_host}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print("✅ Email sent successfully!")
            return True
        
        except smtplib.SMTPAuthenticationError:
            print("❌ SMTP Authentication failed. Check credentials.")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach a file to email message"""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            file_name = os.path.basename(file_path)
            part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
            message.attach(part)
            print(f"   ✓ Attached: {file_name}")
        except Exception as e:
            print(f"   ✗ Failed to attach {file_path}: {e}")
    
    def generate_and_send_report(self, repo_url: str = '', branch: str = ''):
        """Main method to generate and send report"""
        print("\n" + "="*60)
        print("TEST REPORT EMAIL GENERATOR")
        print("="*60)
        
        # Parse results
        passed, failed, skipped, tests = self.parse_test_results()
        
        print(f"\n📊 Test Summary:")
        print(f"   ✓ Passed: {passed}")
        print(f"   ✗ Failed: {failed}")
        print(f"   ⊘ Skipped: {skipped}")
        print(f"   Total: {passed + failed + skipped}")
        
        # Create email body
        status = "PASSED" if failed == 0 else "FAILED"
        subject = f"🧪 Test Report - {status}"
        html_body = self.create_email_body(passed, failed, skipped, tests, repo_url, branch)
        
        # Prepare attachments
        attachments = []
        index_file = Path(self.report_dir) / 'index.html'
        if index_file.exists():
            attachments.append(str(index_file))
        
        # Send email
        print("\n📧 Sending Email Report...")
        success = self.send_email(subject, html_body, attachments)
        
        print("\n" + "="*60)
        return success

def main():
    """Main entry point"""
    repo_url = os.getenv('GITHUB_REPOSITORY', 'rathi-shan/Automation-Frameworks')
    branch = os.getenv('GITHUB_REF_NAME', 'main')
    
    reporter = EmailReporter()
    success = reporter.generate_and_send_report(repo_url, branch)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
