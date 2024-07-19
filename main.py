import matplotlib.pyplot as plt #library untuk menampilkan scatter

#function ini bertujuan untuk mengembalikan tipe data pada a_str
def get_type(a_str):
    try:
      int(a_str)
      return "int"
    except:
      try:
        float(a_str)
        return "float"
      except:
        return "str"

#funtion ini untuk membuat dan mengembalikan kumpulan list dalam list yang didefinisikan dalam dataframe
def read_csv(file_name, delimiter=','):
    data, data_type = [], []

    #membuka file
    with open(file_name, 'r') as file:
        line_of_file = file.readlines()
        if line_of_file == []:raise Exception("Tabel tidak boleh kosong.")

        #membuat list header/nama kolom
        header = line_of_file[0].strip().split(delimiter)

        #membuat list yang berisi data tabel
        for line in line_of_file[1:]:
            line = line.strip("\n")
            data.append(line.split(delimiter))

        for index, element in enumerate(data, 1):
            if len(header) != len(element): raise Exception(f"Banyaknya kolom pada baris {index} tidak konsisten.")

        #membuat list yang berisi type dari masing-masing data
        for index in range(len(header)):
            list_data = [row[index] for row in data]
            list_types = [get_type(item) for item in list_data]
            if 'int' in list_types and 'float' in list_types:
                list_types = ['float' if item == 'int' or item == 'float' else item for item in list_types]
            elif 'float' in list_types and 'str' in list_types:
                list_types = ['str' if item == 'float' or item == 'str' else item for item in list_types]
            elif 'int' in list_types and 'str' in list_types:
                list_types = ['str' if item == 'int' or item == 'str' else item for item in list_types]
            data_type.append(list_types[0])

        #mengembalikan list-list yang telah dibuat
        return data, header, data_type

#function untuk mengembalikan list data
def to_list(dataframe):
    return dataframe[0]

#function untuk mengembalikan list nama kolom
def get_column_names(dataframe):
    return dataframe[1]
  
#function untuk mengembalikan list data type
def get_column_types(dataframe):
    return dataframe[2]

#function untuk membuat dan mengembalikan list dataframe dalam bentuk tabel
def head(dataframe, top_n = 10):
    cols = get_column_names(dataframe)
    out_str = ""
    out_str += "|".join([f"{col[:15]:>15}" for col in cols]) + "\n"
    out_str += ("-" * (15 * len(cols) + (len(cols) - 1))) + "\n"
    for row in to_list(dataframe)[:top_n]:
        out_str += "|".join([f"{col[:15]:>15}" for col in row]) + "\n"
    return out_str

#function untuk membuat dan mengembalikan list nama kolom dan tyoe datanya dalam bentuk tabel
def info(dataframe):
    column_names, column_types = get_column_names(dataframe), get_column_types(dataframe)
    row_lines = []
    for i in range(0, len(get_column_names(dataframe))):
        list = []
        list.append(column_names[i])
        list.append(column_types[i])
        row_lines.append(list)
    cols = ['Kolom', 'Tipe']
    out_str = f"Total Baris = {len(to_list(dataframe))} baris\n\n"
    out_str += " ".join([f"{col[:15]:<15}" for col in cols]) + "\n"
    out_str += ("-" * (15 * len(cols) + (len(cols) - 1))) + "\n"
    for row in row_lines[:len(get_column_names(dataframe))]:
        out_str += " ".join([f"{col[:15]:<15}" for col in row]) + "\n"
    return out_str

#function untuk mengkondisikan input pada parameter condition
def satisfy_cond(value1, condition, value2):
    if condition == "<":
        return value1 < value2
    elif condition == "<=":
        return value1 <= value2
    elif condition == ">":
        return value1 > value2
    elif condition == ">=":
        return value1 >= value2
    elif condition == "!=":
        return value1 != value2
    elif condition == "==":
        return value1 == value2
    else:
        raise Exception(f"Operator {condition} tidak dikenal.")

#function untuk filtering data berdasarkan input parameter condition dan value pada suatu nama kolom
def select_rows(dataframe, col_name, condition, value):
        #exception handling
        if col_name not in get_column_names(dataframe): raise Exception(f"Kolom {col_name} tidak ditemukan.")
        if condition not in ["<", "<=", "==", ">", ">=", "!="]: raise Exception(f"Operator {condition} tidak dikenal.")

        #eksekusi code berdasarkan tujuan fungsi
        for i, element in enumerate(get_column_names(dataframe), 0):
            if col_name == element:
                index = i
                break
        new_data = []
        for element in to_list(dataframe):
            if satisfy_cond(float(element[index]), condition, value):
                new_data.append(element)
        return new_data, get_column_names(dataframe), get_column_types(dataframe)

#funtion yang bertujuan untuk menampilkan data yang telah difilter atau dipilih berdasarkan nama kolom
def select_cols(dataframe, selected_cols):
    #exception handling
    if selected_cols == []: raise Exception("Parameter selected_cols tidak boleh kosong.")
    for element in selected_cols:
        if element not in get_column_names(dataframe): raise Exception(f"Kolom {element} tidak ditemukan.")

    #eksekusi code berdasarkan tujuan fungsi
    header = get_column_types(dataframe)
    index, new_data, new_data_type = [], [], []
    for element in selected_cols:
        for i,data_column in enumerate(get_column_names(dataframe), 0):
            if element == data_column:
                index.append(i)
                break
    for i in to_list(dataframe):
        list = []
        for j in index:
            list.append(i[j])
        new_data.append(list)
    for i in index:
        new_data_type.append(header[i])
    return new_data, selected_cols, new_data_type

