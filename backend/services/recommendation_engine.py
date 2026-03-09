import os

def generate_report(data):

    os.makedirs("reports", exist_ok=True)

    path = "reports/report.txt"

    with open(path, "w") as f:
        f.write(str(data))

    return path