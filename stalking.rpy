# Night Drip — Сталкинг: ключевые слова → страницы (инсайты)
# Масштаб: десятки персонажей, сотни страниц

init -1 python:
    # Страницы сталкинга: keyword -> список страниц (или keyword+character -> одна страница)
    # Каждая страница: id, title, body_text, image (путь), sets_flag, warning (опционально)
    STALKING_PAGES = {
        "art": [
            {
                "id": "sophia_art",
                "character": "sophia",
                "title": "ArtStation / @soph_drafts",
                "body": "Последний пост: «Никогда больше не буду рисовать на заказ. Только для себя.»\n\nНиже: серия скетчей — тёмная комната, окно с дождём, силуэт за ноутбуком. Подпись: «Это не про тебя, студия. Это про меня.»",
                "image": "browser/sophia_art.png",
                "sets_flag": "sophia_art",
                "warning": "Если сказать, что видел её работы — риск потерять доверие.",
            },
        ],
        "freelance": [
            {
                "id": "sophia_studio",
                "character": "sophia",
                "title": "LinkedIn / бывший коллега",
                "body": "Переписка (скрин): «Софь, они до сих пор выставляют твои макеты как свои. Ты что, не подашь?» — «Не хочу вспоминать. Я ушла. Всё.»",
                "image": "browser/sophia_studio.png",
                "sets_flag": "sophia_studio",
                "warning": "Упоминание студии может её ранить или разозлить.",
            },
        ],
        "work": [
            {
                "id": "leo_work",
                "character": "leo",
                "title": "Glassdoor / отзывы о компании",
                "body": "«Токсичная среда. Руководство не слышит. Уволился после двух лет.» — 2 месяца назад.\n\nНиже ещё один: «Бессонница из-за дедлайнов. Кофе по ночам — единственное, что держит.»",
                "image": "browser/leo_work.png",
                "sets_flag": "leo_work",
                "warning": "Давить на тему работы — он может закрыться.",
            },
        ],
        "coffee": [
            {
                "id": "leo_sleep",
                "character": "leo",
                "title": "Форум / бессонница",
                "body": "Старый комментарий (ник не совпадает с именем, но детали сходятся): «Когда-нибудь уйду из этого города. Пока что единственное место, где могу сидеть ночью и не объяснять — одно кафе. Там не спрашивают.»",
                "image": "browser/leo_sleep.png",
                "sets_flag": "leo_sleep",
                "warning": "Сказать, что знаешь — он может почувствовать, что его «вычислили».",
            },
        ],
        "долг": [
            {
                "id": "student_debt",
                "character": "student_debt",
                "title": "Локальная группа / объявления",
                "body": "«Ищем людей на разовую подработку. Оплата сразу.» — много комментариев «осторожно, схема». Ниже: пост от человека с тем же описанием, что и студент: «Нужны деньги до сессии. Кто знает честные варианты?»",
                "image": "browser/student_debt.png",
                "sets_flag": "student_debt",
                "warning": "Подтолкнуть к «лёгким деньгам» — плохой исход. Честный совет — постер «ищем бариста» в кафе.",
            },
        ],
        "депрессия": [
            {
                "id": "influencer_depression",
                "character": "influencer",
                "title": "Закрытый аккаунт (скрин от «друга»)",
                "body": "Пост: «Сегодня снова не могу встать. В сторис — улыбка и кофе. Никто не знает.»\n\nХэштеги: #выгорание #тихо",
                "image": "browser/influencer_depression.png",
                "sets_flag": "influencer_depression",
                "warning": "Дать понять, что здесь можно быть не идеальной — риск или шанс, в зависимости от тона.",
            },
        ],
    }

    def nd_get_stalking_page(keyword):
        """По ключевому слову возвращает первую подходящую страницу или None."""
        if not keyword:
            return None
        kw = keyword.strip().lower()
        for k, pages in STALKING_PAGES.items():
            if k in kw or kw in k:
                if pages and pages[0]["id"] not in store.seen_stalking_pages:
                    return pages[0]
        return None

    def nd_mark_page_seen(page_id):
        store.seen_stalking_pages.append(page_id)
        return None

    def nd_set_knows_from_page(page):
        if page and page.get("sets_flag"):
            store.knows_about[page["sets_flag"]] = True
        return None

    def nd_do_browser_search():
        """Выполнить поиск по введённому слову: показать страницу, отметить просмотр, дать флаг, поднять напряжение."""
        kw = store.browser_search_input.strip()
        page = nd_get_stalking_page(kw)
        if page:
            store.current_browser_page = page
            nd_mark_page_seen(page["id"])
            nd_set_knows_from_page(page)
            nd_after_stalking()  # определена в atmosphere.rpy
        else:
            store.current_browser_page = {
                "title": "Ничего не найдено",
                "body": "Попробуйте другое слово. Или запомните ключевые слова из разговоров в кафе.",
                "image": None,
                "warning": None,
            }
        return None
