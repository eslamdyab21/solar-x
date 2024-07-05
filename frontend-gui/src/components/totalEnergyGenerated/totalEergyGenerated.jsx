import { useEffect, useState } from 'react'
import './totalEergyGenerated.css'


const WS_URL = "ws://localhost:8080"



const webSocket =  new WebSocket(WS_URL)
const TotalEnergyGenerated = () => {
    const [totalEnergy, setTotalEnergy] = useState("Waiting......")
    
    useEffect( () => {

        webSocket.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setTotalEnergy(value["solar_power_w_accum"].toLocaleString('en'))
            console.log(value["solar_power_w_accum"].toLocaleString('en'))
        }

        // return () => {
        //     webSocket.close();
        // };
    })

    
    return(
        <div className="topBox">
            <div className="boxInfo">
                <div className="title">
                    <img src={'/conversionIcon.svg'} alt="" />
                    <span>{'Total Energy Generated'}</span>
                </div>

                <div className="title-info">
                    <h1>{totalEnergy} Wh</h1>
                </div>
            </div>
        </div>
    )
}


export default TotalEnergyGenerated;