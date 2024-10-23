import './topGenerationDays.css'

export const topEnergyDays = [
    {
      id: 1,
      name: "SAT",
      date: "2022/05/4",
      amount: "300.668",
    },
    {
      id: 2,
      name: "SUN",
      date: "2022/05/7",
      amount: "250.8",
    },
    {
      id: 3,
      name: "THU",
      date: "2022/02/4",
      amount: "240.3",
    },
    {
      id: 4,
      name: "SAT",
      date: "2022/03/10",
      amount: "230.1",
    },
    {
      id: 5,
      name: "WED",
      date: "2022/02/4",
      amount: "220.45",
    }
  ];
  
const TopGenerationDays = (props) => {

    return(
        <div className="topBox">
            <h1 className='h1TitleCenter' >Top Days</h1>

            {topEnergyDays.map(day=>(
                <div className="listItem" key={day.id}>    
                    <div className="dayTexts">
                        <span className="name">{day.name}</span>
                        <span className="date">{day.date}</span>
                    </div>
                
                    <span className="amount">{day.amount} KWh</span>

                </div>
            ))}
        </div>
    )


}



export default TopGenerationDays;