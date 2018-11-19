FROM python

CMD ["python", "-c", "import time\nwhile True:\n    print('GREEN')\n    time.sleep(1)"]
