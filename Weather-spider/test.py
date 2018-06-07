s=[
{"no":28,"score":90},
{"no":25,"score":90},
{"no":1,"score":100},
{"no":2,"score":20},

]
print("original s: ",s)
# 单级排序，仅按照score排序
new_s = sorted(s,key = lambda e:e.__getitem__('score'))
print("new s: ", new_s)
# 多级排序,先按照score，再按照no排序
new_s_2 = sorted(new_s,key = lambda e:(e.__getitem__('score'),e.__getitem__('no')))
print("new_s_2: ", new_s_2)