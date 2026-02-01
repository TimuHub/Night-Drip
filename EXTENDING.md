# Night Drip — Как бесконечно дорабатывать игру

Структура проекта сделана так, чтобы можно было **бесконечно добавлять сюжет, персонажей, функции и версии**, не ломая игру. Всё остаётся играбельным.

---

## 1. Версии и ветки

- **game_version** (`game/definitions.rpy`) — номер релиза (0.6.0, 1.0.0, …). Менять при выходе новой сборки.
- **content_version** (`game/definitions.rpy`) — сюжет/контент: `demo_1`, `act_1`, `act_2`, `dlc_sophia`, …  
  Используй в условиях: `if content_version == "act_2":` или `if content_version.startswith("dlc_"):` чтобы включать новые арки и ветки.

Так можно продолжать историю с разных сторон: новый акт, DLC по персонажу, альтернативные финалы.

---

## 2. Добавить нового персонажа

1. **definitions.rpy:** в словари `trust`, `outcome`, при необходимости `knows_about` и `schedule` добавить новый `id`.
2. **characters.rpy:** `define new_char = Character(...)`, объявить спрайты `image new_id emotion = "ch/..."`.
3. **data/characters_registry.json:** добавить запись с `keywords`, `schedule`, `emotions`, `stalking_flags`.
4. **game/dialogue/new_id.rpy:** создать файл с label'ами `dialogue_new_id_day2`, `dialogue_new_id_day3`, … (по дням и контексту).
5. **script.rpy / shift_start:** выбор клиента уже идёт по `schedule` и `renpy.has_label("dialogue_<id>_day2")` — достаточно добавить label в dialogue/new_id.rpy.
6. **stalking.rpy:** при необходимости добавить страницы в `STALKING_PAGES` и флаги в `knows_about`.

Персонаж автоматически начнёт появляться в сменах по расписанию.

---

## 3. Добавить новый день / смену

- В **script.rpy** в label `shift_end` вместо `jump demo_end` можно сделать:
  - `$ day += 1`
  - `$ shift_count += 1`
  - `jump shift_start`
- Тогда следующая «смена» возьмёт клиентов из `schedule` по новому `shift_count` и вызовет `dialogue_<id>_day2` и т.д.
- Для отдельной сюжетной ветки (например, только София): новый label `label day2_sophia_only:` и переход в него из меню или из условия по `content_version`.

Новые дни и смены добавляются без переписывания всей логики — только новые label'ы и переходы.

---

## 4. Добавить новую функцию (механика)

- **Общие функции** с префиксом `nd_` лежат в:
  - `definitions.rpy` (trust, outcome, knows, cafe, cat)
  - `atmosphere.rpy` (tension, good/bad outcome)
  - `stalking.rpy` (поиск, страницы, флаги)
- Новую механику (например, «репутация кафе», «письма», «второй браузер») лучше оформить так:
  1. Новый файл `game/systems/new_feature.rpy` с `default`-переменными и `init python:` функциями.
  2. Вызов из сценария: `$ nd_new_feature_update(...)` или `call screen new_feature_screen`.
  3. В **definitions.rpy** или в своём файле описать в комментарии, что за переменные и как они влияют на сюжет.

Так функции не смешиваются с основным сценарием и их можно включать/выключать по `content_version` или флагу.

---

## 5. Добавить новые «вау»-моменты и полировку

- **Анимации:** в **characters.rpy** уже есть `nd_right_slide`, `nd_left_slide`, `nd_cat_calm`, `nd_cat_alert`, `nd_cat_hiding`. Новый трансформ: `transform nd_my_effect:` и использование `show person at nd_my_effect` в сценарии.
- **Переходы сцен:** в script везде можно заменить `with Dissolve(0.35)` на `with Fade(0.5, 0.2, 0.5)` или свой `with my_transition`.
- **Шрифт:** положи **VT323-Regular.ttf** (Google Fonts) в `game/gui/fonts/`, в **gui.rpy** задать `nd_font = "gui/fonts/VT323-Regular.ttf"` — весь интерфейс переключится на него.
- **Экраны:** новые экраны добавлять в **screens.rpy** (или в отдельный файл `game/screens_extra.rpy`). Главное меню, быстрый доступ, настройки уже переопределены под pastel-goth.

---

## 6. Структура файлов (что куда класть)

| Что добавляешь | Куда |
|----------------|------|
| Новый персонаж (переменные, расписание) | definitions.rpy, data/characters_registry.json |
| Новый персонаж (имя, спрайты) | characters.rpy |
| Диалоги персонажа по дням | dialogue/<id>.rpy |
| Страницы сталкинга | stalking.rpy |
| Исходы и атмосфера | atmosphere.rpy, definitions.rpy (cafe_modifiers) |
| Новый экран (UI) | screens.rpy или screens_extra.rpy |
| Новая механика (логика) | systems/<name>.rpy + вызов из script/dialogue |
| Новый сюжетный акт / DLC | script.rpy (новые label'ы) + content_version |

---

## 7. Чек-лист перед релизом новой версии

- [ ] Обновлён `game_version` и при необходимости `content_version`.
- [ ] Все новые label'ы вызываются из script или из меню (нет «висячих» сцен).
- [ ] Новые персонажи есть в `trust`/`outcome`/`schedule` и в characters.rpy.
- [ ] Сохранения: при смене формата сейвов при необходимости сбросить или мигрировать (обычно Ren'Py справляется сам).
- [ ] Запуск с начала (New Game) и загрузка (Load) проходят без ошибок.

Так проект остаётся **играбельной игрой** и при этом готов к бесконечному расширению сюжета и механик с новыми версиями.
