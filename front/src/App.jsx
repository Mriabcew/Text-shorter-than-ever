import React, { useState } from 'react';
import './App.css';
import TopBarComponent from './components/TopBarComponent';

function App() {
  const [summaryText, setSummaryText] = useState('');
  const [inputText, setInputText] = useState('');
  const [tableData, setTableData] = useState({
    summarize: 'summarized',
    words: 0,
    sentences: 0,
    readingTime: 0,
  });
  const [shorteningPercentage, setShorteningPercentage] = useState(5);

  
  const handleSliderChange = (event) => {
      const value = event.target.value;
      setShorteningPercentage(value);
    };

  const handleSummarize = async () => {
    console.log({ text: inputText });
    try {
      // Tutaj możesz wywołać funkcję, która wykonuje zapytanie do API
      // Przyjmuję, że otrzymasz odpowiedź w formie obiektu response
      const response = await fetch('http://127.0.0.1:5000/text-to-summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error('Nie udało się uzyskać odpowiedzi od serwera.');
      }

      const data = await response.json();

      setTableData({
        words: data.words,
        sentences: data.sentences,
        readingTime: data.readingTime,
      });

      setSummaryText(data.summarize);
    } catch (error) {
      console.error('Błąd podczas przetwarzania danych:', error.message);
    }
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleClean = () => {
    console.log("Before Clean:", inputText, summaryText, tableData);
    setInputText('');
    setSummaryText('');
    setTableData({
      words: 0,
      sentences: 0,
      readingTime: 0,
    });
    console.log("After Clean:", inputText, summaryText, tableData);
  };
  

  return (
    <div>
      <TopBarComponent />
      <div className='Main-Container'>
        <div className="inputContainer">
            <textarea
              type="text"
              id="textInput"
              className="textInput"
              placeholder='Wpisz tutaj swój tekst'
              onChange={handleInputChange}
              value={inputText}
            />
        </div>
        <div className='TableAndButton'>
          <div>
            <table className="blueTable">
              <tbody>
                <tr>
                  <td>Words</td>
                  <td>{tableData.words}</td>
                </tr>
                <tr>
                  <td>Sentences</td>
                  <td>{tableData.sentences}</td>
                </tr>
                <tr>
                  <td>Reading Time in seconds</td>
                  <td>{tableData.readingTime}</td>
                </tr>
              </tbody>
            </table>
            <div style={{ marginTop: '1em' }}>
              <label for="volume">Percentage of shortening</label>
                <input type="range" id="volume" name="volume" min="50" max="100" value={shorteningPercentage} onChange={handleSliderChange} />

                <p>Selected percentage: {shorteningPercentage}%</p>
            </div>
          </div>
          <div>
            <button onClick={handleSummarize} style={{ margin: '1em' }}>Summary</button>
          </div>
          <div>
            <button onClick={handleClean} style={{ margin: '1em' }}>Clean</button>
          </div>
          
        </div>
        <div className="inputContainer">
          <textarea
            type="text"
            id="summaryText"
            className="textInput"
            placeholder='Tutaj otrzymasz podsumowanie'
            style={{ pointerEvents: 'none' }}
            value={summaryText}
            readOnly // Optional: If you want to make it read-only
          />
        </div>
      </div>
    </div>
  );
}

export default App;
