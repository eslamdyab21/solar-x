import LinearIndeterminate from '../linearProgress/linearProgress';
import SolarPowerOutlinedIcon from '@mui/icons-material/SolarPowerOutlined';
import BroadcastOnHomeOutlinedIcon from '@mui/icons-material/BroadcastOnHomeOutlined';
import CellTowerIcon from '@mui/icons-material/CellTower';
import Battery from '../battery/battery'
import { useState , useEffect} from 'react'
import './powerFlow.css'

let is_ideal = true
let status = ''

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

    if (props.batteryEnergyData){
        let keys = Object.keys(props.batteryEnergyData['batteries']);

        for (const key of keys) {
            if (props.batteryEnergyData['batteries'][key]['status'] !== 'ideal') {
                is_ideal = false
                status = props.batteryEnergyData['batteries'][key]['status']
                break
            }
            status = props.batteryEnergyData['batteries'][key]['status']
        }

        batteryStatus !== status ? setBatteryStatus(status) : pass = true
        
    }
    
    

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
                    <LinearIndeterminate animate={currentSolarProductionZeroFlag? true : false}/>
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

            {batteryStatus === 'discharging' ?
            <div className='flex-batteries-container-active'>
                <div className='flex-battery'>
                { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.batteries.battery_1} batteryName={'Battery 1'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>
                <div className='flex-battery'>
                    { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.batteries.battery_2} batteryName={'Battery 2'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>

                <div className='flex-battery'>
                    { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.batteries.battery_3} batteryName={'Battery 3'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>
            </div>
            :
            <div className='flex-batteries-container-ideal'>
                <div className='flex-battery'>
                { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.batteries.battery_1} batteryName={'Battery 1'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>
                <div className='flex-battery'>
                    { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.batteries.battery_2} batteryName={'Battery 2'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>

                <div className='flex-battery'>
                    { props.batteryEnergyData?
                    <Battery batteryEnergyData={props.batteryEnergyData.batteries.battery_3} batteryName={'Battery 3'} icon={props.icon}/>
                    :
                    <h5>Waiting....</h5>
                }
                </div>
            </div>
            }
        </div>
    )
}


export default PowerFlow;