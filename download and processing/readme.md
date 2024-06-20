1. **Создание файла сервиса**

    Убедитесь, что файл `downloader_service.service` находится в корне репозитория. Затем активируйте его следующей командой:
    ```sh
    sudo systemctl enable /home/user/practice/download and processing/downloader_service.service
    sudo systemctl start downloader_service.service
    ```

    Далее можете убедиться в том, что сервис активен:
   ```sh
   sudo systemctl status downloader_service.service
   ```
