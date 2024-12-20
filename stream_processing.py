from quixstreams import Application, State
import datetime



def process_weather(msg,  state: State):
    # time_stamp = msg["current"]["time"]
    time_stamp = str(datetime.datetime.now().replace(microsecond=0))
    is_day = msg["current"]["is_day"]
    wind_speed = msg["current"]["wind_speed_10m"]
    cloud_cover_percentage = msg["current"]["cloud_cover"]
    celcius = msg["current"]["temperature_2m"]

    # if time_stamp.split()[1].split(':')[0] == "24":
    #     solar_power_w_accumulated = 0
    
    new_msg = {
        "time_stamp" : time_stamp,
        "celcius" : celcius,
        "wind_speed" : wind_speed,
        "cloud_cover_percentage" : cloud_cover_percentage,
        "is_day" : is_day
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
    sdf = sdf.apply(process_weather, stateful=True)
    sdf = sdf.to_topic(output_topic)


    app.run(sdf)

if __name__ == "__main__":
    main()