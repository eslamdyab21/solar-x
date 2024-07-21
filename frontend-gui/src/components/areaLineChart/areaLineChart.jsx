import {Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Legend} from "recharts";
import "./areaLineChart.css";



function reformulate(data) {
    let new_data = []
    let new_key = null
    
    
    let keys = Object.keys(data).sort();

    keys.forEach((key) => {
        if (Number(key) < 12){
            new_key = String(Number(key)) + " AM"
        }
        else {
            new_key = String(Number(key) - 12) + " PM"
        }
        new_data.push({"Time":new_key, "Kwh":(data[key]/1000).toFixed(2)})
    });
    

    return new_data

}


const AreaLineChart = (props) => {
    let current_generation_w_accumulated_hourly_chart = []
    let current_consumption_w_accumulated_hourly_chart = []
    let current_batteries_consumption_w_accumulated_hourly_chart = []
    let Energy_kwh_hourly = []

    if (props.solarEnergyData != null && props.homeEnergyData != null && props.batteryEnergyData != null){
        current_generation_w_accumulated_hourly_chart = reformulate(props.solarEnergyData.current_consumption_w_accumulated_hourly)
        current_consumption_w_accumulated_hourly_chart = reformulate(props.homeEnergyData.current_consumption_w_accumulated_hourly)
        current_batteries_consumption_w_accumulated_hourly_chart = reformulate(props.batteryEnergyData.hourly_discharging)

        for (let i = 1; i < (current_generation_w_accumulated_hourly_chart.length) ; i++) {
            Energy_kwh_hourly.push({'time':current_generation_w_accumulated_hourly_chart[i].Time, 
                                    'solar_generation':current_generation_w_accumulated_hourly_chart[i].Kwh, 
                                    'home_consumption':current_consumption_w_accumulated_hourly_chart[i].Kwh,
                                    'battery_consumption':current_batteries_consumption_w_accumulated_hourly_chart[i].Kwh})
        }
    }

    if (props.homeEnergyData != null && props.batteryEnergyData != null){
        current_consumption_w_accumulated_hourly_chart = reformulate(props.homeEnergyData.current_consumption_w_accumulated_hourly)
        current_batteries_consumption_w_accumulated_hourly_chart = reformulate(props.batteryEnergyData.hourly_discharging)

        for (let i = 1; i < (current_consumption_w_accumulated_hourly_chart.length) ; i++) {
            Energy_kwh_hourly.push({'time':current_consumption_w_accumulated_hourly_chart[i].Time, 
                                    'home_consumption':current_consumption_w_accumulated_hourly_chart[i].Kwh,
                                    'battery_consumption':current_batteries_consumption_w_accumulated_hourly_chart[i].Kwh})
        }
    }
    

    return (
        <div className="bigChartBox">
          <h1 className="h1Center">Energy Flow</h1>
          {/* <h4>solar power consumption</h4> */}
          <div className="areaChart">
            <ResponsiveContainer width="99%" height="100%">
              <AreaChart 
                data={Energy_kwh_hourly}
                margin={{
                  top: 10,
                  right: 30,
                  left: 10,
                  bottom: 0,
                }}
              >
                <XAxis dataKey="time" />
                <YAxis  unit=' Kwh'/> 
                <Tooltip contentStyle={{ background: "#384256d7", border: "none" } } 
                         labelStyle={{ display: "none" }} position={{ y: 0 }}/>
                <Legend />
    
          {/*      <Area
                  type="monotone"
                  dataKey="solar_generation"
                  name="Generated"
                  // stackId="1"
                  stroke="#ffc658"
                  fill="#ffc658"
                  unit=' Kwh'
                />*/}
    
                <Area
                  type="monotone"
                  dataKey="home_consumption"
                  name="Home"
                  // stackId="2"
                  stroke="#82ca9d"
                  fill="#82ca9d"
                  unit=' Kwh'
                />

                 <Area
                  type="monotone"
                  dataKey="battery_consumption"
                  name="Battery"
                  // stackId="3"
                  stroke="#49d8ff"
                  fill="#49d8ff"
                  unit=' Kwh'
                />
    
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
    );
}


export default AreaLineChart;



