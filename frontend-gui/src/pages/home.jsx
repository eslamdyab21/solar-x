import './home.css'

const Home = () => {
    return (
        <div className="home">
            <div className="box box_3row_1col">
                Top Days
            </div>
            
            <div className="box box_1row_2col">
                Flow
            </div>

            <div className="box box_3row_1col">
                Solar Energy Flow
            </div>

            <div className="box box_1row_1col">
                total energy generated
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