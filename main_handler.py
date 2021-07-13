from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import split, explode
import pymorphy2

TOP_NUM = 200

spark = SparkSession \
    .builder \
    .appName("P_Handler") \
    .master("local[*]") \
    .getOrCreate()

datasets = ['1000menu', 'edimdoma', 'gastronom', 'gotovim_doma', 'iamcook', 'koolinar', 'namenu', 'povar', 'povarenok', 'webspoon']
lists_top_words = []
list_count_words_bf = [] # лист слов для отслеживания без пустых строк
list_count_words_af = [] # лист слов для отслеживания после исключения служебных слов

for dataset in datasets:
    # Начальная таблица
    df_dataset = spark.read.csv("data/" + dataset + ".csv", inferSchema=True, header=True, sep=";")
    # Таблица разделённая по словам (без пустых слов)
    split_df = df_dataset.select("*", explode(split(df_dataset.Рецепт, " ")).alias("Слова"))
    split_df = split_df.filter(split_df.Слова != '')
    list_count_words_bf.append(split_df.count())

    # Таблица приведённая к нормальной форме
    morph = pymorphy2.MorphAnalyzer()
    list_words = [row['Слова'] for row in split_df.take(split_df.count())]
    list_norm_words =[]

    def pos(word, morth=pymorphy2.MorphAnalyzer()):
        return morth.parse(word)[0].tag.POS

    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}  # function words
    for word in list_words:
        norm_word = morph.parse(word)[0].normal_form
        if (pos(norm_word) not in functors_pos) & (len(norm_word) > 2):
            list_norm_words.append(norm_word)

    list_count_words_af.append(len(list_norm_words))

    from pyspark.sql.types import StringType
    split_norm_df = spark.createDataFrame(list_norm_words, StringType())
    # split_norm_df.show()

    # Таблица подсчитанных слов
    top_words = split_norm_df.select("value").groupby("value").count().orderBy('count', ascending=False)
    list_top_words = [row['value'] for row in top_words.take(TOP_NUM)]
    lists_top_words.append(list_top_words)

    print("Таблица с 200 наиболее употребляемыми словами для сайта " + dataset)
    top_words.show(TOP_NUM)
    print("----------")


# Вывод листов с количеством слов
print("Отслеживание количества слов для сайтов до и после исключения служебных слов")
print(list_count_words_bf)
print(list_count_words_af)

print("----------")

# Поиск одинаковых слов
list_similar = lists_top_words[0].copy()
for list2 in range(1, len(lists_top_words)):
    list_similar[:] = [ x for x in list_similar if x in lists_top_words[list2] ]

print("Общие слова для всех сайтов: " + str(len(list_similar)) + " штук")
for word in list_similar:
    print(word)

print("----------")
# Поиск разных слов для каждого сайта
list_difference = []
for list1 in range(0, len(lists_top_words)):
    temp_diff = lists_top_words[list1].copy()
    for list2 in range(0, len(lists_top_words)):
        if list1 != list2:
            temp_diff[:] = [x for x in temp_diff if x not in lists_top_words[list2]]
    list_difference.append(temp_diff)

number = 0
for site in list_difference:
    print("Имя сайта: " + datasets[number])
    number += 1
    print("Уникальные слова: " + str(len(site)) + " штук")
    for word in site:
        print(word)
