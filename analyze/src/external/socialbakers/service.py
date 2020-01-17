from external.socialbakers.repository import SocialBakersRepository, LocalRepository


class SocialBakersService:

    @staticmethod
    def scraping_twitter(month, output_dir, year='2019'):
        twitter_data = SocialBakersRepository.scraping_from_japan_report_of_twitter_by_monthly(month, year)
        return LocalRepository.save_to_csv(twitter_data, output_dir)