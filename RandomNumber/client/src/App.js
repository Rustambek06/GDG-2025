import {useState} from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [randomNumber, setRandomNumber] = useState(null);

  const apiCall = () => {
    axios.get('http://localhost:8080').then((data) => {
      setRandomNumber(data.data);
    })
    .catch((error) => {
      console.error('Random number response Error', error);
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>Get your random number</div>
        <button onClick={apiCall}>Random number</button>
        <div>
          { randomNumber !== null ? <p>{randomNumber}</p> : <p>Number have not loaded</p>}
        </div>
      </header>
    </div>
  );
}

export default App;