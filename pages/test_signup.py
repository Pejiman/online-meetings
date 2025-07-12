import re
import os
import datetime
import logging
import random
from time import sleep
from pytest_bdd import scenario, when, then, parsers, given
from faker import Faker
from openpyxl import Workbook, load_workbook
from playwright.sync_api import expect
import pytest
from playwright.sync_api import sync_playwright
from functools import wraps

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # True برای تست‌های CI
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},  # نمایشگر بزرگ
            screen={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        yield page
        context.close()
        browser.close()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RESULTS_FILE = "test_results.xlsx"
SCREENSHOT_DIR = "./screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def log_result(test_name, success=True, screenshot_path=None):
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    result = "موفق" if success else "ناموفق"

    if not os.path.exists(RESULTS_FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(["تست", "تاریخ", "ساعت", "نتیجه تست", "مسیر اسکرین‌شات"])
    else:
        wb = load_workbook(RESULTS_FILE)
        ws = wb.active

    ws.append([test_name, date_now, time_now, result, screenshot_path or "-"])
    wb.save(RESULTS_FILE)
    logger.info(f"نتیجه تست '{test_name}' با وضعیت: {result}")


def take_screenshot(page, test_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{timestamp}.png")
    page.screenshot(path=screenshot_path)
    logger.warning(f"📸 اسکرین‌شات گرفته شد: {screenshot_path}")
    return screenshot_path

def log_step(test_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = kwargs.get("page", None)
            try:
                return func(*args, **kwargs)
            except Exception:
                if page:
                    screenshot_path = take_screenshot(page, test_name)
                else:
                    screenshot_path = None
                log_result(test_name, success=False, screenshot_path=screenshot_path)
                raise
        return wrapper
    return decorator

def generate_valid_national_code():
    code = [random.randint(0, 9) for _ in range(9)]
    s = sum([(10 - i) * code[i] for i in range(9)])
    r = s % 11
    if r < 2:
        control_digit = r
    else:
        control_digit = 11 - r
    code.append(control_digit)
    return ''.join(map(str, code))


# ========== تست اول: ورود صحیح ==========

@pytest.mark.order(1)
@scenario("../features/signup.feature", "Correct signup")
def test_signup_Correct():
    pass


@given("کاربر در صفحه ثبت نام قرار دارد")
def open_login_page(page):
    page.goto("https://online-meetings-test.rayanbourse.ir/auth/login/")
    sleep(0.5)
    page.get_by_role("link", name="ثبت نام کنید").click()
    sleep(0.5)

@when("کاربر تمام فیلد ها را به صورت صحیح وارد می‌کند")
def fill_signup_Correct_test(page):

    national_code = generate_valid_national_code()

    page.get_by_placeholder("نام را وارد کنید").click()
    sleep(0.5)
    page.get_by_placeholder("نام را وارد کنید").fill("پژمان")
    sleep(0.5)
    page.get_by_placeholder("نام خانوادگی را وارد کنید").click()
    page.get_by_placeholder("نام خانوادگی را وارد کنید").fill("رنجی دیزچی")
    sleep(0.5)
    page.get_by_placeholder("کد ملی را وارد کنید").click()
    page.get_by_placeholder("کد ملی را وارد کنید").fill(national_code) 
    sleep(0.5)
    page.get_by_placeholder("شماره موبایل را وارد کنید").click()
    page.get_by_placeholder("شماره موبایل را وارد کنید").fill("09125243681")
    sleep(0.5)
    page.get_by_placeholder("تاریخ تولد").click()
    page.get_by_placeholder("تاریخ تولد").fill("۱۳۶۷/۰۲/۲5")
    page.get_by_placeholder("شماره موبایل را وارد کنید").click()
    sleep(0.5)
    page.get_by_placeholder("رمز عبور را وارد کنید", exact=True).click()
    page.get_by_placeholder("رمز عبور را وارد کنید", exact=True).fill("Pejm@n44662618")
    sleep(0.5)
    page.get_by_placeholder("تکرار رمز عبور را وارد کنید").click()
    page.get_by_placeholder("تکرار رمز عبور را وارد کنید").fill("Pejm@n44662618")
    sleep(0.5)

@when("کاربر روی دکمه ثبت‌نام کلیک می‌کند")
def fill_signup_Correct_test_register(page):

   page.get_by_role("button", name="ثبت نام").click()
   sleep(0.5)

@then("پیام موفقیت ثبت‌نام با موفقیت انجام شد نمایش داده می‌شود")
def check_dashboard_loaded(page):
    try:
       
        expect(page.locator("text=ثبت نام با موفقیت انجام شد")).to_be_visible(timeout=15000)
        print("✅ ثبت نام موفق و داشبورد نمایش داده شد.")
    except Exception as e:
        print("❌ ثبت نام موفق نبود یا داشبورد ظاهر نشد.")
        page.screenshot(path="./screenshots/failure_dashboard.png")
        raise e  

# ========== تست دوم: ورود ناموفق با عدم ثبت نام ==========


@pytest.mark.order(2)
@scenario("../features/signup.feature", "signup without name")
def test_signup_without_name():
    pass


@given("کاربر در صفحه ثبت نام قرار دارد")
def open_login_page(page):
    page.goto("https://online-meetings-test.rayanbourse.ir/auth/login/")
    sleep(0.5)
    page.get_by_role("link", name="ثبت نام کنید").click()
    sleep(0.5)

@when("کاربر تمام فیلد ها را به جز فیلد نام به صورت صحیح وارد می کند")
def fill_signup_without_name(page):


    page.get_by_placeholder("نام را وارد کنید").click()
    sleep(0.5)
    page.get_by_placeholder("نام را وارد کنید").fill("")
    sleep(0.5)
    page.get_by_placeholder("نام خانوادگی را وارد کنید").click()
    page.get_by_placeholder("نام خانوادگی را وارد کنید").fill("رنجی دیزچی")
    sleep(0.5)
    page.get_by_placeholder("کد ملی را وارد کنید").click()
    page.get_by_placeholder("کد ملی را وارد کنید").fill("0081071523")  
    sleep(0.5)
    page.get_by_placeholder("شماره موبایل را وارد کنید").click()
    page.get_by_placeholder("شماره موبایل را وارد کنید").fill("09125243681")
    sleep(0.5)
    page.get_by_placeholder("تاریخ تولد").click()
    page.get_by_placeholder("تاریخ تولد").fill("۱۳۶۷/۰۲/۲5")
    page.get_by_placeholder("شماره موبایل را وارد کنید").click()
    sleep(0.5)
    page.get_by_placeholder("رمز عبور را وارد کنید", exact=True).click()
    page.get_by_placeholder("رمز عبور را وارد کنید", exact=True).fill("Pejm@n44662618")
    sleep(0.5)
    page.get_by_placeholder("تکرار رمز عبور را وارد کنید").click()
    page.get_by_placeholder("تکرار رمز عبور را وارد کنید").fill("Pejm@n44662618")
    sleep(0.5)

@when("کاربر روی دکمه ثبت‌نام کلیک می‌کند")
def fill_signup_withoutname(page):

   page.get_by_role("button", name="ثبت نام").click()
   sleep(0.5)

@then("پیام خطای وارد کردن نام الزامی است نمایش داده می‌شود")
def check_dashboard_loaded(page):
    try:
       
        expect(page.locator("text=فیلد الزامی است.")).to_be_visible(timeout=15000)
        print("✅ فیلد نام به درستی اجباری می باشد")
    except Exception as e:
        print("❌ فیلد نام به اشتباه اجباری نمی باشد")
        page.screenshot(path="./screenshots/failure_dashboard.png")
        raise e  
    

    # ==========  تست سوم: ورود ناموفق با عدم ثبت نام خانوادگی ==========


@pytest.mark.order(3)
@scenario("../features/signup.feature", "signup without last name")
def test_signup_without_last_name():
    pass


@given("کاربر در صفحه ثبت نام قرار دارد")
def open_login_page(page):
    page.goto("https://online-meetings-test.rayanbourse.ir/auth/login/")
    sleep(0.5)
    page.get_by_role("link", name="ثبت نام کنید").click()
    sleep(0.5)

@when("کاربر تمام فیلد ها را به جز فیلد نام خانوادگی به صورت صحیح وارد می کند")
def fill_signup_without_last_name(page):


    page.get_by_placeholder("نام را وارد کنید").click()
    sleep(0.5)
    page.get_by_placeholder("نام را وارد کنید").fill("پژمان")
    sleep(0.5)
    page.get_by_placeholder("نام خانوادگی را وارد کنید").fill("")
    sleep(0.5)
    page.get_by_placeholder("کد ملی را وارد کنید").click()
    page.get_by_placeholder("کد ملی را وارد کنید").fill("0081071523") 
    sleep(0.5)
    page.get_by_placeholder("شماره موبایل را وارد کنید").click()
    page.get_by_placeholder("شماره موبایل را وارد کنید").fill("09125243681")
    sleep(0.5)
    page.get_by_placeholder("تاریخ تولد").click()
    page.get_by_placeholder("تاریخ تولد").fill("۱۳۶۷/۰۲/۲5")
    page.get_by_placeholder("شماره موبایل را وارد کنید").click()
    sleep(0.5)
    page.get_by_placeholder("رمز عبور را وارد کنید", exact=True).click()
    page.get_by_placeholder("رمز عبور را وارد کنید", exact=True).fill("Pejm@n44662618")
    sleep(0.5)
    page.get_by_placeholder("تکرار رمز عبور را وارد کنید").click()
    page.get_by_placeholder("تکرار رمز عبور را وارد کنید").fill("Pejm@n44662618")
    sleep(0.5)

@when("کاربر روی دکمه ثبت‌نام کلیک می‌کند")
def fill_signup_without_last_name(page):

   page.get_by_role("button", name="ثبت نام").click()
   sleep(0.5)

@then("پیام خطای وارد کردن نام خانوادگی الزامی است نمایش داده می‌شود")
def check_dashboard_loaded(page):
    try:
       
        expect(page.locator("text=فیلد الزامی است.")).to_be_visible(timeout=15000)
        print("✅ فیلد نام خانوادگی به درستی اجباری می باشد")
    except Exception as e:
        print("❌ فیلد نام خانوادگی به اشتباه اجباری نمی باشد")
        page.screenshot(path="./screenshots/failure_dashboard.png")
        raise e  