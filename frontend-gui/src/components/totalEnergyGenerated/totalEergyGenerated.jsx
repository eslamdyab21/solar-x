import ChartLine from '../chartLine/chatrLine';
import './totalEergyGenerated.css'


const TotalEnergyGenerated = (props) => {

    const solarEnergy = props.solarEnergyData
    
    return(
        <div className="topBox">
            <div className="boxInfo">
                <div className="title">
                    <img src={'/conversionIcon.svg'} alt="" />
                    <span>{'Total Energy Generated'}</span>
                </div>

                <div className="title-info">
                    {
                        solarEnergy ? <h1>{solarEnergy["solar_power_w_accum"].toLocaleString('en')}</h1> :
                        <h1>Waiting....</h1>
                    }
                    <p  style={{ color: "gold" }}>
                        Wh
                    </p>
                </div>
            </div>

            {solarEnergy ? <ChartLine solar_power_w = {solarEnergy["solar_power_w"]} solar_power_w_accum_hourly = {solarEnergy["solar_power_w_accum_hourly"]} dataKey="Wh" color="gold" /> :
             <h1>Waiting....</h1>}

        </div>
    )
}


export default TotalEnergyGenerated;