# Night Drip — Основной сценарий
# Смена → диалоги с ключевыми словами → сталкинг → влияние на исходы и атмосферу

# --- LABEL: START (первый кадр — цепляет с первой секунды) ---
label start:
    scene bg room_messy with Fade(0.4, 0.2, 0.4)
    show cat at nd_cat_calm
    narrator "6:30. Дождь. Окно. И только он — чёрный кот на подоконнике — смотрит на тебя так, будто знает, чем закончится этот день."
    narrator "Телефон вибрирует. Не в первый раз."
    hide cat
    call screen phone_boss_morning
    jump after_phone

label after_phone:
    scene bg street_night with Dissolve(0.4)
    narrator "Ты выбегаешь под дождь. Город ещё спит. Неон в лужах — как масло."
    narrator "«Night Drip». Ночная кофейня. Твоё новое место. Или последнее."
    $ shift_time = "morning"
    $ shift_count += 1
    jump shift_start

# --- Начало смены: кто пришёл (по расписанию) ---
label shift_start:
    scene bg cafe_rainy
    if day == 1 and shift_count == 1:
        jump first_shift_sophia
    # День 2+: смена по циклу (утро → день → вечер → ночь), клиенты из schedule
    $ shift_slots = ["morning", "day", "evening", "night"]
    $ shift_time = shift_slots[(shift_count - 1) % 4]
    $ todays_clients = schedule.get(shift_time, [])
    $ picked = None
    python:
        for cid in todays_clients:
            if renpy.has_label("dialogue_" + cid + "_day2"):
                store.picked = cid
                break
    if picked:
        $ dialogue_label = "dialogue_" + picked + "_day2"
        call expression dialogue_label
    jump shift_end

# --- Первая смена: София ---
label first_shift_sophia:
    scene bg cafe_rainy with Dissolve(0.35)
    show sophia neutral at nd_right_slide
    sophia "Oh, you're here. Boss said you might not show up."
    sophia "I'm Sophia. I guess we'll be working together."
    $ player_name = renpy.input("Enter your name", default="Barista", length=20).strip() or "Barista"
    sophia "Okay. Well, the espresso machine is broken, and we have a customer waiting. Can you handle it?"
    menu:
        "I'll fix the machine.":
            $ nd_set_trust("sophia", 10)
            call minigame_coffee
        "You take the customer.":
            $ nd_set_trust("sophia", 0)
        "Why is everything broken?":
            $ nd_set_trust("sophia", -5)
    jump day1_sophia_talk

# --- День 1: София — диалог с ключевыми словами и ветками по knows_about ---
label day1_sophia_talk:
    scene bg cafe_day with Dissolve(0.35)
    show sophia neutral at nd_right_slide
    sophia "So, why did you take this job? Night shift barista isn't exactly... glamorous."
    menu:
        "I needed a change.":
            $ nd_set_trust("sophia", 5)
        "Money.":
            $ nd_set_trust("sophia", 0)
        "I like the quiet.":
            $ nd_set_trust("sophia", 10)
    sophia "I used to work in a design studio. But I... quit. Now I'm trying freelance. It's... not going well."
    sophia "That notification... that's my {b}art{/b} account. Don't look it up, it's embarrassing."
    # Ключевые слова для запоминания: art, freelance
    $ remembered_keywords = ["art", "freelance"]
    # Ветка: если игрок уже сталкил и знает про студию — особый вариант
    if knows_about.get("sophia_studio", False):
        sophia "You're looking at me like you know something. Do you?"
        menu:
            "I don't know anything.":
                $ nd_set_trust("sophia", 5)
                sophia "Okay. Sorry. I'm just... tired."
            "I heard someone took credit for your work.":
                $ nd_set_trust("sophia", -15)
                show sophia sad at nd_right_slide
                sophia "How do you—? Did you look me up? That's... I thought this place was different."
                $ nd_after_dark_choice()
                jump sophia_betrayed
            "I can tell it still hurts. You don't have to talk.":
                $ nd_set_trust("sophia", 10)
                show sophia sad at nd_right_slide
                sophia "Yeah. Thanks. Really."
    else:
        narrator "You could remember the words «art» or «freelance» — and look them up later."
    scene bg cafe_night with Dissolve(0.4)
    narrator "Evening comes. The rain hasn't stopped."
    jump day1_leo

label sophia_betrayed:
    narrator "Sophia avoids your eyes for the rest of the shift. She doesn't mention it again — but something is broken."
    $ nd_set_outcome("sophia", "worse")
    $ nd_after_bad_outcome("sophia")
    jump shift_end

# --- День 1: Лео ---
label day1_leo:
    scene bg cafe_night with Dissolve(0.35)
    show leo neutral at nd_right_slide
    unknown "Black coffee. No sugar."
    show sophia neutral at nd_left_slide
    sophia "That's Leo. He comes every night. Never talks."
    show leo neutral at nd_right_slide
    menu:
        "Talk to him.":
            $ nd_set_trust("leo", 10)
            show leo neutral at nd_right_slide
            leo "You're new. The last barista was incompetent. This is... adequate."
        "Serve quietly.":
            $ nd_set_trust("leo", 0)
    # Ключевые слова: work, coffee
    $ remembered_keywords = ["work", "coffee"]
    jump shift_end

# --- Конец смены: браузер (сталкинг) — момент «ты узнал то, чего не должен» ---
label shift_end:
    scene bg room_messy with Dissolve(0.4)
    if tension >= 5:
        show cat at nd_cat_alert
        narrator "Дома. Кот не спит — смотрит на экран. Он чувствует, когда ты заходишь слишком далеко."
    else:
        narrator "Дома. Дождь за окном. Ноутбук открыт. Один поиск — и ты увидишь то, что они не сказали вслух."
    $ current_browser_page = None
    $ remembered_keywords = list(set(remembered_keywords + ["art", "freelance", "work", "coffee"]))[:6]
    call screen browser_stalk
    # После браузера — переход
    if day >= 1 and shift_count >= 1:
        jump demo_end
    jump demo_end

# --- MINIGAME: Coffee ---
label minigame_coffee:
    call screen minigame_brew
    return

# --- DEMO END (оставляем желание вернуться + тихий вау) ---
label demo_end:
    scene bg room_messy with Fade(0.5, 0.3, 0.5)
    if tension >= 6:
        show cat at nd_cat_alert
        narrator "Кот всё ещё не спит. Ты знаешь о людях больше, чем они сказали. Завтра они снова придут — и ты решишь: поддержать или надавить. Или молчать."
    else:
        narrator "Одна смена — и ты уже запомнил их слова. Завтра кто-то другой сядет за тот же стол. Ты откроешь браузер снова. Night Drip только начинается."
    narrator "— Demo. Спасибо, что играли. Полная версия — больше гостей, больше судеб, больше последствий."
    return
