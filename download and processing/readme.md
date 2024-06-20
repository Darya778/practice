1. **Создание виртуального окружения и установка зависимостей**
    Установите вирутальное окружение:
    ```sh
    python -m venv venv
    ```
    Активируйте виртуальное окружение:
    ```sh
    source ./venv//bin/activate
    ```
    Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```
    
2. **Создание файла сервиса**

    Убедитесь, что файл `downloader_service.service` находится в корне репозитория. Поменяйте в нём следующие строки, указав свой путь:
    ```sh
    ExecStart=/home/dasha/wotiwan/venv/bin/python /home/dasha/wotiwan/downloader.py
    Environment="PATH=/home/dasha/wotiwan/venv/bin"
    ```
    
    Затем активируйте его следующей командой:
    ```sh
    sudo systemctl enable /home/user/practice/download and processing/downloader_service.service
    sudo systemctl start downloader_service.service
    ```

    Далее можете убедиться в том, что сервис активен:
    ```sh
    sudo systemctl status downloader_service.service
    ```
