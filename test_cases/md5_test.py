import md5
def md5checksum(str1, str2):
    m1 = md5.new()
    m2 = md5.new()
    m1.update(str1)
    m2.update(str2)
    if (m1.digest() == m2.digest()):
        return True
    else:
        return False

def test_answer():
    assert md5checksum("teleoptwist", "teleoptwistr") == False
