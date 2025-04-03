class DataMixin:
    """
    Mixin для добавления заголовка страницы
    """
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['page_title'] = self.title_page