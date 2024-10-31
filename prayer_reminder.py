import tkinter as tk
from tkinter import messagebox
import requests
import datetime
import threading
from plyer import notification



def get_prayer_times(city, country):
    try:
        response = requests.get(f'http://api.aladhan.com/v1/timingsByCity', 
                                params={'city': city, 'country': country, 'method': 2})
        data = response.json()
        if data['code'] == 200:
            return data['data']['timings']
        else:
            messagebox.showerror("Error", "Could not retrieve prayer times")
            return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def show_reminder(prayer):
    notification.notify(
        title='Prayer Reminder',
        message=f"It's time for {prayer}",
        timeout=10
    )

def set_reminders(prayer_times):
    for prayer, time_str in prayer_times.items():
        # تحويل وقت الصلاة إلى كائن وقت
        prayer_time = datetime.datetime.strptime(time_str, "%H:%M").time()
        now = datetime.datetime.now().time()
        # حساب الفارق الزمني بين الوقت الحالي ووقت الصلاة
        if prayer_time > now:
            delta = datetime.datetime.combine(datetime.date.today(), prayer_time) - datetime.datetime.now()
            # جدولة رسالة التذكير
            threading.Timer(delta.total_seconds(), lambda: show_reminder(prayer)).start()

def get_and_set_times():
    city = city_entry.get()
    country = country_entry.get()
    prayer_times = get_prayer_times(city, country)
    if prayer_times:
        set_reminders(prayer_times)

# إنشاء نافذة المستخدم
root = tk.Tk()
root.title("Prayer Times Reminder")

# إنشاء حقول الإدخال
tk.Label(root, text="City (مثال: Mecca):").grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Country (مثال: Saudi Arabia):").grid(row=1, column=0, padx=10, pady=10)
country_entry = tk.Entry(root)
country_entry.grid(row=1, column=1, padx=10, pady=10)

# إنشاء زر للحصول على أوقات الصلاة وتعيين التذكيرات
get_times_button = tk.Button(root, text="Get Prayer Times", command=get_and_set_times)
get_times_button.grid(row=2, columnspan=2, pady=20)

root.mainloop()
