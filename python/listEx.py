import datetime

def main():
    list_a = []
    list_b = list()
    list_c = [3,4,5,"리스트",True]
    print(list_a,list_b,list_c)
    print(type(list_a),type(list_b),type(list_c))
    ptime = datetime.datetime.now()
    list_d = [1,2,3,'jung',ptime]
    print(list_d)
    print(list_d[3][2])
    
    list_of_list=[[1,2,3],[4,5,6,7],[8,9]]
    print(len(list_of_list))
    for list_item in list_of_list:
        for list_item2 in list_item:
            print(list_item2)

if __name__ == "__main__":
    main()