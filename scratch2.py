from datetime import datetime, timedelta
import time

now = datetime.now()

five_days = now - timedelta(days=5)

if now > five_days:
    print("yeet")


