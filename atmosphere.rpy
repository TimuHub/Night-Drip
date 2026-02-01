# Night Drip — Атмосфера: напряжение, кот, кафе, дождь
# Влияние на визуал и тон без морализаторства

init -1 python:
    def nd_add_tension(delta, reason=""):
        """Увеличить/уменьшить общее напряжение (сталкинг, тёмные выборы)."""
        store.tension = max(0, min(10, store.tension + delta))
        if store.tension >= 6 and store.cat_state == "calm":
            store.cat_state = "alert"
        elif store.tension >= 8:
            store.cat_state = "hiding"
        elif store.tension <= 3:
            store.cat_state = "calm"
        return None

    def nd_after_stalking():
        """Вызвать после просмотра страницы сталкинга: лёгкий рост напряжения."""
        nd_add_tension(1)
        return None

    def nd_after_dark_choice():
        """Вызвать после «тёмного» выбора (надавить, манипуляция)."""
        nd_add_tension(2)
        return None

    def nd_after_good_outcome(char_id):
        """После хорошего исхода персонажа: снизить напряжение, обновить кафе."""
        nd_add_tension(-1)
        # Пример: студент — improvement -> постер в кафе
        if char_id == "student_debt" and store.outcome.get(char_id) == "improvement":
            store.cafe_modifiers["poster_barista_wanted"] = True
        if char_id == "artist" and store.outcome.get(char_id) == "improvement":
            store.cafe_modifiers["artist_work_on_wall"] = True
        if char_id == "sophia" and store.trust.get("sophia", 0) >= 30:
            store.cafe_modifiers["flowers_sophia"] = True
        return None

    def nd_after_bad_outcome(char_id):
        """После плохого исхода: напряжение, модификаторы кафе."""
        nd_add_tension(2)
        if char_id == "student_debt" and store.outcome.get(char_id) == "worse":
            store.cafe_modifiers["silhouette_at_window"] = True
        if char_id == "artist" and store.outcome.get(char_id) == "worse":
            store.cafe_modifiers["empty_frame"] = True
        return None

    def nd_rain_intensity():
        """Текущая интенсивность дождя (0..3) по напряжению."""
        t = store.tension
        if t <= 3: return 1
        if t <= 6: return 2
        return 3
