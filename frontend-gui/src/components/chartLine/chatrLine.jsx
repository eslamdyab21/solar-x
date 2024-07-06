import { Line, LineChart, ResponsiveContainer, Tooltip } from "recharts";
import './chartLine.css'



const ChartLine = (props) => {
    
    let solar_power_w_accum_hourly_chart = []
    let keys = Object.keys(props.solar_power_w_accum_hourly).sort();
    keys.forEach((key) => {
        solar_power_w_accum_hourly_chart.push({"time":key, "Wh":props.solar_power_w_accum_hourly[key]})
    });

    // console.log(solar_power_w_accum_hourly_chart)
    
    return(
        <div className="chartInfo">
            <div className="chart">
                <ResponsiveContainer width="99%" height="100%">
                    <LineChart data={solar_power_w_accum_hourly_chart}>
                    <Tooltip
                        contentStyle={{ background: "transparent", border: "none" }}
                        labelStyle={{ display: "none" }}
                        position={{ x: -60, y: 10 }}
                    />
                    <Line
                        type="monotone"
                        dataKey={props.dataKey}
                        stroke={props.color}
                        strokeWidth={2}
                        dot={false}
                    />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            
            <div className="texts">
                <span className="percentage" style={{ color: "limegreen" }}>
                    {props.solar_power_w} w
                </span>
                <span className="duration">generated now</span>
            </div>

        </div>
    )
}


export default ChartLine;