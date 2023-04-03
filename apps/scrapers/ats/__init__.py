# # Требуется отдельное DJango app с Celery (или другой инструмент) для настройки шедулинга.
# # Сейчас псевдокод

import threading

class ATSScheduler:

    def loadData(self):
        print("Загрузка данных...")
        # запуск обнвления данных - ScraperATS().scrape()
        print("Загрузка данных завершена...") 
        threading.Timer(30, self.loadData).start()

    