
site = ["dffd0", "gsrgds", "grsg"]
for word in site:
    print(word)

# my_list = [['а', 'б', 'в', 'г', 'п'], ['а', 'б', 'в', 'д'], ['е', 'б', 'в', 'г'], ['а', 'б', 'т', 'г']]v
#
# temp = my_list[0].copy()
# print(len(my_list))
# for list1 in range(1, len(my_list)):
#     temp[:] = [ x for x in temp if x in my_list[list1] ]
#     print(temp)
#
# print('-----------')
#
# list_difference = []
# for list1 in range(0, len(my_list)):
#     temp = my_list[list1].copy()
#     print(temp)
#     for list2 in range(0, len(my_list)):
#         if list1 != list2:
#             temp[:] = [x for x in temp if x not in my_list[list2]]
#     print(temp)
#     list_difference.append(temp)
#
# print(list_difference)