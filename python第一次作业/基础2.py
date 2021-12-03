for i in range(1,10):
    for j in range(1,11-i):
        print("{} x {} = {}\t".format(i,j,i*j),end=' ')
    print("\n")