#function untuk menghitung banyaknya data yang seragam dengan data type 'str' dalam format dictionary
def count(dataframe, col_name): 
    #exception handling
    if col_name == []: raise Exception("Tabel kosong.")
    if col_name not in get_column_names(dataframe): raise Exception(f"Kolom {col_name} tidak ditemukan.")
    for index, element in enumerate(get_column_names(dataframe), 0):
        if element == col_name:
            if get_column_types(dataframe)[index] != 'str': raise Exception(f"Kolom {col_name} harus bertipe string.")
            break

    #eksekusi code berdasarkan tujuan fungsi
    counts = {}
    data = []
    for element in to_list(dataframe):
        row = dict(zip(get_column_names(dataframe), element))
        data.append(row)
    for row in data:
        value = row[col_name]
        counts[value] = counts.get(value, 0) + 1
    return counts

#menghitung rata-rata pada suatu data dengan type 'int' atau 'float' berdasarkan nama kolom
def mean_col(dataframe, col_name):
    #exception handling
    if dataframe == []: raise Exception("Tabel kosong.")
    if col_name not in get_column_names(dataframe): raise Exception(f"Kolom {col_name} tidak ditemukan.")
    for index, element in enumerate(get_column_names(dataframe), 0):
        if element == col_name:
            if get_column_types(dataframe)[index] == 'str': raise Exception(f"Kolom {col_name} bukan bertipe numerik.") 
            break

    #eksekusi code berdasarkan tujuan fungsi
    count = 0
    for element in to_list(dataframe):
        count += float(element[index])
    mean = count/len(to_list(dataframe))
    return mean

#function yang bertujuan untuk menampilkan scatter berdasarkan input data pada parameter
def show_scatter_plot(x, y, x_label, y_label):
    plt.scatter(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

#function yang berisi konfigurasi data yang akan ditampilkan pada scatter
def scatter(dataframe, col_name_x, col_name_y):
    #exception handling
    if col_name_x not in get_column_names(dataframe): raise Exception(f"Kolom {col_name_x} tidak ditemukan.")
    if col_name_y not in get_column_names(dataframe): raise Exception(f"Kolom {col_name_y} tidak ditemukan.")
    index_x, index_y = 0, 0
    for index, element in enumerate(get_column_names(dataframe), 0):
        if element == col_name_x:
            index_x += index
            if get_column_types(dataframe)[index] == 'str': raise Exception(f"Kolom {col_name_x} bukan bertipe numerik.")
        elif element == col_name_y:
            index_y += index
            if get_column_types(dataframe)[index] == 'str': raise Exception(f"Kolom {col_name_y} bukan bertipe numerik.")

    #eksekusi code berdasarkan tujuan fungsi
    x, y = [], []
    for element in to_list(dataframe):
        x.append(float(element[index_x]))
    for element in to_list(dataframe):
        y.append(float(element[index_y]))
    show_scatter_plot(x, y, col_name_x, col_name_y)

#fitur tambahan: sorting data dalam bentuk tabel
def sorting_menu():
    print("-"*40)
    print("SORTING DATA")
    print("(note: kolom data harus bertipe numerik)")
    print()
    print("1. urutkan data dari terbesar ke terkecil")
    print("2. urutkan data dari terkecil ke terbesar")
    print("-"*40)

#function ini mengurutkan data 'int' atau 'float' dari urutan data terbesar atau terkecil
def sort(dataframe, col_name, input_menu):
    #exception handling
    if col_name not in get_column_names(dataframe): raise Exception(f"Kolom {col_name} tidak ditemukan.")
    index = 0
    for i, element in enumerate(get_column_names(dataframe), 0):
        if element == col_name:
            index += i
            if get_column_types(dataframe)[i] == 'str': raise Exception(f"Kolom {col_name} bukan bertipe numerik.")
    
    #buat data baru dengan format yang sama seperti dataframe
    new_data, sorted_data = [], []
    for element in to_list(dataframe):
        sorted_data.append([element[index]])
    sorted_data.sort()

    #pengkondisian berdasarkan input untuk menu
    if input_menu == 1:
        sorted_data.reverse()
        new_data.append(sorted_data)
        new_data.append([get_column_names(dataframe)[index]])
        new_data.append([get_column_types(dataframe)[index]])
    elif input_menu == 2:
        new_data.append(sorted_data)
        new_data.append([get_column_names(dataframe)[index]])
        new_data.append([get_column_types(dataframe)[index]])
    return new_data

#main program
if __name__ == "__main__":
    dataframe = read_csv("abalone.csv")
    #print(head(dataframe))
    #print(info(dataframe))
    #new_dataframe = select_rows(dataframe, "umur", "<", 21)
    #print(head(new_dataframe))
    new_dataframe = select_cols(dataframe, ["Length", "Diameter", "Rings"])
    #print(info(new_dataframe))
    #print(head(new_dataframe, top_n=5))
    #print(count(dataframe, "Sex"))
    #print(mean_col(dataframe, "Diameter"))
    #print(mean_col(dataframe, "Height"))
    #scatter(dataframe, "Length", "Diameter")
    #print()

    #feature usage
    #------------------------------------------------------
    #sorting_menu()
    #input_menu = int(input("Masukkan perintah: "))
    #print()
    #new_dataframe = sort(dataframe, "Length", input_menu)
    #print(head(new_dataframe))
    #------------------------------------------------------