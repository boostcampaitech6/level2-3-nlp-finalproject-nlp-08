import React from 'react';
import './InputTextBox.css';
import placeholder from './PlaceHolder';

const InputTextBox = ({ value, onChange }) => {

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