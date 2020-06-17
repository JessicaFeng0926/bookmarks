from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # 这样，在images应用加载好的时候，
        # 信号接收程序也就导进来了
        import images.signals
