import os
import shutil
import pytz
from pathlib import Path
from datetime import datetime, timedelta
from suntime import Sun, SunTimeException


# Coordinates for Prague, Czech Republic
latitude = 50.0755
longitude = 14.4378
tz_loc = pytz.timezone('Europe/Prague')

# Sun object for calculating sunrise and sunset
sun = Sun(latitude, longitude)


def is_daytime(dt):
    try:
        sunrise = sun.get_local_sunrise_time(dt, tz_loc)
        sunset = sun.get_local_sunset_time(dt + timedelta(days=1), tz_loc)
        print(f'{sunrise} <= {dt} < {sunset}')
        return sunrise <= tz_loc.localize(dt) < sunset
    except SunTimeException as e:
        print(f'Error calculating sunrise/sunset: {e}')
        return False


def main():
    # Define the source folder and target folders
    base_dir = Path(__file__).parent.absolute()
    source_folder = base_dir.joinpath('source')
    day_folder = base_dir.joinpath('day_photos')
    night_folder = base_dir.joinpath('night_photos')

    # Create target folders if they don't exist
    os.makedirs(day_folder, exist_ok=True)
    os.makedirs(night_folder, exist_ok=True)

    # Iterate over all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.jpg'):
            # Extract the datetime from the filename
            fn_split = filename[:-4].split('_')
            datetime_str = f'{fn_split[1]}_{fn_split[2]}'
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d_%H-%M-%S')
            
            # Determine if the photo is taken during the day or night
            if is_daytime(datetime_obj):
                target_folder = day_folder
            else:
                target_folder = night_folder
            
            # Move the file to the corresponding folder
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            shutil.move(source_path, target_path)
            print(f'{filename} -> {target_folder.name}')

    print('Done')
    return None


if __name__ == '__main__':
    main()
