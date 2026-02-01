# Night Drip — Custom Screens
# Say, Main Menu, Quick Menu, Phone, Minigame, Browser

default phone_messages_shown = 0

# --- SAY (диалог): окно + имя + текст (обязательные id: window, who, what) ---
screen say(who, what):
    window id "window" style "say_window":
        vbox:
            spacing 8
            if who:
                window id "namebox" style "say_namebox":
                    text who id "who" style "say_label"
            text what id "what" style "say_dialogue"

# --- MAIN MENU ---
screen main_menu():
    tag menu
    add "bg room_messy" at transform:
        zoom 1.05
        alpha 0.7
    frame style "main_menu_frame" xalign 0.5 yalign 0.5:
        vbox spacing 28 xalign 0.5:
            text "NIGHT DRIP" style "main_menu_title" xalign 0.5
            null height 24
            textbutton _("Новая игра") action Start() style "choice_button" text_style "choice_button_text" xalign 0.5
            textbutton _("Загрузить") action ShowMenu("load") style "choice_button" text_style "choice_button_text" xalign 0.5
            textbutton _("Настройки") action ShowMenu("preferences") style "choice_button" text_style "choice_button_text" xalign 0.5
            null height 12
            text "v[config.version]" style "main_menu_version" xalign 0.5

# --- QUICK MENU (в игре) ---
screen quick_menu():
    hbox xalign 0.5 yalign 1.0 yoffset -8 spacing 16:
        textbutton _("История") action ShowMenu("history") style "quick_button" text_style "quick_button_text"
        textbutton _("Пропуск") action Skip() style "quick_button" text_style "quick_button_text"
        textbutton _("Авто") action Preference("auto-forward", "toggle") style "quick_button" text_style "quick_button_text"
        textbutton _("Сохранить") action ShowMenu("save") style "quick_button" text_style "quick_button_text"
        textbutton _("Загрузить") action ShowMenu("load") style "quick_button" text_style "quick_button_text"
        textbutton _("Настройки") action ShowMenu("preferences") style "quick_button" text_style "quick_button_text"

# --- GAME MENU (пауза) ---
screen game_menu(title):
    tag menu
    add "#1a202ccc"
    frame style "main_menu_frame" xalign 0.5 yalign 0.5:
        vbox spacing 20 xalign 0.5:
            text title style "say_label" xalign 0.5
            null height 16
            use quick_menu_inside

screen quick_menu_inside():
    vbox spacing 12 xalign 0.5:
        textbutton _("Продолжить") action Return() style "choice_button" text_style "choice_button_text"
        textbutton _("Сохранить") action ShowMenu("save") style "choice_button" text_style "choice_button_text"
        textbutton _("Загрузить") action ShowMenu("load") style "choice_button" text_style "choice_button_text"
        textbutton _("Настройки") action ShowMenu("preferences") style "choice_button" text_style "choice_button_text"
        textbutton _("Главное меню") action MainMenu() style "choice_button" text_style "choice_button_text"

# --- SAVE / LOAD (минимальные слоты) ---
screen save():
    tag menu
    use game_menu(_("Сохранить"))
    vbox xalign 0.5 yalign 0.55 spacing 14:
        for i in range(1, 6):
            textbutton _("Слот %s") % i action FileSave(i) style "choice_button" text_style "choice_button_text"

screen load():
    tag menu
    use game_menu(_("Загрузить"))
    vbox xalign 0.5 yalign 0.55 spacing 14:
        for i in range(1, 6):
            textbutton _("Слот %s") % i action FileLoad(i) style "choice_button" text_style "choice_button_text"

# --- PREFERENCES ---
screen preferences():
    tag menu
    use game_menu(_("Настройки"))
    vbox xalign 0.5 yalign 0.55 spacing 16:
        null height 20
        text _("Скорость текста") style "say_label"
        bar value Preference("text speed") range 20 100 style "slider" xsize 400
        text _("Громкость музыки") style "say_label"
        bar value Preference("music volume") style "slider" xsize 400
        text _("Громкость звука") style "say_label"
        bar value Preference("sound volume") style "slider" xsize 400

