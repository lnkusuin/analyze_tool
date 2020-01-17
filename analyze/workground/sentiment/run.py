from asari.api import Sonar

import os

import setting
from context.nlp import CleanText
from external.twitter.common import convert_from_utc_to_jst
from repository import FileRepository


def main(json_path):
    sonar = Sonar()
    results = []

    for item in FileRepository.load_json(json_path):
        text = CleanText(item['text']).to_adjust_line_code().text

        if text.startswith('RT '):
            continue

        ret = sonar.ping(text=text)
        results.append({
            'text': text,
            'created_at': str(convert_from_utc_to_jst(item['created_at'])),
            'negative': -[x['confidence'] for x in ret['classes'] if x['class_name'] == 'negative'][0],
            'positive': [x['confidence'] for x in ret['classes'] if x['class_name'] == 'positive'][0],
        })

    FileRepository.to_csv(results, 'results.csv')


if __name__ == '__main__':
    """ Twitterで収集した情報からセンチメント分析を行いファイルに結果を保存します。"""
    main(os.environ['JSON_PATH'])
