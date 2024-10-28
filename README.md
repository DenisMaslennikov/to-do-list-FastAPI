# API Задач
Небольшой проект для изучения построения API с нуля на FastAPI + SQLAlchemy. 
C последующим покрытием тестами и CI/CD посредством github action.

## Как запустить проект 
- Для запуска требуется установленный docker compose

## Development версия
- Клонировать репозиторий 
```bash 
git clone https://github.com/DenisMaslennikov/to-do-list-FastAPI.git
```
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template** в той же папке.
- Создать RSA ключи для генерации JWT в папке /backend/certs/ например использовав openssl (под Windows можно использовать openssl из состава git расположенного в C:\Program Files\Git\usr\bin\openssl.exe)
```bash
openssl genrsa -out private_key 2048
openssl rsa -pubout -in private_key -out public_key.pub
```
- Запустить контейнеры. 
```bash 
docker compose up --build
```
- После запуска всех контейнеров документация Swagger будет доступна по ссылке http://127.0.0.1:8000/docs
