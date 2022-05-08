import csv
import os
import uuid

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from metadata.models import Music
from metadata.util import read_csv_file, clean_csv_data, write_csv_to_database

raw_test__data = [
    ['title', 'contributors', 'iswc'],
    ['Shape of You', 'Edward Christopher Sheeran', 'T9204649558'],
    ['Adventure of a Lifetime', 'O Brien Edward John|Yorke Thomas Edward|Greenwood Colin Charles',
     'T0101974597'],
    ['Adventure of a Lifetime', 'O Brien Edward John|Selway Philip James', 'T0101974597'],
    ['Me Enamoré', 'Rayo Gibo Antonio|Ripoll Shakira Isabel Mebarak', 'T9214745718'],
    ['Je ne sais pas', 'Obispo Pascal Michel|Florence Lionel Jacques', ''],
    ['Je ne sais pas', 'Obispo Pascal Michel|Florence Lionel Jacques', 'T0046951705']
]

test_music_data = [
    {'title': 'A song about love', 'contributors': 'Ad Homen|Ray Ban', 'iswc': 'T8983567112'},
    {'title': 'Be happy', 'contributors': 'Knight King|Charles Bruck|Henry Mart', 'iswc': 'T8983457112'},
    {'title': 'Cry no more', 'contributors': 'Saint Mark|Puff Diddy', 'iswc': 'T1233567112'},
    {'title': 'I will be there', 'contributors': 'Booby Hings|', 'iswc': 'T7303567112'}
]


class TestUtil(TestCase):

    def setUp(self):
        self.file_name = 'test.csv'
        with open(self.file_name, 'w') as test_file:
            writer = csv.writer(test_file)
            writer.writerow(raw_test__data[0])
            writer.writerow(raw_test__data[1])
            writer.writerow(raw_test__data[2])
            writer.writerow(raw_test__data[3])
            writer.writerow(raw_test__data[4])
            writer.writerow(raw_test__data[5])
            writer.writerow(raw_test__data[6])

        self.bad_file = 'test.txt'
        with open(self.bad_file, 'w') as f:
            f.write('readme')

    def tearDown(self) -> None:
        os.remove(self.file_name)
        os.remove(self.bad_file)

    def test_read_csv_with_csv_extension(self):
        data_csv = read_csv_file(self.file_name)
        self.assertEqual(type(data_csv), list)
        self.assertEqual(type(data_csv[0]), dict)

    def test_read_csv_with_not_allowed_extension(self):
        with self.assertRaises(ValueError):
            data_txt = read_csv_file(self.bad_file)
            self.assertEqual(data_txt, 'Only CSV files are allowed')

    def test_read_csv_with_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            read_csv_file('non_existent.csv')

    def test_clean_csv_data_with_csv_file(self):
        data_csv = clean_csv_data(self.file_name)
        self.assertEqual(type(data_csv), dict)

    def test_clean_csv_data_with_file_with_no_extension(self):
        with self.assertRaises(FileNotFoundError):
            clean_csv_data('test')

    def test_clean_csv_data_with_bad_file_extension(self):
        with self.assertRaises(ValueError):
            clean_csv_data(self.bad_file)

    def test_write_csv_to_database_with_file_no_extension(self):
        with self.assertRaises(FileNotFoundError):
            write_csv_to_database('test')

    def test_write_csv_to_database_with_bad_file_extension(self):
        with self.assertRaises(ValueError):
            write_csv_to_database(self.bad_file)

    def test_write_csv_to_database_with_csv_file_extension(self):
        data_csv = write_csv_to_database(self.file_name)
        self.assertEqual(Music.objects.all().count(), 4)
        self.assertEqual(data_csv, 'Music data loaded successfully')


class TestMusicViewSet(TestCase):
    def setUp(self) -> None:
        for music_data in test_music_data:
            Music.objects.create(title=music_data.get('title'), contributors=music_data.get('contributors'),
                                 iswc=music_data.get('iswc'), id=uuid.uuid4())

    def test_get_music_by_iswc_with_existing_iswc_value(self):
        response = self.client.get(reverse('music-get-music-by-iswc'), {'iswc': 'T8983567112'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response), JsonResponse)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(response.json()[0].get('contributors'), 'Ad Homen|Ray Ban')

    def test_get_music_by_iswc_with_non_existing_iswc_value(self):
        response = self.client.get(reverse('music-get-music-by-iswc'), {'iswc': 'T8213567113'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response), JsonResponse)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(type(response.json()), list)
