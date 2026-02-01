# Night Drip — Pastel-goth GUI
# Цвета: мята, лаванда, розовый + тёмный фон. Шрифт: положи VT323-Regular.ttf в gui/fonts/

init -1 python:
    nd_mint = "#81e6d9"
    nd_lavender = "#b794f4"
    nd_pink = "#f687b3"
    nd_dark = "#1a202c"
    nd_darker = "#0d1117"
    nd_text = "#e2e8f0"
    nd_accent = nd_mint
    # Шрифт: если есть gui/fonts/VT323-Regular.ttf — раскомментировать и использовать
    nd_font = None  # "gui/fonts/VT323-Regular.ttf"

init -1 style default:
    size 28
    color nd_text
    outlines [(2, nd_dark, 0, 0)]
    if nd_font:
        font nd_font

init -1 style narrator_text:
    size 26
    color "#cbd5e0"
    italic True
    if nd_font:
        font nd_font

init -1 style say_label:
    color nd_mint
    bold True
    size 28
    if nd_font:
        font nd_font

init -1 style say_dialogue:
    color nd_text
    size 28
    if nd_font:
        font nd_font

init -1 style say_window:
    background "#1a202cee"
    padding (32, 28)
    outline_width 2
    outline_color nd_mint
    xsize 1200
    ysize 220

init -1 style say_namebox:
    background nd_mint
    padding (14, 8)
    xoffset 20
    yoffset -8

init -1 style button:
    background "#2d3748"
    hover_background nd_mint
    selected_background nd_lavender
    padding (24, 12)
    outline_width 2
    outline_color nd_mint

init -1 style choice_button:
    background "#2d3748"
    hover_background nd_pink
    padding (20, 16)
    outline_width 2
    outline_color nd_lavender

init -1 style choice_button_text:
    color nd_text
    hover_color "#1a202c"
    size 26
    if nd_font:
        font nd_font

init -1 style quick_button:
    background "#2d3748"
    hover_background nd_mint
    padding (12, 8)
    xsize 160

init -1 style quick_button_text:
    color nd_text
    hover_color nd_darker
    size 20
    if nd_font:
        font nd_font

init -1 style main_menu_frame:
    background "#1a202cee"
    padding (48, 36)
    outline_width 3
    outline_color nd_mint

init -1 style main_menu_title:
    color nd_mint
    size 72
    bold True
    outlines [(3, nd_darker, 0, 0)]
    if nd_font:
        font nd_font

init -1 style main_menu_version:
    color "#718096"
    size 18
    if nd_font:
        font nd_font

init -1 style slider:
    xsize 400
    left_bar "#2d3748"
    right_bar nd_mint
    thumb_offset 8
