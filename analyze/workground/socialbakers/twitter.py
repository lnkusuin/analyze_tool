import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from external.socialbakers.model import MONTHLY_LIST
from external.socialbakers.service import SocialBakersService

if __name__ == '__main__':
    out_dir = "./"
    SocialBakersService.scraping_twitter(MONTHLY_LIST["JANUARY"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["FEBRUARY"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["MARCH"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["APRIL"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["MAY"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["JUNE"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["JULY"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["AUGUST"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["SEPTEMBER"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["OCTOBER"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["NOVEMBER"], out_dir)
    SocialBakersService.scraping_twitter(MONTHLY_LIST["DECEMBER"], out_dir)