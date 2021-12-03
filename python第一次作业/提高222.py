class MyOperation:
    cnt = 0

    def __init__(self):
        MyOperation.cnt += 1
        print(MyOperation.cnt)

    @staticmethod
    def add(a, b):
        return a+b


if __name__ == '__main__':
    a = MyOperation()
    b = MyOperation()
    c = MyOperation()
    answer = MyOperation.add(1, 5)
    print(answer)
