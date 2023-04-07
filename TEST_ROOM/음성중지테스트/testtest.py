import threading, time


def playmusic():


def wrapper(func, args, res):
    res.append(func(*args))

res = []
t = threading.Thread(target=wrapper, args=(findcluster, (companyid,), res))
t.start()
while t.is_alive():
    # print next iteration of ASCII spinner
    t.join(0.2)

print (res[0])