import React from 'react';
import './NormalButton.css';

function NormalButton({ label, onClick }) {
  return (
    <button className="normal-button" onClick={onClick}>
      {label}
    </button>
  );
}

export default NormalButton;