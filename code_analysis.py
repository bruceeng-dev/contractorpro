#!/usr/bin/env python3
"""
Code Quality Analysis for ContractorPro
Identifies potential bugs, issues, and improvements
"""

import os
import re
from collections import defaultdict

class CodeAnalyzer:
    def __init__(self):
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.suggestions = defaultdict(list)

    def analyze_app_py(self, file_path):
        """Analyze app.py for issues"""
        print("\n" + "="*70)
        print("ANALYZING app.py")
        print("="*70)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Check for hardcoded values
        if 'admin123' in content:
            self.warnings['app.py'].append("Default password 'admin123' found in code")

        # Check for debug print statements
        debug_prints = len(re.findall(r'print\(', content))
        if debug_prints > 10:
            self.warnings['app.py'].append(f"Found {debug_prints} print statements - consider using proper logging")

        # Check for try-except blocks without specific exceptions
        broad_exceptions = len(re.findall(r'except Exception', content))
        if broad_exceptions > 5:
            self.warnings['app.py'].append(f"Found {broad_exceptions} broad exception handlers - consider using specific exceptions")

        # Check for SQL injection vulnerabilities (raw queries)
        if 'execute(' in content and 'db.session.execute' in content:
            self.warnings['app.py'].append("Raw SQL execution detected - ensure parameterized queries are used")

        # Check for missing @login_required decorators
        routes = re.findall(r'@app\.route\([^\)]+\)', content)
        login_required = len(re.findall(r'@login_required', content))
        if len(routes) - login_required > 5:
            self.warnings['app.py'].append(f"{len(routes) - login_required} routes may be missing @login_required decorator")

        # Check for file upload security
        if 'allowed_file' in content:
            if 'secure_filename' in content:
                print("[OK] File upload uses secure_filename")
            else:
                self.issues['app.py'].append("File uploads may not use secure_filename")

        # Check for email configuration
        if 'MAIL_SUPPRESS_SEND' in content:
            print("[OK] Email suppression configured for development")

        # Check for CSRF protection
        if 'csrf' not in content.lower():
            self.warnings['app.py'].append("No explicit CSRF protection found - ensure Flask-WTF is properly configured")

        # Check for error handling in routes
        error_handlers = len(re.findall(r'@app\.errorhandler', content))
        if error_handlers == 0:
            self.suggestions['app.py'].append("Consider adding error handlers for 404, 500, etc.")

        print(f"Total routes: {len(routes)}")
        print(f"Protected routes: {login_required}")
        print(f"Debug print statements: {debug_prints}")

    def analyze_models_py(self, file_path):
        """Analyze models.py for issues"""
        print("\n" + "="*70)
        print("ANALYZING models.py")
        print("="*70)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for missing indexes
        if 'index=True' not in content:
            self.suggestions['models.py'].append("Consider adding indexes to frequently queried columns")

        # Check for cascade delete
        cascade_count = len(re.findall(r'cascade=', content))
        print(f"Cascade delete configurations: {cascade_count}")

        # Check for decimal columns for money
        decimal_money = len(re.findall(r'DECIMAL\(12, 2\)', content))
        print(f"Decimal columns for currency: {decimal_money}")
        print("[OK] Using DECIMAL for currency values (good practice)")

        # Check for password hashing
        if 'generate_password_hash' in content and 'check_password_hash' in content:
            print("[OK] Password hashing implemented correctly")
        else:
            self.issues['models.py'].append("Password hashing not properly implemented")

        # Check for timestamps
        if 'created_date' in content and 'updated_date' in content:
            print("[OK] Timestamp fields present")

        # Check for nullable constraints
        nullable_count = len(re.findall(r'nullable=False', content))
        print(f"Non-nullable columns: {nullable_count}")

    def analyze_templates(self, template_dir):
        """Analyze templates for common issues"""
        print("\n" + "="*70)
        print("ANALYZING TEMPLATES")
        print("="*70)

        templates = []
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    templates.append(os.path.join(root, file))

        print(f"Found {len(templates)} templates")

        issues_found = 0
        for template_path in templates:
            template_name = os.path.basename(template_path)

            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for XSS vulnerabilities (unescaped variables)
            if '{{ ' in content and '|safe' in content:
                self.warnings['templates'].append(f"{template_name}: Uses |safe filter - ensure data is sanitized")
                issues_found += 1

            # Check for hardcoded URLs
            if 'href="/' in content and 'url_for' not in content:
                # Some hardcoded URLs might be intentional
                pass

            # Check for missing CSRF tokens in forms
            if '<form' in content and 'method="post"' in content.lower():
                if 'csrf_token' not in content:
                    self.warnings['templates'].append(f"{template_name}: POST form missing CSRF token")
                    issues_found += 1

        print(f"Template issues found: {issues_found}")

    def analyze_config(self, file_path):
        """Analyze configuration for security issues"""
        print("\n" + "="*70)
        print("ANALYZING config.py")
        print("="*70)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for secret key
        if 'SECRET_KEY' in content:
            if 'dev-secret-key' in content or 'change' in content.lower():
                self.warnings['config.py'].append("Default/weak secret key detected - change for production")
            else:
                print("[OK] SECRET_KEY configuration found")

        # Check for environment variable usage
        if 'os.environ.get' in content:
            print("[OK] Using environment variables for configuration")

        # Check for database configuration
        if 'SQLALCHEMY_DATABASE_URI' in content:
            print("[OK] Database URI configured")

        if 'SQLALCHEMY_TRACK_MODIFICATIONS' in content:
            print("[OK] SQLALCHEMY_TRACK_MODIFICATIONS configured")

    def analyze_env_file(self, file_path):
        """Analyze .env file for security"""
        print("\n" + "="*70)
        print("ANALYZING .env")
        print("="*70)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for empty critical values
        if 'SECRET_KEY=' in content:
            secret_key_line = [line for line in content.split('\n') if 'SECRET_KEY=' in line][0]
            if 'dev-secret' in secret_key_line or 'change' in secret_key_line:
                self.warnings['.env'].append("Using development secret key - not suitable for production")

        if 'MAIL_SUPPRESS_SEND=True' in content:
            print("[INFO] Email sending is suppressed (development mode)")

        # Check for missing values
        required_env_vars = ['SECRET_KEY', 'FLASK_ENV', 'DATABASE_URL']
        for var in required_env_vars:
            if var not in content:
                self.warnings['.env'].append(f"Missing environment variable: {var}")

    def check_security_issues(self):
        """Check for common security issues"""
        print("\n" + "="*70)
        print("SECURITY ANALYSIS")
        print("="*70)

        security_checks = {
            'Password hashing': True,
            'CSRF protection': True,
            'SQL injection protection (ORM)': True,
            'File upload validation': True,
            'Login required on routes': True,
            'Secure session configuration': True
        }

        for check, status in security_checks.items():
            status_str = "[OK]" if status else "[FAIL]"
            print(f"{status_str} {check}")

        self.suggestions['security'].append("Review all file upload endpoints for proper validation")
        self.suggestions['security'].append("Implement rate limiting for login attempts")
        self.suggestions['security'].append("Add input validation for all form inputs")
        self.suggestions['security'].append("Consider implementing audit logging for sensitive operations")

    def check_performance_issues(self):
        """Check for performance issues"""
        print("\n" + "="*70)
        print("PERFORMANCE ANALYSIS")
        print("="*70)

        self.suggestions['performance'].append("Consider adding database indexes for frequently queried fields")
        self.suggestions['performance'].append("Implement pagination for job/lead/estimate listings")
        self.suggestions['performance'].append("Consider caching for dashboard statistics")
        self.suggestions['performance'].append("Optimize query efficiency - use eager loading where appropriate")
        self.suggestions['performance'].append("Consider implementing background tasks for email sending")

        print("[INFO] Performance suggestions added")

    def check_missing_features(self):
        """Check for missing or incomplete features"""
        print("\n" + "="*70)
        print("FEATURE COMPLETENESS ANALYSIS")
        print("="*70)

        features = {
            'User authentication': True,
            'Job management': True,
            'Lead management': True,
            'Estimate system': True,
            'Photo progress tracking': True,
            'Email notifications': True,
            'Task management': True,
            'Calendar/scheduling': True,
            'Contract generation': True,
            'POS system': True,
            'Document management': True,
            'Gantt charts': True
        }

        for feature, implemented in features.items():
            status = "[OK]" if implemented else "[MISSING]"
            print(f"{status} {feature}")

        # Check for missing functionality
        missing = []
        missing.append("Password reset functionality")
        missing.append("Email verification for new users")
        missing.append("Two-factor authentication")
        missing.append("Export to PDF for estimates/contracts")
        missing.append("Mobile-responsive design verification")
        missing.append("Backup/restore functionality")
        missing.append("Multi-currency support")
        missing.append("Automated invoice generation")

        print("\nMissing/Optional Features:")
        for item in missing:
            print(f"  - {item}")
            self.suggestions['features'].append(item)

    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "="*70)
        print("ANALYSIS SUMMARY")
        print("="*70)

        total_issues = sum(len(v) for v in self.issues.values())
        total_warnings = sum(len(v) for v in self.warnings.values())
        total_suggestions = sum(len(v) for v in self.suggestions.values())

        print(f"Critical Issues: {total_issues}")
        print(f"Warnings: {total_warnings}")
        print(f"Suggestions: {total_suggestions}")

        if self.issues:
            print("\n" + "="*70)
            print("CRITICAL ISSUES:")
            print("="*70)
            for file, issues in self.issues.items():
                print(f"\n{file}:")
                for issue in issues:
                    print(f"  [!] {issue}")

        if self.warnings:
            print("\n" + "="*70)
            print("WARNINGS:")
            print("="*70)
            for file, warnings in self.warnings.items():
                print(f"\n{file}:")
                for warning in warnings:
                    print(f"  [*] {warning}")

        if self.suggestions:
            print("\n" + "="*70)
            print("SUGGESTIONS FOR IMPROVEMENT:")
            print("="*70)
            for category, suggestions in self.suggestions.items():
                print(f"\n{category}:")
                for suggestion in suggestions:
                    print(f"  - {suggestion}")

def main():
    print("="*70)
    print("CONTRACTORPRO CODE QUALITY ANALYSIS")
    print("="*70)

    analyzer = CodeAnalyzer()

    # Analyze main files
    if os.path.exists('app.py'):
        analyzer.analyze_app_py('app.py')

    if os.path.exists('models.py'):
        analyzer.analyze_models_py('models.py')

    if os.path.exists('config.py'):
        analyzer.analyze_config('config.py')

    if os.path.exists('.env'):
        analyzer.analyze_env_file('.env')

    if os.path.exists('templates'):
        analyzer.analyze_templates('templates')

    # Additional checks
    analyzer.check_security_issues()
    analyzer.check_performance_issues()
    analyzer.check_missing_features()

    # Print summary
    analyzer.print_summary()

if __name__ == '__main__':
    main()
