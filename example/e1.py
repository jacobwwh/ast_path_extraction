def main():
    a=[1,2,3]
    if len(a)>5:
        print('a')
    for i in range(3):
        if i==0:
            b=0
        elif i==1:
            for j in range(2):
                if j==0:
                    c=0
                else:
                    c=1
        else:
            b=2
