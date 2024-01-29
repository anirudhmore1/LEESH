from random import random
def myFunc(e):
    return e[1]
def main():

    tobj={}
    taskobj={}
    tind=0
    out=[]
    for i in range(1, 101):
        arrloc=[]
        arrvt=[]
        for j in range(0,3):
            arrloc.append([j,random()])
            arrvt.append([j,random()])
        arrvt.append([3,random()])
        #print(arrloc,arrvt)

        arrloc.sort(key = lambda x: x[1])
        out=[arrloc[0][0],arrloc[1][0],arrloc[2][0],3]

        arrvt.sort(key=myFunc)

        for j in range(0,4):
            tind+=1
            tobj["index"] = tind
            tobj["lpt"] = 2
            tobj["loc"]=arrvt[j][0]
            tobj["vt"]=out[j]
            print(tobj, ",")
        print()
    return;




if __name__ == '__main__':
    main();
