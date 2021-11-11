from typing import List, Dict
from datetime import date
import re

from .dto import ScrappedEvent

import requests
from bs4 import BeautifulSoup


class AfishaUzScraper:
    """
    Scraper for events from https://afisha.uz
    """
    _HOST = 'https://www.afisha.uz'

    def scrape_categories(self, categories: List[str]) -> Dict[str, List[ScrappedEvent]]:
        """
        Scrape events from categories on https://afisha.uz
        :param categories: allowed categories to scrape
        :return: list with data of scrapped events
        """
        categories_links = self._get_categories_links(categories)
        result = {}
        for link in categories_links:
            events = self._try_parse_category(link)
            result[link] = events
        return result

    def _get_categories_links(self, categories: List[str]):
        home_page_response = requests.get(self._HOST)
        home_page_soup = BeautifulSoup(home_page_response.text, 'html.parser')
        menu_soup = home_page_soup.find('ul', {'class': 'menu'})
        links = []
        for category in categories:
            menu_a_bs = menu_soup.find('a', text=category)
            links.append(self._HOST + menu_a_bs['href'])
        return links

    def _try_parse_category(self, link: str) -> List[ScrappedEvent]:
        events = self._parse_table_type_category(link)
        if len(events) == 0:
            events = self._parse_block_type_category(link)
        return events

    def _parse_table_type_category(self, link: str) -> List[ScrappedEvent]:
        category_response = requests.get(link)
        category_bs = BeautifulSoup(category_response.text, 'html.parser')
        category_tables = category_bs.find_all('table', {'class': 'when-list mat-list'})
        result = []
        for table in category_tables:
            table_what_td = table.find('td', {'class': 'what'})
            table_what_td_events = table_what_td.findChildren('div', class_=lambda x: x != 'next-item2',
                                                              recursive=False)
            events = []
            for table_event in table_what_td_events:
                table_event_content = table_event.find('div', {'class': 'item2'})
                table_event_link = table_event_content.find('h3').find('a')['href']
                table_event_content_desc = table_event_content.find('p', {'class': 'desc'}).text
                scraped_event = self._scrape_event(self._HOST + table_event_link)
                scraped_event.short_description = table_event_content_desc
                events.append(scraped_event)
            result.extend(events)
        return result

    def _parse_block_type_category(self, link: str) -> List[ScrappedEvent]:
        category_response = requests.get(link)
        category_bs = BeautifulSoup(category_response.text, 'html.parser')
        events = []
        main_event_bs = category_bs.find('div', {'class': 'block_grey'})
        main_event_link = main_event_bs.find('a')['href']
        main_event = self._scrape_event(self._HOST + main_event_link)
        main_event.short_description = main_event_bs.find('a').find('span').find('p').text
        events.append(main_event)
        events_block_bs = category_bs.find('div', {'class': 'block-blank'})
        regex = re.compile('c2.*')
        events_bs = events_block_bs.find_all('div', {'class': regex})
        for event_bs in events_bs:
            event_link = event_bs.findChild('a', recursive=False)['href']
            scraped_event = self._scrape_event(self._HOST + event_link)
            desc = event_bs.find('div', {'class': 'desc'}).find('p').text
            scraped_event.short_description = desc
            events.append(scraped_event)
        return events

    def _scrape_event(self, link: str) -> ScrappedEvent:
        event_response = requests.get(link)
        event_bs = BeautifulSoup(event_response.text, 'html.parser')
        event_title = event_bs.find('div', {'class': 'body'}).findChild('h1', recursive=False).text
        date_place_block = event_bs.find('div', {'class': 'wherewhen'})
        date = None
        place = None
        if date_place_block:
            date = date_place_block.find_all('p')[0].text
            place = date_place_block.find_all('p')[1].text
        image_url = event_bs.find('th', {'class', 'image'}).find('img')['src']
        event_content = str(event_bs.find('div', {'class', 'js-mediator-article'}))
        return ScrappedEvent(
            event_title,
            date=date,
            place=place,
            description=event_content,
            image_url=image_url
        )
