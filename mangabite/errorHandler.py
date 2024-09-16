def retryWithRefreshOnError(func, args=[], kwargs={}, cleanFunc=None):
    while True:
        try:
            return func(*args, **kwargs)
        except:
            print("retryWithRefreshOnError triggered")
            if cleanFunc:cleanFunc()