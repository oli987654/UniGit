function x(y=2,n)
    if n>0:
        y=y*n
        y=x(y,n-1)
    else:
        y-=1
    return y