import React from 'react';

const FixedTextBox = ({ value }) => {

  return (
    <div className="left-container">
      <textarea
        className="large-left-textbox"
        value={value}
      />
    </div>
  );
};

export default FixedTextBox;