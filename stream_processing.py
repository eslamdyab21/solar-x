from quixstreams import Application, State
import datetime

solar_power_w_accumulated = 0
def process_weather(msg):
    global solar_power_w_accumulated
    # time_stamp = msg["current"]["time"]
    time_stamp = str(datetime.datetime.now().replace(microsecond=0))
    is_day = msg["current"]["is_day"]
    wind_speed = msg["current"]["wind_speed_10m"]
    cloud_cover_percentage = msg["current"]["cloud_cover"]
    celcius = msg["current"]["temperature_2m"]
    solar_panel_size = 100
    solar_power_w = solar_panel_size * is_day * (wind_speed / (celcius * (1 - cloud_cover_percentage/100)))
    
    
    if solar_power_w_accumulated is None:
        solar_power_w_accumulated = solar_power_w
    else:
        solar_power_w_accumulated  += solar_power_w

    new_msg = {
        "time_stamp" : time_stamp,
        "celcius" : celcius,
        "wind_speed" : wind_speed,
        "cloud_cover_percentage" : cloud_cover_percentage,
        "is_day" : is_day,
        "solar_power_w" : round(solar_power_w, 2),
        "solar_power_w_accum" : round(solar_power_w_accumulated, 2)
    }

    return new_msg


def main():
    app = Application(
        broker_address = "localhost:9092",
        loglevel = "DEBUG",
        auto_offset_reset = "earliest",
        consumer_group = "weather_processor",
    )
    
    
    input_topic = app.topic("weather_data")
    output_topic = app.topic("weather_processed")


    sdf = app.dataframe(input_topic)
    sdf = sdf.apply(process_weather)
    sdf = sdf.to_topic(output_topic)


    app.run(sdf)

if __name__ == "__main__":
    main()