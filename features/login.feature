Feature: login
  کاربر در صفحه ی ورود اطلاعات مورد نظر را وارد کرده و وارد سایت می شود
  

  Background: وجود کاربر عادی
        کاربر ادمین تعریف شده است 
  
  Scenario Outline:  Correct login
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر اطلاعات ورود را به صورت صحیح وارد می‌کند
    Then کاربر با موفقیت وارد سامانه می‌شود و داشبورد نمایش داده می‌شود
    
    
    
  
  Scenario Outline: Login with incorrect username
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر نام کاربری  نامعتبر را وارد می‌کند
    And کاربر رمز عبور و کد امنیتی معتبر را وارد می‌کند
    And کاربر روی دکمه ورود کلیک می‌کند
    Then پیغام خطای ورود با نام کاربری اشتباه نمایش داده می‌شود    
    
    
  
  Scenario Outline: Login with incorrect password
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر رمز عبور نامعتبر را وارد می‌کند
    And کاربر نام کاربری و کد امنیتی صحیح را وارد می‌کند
    And کاربر روی دکمه ورود کلیک می‌کند
    Then پیغام خطای ورود با رمز عبور اشتباه نمایش داده می‌شود    
    
    
  
  Scenario Outline: Login with incorrect captcha code
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر نام کاربری و رمز عبور صحیح را وارد می‌کند
    And کاربر کد کپچای نادرست را وارد می‌کند
    And کاربر روی دکمه ورود کلیک می‌کند
    Then پیغام خطای ورود با کد کپچا اشتباه نمایش داده می‌شود    
    
    
  
  Scenario Outline: Login without username
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر نام کاربری را وارد نمی‌کند
    And کاربر رمز عبور و کد امنیتی معتبر را وارد می‌کند
    And کاربر روی دکمه ورود کلیک می‌کند
    Then پیغام خطای ورود با عدم درج نام کاربری نمایش داده می‌شود  
    
    
    
  
  Scenario Outline: Login without password
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر رمز عبور را وارد نمی‌کند
    And کاربر نام کاربری و کد امنیتی صحیح را وارد می‌کند
    And کاربر روی دکمه ورود کلیک می‌کند
    Then پیغام خطای ورود با عدم درج پسورد نمایش داده می‌شود    
    
    
  
   Scenario Outline: Login without captcha
    
    Given کاربر در صفحه ورود به سامانه قرار دارد
    When کاربر نام کاربری و رمز عبور صحیح را وارد می‌کند
    And کاربر کد کپچای را وارد نمی کند
    And کاربر روی دکمه ورود کلیک می‌کند
    Then پیغام خطای ورود با عدم درج کپچا نمایش داده می‌شود    
      
    
    
  
#   Scenario Outline: Login by maximum characters in the username and password and captcha
    
#     Given کاربر در صفحه ورود به سامانه قرار دارد
#     When کاربر نام کاربری با بیش از حد مجاز کاراکتر  را وارد می‌کند
#     And کاربر رمز عبور با بیش از حد مجاز کاراکتر  را وارد می‌کند
#     And کاربر کد امنیتی با بیش از حد مجاز کاراکتر  را وارد می‌کند
#     And کاربر روی دکمه ورود کلیک می‌کند
#     Then پیغام خطای طول ورودی بیش از حد مجاز است برای هر فیلد نمایش داده می‌شود
    
    
    
  