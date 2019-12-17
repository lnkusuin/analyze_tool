from external.socialbakers.model import MONTHLY_LIST
from external.socialbakers.repository import SocialBakersRepository, LocalRepository


class SocialBakersService:

    @staticmethod
    def scraping_twitter(month, output_dir):
        twitter_data = SocialBakersRepository.scraping_from_japan_report_of_twitter_by_monthly(month)
        return LocalRepository.save_to_csv(twitter_data, output_dir)


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
    # SocialBakersService.scraping_twitter(MONTHLY_LIST["DECEMBER"], out_dir)
