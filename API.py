from flask import Flask, request, redirect, jsonify, url_for 
import HospitalData as hd
import haversine as hs #used for distance in locations
from haversine import Unit #Converts distnace to other units


app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Please enter the correct API route!</h1>"

#Temperature
@app.route('/api/v1/patientData/PatientTemperature')
def sendTemperature():
    TemperatureJSON = jsonify(
            {
                "Temperature" : hd.get_temperature()
            }
        )
    
    TemperatureJSON.headers.add('Access-Control-Allow-Origin', '*')

    return TemperatureJSON

#Pressure
@app.route('/api/v1/patientData/PatientPressure')
def sendPressure():
    PressureJSON = jsonify(
            {
                "Pressure" : hd.get_pressure()
            }
        )
    
    PressureJSON.headers.add('Access-Control-Allow-Origin', '*')

    return PressureJSON

#Humidity
@app.route('/api/v1/patientData/PatientHumidity')
def sendHumidity():
    HumidityJSON = jsonify(
            {
                "Humidity" : hd.get_humidity()
            }
        )
    
    HumidityJSON.headers.add('Access-Control-Allow-Origin', '*')

    return HumidityJSON

#Temperature, Pressure and Humidity together
@app.route('/api/v1/patientData/PatientStats')
def sendStats():
    StatsJSON = jsonify(
            {
                "Temperature" : hd.get_temperature(),
                "Pressure" : hd.get_pressure(),
                "Humidity" : hd.get_humidity()
            }
        )
    
    StatsJSON.headers.add('Access-Control-Allow-Origin', '*')

    return StatsJSON

#Acceleration
@app.route('/api/v1/patientData/PatientAcceleration')
def sendAcceleration():
    AccelerationJSON = jsonify(
        {
            "Acceleration" : hd.get_acceleration()
        }
    )

    AccelerationJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return AccelerationJSON

#Fall detection
@app.route('/api/v1/patientData/PatientFall')
def sendFallAndAcceleration():
    fall = False
    acceleration = hd.get_acceleration()

    if ((acceleration[0] < -5 or acceleration[0] > 5) or (acceleration[1] < -5 or acceleration[1] > 5) or (acceleration[2] < -5 or acceleration[2] > 5)): 
        fall = True

    AccelerationJSON = jsonify(
        {
            "HasFallen" : fall,
            "RawAcceleration" : acceleration
        }
    )

    AccelerationJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return AccelerationJSON

#Current Location
@app.route('/api/v1/patientData/PatientLocation')
def sendLocation():
    LocationJSON = jsonify(
        {
            "Patient Location" : hd.get_current_location()
        }
    )

    LocationJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return LocationJSON

#Distance from hospital bed
@app.route('/api/v1/patientData/PatientHospitalDistance')
def sendHospitalDistance():
    patient = hd.get_current_location()
    HospitalBed = hd.get_hospital_bed_location()
    Distance = hs.haversine(HospitalBed,patient,unit=Unit.METERS) #Calculates distance between locations
    HospitalDistanceJSON = jsonify(
        {
            "Patient Location" : patient,
            "Hospital Bed" : HospitalBed,
            "Distance in meteres" : Distance 
        }
    )

    HospitalDistanceJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return HospitalDistanceJSON

#Distance from area limit
@app.route('/api/v1/patientData/PatientArea')
def sendArea():
    area = hd.get_geofence_area() #(min,max)
    patientLocation = hd.get_current_location()
    Distance1 = hs.haversine(area[0],patientLocation,unit=Unit.METERS) #Using min longitude and latitude
    Distance2 = hs.haversine(area[1],patientLocation,unit=Unit.METERS) #Using max longitude and latitude
    MedianDistance = (((Distance1 + Distance2)/2)-500) 
    within = hd.is_location_within_geofence(patientLocation)
    if (within == False):
        MedianDistance = -abs(MedianDistance)
   
    AreaJSON = jsonify(
        {
            "Patient Location" : patientLocation,
            "Distance from area in meteres" :MedianDistance
        }
    )

    AreaJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return AreaJSON

#Is patient within area limit
@app.route('/api/v1/patientData/PatientWithinArea')
def sendWithinArea():
    area = hd.get_geofence_area() #(min,max)
    patientLocation = hd.get_current_location()
    Distance1 = hs.haversine(area[0],patientLocation,unit=Unit.METERS) #Using minimum longitude and latitude
    Distance2 = hs.haversine(area[1],patientLocation,unit=Unit.METERS) #Using maximum longitude and latitude
    MedianDistance = (((Distance1 + Distance2)/2)-500) 
    within = hd.is_location_within_geofence(patientLocation)
    if (within == False):
        MedianDistance = -abs(MedianDistance)
   
    WithinAreaJSON = jsonify(
        {
            "Patient Location" : patientLocation,
            "Distance from area in meteres" :MedianDistance,
            "Is patient in agreed area" : within
        }
    )

    WithinAreaJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return WithinAreaJSON

#Sounding alarm
@app.route('/api/v1/SoundingAlarm')
def sendAlarm():
    alarm = hd.play_sound_speakers(10)

    AlarmJSON = jsonify(
        {
            "Alarm" : alarm
        }
    )

    AlarmJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return AlarmJSON

#Display LED and message
@app.route('/api/v1/DisplayLEDMessage')
def sendLedMessage():
    message = "Patient has fallen!!"
    Display = hd.send_message(message)
    Colour = 255, 0, 0
    Led = hd.display_led_alert(Colour)

    LedMessageJSON = jsonify(
        {
            "Message" : Display,
            "LED" : Led
        }
    )

    LedMessageJSON.headers.add('Access-Control-Allow-Origin', '*')
    
    return LedMessageJSON

if __name__ == '__main__':
    app.run(debug=True)