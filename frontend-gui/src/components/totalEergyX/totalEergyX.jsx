import ChartLine from '../chartLine/chatrLine';
import './totalEergyX.css'


const TotalEnergyX = (props) => {

    const Energy = props.EnergyData
    
    return(
        <div className="LineBox">
            <div className="boxInfo">
                <div className="title">
                    <img src={props.icon} alt="" />
                    <span>{props.title}</span>
                </div>

                <div className="title-info">
                    {
                        Energy ? <h1>{Energy["consumption_accumulated_w"].toLocaleString('en')}</h1> :
                        <h1>Waiting....</h1>
                    }
                    {
                        props.color === "gold" ? <p  style={{ color: "gold" }}>Wh</p> : <p  style={{ color: "#82ca9d" }}>Wh</p>
                    }
                    
                </div>
            </div>

            {Energy ? <ChartLine current_consumption_w = {Energy["current_consumption_w"]} current_consumption_w_accumulated_hourly = {Energy["current_consumption_w_accumulated_hourly"]} dataKey={props.dataKey} color={props.color} /> :
             <h1>Waiting....</h1>}

        </div>
    )
}


export default TotalEnergyX;