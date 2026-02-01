# Night Drip — Characters & Images
# Pastel-goth VN: barista, Sophia, Leo, cat

# --- TRANSFORMS (анимации появления/ухода) ---
transform nd_right_slide:
    xalign 1.0 yalign 1.0
    xoffset 80
    alpha 0.0
    linear 0.35 xoffset 0 alpha 1.0

transform nd_left_slide:
    xalign 0.0 yalign 1.0
    xoffset -80
    alpha 0.0
    linear 0.35 xoffset 0 alpha 1.0

transform nd_center_fade:
    xalign 0.5 yalign 1.0
    alpha 0.0
    linear 0.3 alpha 1.0

transform nd_cat_calm:
    xalign 0.15 yalign 0.9
    zoom 0.85
    alpha 1.0

transform nd_cat_alert:
    xalign 0.15 yalign 0.9
    zoom 0.9
    alpha 1.0
    block:
        linear 0.5 zoom 0.92
        linear 0.5 zoom 0.9
        repeat

transform nd_cat_hiding:
    xalign 0.05 yalign 0.95
    zoom 0.6
    alpha 0.6

# --- CHARACTERS ---
define narrator = Character(None, what_style="narrator_text")
define mc = Character("[player_name]", color="#9f7aea")
define sophia = Character("Sophia", color="#81e6d9", image="sophia")
define leo = Character("Leo", color="#b794f4", image="leo")
define boss = Character("Boss", color="#fc8181")
define unknown = Character("???", color="#a0aec0")

# --- BACKGROUNDS ---
# Cafe (time of day)
image bg cafe_morning = "bg/cafe_morning.jpg"
image bg cafe_day = "bg/cafe_day.jpg"
image bg cafe_evening = "bg/cafe_evening.jpg"
image bg cafe_night = "bg/cafe_night.jpg"
# Other
image bg room_messy = "bg/sophia_room.jpg"
image bg street_night = "bg/street_rain.jpg"
image bg cafe_rainy = "bg/cafe_night.jpg"
image bg park_autumn = "bg/park_autumn.jpg"
image bg studio = "bg/studio.jpg"

# --- SPRITES (existing assets) ---
# Sophia: happy, neutral, sad
image sophia happy = "ch/sophia_happy.png"
image sophia neutral = "ch/sophia_neutral.png"
image sophia sad = "ch/sophia_sad.png"
# Leo: neutral, worried
image leo neutral = "ch/leo_neutral.png"
image leo worried = "ch/leo_worried.png"
# Cat (mascot / tension indicator); варианты по cat_state
image cat = "ch/cat.png"
image cat calm = Transform("ch/cat.png", **{"xalign": 0.15, "yalign": 0.9, "zoom": 0.85})
image cat alert = Transform("ch/cat.png", **{"xalign": 0.15, "yalign": 0.9, "zoom": 0.9})
image cat hiding = Transform("ch/cat.png", **{"xalign": 0.05, "yalign": 0.95, "zoom": 0.6, "alpha": 0.6})

# Placeholder for missing emotions (optional — add when you have art)
# image sophia angry = "ch/sophia_angry.png"
# image sophia surprised = "ch/sophia_surprised.png"
# image leo happy = "ch/leo_happy.png"
# image leo sad = "ch/leo_sad.png"
