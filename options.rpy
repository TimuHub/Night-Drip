# Night Drip — Options
# Pastel-goth visual novel / cozy-gothic romance

define config.name = _("Night Drip")
define config.version = "0.6.0"
define gui.show_name = True
define config.save_directory = "NightDrip-163729"
define config.window = "auto"
define config.window_title = "Night Drip"
define config.screen_width = 1920
define config.screen_height = 1080
define config.developer = True

# FPS
define config.framerate = 60

# Audio
define config.has_sound = True
define config.has_music = True
define config.has_voice = False

# Text: скорость появления, пропуск, авто-продолжение
define config.allow_skipping = True
define config.skip_after_choices = False
define config.skip_delay = 3
define preferences.text_cps = 35
define preferences.afm_time = 5
define preferences.afm_enable = False

# Transitions (плавные, не резкие)
define config.enter_transition = Dissolve(0.35)
define config.exit_transition = Dissolve(0.25)
define config.intra_transition = Dissolve(0.2)
define config.main_game_transition = Dissolve(0.4)
define config.game_main_transition = Dissolve(0.3)
define config.splash_screen_transition = Fade(0.5, 0.3, 0.5)
define config.after_load_transition = Dissolve(0.3)
define config.end_splash_transition = Fade(0.5, 0.3, 0.5)
define config.end_game_transition = Fade(1.0, 0.5, 1.0)
define config.after_replay_transition = Dissolve(0.2)

# Build: Android APK — Ren'Py Launcher → Build → Android
