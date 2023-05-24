import random, math

def get_temperature():
    # Generate a random temperature in the range 18-25 degrees Celsius
    return random.uniform(18, 25)

def get_pressure():
    # Generate a random pressure in the range 1010-1020 hPa
    return random.uniform(1010, 1020)

def get_humidity():
    # Generate a random humidity in the range 50-80%
    return random.uniform(50, 80)

def get_heading():
    # Generate a random heading in the range 0-360 degrees, where 0 is North, 90 is East, 180 is South, and 270 is West
    return random.uniform(0, 360)

def get_acceleration():
    # Generate a random acceleration in the range -10 to 10
    return [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]

def get_current_location():
    # Load a dataset of locations within Taunton, Somerset, UK
    locations = [
        (51.0336, -3.1294), # Taunton Deane Borough Council
        (51.011496, -3.120189), # Musgrove Park Hospital
        (51.0131, -3.1064), # Taunton train station
        (51.0355, -3.0946), # Taunton Castle
        (51.0455, -3.0931), # Vivary Park
        (51.0276, -3.0747), # Taunton School
        (51.0569, -3.1051), # Bishops Hull
        (51.0659, -3.0934), # Blackbrook
        (51.0497, -3.1374), # Monkton Heathfield
        (51.0165, -3.0672), # Priorswood
    ]
    
    # Return a random location from the dataset
    return random.choice(locations)

def get_hospital_bed_location():
    # Musgrove Park Hospital location: -3.0792, 51.0068
    return [51.011496, -3.120189]

def get_geofence_area():
    # Musgrove Park Hospital location: -3.0792, 51.0068
    hospital_latitude = 51.0068
    hospital_longitude = -3.0792
    
    # Geofence radius of 500 meters
    geofence_radius = 500
    
    # Calculate the minimum and maximum latitude and longitude values for the geofence area
    min_latitude = hospital_latitude - (geofence_radius / 111111)
    max_latitude = hospital_latitude + (geofence_radius / 111111)
    min_longitude = hospital_longitude - (geofence_radius / (111111 * math.cos(math.radians(hospital_latitude))))
    max_longitude = hospital_longitude + (geofence_radius / (111111 * math.cos(math.radians(hospital_latitude))))
    
    # Return the geofence area as a rectangle with minimum and maximum latitude and longitude values
    return [(min_latitude, min_longitude), (max_latitude, max_longitude)]

def is_location_within_geofence(location):
    # Get the geofence area
    geofence_area = get_geofence_area()
    
    # Unpack the location coordinates
    latitude, longitude = location
    
    # Check if the location is within the geofence area
    return (latitude >= geofence_area[0][0] and latitude <= geofence_area[1][0] and
            longitude >= geofence_area[0][1] and longitude <= geofence_area[1][1])

def play_sound_speakers(duration):
    # Play a sound through the computer's speakers for the given duration.
    return "Played sound for " + str(duration) + " seconds."

def send_message(message):
    # Display a given message on the screen.
    return "Displayed " + message + "."

def display_led_alert(colour):
    # Display a given RGB colour using the computer's LEDs.
    try:
        usedColour = []
        for value in colour:
            usedColour.append(int(value))
        return "Displayed RGB colour " + str(colour[0]) + "," + str(colour[1]) + "," + str(colour[2]) + "."
    except:
        # Handle cases where the given colour is not in the expected format.
        return "Unexpected colour format - expected int,int,int, recieved " + str(colour) + "."