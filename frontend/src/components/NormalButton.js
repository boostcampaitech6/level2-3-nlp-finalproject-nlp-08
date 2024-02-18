import React from 'react';

function NormalButton({ label, onClick }) {
  return (
    <button className="normal-button" onClick={onClick}>
      {label}
    </button>
  );
}

export default NormalButton;