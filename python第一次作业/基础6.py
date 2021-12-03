class product:
    def __init__(self,num1,name1,price1,total1,remain1):
        self.__num = num1
        self.__name = name1
        self.__price = price1
        self.__total = total1
        self.__remain = remain1

    def display(self):
        print(self.__num,self.__name,self.__price,self.__total,self.__remain)

    def income(self):
        income_ = (self.__total - self.__remain) * self.__price
        print(income_)

    def setdata(self,buy):
        self.__remain = self.__total - buy

if __name__ == '__main__':
    business = product(5,'phone',1000,500,500)
    business.display()
    business.setdata(100)
    business.display()
    business.income()
