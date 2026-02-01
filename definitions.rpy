# Night Drip — Глобальные переменные (масштаб: десятки персонажей, сотни вариантов)
# Версии: game_version — релиз; content_version — сюжет/контент (для веток и расширений)

define game_version = "0.6.0"
define content_version = "demo_1"  # demo_1 | act_1 | act_2 | dlc_* — для бесконечного расширения сюжета

init -1 python:
    def nd_set_trust(char_id, delta):
        store.trust[char_id] = store.trust.get(char_id, 0) + delta
    def nd_set_outcome(char_id, result):
        store.outcome[char_id] = result
    def nd_set_knows(flag_name, value=True):
        store.knows_about[flag_name] = value
    def nd_set_cafe_modifier(mod_id, value=True):
        store.cafe_modifiers[mod_id] = value
    def nd_set_cat_state(state):
        store.cat_state = state

# --- Игрок ---
default player_name = "Barista"

# --- День и смена ---
default day = 1
default shift_time = "morning"  # morning / day / evening / night
default shift_count = 0  # всего отыграно смен

# --- Доверие по персонажам (id -> число) ---
default trust = {
    "sophia": 0,
    "leo": 0,
    "boss": 0,
    "student_debt": 0,
    "artist": 0,
    "runaway": 0,
    "old_man": 0,
    "influencer": 0,
}

# --- Исходы по персонажам: "locked" | "improvement" | "neutral" | "worse" ---
default outcome = {
    "sophia": "locked",
    "leo": "locked",
    "student_debt": "locked",
    "artist": "locked",
    "runaway": "locked",
    "old_man": "locked",
    "influencer": "locked",
}

# --- Сталкинг: запомненные слова за текущую смену (макс 2) ---
default remembered_keywords = []

# --- Сталкинг: какие инсайты уже видел (page_id или "keyword_character") ---
default seen_stalking_pages = []

# --- Сталкинг: флаги "знает_X_о_Y" (игрок видел страницу и может использовать знание) ---
default knows_about = {
    "sophia_art": False,
    "sophia_studio": False,
    "leo_work": False,
    "leo_sleep": False,
    "student_debt": False,
    "artist_doubt": False,
    "runaway_husband": False,
    "old_man_wife": False,
    "influencer_depression": False,
}

# --- Кафе: визуальные модификаторы (влияние исходов) ---
default cafe_modifiers = {
    "poster_barista_wanted": False,
    "artist_work_on_wall": False,
    "empty_frame": False,
    "silhouette_at_window": False,
    "broken_mug": False,
    "flowers_sophia": False,
    "two_tables_split": False,
}

# --- Атмосфера ---
default tension = 0        # 0..10, растёт от сталкинга и «тёмных» выборов
default rain_intensity = 1 # 0..3, визуал/звук дождя
default cat_state = "calm" # "calm" | "alert" | "hiding"

# --- Расписание: кто когда может прийти (для выбора сцен) ---
default schedule = {
    "morning": ["sophia", "student_debt", "old_man"],
    "day": ["sophia", "artist", "influencer"],
    "evening": ["leo", "runaway", "influencer"],
    "night": ["leo", "runaway"],
}

# --- Браузер: ввод и текущая открытая страница ---
default browser_search_input = ""
default current_browser_page = None

# --- Выбор клиента на смене (день 2+) ---
default picked = None
