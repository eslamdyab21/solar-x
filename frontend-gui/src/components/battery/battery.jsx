import './battery.css'


const Battery = (props) => {
	return(
		<div className="topBox">
		    <div className="boxInfo">
		        <div className='title'> 
		            <img className='icon' src={props.icon} alt="" />
		            <span>Battery</span>
		        </div>

		        <div className='title-info'>
		            {props.batteryEnergyData? 
		                <h4> {props.batteryEnergyData.current_energy_wh.toLocaleString('en')} </h4>
		                :
		                <h5> Wating... </h5>
		            }
		             <h6  style={{ color: "gold" }}>Wh</h6>
		        </div>
		    </div>
		</div>
	)
}


export default Battery;