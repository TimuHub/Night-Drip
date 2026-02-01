# Night Drip — Сборка в APK (Android)

Игра сделана на **Ren'Py**. APK собирается **официальным способом Ren'Py** (RAPT), а **не** через Buildozer.

---

## Важно: Ren'Py ≠ Buildozer

| | Ren'Py (наш проект) | Buildozer |
|---|---------------------|-----------|
| **Для чего** | Визуальные новеллы (Ren'Py) | Kivy / Python-приложения |
| **Сборка Android** | Ren'Py Launcher → Build → Android (RAPT) | `buildozer android debug` |
| **Google Colab** | Не стандартный способ; возможен через скрипты/CI | Часто используют Colab для Kivy |

**Night Drip — проект Ren'Py.** Собирать нужно через **Ren'Py Launcher** (или через GitHub Actions, см. ниже). Buildozer для этого проекта **не подходит**.

---

## 1. Установка Ren'Py (локально)

1. Скачайте **Ren'Py** с https://www.renpy.org/latest.html  
2. Установите (или распакуйте portable).  
3. Запустите **Ren'Py Launcher**.

---

## 2. Подключение проекта

1. В лаунчере: **Preferences** → укажите путь к папке с игрой (корень **NightDrip**, где лежат `game/`, `README.md` и т.д.).  
2. Либо: **List Projects** → **Add** → выберите папку **NightDrip**.  
3. Проект появится в списке. Выберите его и нажмите **Launch** — проверьте, что игра запускается.

---

## 3. Ассеты в game/

Ren'Py читает ресурсы только из папки `game/`. Убедитесь, что скопированы:

- `assets/bg/*` → `game/bg/`
- `assets/ch/*` → `game/ch/`

На Windows (PowerShell из корня проекта):

```powershell
New-Item -ItemType Directory -Force -Path game\bg, game\ch
Copy-Item -Path assets\bg\* -Destination game\bg\
Copy-Item -Path assets\ch\* -Destination game\ch\
```

---

## 4. Сборка Android APK (официальный способ)

1. В **Ren'Py Launcher** выберите проект **Night Drip**.  
2. Нажмите **Build** → **Android**.  
3. При первом запуске:
   - лаунчер предложит скачать **Android SDK** и **NDK** — согласитесь;
   - укажите путь к **Java JDK 8** (или 11), если спросит.
4. Дождитесь окончания сборки.  
5. Готовый APK будет в подпапке проекта, например:  
   `NightDrip/android/dist/Night Drip-1.0.apk`  
   (имя может отличаться в зависимости от версии и настроек.)

Иконка и имя пакета настраиваются в лаунчере: **Build** → **Android** → **Configure** (package name, icon и т.д.).

---

## 5. Сборка без своего ПК (облако / CI)

Ren'Py официально рассчитан на сборку с **десктопа** (Windows/macOS/Linux). Варианты без своего компьютера:

### Вариант A: GitHub Actions (Renconstruct)

Можно автоматизировать сборку через **Renconstruct** (инструмент Ren'Py для CI):

- Репозиторий: https://github.com/devorbitus/renconstruct-build-action  
- В своём репо добавляете workflow: по пушу в ветку собирается APK и выкладывается в артефакты/релиз.  
- Требуется: репо на GitHub, настройка секретов при необходимости (например, подпись ключом).

Так вы получите APK **без** установки Ren'Py и SDK у себя — только коммит и скачивание готового APK из Actions.

### Вариант B: Google Colab

**Buildozer** в Colab используют для **Kivy**, не для Ren'Py. Собрать Ren'Py-игру в Colab можно только неофициально:

- Установить в Colab SDK Ren'Py (Linux), затем через командную строку запустить сборку RAPT.  
- Инструкций «из коробки» мало; обычно проще использовать **GitHub Actions** (вариант A) или **локальный Ren'Py** (раздел 4).

Итог: для Night Drip надёжный способ — **локальный Ren'Py** или **GitHub Actions (Renconstruct)**. Buildozer и Colab для Kivy — это другой стек.

---

## 6. Краткий чек-лист перед сборкой

- [ ] В папке `game/` есть `bg/` и `ch/` с картинками (фоны и спрайты).  
- [ ] В лаунчере проект запускается без ошибок (Launch).  
- [ ] Выбран **Build** → **Android**; при первом разе скачаны SDK/NDK и указан JDK.  
- [ ] После сборки APK лежит в `NightDrip/android/dist/`.  
- [ ] Установка на устройство/эмулятор: скопировать APK и установить вручную или через `adb install`.

После этого игра собирается в один APK-файл для установки на Android. Для распространения (например, TikTok) можно выкладывать APK в itch.io, Google Play (при наличии аккаунта) или раздавать ссылкой на скачивание из GitHub Releases (если настроите Actions).
