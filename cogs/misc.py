import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import base64
from os import path
from os import mkdir
import config
import datetime

cookies = {
    '_ga': 'GA1.1.901042886.1703880994',
    '_ga_FS4ESHM7K5': 'GS1.1.1703980642.3.0.1703980642.0.0.0',
    'fp': '9d384e9f00beea637f4f7098f5cf10c1',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/ \
              avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


class Workers:
    @staticmethod
    async def _get_countries():
        if path.exists('./misc_files/index.html') is False:
            response = requests.get('http://free-proxy.cz/en/', cookies=cookies, headers=headers)
            mkdir('./misc_files/')
            with open('./misc_files/index.html', 'w') as file:
                file.write(response.text)

        with open('./misc_files/index.html', 'r') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        countries = soup.find('select', id='frmsearchFilter-country').find_all('option')

        dictionary = {}

        for c in countries:
            short_name = c.get('value')

            name = c.text.split('(')
            dictionary[short_name] = name[0].strip()
        return dictionary

    @staticmethod
    def _get_proxy(country):
        url_dump = f'http://free-proxy.cz/en/proxylist/country/{country}/all/ping/all'
        s = requests.Session()
        response = requests.get(url_dump, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        table_trs = soup.find('table', id='proxy_list').find('tbody').find_all('tr')

        ip_list = []

        for tr in table_trs:
            try:
                ip = tr.find('td').find('script').text
            except Exception as ex:
                print(ex)
                continue

            if ip:
                ip = base64.b64decode(ip.split('"')[1]).decode('utf-8')
                port = tr.find('span', class_='fport').text
                ip_list.append(f'{ip}:{port}')
            else:
                continue

        date = datetime.date

        if path.exists(f'cashed_proxy/ip_list_{country}_{date.today()}.txt') is False:
            with open(f'cashed_proxy/ip_list_{country}_{date.today()}.txt', 'w') as file:
                file.writelines(f'{ip}\n' for ip in ip_list)

        with open(f'cashed_proxy/ip_list_{country}_{date.today()}.txt') as file:
            statement = f'{file.read()}'

        return statement


class Misc(commands.Cog, Workers):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def proxy_countries(self, ctx):
        """Выводит список доступных стран для поиска в команде 'proxy'"""
        dictionary = await self._get_countries()
        statement = ''
        for keys, values in dictionary.items():
            statement += f'{keys} -- {values}\n'
        statement += f'\n\nUse shortcuts like "US" for {config.settings.get("prefix")}proxy command'
        embed = discord.Embed(color=0x191F46, title='Proxy Countries', description=statement)
        await ctx.send(embed=embed)

    @commands.command()
    async def proxy(self, ctx, *, country):
        """Выводит прокси для выбранной страны, пример тега: US, RU, CZ"""
        proxy = self._get_proxy(country)
        embed = discord.Embed(color=0x191F46, title=f'Proxy List for {country}', description=proxy.strip())
        await ctx.send(embed=embed)

    # @commands.command()
    # async def proxy_check(self, ctx, *, proxy):
    #     """
    #     Проверяет прокси на валидность
    #     Не работает.
    #     """
    #     print(proxy)
    #     checker = ProxyChecker()
    #     proxy = proxy.strip()
    #     check = checker.check_proxy(proxy, check_country=False, check_address=True)
    #     country = checker.get_country(proxy)
    #     embed = discord.Embed(color=0x191F46, title=f'Proxy check for {proxy}',
    #                           description=f'{check} | {country} | {proxy}')
    #     await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
