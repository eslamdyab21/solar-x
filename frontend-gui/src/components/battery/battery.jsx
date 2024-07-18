import './battery.css'


const Battery = (props) => {
	let battery_precentage = 100 * props.batteryEnergyData.current_energy_wh	/ (props.batteryEnergyData.capacity_kwh*1000)

	return(
	    <div className="boxInfo">
	        <div className='title'> 
	            <img className='icon' src={props.icon} alt="" />
	            <span>{props.batteryName}</span>
	        </div>

	        <div>
		        <div className='title-info'>
		            {props.batteryEnergyData? 
		                <h4> {props.batteryEnergyData.current_energy_wh.toLocaleString('en')} </h4>
		                :
		                <h5> Wating... </h5>
		            }
		             <h6  style={{ color: "gold" }}>Wh</h6>
		        </div>

		        <div className="battery_precentage" style={{ color: "limegreen" }}>
	                <h4> {battery_precentage.toFixed(1)} % </h4>
	            </div>
            </div>

	    </div>
	)
}


export default Battery;