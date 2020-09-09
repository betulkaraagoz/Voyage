import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from accommodation.models import Hotel, Room


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('accommodation/management/commands/db.csv', "r", encoding="UTF-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    if line_count <200:
                        owner = User.objects.get(username='betul')
                    elif line_count <400:
                        owner = User.objects.get(username='emine')
                    elif line_count <600:
                        owner = User.objects.get(username='zeynep')
                    elif line_count <800:
                        owner = User.objects.get(username='cagri')
                    elif line_count <1000:
                        owner = User.objects.get(username='simge')
                    else:
                        owner = User.objects.get(username='eylul')

                    stars = 5
                    if len(row[14]) == 1:
                        stars = row[14]


                    new_hotel = Hotel.objects.create(
                        name=row[1],
                        location=row[7] + ', ' + row[8],
                        location_url='https://www.google.com/maps/search/?api=1&query={}+Hotel+{}+Street+{}+{}+{}+{}+{}+{}+{}'.format(
                                                row[1].strip(), row[2].strip(), row[4], row[3], row[5], row[6], row[7], row[8], row[9]).replace(" ", ""),
                        number_of_rooms=10,
                        description="Hotel in" + row[7] + "," + row[8],
                        owner=owner,
                        type=row[0],
                        telephone=row[10],
                        email=row[11],
                        hotel_website=row[12],
                        number_of_stars=stars,
                        geo_latitude=row[15],
                        geo_longitude=row[16],
                    )

                    new_hotel.save()

                    for i in range(10):
                        if new_hotel.number_of_stars == 5:
                            price = 2000
                        elif new_hotel.number_of_stars == 5:
                            price = 1500
                        elif new_hotel.number_of_stars == 5:
                            price = 1250
                        elif new_hotel.number_of_stars == 5:
                            price = 1000
                        elif new_hotel.number_of_stars == 5:
                            price = 750
                        else:
                            price = 1000

                        new_room = Room(
                            name='room' + str(i),
                            price=price,
                            number_of_people=4,
                            assoc_hotel=new_hotel,
                        )
                        new_room.save()

                    line_count += 1
            print(f'Processed {line_count} lines.')

