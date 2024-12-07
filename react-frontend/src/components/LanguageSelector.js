import React from "react";

function LanguageSelector({ setLanguage }) {
  return (
    <div className="language-selector">
      <label htmlFor="language-select">Select Language:</label>
      <select
        id="language-select"
        defaultValue={"auto"}
        onChange={(e) => setLanguage(e.target.value)}
      >
        <option value="auto">Auto</option>
        <option value="en">English</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        <option value="de">German</option>
        <option value="ar">Arabic</option>
        <option value="pt">Portuguese</option>
        <option value="ru">Russian</option>
        <option value="ja">Japanese</option>
        <option value="ko">Korean</option>
        <option value="it">Italian</option>
        <option value="nl">Dutch</option>
        <option value="tr">Turkish</option>
        <option value="sv">Swedish</option>
        <option value="pl">Polish</option>
        <option value="ro">Romanian</option>
        <option value="el">Greek</option>
        <option value="th">Thai</option>
        <option value="vi">Vietnamese</option>
        <option value="ur">Urdu</option>
      </select>
    </div>
  );
}

export default LanguageSelector;
