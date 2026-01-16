# wait used to delay actions
def wait(field, seconds):
    start = field.timestamp
    while True:
        elapsed = field.timestamp - start

        if elapsed > seconds * 30:
            break