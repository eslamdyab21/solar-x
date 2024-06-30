from quixstreams import Application, State
import datetime


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