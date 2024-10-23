import './App.css';
import Home from './pages/home';
import background from './img/background.png'

function App() {
  return (
    <div className="main" style={{ backgroundImage: `url(${background})`, opacity: 0.85 }}>
      
      <div className="container" style={{opacity: 0.9, 'backgroundColor': '#2a3447' }}>
          <div className="menuContainer">
            menu
          </div>
          <div className="contentContainer">
            <Home />
          </div>
      </div>
      
    </div>
  );
}

export default App;
