FROM python

CMD ["python", "-c", "import time\nwhile True:\n    print('RED')\n    time.sleep(1)"]
