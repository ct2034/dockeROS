FROM python

CMD ["python", "-c", "import time\nwhile True:\n    print('BLUE')\n    time.sleep(1)"]
