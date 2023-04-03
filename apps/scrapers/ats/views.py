from django.shortcuts import render
from apps.scrapers.ats.models import market_source_data_ats
from apps.scrapers.ats.scraper import ScraperATS
from asgiref.sync import sync_to_async


async def view_ats(request):

  if(request.GET.get('deleteBtn')):
    await delete_all_items()

  if(request.GET.get('refreshBtn')):
    scraper = ScraperATS()
    await scraper.scrape()

  list = await get_all_items()
  context = {"list": list}
  return render(request,'view_ats.html', context)


@sync_to_async
def get_all_items():
  return list(market_source_data_ats.objects.all())

@sync_to_async
def delete_all_items():
  return list(market_source_data_ats.objects.all().delete())

 