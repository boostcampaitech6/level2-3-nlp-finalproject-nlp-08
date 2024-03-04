import React from 'react';
import './FixedTextBox.css';

const FixedTextBox = ({ value }) => {

  return (
    <div className="result-container">
      <textarea
        className="large-result-textbox"
        disabled={true}
        value={value}
      />
    </div>
  );
};

export default FixedTextBox;