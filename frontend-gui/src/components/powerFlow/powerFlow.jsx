import LinearIndeterminate from '../linearProgress/linearProgress';
import SolarPowerOutlinedIcon from '@mui/icons-material/SolarPowerOutlined';
import BroadcastOnHomeOutlinedIcon from '@mui/icons-material/BroadcastOnHomeOutlined';
import { useState } from 'react'
import './powerFlow.css'

const PowerFlow = (props) => {
    const [currentConsumptionZeroFlag, setCurrentConsumptionZeroFlag] = useState(false)
    let pass = 0

    if (props.solarEnergyData){
        if (props.solarEnergyData.current_consumption_w == 0){
            !currentConsumptionZeroFlag? setCurrentConsumptionZeroFlag(true) : pass = null
        }
        else{
            currentConsumptionZeroFlag? setCurrentConsumptionZeroFlag(false) : pass = null
        }
    }
    
    return(
        <div className="powerFlow">
            {!currentConsumptionZeroFlag? 
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
                <LinearIndeterminate animate={props.solarEnergyData.current_consumption_w != 0? false : true}/>
                : 
                <LinearIndeterminate animate={false}/>} 
            </div>



            {!currentConsumptionZeroFlag? 
            <div className='box_flow box_1row_1col_flow'> 
                <div className='grid_power_icon_white'>
                    <SolarPowerOutlinedIcon fontSize='large' sx={{ fontSize: 50 }} />
                </div>
            </div> :
            <div className='box_flow box_1row_1col_flow_grid_power_icon'> 
                <div className='grid_power_icon_black'>
                    <SolarPowerOutlinedIcon fontSize='large' sx={{ fontSize: 50 }} />
                </div>
            </div>
            }



            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
        </div>
    )
}


export default PowerFlow;