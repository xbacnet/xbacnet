<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Публикация любых данных как BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | [Français](./README_FR.md) | [Español](./README_ES.md) | [Русский](./README_RU.md) | [Português](./README_PT.md) | [हिन्दी](./README_HI.md) | [Bahasa Indonesia](./README_ID.md) | [Bahasa Melayu](./README_MS.md) | [Tiếng Việt](./README_VI.md) | [Türkçe](./README_TR.md) | [العربية](./README_AR.md)

## Введение xBACnet

xBACnet публикует любые данные как BACnet!

Это приложение представляет собой серверное программное обеспечение BACnet, используемое для публикации различных данных в качестве множественных основных сервисов в сети BACnet.
Поддерживаемые сервисы включают Who-Is, I-Am для привязки устройств, чтение/запись свойств, чтение/запись множественных свойств и подписку на изменения значений.


## Предварительные требования
База данных MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Установка

* Клонировать исходный код
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Создать базу данных
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Установить зависимости
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Настроить xbacnet-server

Открыть файл конфигурации
Изменить адрес: lo на реальное имя интерфейса, выполнив 'ip a'
Изменить идентификатор объекта
```
$ sudo nano /xbacnet-server/config.ini
```

Редактировать файл настроек базы данных
```
sudo nano /xbacnet-server/settings.py
```

* Открыть порт брандмауэра
```
$ sudo ufw allow 47808
```


### Пример config.ini
```
[BACpypes]
objectName: xBACnet Server
address: 192.168.20.193
objectIdentifier: 20193
description: xBACnet Server
vendorName: xBACnet Inc.
maxApduLengthAccepted: 1024
segmentationSupported: segmentedBoth
vendorIdentifier: 1524
foreignBBMD: 192.168.1.1
foreignTTL: 30
systemStatus: operational
```


* Отладка
```
$ sudo python3 server.py --debug --ini config.ini
-- Использовать --help для справки
$ sudo python3 server.py --help
```

* Развернуть xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

## Как использовать
Добавить объекты в базу данных, редактировать свойства объектов, записать данные для публикации в present_value

## Веб-интерфейс управления

xBACnet теперь включает современный веб-интерфейс управления для удобной настройки и мониторинга объектов BACnet.

### Возможности

#### 🔐 Аутентификация пользователя
- Безопасная система входа с контролем доступа на основе ролей
- Учетные данные по умолчанию: `administrator` / `!BACnetPro1`

![Страница входа](images/login.png)

#### 📊 Панель управления
- Обзор системы со статистикой в реальном времени
- Интерактивные графики, показывающие распределение объектов
- Мониторинг состояния системы
- Журналы недавней активности

![Панель управления](images/dashboard.png)

#### 🏗️ Управление объектами BACnet
Полные операции CRUD для всех типов объектов BACnet:

**Аналоговые объекты**
- **Аналоговые входы**: Мониторинг аналоговых входных значений с датчиков
- **Аналоговые выходы**: Управление аналоговыми выходными устройствами
- **Аналоговые значения**: Хранение и управление аналоговыми значениями

![Аналоговые входы](images/analog-inputs.png)
![Аналоговые выходы](images/analog-outputs.png)
![Аналоговые значения](images/analog-values.png)

**Двоичные объекты**
- **Двоичные входы**: Мониторинг состояний двоичного входа (вкл/выкл)
- **Двоичные выходы**: Управление двоичными выходными устройствами
- **Двоичные значения**: Хранение и управление двоичными значениями

![Двоичные входы](images/binary-inputs.png)
![Двоичные выходы](images/binary-outputs.png)
![Двоичные значения](images/binary-values.png)

**Многосостоятельные объекты**
- **Многосостоятельные входы**: Мониторинг многосостоятельных входных устройств
- **Многосостоятельные выходы**: Управление многосостоятельными выходными устройствами
- **Многосостоятельные значения**: Хранение и управление многосостоятельными значениями

![Многосостоятельные входы](images/multi-state-inputs.png)
![Многосостоятельные выходы](images/multi-state-outputs.png)
![Многосостоятельные значения](images/multi-state-values.png)

#### 👥 Управление пользователями
- Создание, редактирование и удаление учетных записей пользователей
- Разрешения на основе ролей
- Отслеживание активности пользователей

![Управление пользователями](images/user-management.png)

### Быстрый старт

1. **Запустить API-сервер**
   ```bash
   cd xbacnet-api
   python run.py --port 8000
   ```

2. **Запустить веб-интерфейс**
   ```bash
   cd xbacnet-web
   npm install
   npm run dev
   ```

3. **Доступ к интерфейсу**
   - Открыть браузер на `http://localhost:3000`
   - Войти с: `administrator` / `!BACnetPro1`

### Технологический стек
- **Frontend**: Vue 3 + Element Plus + ECharts
- **Backend**: Python Falcon REST API
- **База данных**: MySQL
- **Аутентификация**: Безопасность на основе JWT

## Группа WeChat

![WeChat Group](qr_code_wechat_group.png)
