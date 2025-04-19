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
    // fetch samples of each word from the API
    const words = newpoem.split(" ");
    const sample_urls = [];
    for (let i = 0; i < words.length; i++) {
      sample_urls.push(`${API}/known/${words[i]}`);
    }
    const sample_responses = await Promise.all(
      sample_urls.map((url) => fetch(url))
    );
    const samples = [];
    for (let i = 0; i < sample_responses.length; i++) {
      const data = await sample_responses[i].json();
      if (data.data.length === 0) {
        console.log(`Word "${words[i]}" not found in database`);
        // search call to API
        fetch(`${API}/search/`, {
          method: "POST",
          body: JSON.stringify({ word: words[i].toLowerCase() }),
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            if (data.status === "success") {
              samples[i] = data.data;
            } else {
              console.log("Error: search failed");
            }
          })
          .catch((error) => {
            console.log("Error:", error);
          });
      }
      samples.push(data.data);
    }
    console.log(samples);

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
        className="poem-input"
        type="text"
        lang="en"
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
        Enter a poem and click "Submit" and see it reflected in the soundscape.
      </p>
    </>
  );
}

export default App;