# --- HISTORY ---
screen history():
    tag menu
    add "#1a202cee"
    frame style "say_window" xalign 0.5 yalign 0.5 xsize 900:
        viewport:
            scrollbars "vertical"
            mousewheel True
            vbox spacing 12:
                for h in _history_list:
                    if h.who:
                        text h.who style "say_label" size 22
                    text h.what style "say_dialogue" size 24
                null height 20
        textbutton _("Назад") action Return() style "choice_button" text_style "choice_button_text" xalign 0.5 yalign 1.0 yoffset 8
default brew_score = 0
default brew_time_left = 5

# --- PHONE: Boss morning ---
screen phone_boss_morning():
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xsize 400
        ysize 700
        background "#1a202c"
        padding (20, 20)
        vbox:
            spacing 10
            text "Boss" size 24 color "#81e6d9"
            null height 20
            text "Where are you? Shift started 10 mins ago!" size 20 color "#e2e8f0" xalign 0.0
            text "06:30" size 14 color "#718096"
            null height 10
            text "Last warning." size 20 color "#e2e8f0" xalign 0.0
            text "06:31" size 14 color "#718096"
            null height 40
            text "Reply:" size 18 color "#a0aec0"
            textbutton "Sorry, running late!":
                action [Function(nd_set_trust, "boss", 5), Return()]
                text_style "choice_button_text"
            textbutton "I quit.":
                action [Function(nd_set_trust, "boss", -100), Return()]
                text_style "choice_button_text"
            textbutton "(Ignore)":
                action [Function(nd_set_trust, "boss", 0), Return()]
                text_style "choice_button_text"

# --- MINIGAME: Brew coffee (tap) ---
screen minigame_brew():
    default brew_score = 0
    default brew_time_left = 5
    timer 1.0 repeat True action If(brew_time_left > 0, SetScreenVariable("brew_time_left", brew_time_left - 1), Return())
    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 500
        background "#2d3748"
        vbox:
            xalign 0.5
            spacing 20
            text "BREW THE COFFEE!" size 36 color "#81e6d9" xalign 0.5
            text "TAP RAPIDLY!" size 24 color "#f687b3" xalign 0.5
            null height 20
            textbutton "TAP":
                xalign 0.5
                action SetScreenVariable("brew_score", brew_score + 10)
                text_size 32
                text_color "#1a202c"
                background "#81e6d9"
                hover_background "#f687b3"
            text "Score: [brew_score]" size 28 color "#e2e8f0" xalign 0.5
            text "Time: [brew_time_left]s" size 28 color "#e2e8f0" xalign 0.5

# --- BROWSER (stalking): ввод слова → одна страница инсайта ---
screen browser_stalk():
    modal True
    frame:
        xsize 900
        ysize 700
        xalign 0.5
        yalign 0.5
        background "#0d1117"
        padding (30, 30)
        vbox:
            spacing 16
            text "Поиск" size 22 color "#81e6d9"
            input:
                value VariableInputValue("browser_search_input")
                length 40
                allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            textbutton "Искать":
                action Function(nd_do_browser_search)
            null height 12
            text "Слова из смены (можно ввести любое): [remembered_keywords]" size 16 color "#718096"
            null height 12
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 840
                ysize 420
                vbox:
                    spacing 12
                    if current_browser_page:
                        text current_browser_page.get("title", "") size 20 color "#81e6d9"
                        null height 8
                        text current_browser_page.get("body", "") size 18 color "#e2e8f0"
                        if current_browser_page.get("warning"):
                            null height 8
                            text "[!] " + current_browser_page.get("warning", "") size 16 color "#f687b3"
                    else:
                        text "Введи слово, которое запомнил из разговора в кафе — и нажми Search. Один поиск = одна страница. То, что они не сказали вслух." color "#718096" size 18
                        null height 12
                        text "Подсказка: art, freelance, work, coffee (англ.); долг, депрессия (рус.)." color "#4a5568" size 16
            textbutton "Закрыть":
                action [SetVariable("current_browser_page", None), Return()]
                xalign 0.5
