import { useEffect, useState } from 'react'
import TotalEnergyX from '../components/totalEergyX/totalEergyX';
import PowerFlow from '../components/powerFlow/powerFlow';
import AreaLineChart from '../components/areaLineChart/areaLineChart';
import TopGenerationDays from '../components/topGenerationDays/topGenerationDays';
import './home.css'

const WS1_URL = process.env.REACT_APP_WS1_URL
const WS2_URL = process.env.REACT_APP_WS2_URL
const WS3_URL = process.env.REACT_APP_WS3_URL

console.log('WS1_URL: ', WS1_URL)
console.log('WS2_URL: ', WS2_URL)
console.log('WS3_URL: ', WS3_URL)

const webSocket1 =  new WebSocket(WS1_URL)
const webSocket2 =  new WebSocket(WS2_URL)
const webSocket3 =  new WebSocket(WS3_URL)


const Home = () => {
    const [solarEnergy, setSolarEnergy] = useState(null)
    const [homeEnergy, setHomeEnergy] = useState(null)
    const [batteryEnergy, setBatteryEnergy] = useState(null)

    useEffect( () => {

        webSocket1.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setSolarEnergy(value)
            console.log('webSocket1', value)
        }

        webSocket2.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setHomeEnergy(value)
            console.log('webSocket2', value)
        }

        webSocket3.onmessage = (msg) => {
            const value = JSON.parse(msg.data)
            setBatteryEnergy(value)
            console.log('webSocket3', value)
        }
    })


    return (
        <div className="home">
            <div className="box box_3row_1col">
                <TopGenerationDays />
            </div>
            
            <div className="box box_1row_2col">
                <PowerFlow solarEnergyData={solarEnergy} batteryEnergyData={batteryEnergy} homeEnergyData={homeEnergy} icon={'/batteryIcon.svg'}/>
            </div>

            <div className="box box_3row_1col">
                Solar Energy Flow
            </div>

            <div className="box box_1row_1col">
                <TotalEnergyX EnergyData={solarEnergy} title={'Solar Energy Production'} dataKey={"Wh"} color={"gold"} icon={'/conversionIcon.svg'}/>
            </div>

            <div className="box box_1row_1col">
                <TotalEnergyX EnergyData={homeEnergy} title={'Home Energy Consumption'} dataKey={"Wh"} color={"#82ca9d"} icon={'/revenueIcon.svg'} />
            </div>

            <div className="box box_2row_2col">
                <AreaLineChart solarEnergyData={solarEnergy} homeEnergyData={homeEnergy} batteryEnergyData={batteryEnergy}/>
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