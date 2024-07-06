import LinearIndeterminate from '../linearProgress/linearProgress';
import SolarPowerOutlinedIcon from '@mui/icons-material/SolarPowerOutlined';
import BroadcastOnHomeOutlinedIcon from '@mui/icons-material/BroadcastOnHomeOutlined';
import './powerFlow.css'

const PowerFlow = (props) => {
    
    return(
        <div className="powerFlow">
            <div className='box_flow box_1row_1col_flow'> 
                <div className='solar_icon'>
                    <SolarPowerOutlinedIcon fontSize='large' sx={{ fontSize: 50 }}/>
                </div>
            </div>

            <div className='box_1row_2col_flow'>
                {props.solarEnergyData ? <LinearIndeterminate animate={props.solarEnergyData.solar_power_w === 0? false : true}/>
                : <LinearIndeterminate animate={false}/>}
                
            </div>

            <div className='box_flow box_1row_1col_flow'>
                <div className='solar_icon'>
                    <BroadcastOnHomeOutlinedIcon fontSize='large' sx={{ fontSize: 50 }}/>
                </div>
            </div>

            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
            <div className='box_flow box_1row_1col_flow'></div>
        </div>
    )
}


export default PowerFlow;