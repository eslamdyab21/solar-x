import LinearIndeterminate from '../linearProgress/linearProgress';
import SolarPowerOutlinedIcon from '@mui/icons-material/SolarPowerOutlined';
import BroadcastOnHomeOutlinedIcon from '@mui/icons-material/BroadcastOnHomeOutlined';
import CellTowerIcon from '@mui/icons-material/CellTower';
import Battery from '../battery/battery'
import { useState } from 'react'
import './powerFlow.css'


const PowerFlow = (props) => {
    const [currentSolarProductionZeroFlag, setCurrentSolarProductionZeroFlagZeroFlag] = useState(false)
    let pass = false


    if (props.solarEnergyData){
        if (props.solarEnergyData.current_consumption_w === 0){
            !currentSolarProductionZeroFlag? setCurrentSolarProductionZeroFlagZeroFlag(true) : pass = true
        }
        else{
            currentSolarProductionZeroFlag? setCurrentSolarProductionZeroFlagZeroFlag(false) : pass = true
        }
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



                {currentSolarProductionZeroFlag? 
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

            <div className='flex-batteries-container-active'>
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