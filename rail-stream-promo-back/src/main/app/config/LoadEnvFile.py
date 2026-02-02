import os
import glob

#======================================
# Функция выполняет поиск файла *.env в каталоге проекта
# (Если вызов выше чем src, а файл .env не был найден, выбрасыватся исключение ) 
# выплняет чтение *.env файла и переносит объявленные переменые в этом
# файле к переменным окружения.

# !!!!!ВАЖНО!!!!! Первично выполняется поиск ВНИЗ, 
# по этому если вызов данного метода выполняется из кореневой директории "/"
# то 1-й найденый файл .env (не относящийся к необходимому проекту) и будет считан
#======================================
def load_env_file():

    latest_catalog = "src"

    #=====================================
    # Движение ВНИЗ по каталогам от точки 
    # вызова метода
    #=====================================

    file_path = None
    
    for file in glob.glob("**/*.env", recursive=True):
        file_path = file

        if file_path != None: # Условие использования 1-го найденого файла
            file_path = os.path.abspath(file_path)
            break


    if file_path == None:

        level_up =  os.path.dirname(os.getcwd())

        stop_search_flag = 0

        #=================================================
        # Движение ВВЕРХ по каталогам от точки вызова метода
        #=================================================
        while(True):

            if level_up.split("/")[-1] == latest_catalog:
                stop_search_flag += 1

            pattern = os.path.join(level_up, "**", "*.env")

            file_list = glob.glob(pattern, recursive=True)

            if file_list:
                file_path = file_list[0]
                break


            elif not file_list and stop_search_flag != 1:
                level_up = os.path.dirname(level_up)

            else: 
                break
        
        #==================================
        # Проброс исключения т.к. *.env 
        # файл не найден
        #==================================
        if file_path == None:
            # TODO! Выбросить исключение о том, что в рабочем проекте нет файла .env

            pass
    
    #================================
    # Чтение найденого *.env файла и фиксация
    # указанных переменных в переменные окружения
    #================================
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()

                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                
                # Разделяем на ключ и значение
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Удаляем кавычки если есть
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    os.environ[key] = value
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")