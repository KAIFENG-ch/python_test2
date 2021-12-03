str1 = input("请输入一个数组：")
list1 = str1.split(",")
list1 = [str(str1[i]) for i in range(len(str1))]
digit = []
for j in range(len(list1)):
    if list1[j].isdigit():
        element = int(list1[j])
        digit.append(element)
print(digit)
print(sum(digit))
