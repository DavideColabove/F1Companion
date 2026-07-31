from datetime import datetime
import time

def sync_time(current_time_str, prev_time_obj):
    if current_time_str is None:
        return prev_time_obj

    current_time_obj = datetime.fromisoformat(current_time_str)

    if prev_time_obj is not None:
        delta = (current_time_obj - prev_time_obj).total_seconds()

        if delta > 0:
            time.sleep(delta)

    return current_time_obj