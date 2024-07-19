import LinearIndeterminate from '../linearProgress/linearProgress';
import SolarPowerOutlinedIcon from '@mui/icons-material/SolarPowerOutlined';
import BroadcastOnHomeOutlinedIcon from '@mui/icons-material/BroadcastOnHomeOutlined';
import CellTowerIcon from '@mui/icons-material/CellTower';
import Battery from '../battery/battery'
import { useState , useEffect} from 'react'
import './powerFlow.css'

let initial = true
let prev_w, current_w = 0


function battery_charge_x_consume (batteryEnergyData) {
    let keys = Object.keys(batteryEnergyData);
    let status
    

    keys.forEach((key) => {
        if (key !== 'time_stamp' && initial){
            prev_w = prev_w + batteryEnergyData[key]['current_energy_wh']
            initial = false 
        }
        else if(key !== 'time_stamp'){
            current_w = current_w +  batteryEnergyData[key]['current_energy_wh']
        }
    });

    current_w - prev_w > 0 ? status = 'charging' 
    : current_w - prev_w < 0 ? status = 'draining' : status = 'ideal' 

    prev_w = current_w

    return status
}


let status, prev_status = null

const PowerFlow = (props) => {
    const [currentSolarProductionZeroFlag, setCurrentSolarProductionZeroFlagZeroFlag] = useState(false)
    const [batteryStatus, setBatteryStatus] = useState('')
    let pass = false


    if (props.solarEnergyData){
        if (props.solarEnergyData.current_consumption_w === 0){
            !currentSolarProductionZeroFlag? setCurrentSolarProductionZeroFlagZeroFlag(true) : pass = true
        }
        else{
            currentSolarProductionZeroFlag? setCurrentSolarProductionZeroFlagZeroFlag(false) : pass = true
        }
    }
    
    

    useEffect( () => {
        setInterval(() => {
            if(props.batteryEnergyData){
                status = battery_charge_x_consume(props.batteryEnergyData)
                console.log('batteryStatus: ', status)
                status !== prev_status ? setBatteryStatus(status) : pass = true
                prev_status = status
            }
        }, 5 *1000)
    }, [])

    return(
        <div>
            <div className="powerFlow">
                {!currentSolarProductionZeroFlag? 
                <div className='box_flow box_1row_1col_flow_solar_icon'> 
                    <div className='solar_icon'>
                        <SolarPowerOutlinedIcon fontSize='large' sx={{ fontSize: 50 }} />
                    </div>
                </div> :
                <div className='box_flow box_1row_1col_flow'> 
                    <div className='solar_icon'>
                        <SolarPowerOutlinedIcon fontSize='large' sx={{ fontSize: 50 }} />
                    </div>
                </div>
                }


                <div className='box_1row_1col_flow_pad'>
                    {props.solarEnergyData ? 
                    <LinearIndeterminate animate={props.solarEnergyData.current_consumption_w === 0? false : true}/>
                    : 
                    <LinearIndeterminate animate={false}/>} 
                </div>



                <div className='box_flow box_1row_1col_flow'>
                    <div className='home_icon'>
                        <BroadcastOnHomeOutlinedIcon fontSize='large' sx={{ fontSize: 50 }}/>
                    </div>
                </div>




                <div className='box_1row_1col_flow_pad'>
                    {props.solarEnergyData ? 
                    <LinearIndeterminate animate={currentSolarProductionZeroFlag && batteryStatus === 'ideal'? true : false}/>
                    : 
                    <LinearIndeterminate animate={false}/>} 
                </div>



                {currentSolarProductionZeroFlag && batteryStatus === 'ideal'? 
                <div className='box_flow box_1row_1col_flow_grid_power_icon'> 
                    <div className='grid_power_icon_black'>
                        <CellTowerIcon fontSize='large' sx={{ fontSize: 50 }} />
                    </div>
                </div> :
                
                <div className='box_flow box_1row_1col_flow'> 
                    <div className='grid_power_icon_white'>
                        <CellTowerIcon fontSize='large' sx={{ fontSize: 50 }} />
                    </div>
                </div>
                }
            </div>

            <div className='flex-batteries-container-active' sx={{ fontSize: 5000 }}>
                <div className='flex-battery'>
                { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.battery_1} batteryName={'Battery 1'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>
                <div className='flex-battery'>
                    { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.battery_2} batteryName={'Battery 2'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>

                <div className='flex-battery'>
                    { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.battery_3} batteryName={'Battery 3'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>

            </div>
        </div>
        
    )
}


export default PowerFlow;