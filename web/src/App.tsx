import { useEffect, useState } from "react";
import "./App.css";

const API = import.meta.env.VITE_API_URL;

function App() {
  const [poem, setPoem] = useState("");
  const [location, setLocation] = useState([0, 0]);

  const Navigator = window.navigator;

  useEffect(() => {
    if (Navigator.geolocation) {
      Navigator.geolocation.getCurrentPosition((coords) => {
        setLocation([coords.coords.latitude, coords.coords.longitude]);
      });
    }
  }, [Navigator.geolocation, location]);

  useEffect(() => {
    async function getPoem() {
      const response = await fetch(`${API}/current`);
      const data = await response.json();
      setPoem(data.data.poem);
    }
    getPoem();
  }, []);

  const updatePoem = async (newpoem: string) => {
    const response = await fetch(`${API}/update-poem`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        poem: newpoem,
        latitude: location[0],
        longitude: location[1],
      }),
    });
    console.log(response);
    setPoem(newpoem);
  };

  return (
    <>
      <input
        className='poem-input'
        type="text"
        lang='en'
        multiple
        placeholder="A poem made of words"
        onChange={(e) => setPoem(e.target.value)}
        value={poem}
      />
      <div className="card">
        <button onClick={() => updatePoem(poem)}>Submit</button>
        <p>This poem was made by visitors like you.</p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
