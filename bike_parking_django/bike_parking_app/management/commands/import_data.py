import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from bike_parking_app.models import BikeRackData

class Command(BaseCommand):
    help = 'Import data from CSV file into SQLite database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert the datetime string to a datetime object
                datetime_string = row['Date_Inst']
                if datetime_string:
                    date_inst = datetime.strptime(datetime_string, "%m/%d/%Y %I:%M:%S %p")
                else:
                    date_inst = None  # or any default value you prefer


                # Create a new instance of MyModel and save it to the database
                my_model_instance = BikeRackData.objects.create(
                        the_geom=row['the_geom'],
                        BoroCode=int(row['BoroCode']),
                        BoroName=row['BoroName'],
                        BoroCD=int(row['BoroCD']),
                        CounDist=int(row['CounDist']),
                        AssemDist=int(row['AssemDist']),
                        StSenDist=int(row['StSenDist']),
                        CongDist=int(row['CongDist']),
                        Program=row['Program'],
                        Site_ID=row['Site_ID'],
                        Group_ID=row['Group_ID'],
                        Borough=row['Borough'],
                        IFOAddress=row['IFOAddress'],
                        OnStreet=row['OnStreet'],
                        FromStreet=row['FromStreet'],
                        ToStreet=row['ToStreet'],
                        Side_of_St=row['Side_of_St'],
                        RackType=row['RackType'],
                        Date_Inst=date_inst,  # Assuming you've already parsed it as a datetime object
                        X=float(row['X']),
                        Y=float(row['Y']),
                        NTAName=row['NTAName'],
                        FEMAFldz=row['FEMAFldz'],
                        FEMAFldT=row['FEMAFldT'],
                        HrcEvac=int(row['HrcEvac']) if row['HrcEvac'] else None,  # Handle null values
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))