# پایه: پایتون
FROM python:3.10

# ست کردن دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی کل پروژه
COPY . .

# نصب پکیج‌ها
RUN pip install --no-cache-dir -r requirements.txt

# نصب Playwright با مرورگرها
RUN python -m playwright install --with-deps

# اجرای فایل تست به عنوان دستور پیش‌فرض
CMD ["python", "test_run_all_tests.py"]
