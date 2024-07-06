import { useEffect, useState } from 'react'
import TotalEnergyGenerated from '../components/totalEnergyGenerated/totalEergyGenerated';
import PowerFlow from '../components/powerFlow/powerFlow';
import './home.css'

const WS_URL = "ws://localhost:8080"
const webSocket =  new WebSocket(WS_URL)


const Home = () => {
    const [solarEnergy, setSolarEnergy] = useState(null)

    useEffect( () => {

        webSocket.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setSolarEnergy(value)
            console.log(value["solar_power_w"])
        }
    })


    return (
        <div className="home">
            <div className="box box_3row_1col">
                Top Days
            </div>
            
            <div className="box box_1row_2col">
                <PowerFlow webSocket={webSocket} solarEnergyData={solarEnergy}/>
            </div>

            <div className="box box_3row_1col">
                Solar Energy Flow
            </div>

            <div className="box box_1row_1col">
                <TotalEnergyGenerated webSocket={webSocket} solarEnergyData={solarEnergy}/>
            </div>

            <div className="box box_1row_1col">
                total energy used
            </div>

            <div className="box box_2row_2col">
                Solar Energy Flow
            </div>

            <div className="box box_1row_1col">
                Pervious week energy
            </div>

            <div className="box box_1row_1col">
                Previous week home usage
            </div>
        </div>
    )
}


export default Home;