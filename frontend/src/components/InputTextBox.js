import React from 'react';
import './InputTextBox.css';

const InputTextBox = ({ value, onChange, placeholder }) => {

  return (
    <div className="center-container">
      <textarea
        className="large-input"
        value={value}
        onChange={onChange} 
        placeholder={placeholder}
      />
    </div>
  );
};

export default InputTextBox;