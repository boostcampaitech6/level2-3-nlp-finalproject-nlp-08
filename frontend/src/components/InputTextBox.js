import React from 'react';

const InputTextBox = ({ value, onChange }) => {

  return (
    <div className="center-container">
      <textarea
        className="large-input"
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

export default InputTextBox;