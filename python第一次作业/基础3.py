var = input("请输入字符串：")
str1 = str(var)
dict1 = {}
for i in range(len(str1)):
    dict1[i] = str1[i]
print(dict1)