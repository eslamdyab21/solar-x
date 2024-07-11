import { useEffect, useState } from 'react'
import TotalEnergyGenerated from '../components/totalEnergyGenerated/totalEergyX';
import PowerFlow from '../components/powerFlow/powerFlow';
import './home.css'

const WS_URL = "ws://localhost:8080"
const WS2_URL = "ws://localhost:9090"
const webSocket =  new WebSocket(WS_URL)
const webSocket2 =  new WebSocket(WS2_URL)


const Home = () => {
    const [solarEnergy, setSolarEnergy] = useState(null)
    const [homeEnergy, setHomeEnergy] = useState(null)

    useEffect( () => {

        webSocket.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setSolarEnergy(value)
            console.log('webSocket1', value)
        }

        webSocket2.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setHomeEnergy(value)
            console.log('webSocket2', value)
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
                <TotalEnergyGenerated webSocket={webSocket} EnergyData={solarEnergy} title={'Total Energy Generated'} dataKey={"Wh"} color={"gold"} />
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