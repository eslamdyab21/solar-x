import { Line, LineChart, ResponsiveContainer, Tooltip } from "recharts";
import './chartLine.css'



const ChartLine = (props) => {
    
    let current_consumption_w_accumulated_hourly_chart = []
    let keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    keys.forEach((key) => {
        current_consumption_w_accumulated_hourly_chart.push({"time":key, "Wh":props.current_consumption_w_accumulated_hourly[key]})
    });

    // console.log(current_consumption_w_accumulated_hourly_chart)
    
    return(
        <div className="chartInfo">
            <div className="chart">
                <ResponsiveContainer width="99%" height="100%">
                    <LineChart data={current_consumption_w_accumulated_hourly_chart}>
                    <Tooltip
                        contentStyle={{ background: "transparent", border: "none" }}
                        labelStyle={{color:'gold' }}
                        labelFormatter={(name) => 'Hour: '+ name} 
                        position={{ x: -65, y: 10 }}
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
                    {props.current_consumption_w} w
                </span>
                <span className="duration">Currently</span>
            </div>

        </div>
    )
}


export default ChartLine;