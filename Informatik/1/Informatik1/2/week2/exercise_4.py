import time

total_sec = time.time()
current_sec = total_sec % 60
total_min = total_sec // 60
current_min = total_min % 60
total_hours = total_min // 60
current_hour = total_hours % 24

print('%02d:%02d:%02d' % (current_hour, current_min, current_sec))
