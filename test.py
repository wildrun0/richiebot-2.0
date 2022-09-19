lists = [
    ["1","2","3","4",'123123123', '0000000'],
    ['1231223123', '00010000'],
    ["ричи пока", "ричи п1ока","ричи привет"],
]


text = 'ричи привет 1'

# def check(e):
# test = list(
#     filter(lambda a: list(a[1])[0] is True,
#         enumerate(map(lambda b: map(text.startswith, b), lists))
#     )
# )

# print(test[0][0])
# kek = filter(lambda a: a.startswith(text), lists)
# kek = (
#     filter(lambda a: True in dict(a[1]).values(),
#            enumerate(map(lambda b: enumerate(map(text.startswith, b)), lists)
#     )
# ))
for i in enumerate(map(lambda b: map(text.startswith, b), lists)):
    commands_indexes = list(i[1])
    if True in commands_indexes:
        print(lists[i[0]][commands_indexes.index(True)])
        
    # print(True in dict(i[1]).values())

# for i in kek:
#     print(i)
#     print('idx: ',i[0])
#     print('idx_pos:', list(i[1]))