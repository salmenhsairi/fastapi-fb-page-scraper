from typing import Any, Mapping, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import logging


logger = logging.getLogger(__name__)


def has_numbers(input_str):
    return any(char.isdigit() for char in input_str)


class FacebookScraper:
    def __init__(self, url) -> None:
        self.url = url
        self.browser = None
        self.soup = None
        self.initialized = False
        self.key = None
        self.description_section = None
        self.posts_section = None

    async def initialize(self) -> None:
        await self.__open_brower()
        await self.__refresh_soup()
        self.key = self.__get_key()
        self.initialized = True

    async def __open_brower(self):
        logger.info('starting chrome browser')
        chrome_options = Options()
        # disable notifications
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument("--start-maximized")
        # open chrome in private mode to disable cookies
        chrome_options.add_argument('--incognito')
        self.browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)

    async def __refresh_soup(self):
        html = self.browser.page_source
        src = bytes(html, 'utf-8')
        self.soup = BeautifulSoup(src, "html.parser")
        self.description_section = self.__get_description_section()
        self.posts_section = self.__get_posts_section()

    def __get_key(self) -> Union[str, None]:
        parse = urlparse(self.url)
        key = parse.path.strip('/')
        return key

    async def is_valid_page(self) -> bool:
        valid = False
        await self.__refresh_soup()
        if self.key and self.key.find('/') == -1:
            if isinstance(self.soup, BeautifulSoup) and self.soup.findAll(text="Page transparency"):
                valid = True
        if not valid:
            return False
        return True

    def __get_description_section(self) -> Union[any, None]:
        description_section = self.soup.find(
            "div", class_="bdao358l om3e55n1 g4tp4svg aeinzg81 cgu29s5g i15ihif8 th51lws0 h07fizzr mfn553m3 jbg88c62 s9djjbeh svm27lag ksav2qyx sl4bvocy")
        return description_section

    def __get_posts_section(self) -> Union[any, None]:
        posts_section = self.soup.find(
            "div", class_="bdao358l om3e55n1 g4tp4svg aeinzg81 cgu29s5g i15ihif8 th51lws0 h07fizzr mfn553m3 jbg88c62 s9djjbeh t1fg2s7t ksav2qyx")
        return posts_section

    def __get_basic_info(self):
        title = str(self.soup.find(
            'meta', property='og:title').attrs['content'])
        location_tag = self.description_section.find(
            'span', class_="b6ax4al1 lq84ybu9 hf30pyar om3e55n1")
        location = location_tag.text if location_tag else None
        created_at_tag = self.description_section.find(
            "span", class_='gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas m2nijcs8 hxfwr5lz k1z55t6l oog5qr5w innypi6y pbevjfx6')
        created_at = created_at_tag.text.split(
            '-')[-1].strip() if created_at_tag and created_at_tag.text.find('Page created') != -1 else None

        description_a_tags = self.description_section.find_all(
            'a', class_="qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq cxfqmxzd ezidihy3")
        filtered_website = list(filter(lambda a: a.text.startswith(
            'http') or a.text.startswith('https'), description_a_tags))
        filtered_email = list(
            filter(lambda a: a.attrs['href'].startswith('mailto:'), description_a_tags))

        website = filtered_website[0].text if filtered_website else None
        email = filtered_email[0].text if filtered_email else None
        return {'title': title, 'location': location, 'website': website, 'email': email, "created_at": created_at}

    @staticmethod
    def __get_stats(description_span_tag):
        description_stat_text = list(
            map(lambda span: span.text, description_span_tag))
        description_stat_text.append('')
        stats_dict = {'like': [], 'follow': [], 'checked_in': []}
        logger.info(stats_dict)
        for stat_key in stats_dict.keys():
            def filter_func(t): return ((t.find(stat_key.replace('_', ' ')) != -1
                                         or (description_stat_text[description_stat_text.index(t)+1].find(stat_key.replace('_', ' ')) != -1)
                                         and not has_numbers(description_stat_text[description_stat_text.index(t)+1]))
                                        and has_numbers(t)
                                        )
            filter_list = list(filter(filter_func, description_stat_text[:-1]))
            stats_dict[stat_key] = filter_list[0].split()[
                0] if filter_list else None
        return stats_dict

    def __get_description_section_fields(self):
        basic_info = self.__get_basic_info()
        description_span_tag = self.description_section.find_all(
            'span', class_='gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw k1z55t6l oog5qr5w tes86rjd pbevjfx6')
        stats = self.__get_stats(description_span_tag)
        drop_na_basic_info = {k: v for k,
                              v in basic_info.items() if basic_info[k]}
        drop_na_stats = {k: v for k, v in stats.items() if stats[k]}
        return {**drop_na_basic_info, **drop_na_stats}

    @staticmethod
    def __get_single_post_content(post_description, single_post_stat):
        post_stats = {"description": None, "reacts": None,
                      "comments": None, "shares": None}
        post_stats['description'] = post_description.text
        post_stats['reacts'] = single_post_stat.find(
            'span', class_="nnzkd6d7").text
        comments_shares = single_post_stat.find_all(
            'span', class_="gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas m2nijcs8 hxfwr5lz k1z55t6l oog5qr5w tes86rjd rtxb060y")
        if comments_shares:
            for item in comments_shares:
                if item.text.find('Comments') != -1 or item.text.find('Comment') != -1:
                    post_stats['comments'] = item.text.split()[0]
                elif item.text.find('Shares') != -1 or item.text.find('Share') != -1:
                    post_stats['shares'] = item.text.split()[0]
        return {k: v for k, v in post_stats.items() if v}

    def __get_posts(self):
        post_descriptions = self.posts_section.find_all(
            "span", class_="gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas m2nijcs8 hxfwr5lz k1z55t6l oog5qr5w tes86rjd pbevjfx6 ztn2w49o")
        post_stats = self.posts_section.find_all(
            'div', class_="hf30pyar lq84ybu9 ta68dy8c kpwa50dg lk0hwhjd cmg2g80i")
        # try:
        #     assert len(post_descriptions) == len(post_stats)
        # except AssertionError as e:
        #     raise (Exception("cannot handle page posts"))

        posts = []
        for description, stat in zip(post_descriptions, post_stats):
            posts.append(self.__get_single_post_content(description, stat))
        return posts

    async def get_page_data(self):
        await self.__refresh_soup()
        description_section_fields = self.__get_description_section_fields()
        posts = self.__get_posts()
        return {"url": self.url, "key": self.key, **description_section_fields, 'posts': posts}

    async def scroll_down(self):
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        await self.__refresh_soup()

    def close_browser(self) -> None:
        self.browser.quit()


def check_valid_url(url) -> Union[bool, None]:
    parse = urlparse(url)
    domain = parse.hostname
    key = parse.path.strip('/')
    if (domain != 'www.facebook.com' and domain != 'facebook.com') or not key:
        return False
    return True


async def scrap_fb_page(url="https://www.facebook.com/GOOAL-TN-388424355107967") -> Union[Mapping[str, Any], None]:
    # url = "https://www.facebook.com/sports24tunisie"
    facebook_scraper = FacebookScraper(url)
    if not facebook_scraper.initialized:
        await facebook_scraper.initialize()
    if not await facebook_scraper.is_valid_page():
        facebook_scraper.close_browser()
        raise (
            Exception('please make sure that the provided URL is a valid facebook page structure'))
    time.sleep(5)
    fb_page_data = await facebook_scraper.get_page_data()
    facebook_scraper.close_browser()
    return fb_page_data
